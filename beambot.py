#!/usr/bin/env python3

# -+=============================================================+-
#	Version: 	3.2.10(pre1)
#	Author: 	RPiAwesomeness
#	Date:		September 26, 2015
#
#	Changelog:	Fixed bug where bot wasn't connecting to the correct API
#					endpoint & thus wasn't authenticating, crashing the bot
#				You can now pass the -nsm/--nostartmsg argument when starting
#					the bot to stop it from sending the startup greeting message
#				Fixed micro bug where Terminal output would only show the URL or
#					emoticon if either were included, not the full message
#				Added messages.py to handle message sending and websocket
#					closing - need to test to make sure it's totally
#					working/finish implementing it
# -+=============================================================+

import sys, os
import json
import asyncio, websockets, requests
import time, random
import pickle
import argparse
import ast
import responses, commands, messages
from datetime import datetime
from control import goodbye
from control import controlChannel

@asyncio.coroutine
def autoCurrency():

	global activeChat

	timeIncr = 0

	while True:

		with requests.Session() as session:		# Get the list of currently active users
			usersRet = session.get(
				addr + '/chats/' + str(channel) + '/users')

		usersRet = usersRet.json()

		for user in usersRet:					# Give all users +1 gear per minute
			user_name = user['userName']

			curItem = '!give ' + user_name + " 1"
			autoCurrencyResponse = responses.give('pybot', curItem, is_mod=True, is_owner=False)	# Give the users +1 gear

		if timeIncr == 3:

			for user in usersRet:					# Check all the currently active users
				user_name = user['userName']

				if user_name in activeChat:				# Has the user chatted in the last 3 minutes?

					curItem = '!give ' + user_name + " 3"
					autoCurrencyResponse = responses.give('pybot', curItem, is_mod=True, is_owner=False)	# Give the users +3 gear for being involved


			timeIncr = 0	# Reset the time incrementer
			activeChat = []	# Reset the active chat watcher thingy

		yield from asyncio.sleep(60)

		timeIncr += 1

@asyncio.coroutine
def connect():

	global initTime, authkey_control, endpoint_control, user_id

	websocket = yield from websockets.connect(endpoint_control)
	content = [22085, user_id, authkey_control]

	ret = yield from messages.sendMsg(websocket, content, is_auth=True)
	ret = ret.split('"id"')[0][:-1] + "}"

	ret = json.loads(ret)

	if ret["error"] != None:
		print ('CONTROL CHANNEL')
		print ('Error:\t',ret["error"])
		print ("Error - Non-None error returned!")
		quit()

	curTime = str(datetime.now().strftime('%H.%M.%S')) + ' - ' + str(datetime.now().strftime('%D'))

	msg_to_send = 'Bot online - Current Date/Time: {}'.format(str(curTime))
	ret_msg = yield from messages.sendMsg(websocket, msg_to_send)
	ret_msg = json.loads(ret_msg)

	yield from messages.close(websocket)

	websocket = yield from websockets.connect(endpoint)
	content = [channel, user_id, authkey]

	ret = yield from messages.sendMsg(websocket, content, is_auth=True)
	ret = ret.split('"id"')[0][:-1] + "}"
	ret = json.loads(ret)

	if ret["error"] != None:
		print ("MAIN CHANNEL")
		print (ret["error"])
		print ("Error - Non-None error returned!")
		quit()

	if not args.nostartmsg:
		if int(datetime.now().strftime('%H')) < 12:		# It's before 12 PM - morning
			timeStr = "mornin'"
		elif int(datetime.now().strftime('%H')) >= 12 and int(datetime.now().strftime('%H')) < 17:		# It's afternoon
			timeStr = "afternoon"
		elif int(datetime.now().strftime('%H')) >= 17:	# It's after 5 - evening
			timeStr = "evenin'"

		msg_to_send = 'Top o\' the {} to you!'.format(timeStr)
		ret_msg = yield from messages.sendMsg(websocket, msg_to_send)
		ret_msg = json.loads(ret_msg)

		yield from messages.close(websocket)

	else:
		yield from messages.close(websocket)

