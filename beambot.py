#!/usr/bin/env python3 

# -+=============================================================+-
#	Version: 	0.1.1 RC 1
#	Author: 	RPiAwesomeness (AKA ParadigmShift3d)
#	Date:		June 11, 2015
#
#	Changelog:	Got commands working with proper chat responses.
#				Not full release level yet because not all commands are fully programmed yet
#				Need to add: 	Command timeout, mod controls, !command
#				Need to update:	!give, !ban, !quote, !gears, !live
#				Changed initilization message
# -+=============================================================+

import requests
import config
import json
import asyncio
import websockets
import time
import pickle
from datetime import datetime
import random
import responses

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
	print (ret)
	
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
							
							# Commands
							# ----------------------------------------------------------
							if curItem[1:] == "hey":				# Say hey
								response = responses.hey(userName)

							elif curItem[1:] == "ping":				# Ping Pong Command
								response = responses.ping()

							elif curItem[1:] == "gears":			# Get user balance
								response = responses.gears(userName, curItem)

							elif curItem[1:].split()[0] == "give":	# Give gears to a user
								response = responses.give(curItem)

							elif curItem[1:].split()[0] == "ban":	# Ban a user from chatting
								response = responses.ban(curItem)

							elif curItem[1:].split()[0] == "quote":	# Get random quote from DB
								response = responses.quote(curItem)

							elif curItem[1:].split()[0] == "tackle":# Tackle a user!
								response = responses.tackle(curItem)

							elif curItem[1:].split()[0] == "slap":	# Slap someone
								response = responses.slap()

							elif curItem[1:].split()[0] == "uptime":# Bot uptime
								response = responses.uptime(initTime)

							elif curItem[1:].split()[0] == "hug":	# Give hugs!
								response = responses.hug(userName, curItem)

							elif curItem[1:].split()[0] == "live":	# Let the bot know you're live
								response = responses.live()

							elif curItem[1:].split()[0] == "whoami":	# Who am I? I'M A GOAT. DUH.
								response = responses.whoami(userName)

							# ----------------------------------------------------------
							# Set up websocket
							# ----------------------------------------------------------
							websocket = yield from websockets.connect(endpoint)
							
							packet = {
								"type":"method",
								"method":"auth",
								"arguments":[channel, user_id, authkey],
								"id":0
							}
							
							yield from websocket.send(json.dumps(packet))	# Send the message

							ret = yield from websocket.recv()				# Recieve the response
							ret = json.loads(ret)			# Convert the response to JSON
							
							if ret["error"] != None:		# Check to make sure we didn't get a Non-None response
								print (ret["error"])
								print ("EEEK!")
								yield from websocket.close()
								quit()

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

							print (response)	# Console logging

							msgLocalID += 1		# Increment the msg number variable

							yield from websocket.send(json.dumps(packet))	# Send the message
							ret_msg = yield from websocket.recv()			# Get the response
							ret_msg = json.loads(ret_msg)			# Convert response to JSON

							#print ('ret:\t\t',ret_msg)

							yield from websocket.close()			# Close the connection

							packet['arguments'][0] = ''				# Clear the message arguments

				if msgID not in msgs_acted:		# Don't add duplicates
					msgs_acted.append(msgID)		# Make sure we don't act on messages again
					
					# Dump the list of msgs_acted into the blacklist.p pickle file so we don't act on those
					# messages again.
					pickle.dump(msgs_acted, open('blacklist.p', 'wb'))
		
		print ('Waiting 1 seconds...')
		time.sleep(1)		# Don't spam the server >.<
		
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
	loop.run_until_complete(connect())
	loop.run_until_complete(readChat())
	loop.close()

if __name__ == "__main__":
	main()