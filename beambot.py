#!/usr/bin/env python3

# -+=============================================================+-
#	Version: 	3.2.5
#	Author: 	RPiAwesomeness
#	Date:		August 25, 2015
#
#	Changelog:	Fixed bug where only the first custom command would actually work
#				Fixed bug where non-existent commands would elicit a blank message from the bot 
# -+=============================================================+

import os
import json
import asyncio, websockets, requests
import time, random
import pickle
import responses, commands
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
				addr + '/api/v1/chats/' + str(channel) + '/users')

		usersRet = usersRet.json()

		for user in usersRet:					# Give all users +1 gear per minute
			user_name = user['userName']

			curItem = '!give ' + user_name + " 1"
			autoCurrencyResponse = responses.give('pybot', curItem, is_mod=True)	# Give the users +1 gear

		if timeIncr == 3:

			for user in usersRet:					# Check all the currently active users
				user_name = user['userName']

				if user_name in activeChat:				# Has the user chatted in the last 3 minutes?

					curItem = '!give ' + user_name + " 3"
					autoCurrencyResponse = responses.give('pybot', curItem, is_mod=True)	# Give the users +3 gear for being involved


			timeIncr = 0	# Reset the time incrementer
			activeChat = []	# Reset the active chat watcher thingy

		yield from asyncio.sleep(60)

		timeIncr += 1

@asyncio.coroutine
def connect():

	global initTime, authkey_control, endpoint_control, user_id

	websocket = yield from websockets.connect(endpoint_control)

	packet = {
	    "type":"method",
	    "method":"auth",
	    "arguments":[22085, user_id, authkey_control],
	    "id":0
	}

	yield from websocket.send(json.dumps(packet))
	ret = yield from websocket.recv()
	ret = json.loads(ret)

	if ret["error"] != None:
	    print ('Error:\t',ret["error"])
	    print ("Error - Non-None error returned!")
	    quit()

	curTime = str(datetime.now().strftime('%H.%M.%S')) + ' - ' + str(datetime.now().strftime('%D'))

	packet = {
	    "type":"method",
	    "method":"msg",
	    "arguments":['Bot online - Current Date/Time: {}'.format(str(curTime))],
	    "id":1
	}

	yield from websocket.send(json.dumps(packet))
	ret_msg = yield from websocket.recv()
	ret_msg = json.loads(ret_msg)

	yield from websocket.close()

	websocket = yield from websockets.connect(endpoint)

	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":1
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

	global initTime, activeChat, user_id

	activeChat = []
	msgLocalID = 0

	session = requests.Session()

	activeChat = []

	websocket = yield from websockets.connect(endpoint)

	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":msgLocalID
	}

	response = yield from websocket.send(json.dumps(packet))

	while True:

		timeCur = datetime.now().strftime("%S")

		result = yield from websocket.recv()

		if result != None:
			result = json.loads(result)

		if 'event' in result:		# Otherwise it crashes when type = response

			if result['event'] == 'UserJoin':
				print ('User joined:\t', result['data']['username'],
						'-', result['data']['id'],
						end='\n\n')

			elif result['event'] == 'UserLeave':
				print ('User left:\t', result['data']['username'],
						'-', result['data']['id'],
						end='\n\n')

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
					for section in user_msg:

						msg_text = ''

						if section['type'] == 'text' and section['data'] != '':
							msg_text += section['data']

						elif 'text' in section:		# Emoticon

							msg_text += section['text']

					print ('Message:\t', msg_text, end='\n\n')

				else:		# Just plain chat text
					print ('Message:\t',user_msg[0]['data'], end='\n\n')

				if user_name not in activeChat:
					activeChat.append(user_name)

				response, goodbye = commands.prepCMD(msg, msgLocalID)

				if goodbye:							# If goodbye is set to true, bot is supposed to turn off

					yield from websocket.send(json.dumps(response))	# Send the message
					yield from websocket.close()
					quit()

				if response == None or response == "":	# Make sure response isn't nothing
					next
				else:
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

		raise NotAuthed(loginRet.text)

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

	chat_ret = session.get(
		addr + '/api/v1/chats/{}'.format(channel)
	)

	control_ret = session.get(
		addr + '/api/v1/chats/22085'
	)

	if control_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',control_ret.json())
		raise ChatConnectFailure(control_ret.json())

	if chat_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',chat_ret.json())
		raise ChatConnectFailure(chat_ret.json())

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
	try:
		main()
	except KeyboardInterrupt:
		if input("\033[1;34mAre you sure you would like to quit? (Y/n)\033[0m ").lower().startswith('y'):
			sys.exit("\033[1;31mTerminated.\033[0m")
		else:
			main()
	except Exception as e:
		exception_type, exception_obj, exception_tb = sys.exc_info()
		filename = exception_tb.tb_frame.f_code.co_filename

		print('\033[1;31mI have crashed.\033[33m\n\nFile "{file}", line {line}\n{line_text}\n{exception}\033[0m'.format(file=filename, line=exception_tb.tb_lineno, line_text=open(filename).readlines()[exception_tb.tb_lineno-1], exception=repr(e)))
		print('\033[1;32mRestarting in 10 seconds. Ctrl-C to cancel.\033[0m')
		sleep(10)
		os.execl(sys.executable, sys.executable, * sys.argv)