@asyncio.coroutine
def readChat():

	global initTime, activeChat, user_id

	activeChat = []
	msgLocalID = 0
	goodbye = False

	session = requests.Session()

	activeChat = []

	websocket = yield from websockets.connect(endpoint)
	content = [channel, user_id, authkey]
	yield from messages.sendMsg(websocket, content, is_auth=True)

	while True:

		time_pre_recv = (datetime.now().strftime("%M"))

		result = yield from websocket.recv()

		if result != None:
			result = json.loads(result)

		if 'event' in result:		# Otherwise it crashes when type = response

			if result['event'] == 'UserJoin':
				print ('User joined:\t', result['data']['username'],
						'-', result['data']['id'],
						end='\n\n')

				if result['data']['id'] != 25873:		# PyBot ID
					if config['announce_enter'] and result['data']['username'] != None:
						response = "Welcome " + result['data']['username'] + " to the stream!"

			elif result['event'] == 'UserLeave':
				print ('User left:\t', result['data']['username'],
						'-', result['data']['id'],
						end='\n\n')

				if result['data']['id'] != 25873:		# PyBot ID
					if config['announce_leave'] and result['data']['username'] != None:
						response = "See you later " + result['data']['username'] + "!"

			elif result['event'] == "ChatMessage":

				msg = result['data']
				msg_id = msg['id']

				user_roles = msg['user_roles']
				user_name = msg['user_name']
				user_id = msg['user_id']
				user_msg = msg['message']

				print ('User:\t\t', user_name,
						'-', user_id)

				if len(user_msg) > 1:	# There's an emoticon in there
					msg_text = ''

					for section in user_msg:

						if section['type'] == 'text' and section['data'] != '':
							msg_text += section['data']

						elif section['type'] == 'emoticon':		# Emoticon
							msg_text += section['text']

						elif section['type'] == 'link':			# Link/URL
							msg_text += section['text']

					print ('Message:\t', msg_text, end='\n\n')

				else:		# Just plain chat text
					print ('Message:\t',user_msg[0]['data'], end='\n\n')

				if user_name not in activeChat:
					activeChat.append(user_name)

				response, goodbye = commands.prepCMD(msg, msgLocalID)

				if goodbye:							# If goodbye is set to true, bot is supposed to turn off

					yield from messages.sendMsg(websocket, response)	# Send the message
					yield from messages.close(websocket)
					quit()

				if response == None or response == "":	# Make sure response isn't nothing
					next
				else:
					#----------------------------------------------------------
					# Send the message
					#----------------------------------------------------------

					ret_msg = yield from messages.sendMsg(websocket, response)
					ret_msg = json.loads(ret_msg)			# Convert response to JSON

					print ('ret_msg:\t', ret_msg)
					print ('Response:\t', ret_msg['data'])

					if ret_msg['error'] != None:
						print ('Error:\t',ret_msg['error'])
						print ('Code:\t',ret_msg['id'])

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

	global authkey_control, endpoint_control

	if os.path.exists('data/config.json'):
		config = json.load(open('data/config.json', 'r'))
	else:
		print ('\033[1;31mConfig file missing!\033[0m\n')
		print ('Please run setup before launching the bot.')
		print ('To do so run:\tpython3 setup.py')
		quit()

	addr = config['BEAM_ADDR']

	session = requests.Session()

	loginRet = session.post(
		addr + '/users/login',
		data=_get_auth_body()
	)

	if loginRet.status_code != requests.codes.ok:
		print (loginRet.text)
		print ("Not Authenticated!")

	user_id = loginRet.json()['id']

	if config['CHANNEL'] == None:		# If it's NOT None, then there's no auto-connect

		chanOwner = input("Channel [Channel owner's username]: ").lower()
		chatChannel = session.get(
			addr + '/channels/' + chanOwner
		)

		if chatChannel.status_code != requests.codes.ok:
			print ('ERROR!')
			print ('Message:\t',chatChannel.json()['message'])
			quit()

		channel = chatChannel.json()['id']

	else:
		channel = config['CHANNEL']

	chat_ret = session.get(
		addr + '/chats/{}'.format(channel)
	)

	control_ret = session.get(
		addr + '/chats/22085'
	)

	if control_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',control_ret.json())
		print(control_ret.json())
		quit()

	if chat_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',chat_ret.json())
		print(chat_ret.json())
		quit()

	chat_details = chat_ret.json()
	chat_details_control = control_ret.json()

	endpoint_control = chat_details_control['endpoints'][0]
	endpoint = chat_details['endpoints'][0]

	authkey = chat_details['authkey']
	authkey_control = chat_details_control['authkey']

	print ('authkey:\t',authkey)
	print ('endpoint:\t',endpoint, end='\n\n')

	loop = asyncio.get_event_loop()
	tasks = [
		asyncio.async(readChat()),
		asyncio.async(autoCurrency()),
		asyncio.async(controlChannel())
	]
	loop.run_until_complete(connect())		# Announce your presence!

	loop.run_until_complete(asyncio.wait(tasks))

	loop.close()

if __name__ == "__main__":
	global args

	parser = argparse.ArgumentParser()
	parser.add_argument('-nsm', '--nostartmsg', help="Start the bot without the startup greeting", action="store_true")

	args = parser.parse_args()

	main()
