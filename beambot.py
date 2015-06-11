#!/usr/bin/env python3 

# -+=============================================================+-
#	Version: 	0.1.0 RC 1
#	Author: 	RPiAwesomeness (AKA ParadigmShift3d)
#	Date:		June 11, 2015
#
#	Changelog:	Got commands working with proper chat responses.
#				Not full release level yet because not all commands are fully programmed yet
#				Need to add: 	!give, !ban, !quote, !gears, !tackle, !slap, !uptime, !live,
#								!command, !whoami
# -+=============================================================+-


import requests
import config
import json
import asyncio
import websockets
import time
import signal
import pickle

@asyncio.coroutine
def connect():

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
	print (ret)
	
	if ret["error"] != None:
		print (ret["error"])
		print ("EEEK!")
		quit()

	# If the message doesn't send initially, send it again. The bot just needs to wake up chat
	packet = {
		"type":"method",
		"method":"msg",
		"arguments":['pybot online!'],
		"id":2
	}

	yield from websocket.send(json.dumps(packet))
	ret_msg = yield from websocket.recv()
	ret_msg = json.loads(ret_msg)

	print ('ret')
	print (ret_msg)

	yield from websocket.close()

@asyncio.coroutine
def readChat():

	session = requests.Session()
	msgs_acted = pickle.load(open ('blacklist.p', "rb"))

	while True:
		
		get_msg = session.get(	# Should be changed so that it automatically selects correct chat
			addr + '/api/v1/chats/' + str(config.CHANNEL_PARA) + '/message'
		)	

		for msg in get_msg.json():		# Get the individual messages from chat

			userID = msg['user_id']
			userName = msg['user_name']
			msgID = msg['id']

			for item in msg['message']:	# Iterate through the message

				msgLocalID = 0

				for i in iter(item.keys()):

					curItem = str(item[i])

					if item[i] == '':	# Empty data, indicating a link
						next

					if len(curItem) >= 1:	# Just make sure it's an actual message

						if curItem[0] == '!' and msgID not in msgs_acted:	# It's a command! Pay attention!
							
							if curItem[1:] == "hey":		# Hello command

								# Set up websocket
								# ----------------------------------------------------------
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
									print ("EEEK!")
									yield from websocket.close()
									quit()

								#----------------------------------------------------------

								response = "Saluton Mondo {} !".format(userName)
								print (response)

								packet = {
									"type":"method",
									"method":"msg",
									"arguments":[response],
									"id":msgLocalID
								}


								msgLocalID += 1

								yield from websocket.send(json.dumps(packet))
								ret_msg = yield from websocket.recv()
								ret_msg = json.loads(ret_msg)

								print ('ret:\t\t',ret_msg)

								yield from websocket.close()

								packet['arguments'][0] = ''

							elif curItem[1:] == "ping":	# Ping Pong Command

								# Set up websocket
								# ----------------------------------------------------------
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
									print ("EEEK!")
									yield from websocket.close()
									quit()

								#----------------------------------------------------------

								response = "Pong!"
								print (response)

								packet = {
									"type":"method",
									"method":"msg",
									"arguments":[response],
									"id":msgLocalID
								}

								msgLocalID += 1

								yield from websocket.send('')
								ret = yield from websocket.recv()

								yield from websocket.send(json.dumps(packet))
								ret_msg = yield from websocket.recv()
								ret_msg = json.loads(ret_msg)

								print ('ret:\t\t',ret_msg)

								yield from websocket.close()

								packet['arguments'][0] = ''

							elif curItem[1:] == "gears":	# User balance, need to get user ID for

								# Set up websocket
								# ----------------------------------------------------------
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
									print ("EEEK!")
									yield from websocket.close()
									quit()

								#----------------------------------------------------------

								response = "Not implemented yet ;("
								print (response)

								packet = {
									"type":"method",
									"method":"msg",
									"arguments":[response],
									"id":msgLocalID
								}

								msgLocalID += 1

								yield from websocket.send(json.dumps(packet))
								ret_msg = yield from websocket.recv()
								ret_msg = json.loads(ret_msg)

								print ('ret:\t\t',ret_msg)

								yield from websocket.close()

								packet['arguments'][0] = ''

				if msgID not in msgs_acted:		# Don't add duplicates
					msgs_acted.append(msgID)		# Make sure we don't act on messages again
					pickle.dump(msgs_acted, open('blacklist.p', 'wb'))
		
		print ('Waiting 3 seconds...')
		time.sleep(3)
		
# ----------------------------------------------------------------------
# Main Code
# ----------------------------------------------------------------------

def _get_auth_body():

	return {
		'username': config.USERNAME,
		'password': config.PASSWORD
	}

def main():

	global authkey, endpoint, channel, user_id, addr

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
		addr + '/api/v1/chats/%s' % channel
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
	#loop.run_until_complete(connect())
	loop.run_until_complete(readChat())
	loop.close()

if __name__ == "__main__":
	main()