#!/usr/bin/env python3 

# -+=============================================================+-
#	Version: 	0.3.0 (RC 3)
#	Author: 	RPiAwesomeness (AKA ParadigmShift3d)
#	Date:		June 22, 2015
#
#	Changelog:	Got commands working with proper chat responses.
#				Not full release level yet because not all commands are fully programmed yet
#				Need to update:	users getting gears automatically
#				Added !command, !command+, and !command- commands for custom commands
# -+=============================================================+

import os
import requests
import json
import asyncio, websockets
import time
import pickle
import random
import config, responses
from datetime import datetime

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

	initTime = datetime.now().strftime('%H.%M.%S')

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

	global initTime

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
		pickle.dump(bannedUsers, open('data/blacklist.p', 'wb'))

	websocket = yield from websockets.connect(endpoint)

	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":0
	}

	response = yield from websocket.send(json.dumps(packet))

	timeInit = int(datetime.now().strftime("%S"))

	if timeInit == 0:
		timeInit += 1

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

				userID = msg['user_id']
				userName = msg['user_name']
				msgID = msg['id']

				if userName in bannedUsers:		# Is the user chatbanned?
					session = requests.session()

					login_r = session.post(
						addr + '/api/v1/users/login',
						data=_get_auth_body()
					)

					if login_r.status_code != requests.codes.ok:
						print (login_r.text)
						print ("Not Authenticated!")
						quit()

					print (login_r.json())

					del_r = session.delete(addr + '/api/v1/chats/' + str(channel) + '/message/' + msgID)	# Delete the message

					if del_r.status_code != requests.codes.ok:
						print ('Response:\t\t',del_r.json())
						quit()

					session.close()

				curItem = ''
				for i in range(0, len(msg['message'])):
					if i % 2:		# Every 2 messages
						curItem += msg['message'][i]['text']
					else:
						curItem += msg['message'][i]['data']

				for item in msg['message']:	# Iterate through the message

					msgLocalID = 0

					if len(curItem) >= 1:	# Just make sure it's an actual message

						if curItem[0] == '!' and msgID not in msgs_acted:	# It's a command! Pay attention!
							
							# Commands
							# ----------------------------------------------------------
							cmd = curItem[1:].split()

							if cmd[0] == "hey":				# Say hey
								response = responses.hey(userName)

							elif cmd[0] == "ping":				# Ping Pong Command
								response = responses.ping(userName)

							elif cmd[0] == "gears":			# Get user balance
								response = responses.gears(userName, curItem)

							elif cmd[0] == "give":	# Give gears to a user
								response = responses.give(userName, curItem)

							elif cmd[0] == "ban":	# Ban a user from chatting
								response, banUser = responses.ban(userName, curItem)
								bannedUsers.append(banUser)

								pickle.dump(bannedUsers, open('data/bannedUsers.p', "wb"))

							elif cmd[0] == "unban":	# Unban a user
								response, uBanUser = responses.unban(userName, curItem)
								bannedUsers.remove(uBanUser)

								pickle.dump(bannedUsers, open('data/bannedUsers.p', "wb"))

							elif cmd[0] == "quote":	# Get random quote from DB
								response = responses.quote(userName, curItem)

							elif cmd[0] == "tackle":# Tackle a user!
								response = responses.tackle(userName, curItem)

							elif cmd[0] == "slap":	# Slap someone
								response = responses.slap(userName)

							elif cmd[0] == "uptime":# Bot uptime
								response = responses.uptime(userName, initTime)

							elif cmd[0] == "hug":	# Give hugs!
								response = responses.hug(userName, curItem)

							elif cmd[0] == "whoami":	# Who am I? I'M A GOAT. DUH.
								response = responses.whoami(userName)

							elif cmd[0] == "command":	# Add command for any users
								response = responses.command(userName, curItem)

							elif cmd[0] == "command+":	# Add mod-only command
								response = responses.commandMod(userName, curItem)

							elif cmd[0] == "command-":	# Remove a command
								response = responses.commandRM(userName, curItem)

							elif cmd[0] == "whitelist":	# Whitelist a user
								print (len(cmd))
								if len(cmd) >= 3:	# True means it has something like `add` or `remove`
									if cmd[1] == 'add':
										response = responses.whitelist(userName, curItem)
									elif cmd[1] == 'remove':
										response = responses.whitelistRM(userName, curItem)
									else: 	# Not add or remove
										response = None
								else:		# Just get the whitelist
									response = responses.whitelistLS(userName, curItem)

							elif cmd[0] == "goodbye":	# Turn off the bot correctly

								packet = {
									"type":"method",
									"method":"msg",
									"arguments":['Good night!'],
									"id":msgLocalID
								}

								yield from websocket.send(json.dumps(packet))

								yield from websocket.close()		# Close the websocket/connection
								quit()					# Quit the bot

							else:					# Unknown or custom command
								response = responses.custom(userName, curItem)

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

							print ('command:\t',cmd,'\n',
									'response:\t',response,'\n')	# Console logging

							msgLocalID += 1		# Increment the msg number variable

							yield from websocket.send(json.dumps(packet))	# Send the message
							ret_msg = yield from websocket.recv()			# Get the response
							ret_msg = json.loads(ret_msg)			# Convert response to JSON

							packet['arguments'][0] = ''				# Clear the message arguments

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

		# Code for automatically giving gears out - not working 0.3.0
		#Needs to be separate thread because while True loop won't loop until next chat event
		#--------------------------------------------------------------------------------------

		# session = requests.Session()

		# users_r = session.get(
		# 	addr + '/api/v1/chats/' + str(channel) + '/users')

		# session.close()

		# users_r = users_r.json()

		# for user in users_r:
		# 	userName = user['userName']
		# 	curItem = "!give " + userName + " 1"

		# 	responses.give('ParadigmShift3d', curItem)

		# 	timeCur = int(datetime.now().strftime("%S"))

		# 	if timeCur	== 0:
		# 		timeCur += 1

		# 	if timeInit / timeCur>= 0:		# It's divisible by 3, thus 3 seconds
		# 		if userName in activeChat:	# Has the user chatted in the last 60 seconds?
		# 			curItem = "!give " + userName + " 2"
		# 			responses.give('ParadigmShift3d', curItem)
		# 			timeIncr += 1

		# 	elif timeCur == 60:		# It's been 60 seconds
		# 		curItem = '!give ' + userName + " 1"
		# 		responses.give('ParadigmShift3d', curItem)	# Give the users however many they've accumulated

		# 		timeIncr = 0	# Reset the time incrementer
		# 		activeChat = []	# Reset the active chat watcher thingy
				
