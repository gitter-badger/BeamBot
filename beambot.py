#!/usr/bin/env python3

# -+=============================================================+-
#	Version: 	3.2.0
#	Author: 	RPiAwesomeness
#	Date:		July 10, 2015
#
#	Changelog:	Added response variables to custom commands
#				Added !currency command
#				Updated !give, !gears, and !quote to support @USERNAME as well
#					as the current USERNAME (sans-@)
#				Various bug fixes
# -+=============================================================+

import os
import json
import asyncio, websockets, requests
import time, random
import pickle
import responses, commands
from datetime import datetime

@asyncio.coroutine
def autoCurrency():

	global activeChat

	timeIncr = 0

	while True:

		with requests.Session() as session:		# Get the list of currently active users
			usersRet = session.get(
				addr + '/api/v1/chats/' + str(channel) + '/users')

		usersRet = usersRet.json()

		for user in usersRet:					# Give all users +1 gear per minute
			userName = user['userName']

			curItem = '!give ' + userName + " 1"
			autoCurrencyResponse = responses.give('pybot', curItem)	# Give the users +1 gear

		if timeIncr == 3:

			for user in usersRet:					# Check all the currently active users
				userName = user['userName']

				if userName in activeChat:				# Has the user chatted in the last 3 minutes?

					curItem = '!give ' + userName + " 3"
					autoCurrencyResponse = responses.give('pybot', curItem)	# Give the users +3 gear for being involved


			timeIncr = 0	# Reset the time incrementer
			activeChat = []	# Reset the active chat watcher thingy

		yield from asyncio.sleep(60)

		timeIncr += 1

@asyncio.coroutine
def connect():

	global initTime

	websocket = yield from websockets.connect(endpoint)

	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":0
	}

	yield from websocket.send(json.dumps(packet))
	ret = yield from websocket.recv()
	ret = json.loads(ret)

	if ret["error"] != None:
		print (ret["error"])
		print ("Error - Non-None error returned!")
		quit()

	if int(datetime.now().strftime('%H')) < 12:		# It's before 12 PM - morning
		timeStr = "mornin'"
	elif int(datetime.now().strftime('%H')) >= 12 and int(datetime.now().strftime('%H')) < 17:		# It's afternoon
		timeStr = "afternoon"
	elif int(datetime.now().strftime('%H')) >= 17:	# It's after 5 - evening
		timeStr = "evenin'"

	# If the message doesn't send initially, send it again. The bot just needs to wake up chat
	packet = {
		"type":"method",
		"method":"msg",
		"arguments":['Top o\' the {} to you!'.format(timeStr)],
		"id":1
	}

	yield from websocket.send(json.dumps(packet))
	ret_msg = yield from websocket.recv()
	ret_msg = json.loads(ret_msg)

	yield from websocket.close()

@asyncio.coroutine
def readChat():

	global initTime, activeChat

	activeChat = []
	msgLocalID = 0

	session = requests.Session()

	if os.path.exists('data/blacklist.p'):
		msgs_acted = pickle.load(open('data/blacklist.p', "rb"))
	else:
		msgs_acted = []
		pickle.dump(msgs_acted, open('data/blacklist.p', 'wb'))

	activeChat = []

	if os.path.exists('data/bannedUsers.p'):
		bannedUsers = pickle.load(open('data/bannedUsers.p', 'rb'))
	else:
		bannedUsers = []
		pickle.dump(bannedUsers, open('data/bannedUsers.p', 'wb'))

	websocket = yield from websockets.connect(endpoint)

	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":0
	}

	response = yield from websocket.send(json.dumps(packet))

	while True:

		timeCur = datetime.now().strftime("%S")

		result = yield from websocket.recv()

		if result != None:
			result = json.loads(result)
			next

		print ('result:\t',result,'\n')

		if 'event' in result:
			if result['event'] == "ChatMessage":

				msg = result['data']
				msgID = msg['id']
				userName = msg['user_name']

				if userName not in activeChat:
					activeChat.append(userName)

				response, goodbye = commands.prepCMD(msg, bannedUsers, msgLocalID, msgs_acted)

				if goodbye:							# If goodbye is set to true, bot is supposed to turn off
					yield from websocket.send(json.dumps(response))	# Send the message
					yield from websocket.close()
					quit()

				if response != None:			# Make sure response isn't nothing
					#----------------------------------------------------------
					# Send the message
					#----------------------------------------------------------
					# Create the packet
					packet = {
						"type":"method",
						"method":"msg",
						"arguments":[response],
						"id":msgLocalID
					}

					msgLocalID += 1		# Increment the msg number variable

					yield from websocket.send(json.dumps(packet))	# Send the message
					ret_msg = yield from websocket.recv()			# Get the response
					ret_msg = json.loads(ret_msg)			# Convert response to JSON

					print ('ret_msg:\t',ret_msg)

				if msgID not in msgs_acted:		# Don't add duplicates
					msgs_acted.append(msgID)		# Make sure we don't act on messages again

					# Dump the list of msgs_acted into the blacklist.p pickle file so we don't act on those
					# messages again.
					f = open('data/.blist_temp.p', 'wb')
					pickle.dump(msgs_acted, f)

					f.flush()
					os.fsync(f.fileno())
					f.close()

					os.rename('data/.blist_temp.p', 'data/blacklist.p')

# ----------------------------------------------------------------------
# Main Code
# ----------------------------------------------------------------------

def _get_auth_body():

	return {
		'username': config['USERNAME'],
		'password': config['PASSWORD']
	}

def main():

	global authkey, endpoint, channel, user_id, addr, loop, config

	config = json.load(open('data/config.json', 'r'))

	addr = config['BEAM_ADDR']

	session = requests.Session()

	loginRet = session.post(
		addr + '/api/v1/users/login',
		data=_get_auth_body()
	)

	if loginRet.status_code != requests.codes.ok:
		print (loginRet.text)
		print ("Not Authenticated!")
		quit()

	user_id = loginRet.json()['id']

	if config['CHANNEL'] == None:		# If it's NOT None, then there's no auto-connect

		chanOwner = input("Channel [Channel owner's username]: ").lower()
		chatChannel = session.get(
			addr + '/api/v1/channels/' + chanOwner
		)

		if chatChannel.status_code != requests.codes.ok:
			print ('ERROR!')
			print ('Message:\t',chatChannel.json()['message'])
			quit()

		channel = chatChannel.json()['id']

	else:
		channel = config['CHANNEL']

	chatRet = session.get(
		addr + '/api/v1/chats/{}'.format(channel)
	)

	if chatRet.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',chatRet.json())
		quit()

	chat_details = chatRet.json()

	endpoint = chat_details['endpoints'][0]

	authkey = chat_details['authkey']

	print ('authkey:\t',authkey)
	print ('endpoint:\t',endpoint)

	loop = asyncio.get_event_loop()
	tasks = [
		asyncio.async(readChat()),
		asyncio.async(autoCurrency())
	]
	loop.run_until_complete(connect())

	loop.run_until_complete(asyncio.wait(tasks))

	loop.close()

if __name__ == "__main__":
	main()