# ----------------------------------------------------------------------
# Main Code
# ----------------------------------------------------------------------

def _get_auth_body():

	return {
		'username': config.USERNAME,
		'password': config.PASSWORD
	}

def main():

	global authkey, endpoint, channel, user_id, addr, loop

	addr = config.BEAM_ADDR

	session = requests.Session()

	login_r = session.post(
		addr + '/api/v1/users/login',
		data=_get_auth_body()
	)

	if login_r.status_code != requests.codes.ok:
		print (login_r.text)
		print ("Not Authenticated!")
		quit()
	
	user_id = login_r.json()['id']

	channel = input("Channel? ")

	if channel == 'p':		# Paradigm, me
		channel = config.CHANNEL_PARA
	elif channel == 'du':	# Duke
		channel = config.CHANNEL_DUKE
	elif channel == 'de':	# Deci
		channel = config.CHANNEL_DECI

	chat_r = session.get(
		addr + '/api/v1/chats/{}'.format(channel)
	)
	if chat_r.status_code != requests.codes.ok:
		print ('Unknown error!')
		quit()

	chat_details = chat_r.json()

	endpoint = chat_details['endpoints'][0]

	authkey = chat_details['authkey']

	print ('authkey:\t',authkey)
	print ('endpoint:\t',endpoint)

	loop = asyncio.get_event_loop()
	loop.run_until_complete(connect())
	loop.run_until_complete(readChat())
	loop.close()

if __name__ == "__main__":
	main()