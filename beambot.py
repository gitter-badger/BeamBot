#!/usr/bin/env python3

"""
	This file is part of PyBot,
	PyBot(c) RPiAwesomeness 2015-2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/agpl.html>.

-+=============================================================+-
	Version: 	3.3.4
	Author: 	RPiAwesomeness
	Date:		January 30, 2016

	Changelog:	Fixed issue with !command remove returning the usage & not removing cmd
				Fixed issue with !command add that had a link creating multiple versions
				Updated setup script to accept empty input for custom currency command - now reverts command
					to currency name
-+=============================================================+
"""

import sys, os
import json
import asyncio, websockets, requests
import time, random
import pickle
import argparse
import subprocess
import responses, commands, messages, schedule, announce

from datetime import datetime
from time import sleep

from control import goodbye
from control import controlChannel
from control import keepAlive

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

			cur_item = ["auto", user_name, 1]

			autoCurrencyResponse = responses.give('PyBot', cur_item, is_mod=True, is_owner=False)	# Give the users +1 gear

		if timeIncr == 3:

			for user in usersRet:					# Check all the currently active users
				user_name = user['userName']

				if user_name in activeChat:				# Has the user chatted in the last 3 minutes?
					cur_item = ["auto", user_name, 3]
					autoCurrencyResponse = responses.give('PyBot', cur_item, is_mod=True, is_owner=False)	# Give the users +3 gear for being involved

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

		yield from messages.close(websocket)

	else:
		yield from messages.close(websocket)

@asyncio.coroutine
def readChat():

	global initTime, activeChat, user_id, websocket, chat_socket

	activeChat = []
	msgLocalID = 0
	goodbye = False
	announce_users = {}

	session = requests.Session()

	activeChat = []
	websocket = yield from websockets.connect(endpoint)

	content = [channel, user_id, authkey]
	yield from messages.sendMsg(websocket, content, is_auth=True)

	while True:

		time_pre_recv = (datetime.now().strftime("%M"))

		result = yield from websocket.recv()

		schedule.registerWebsocket(websocket)
		announce.registerWebsocket(websocket)

		if result == None:
			continue
		try:
			result = json.loads(result)
		except TypeError as e:
			continue

		if 'event' in result:		# Otherwise it crashes when type = response

			event = result['event']
			if 'username' in result['data']:
				result_user = result['data']['username']
			elif 'user_name' in result['data']:
				result_user = result['data']['user_name']

			cur_time = int(datetime.now().strftime("%M"))

			if event == "UserJoin":
				yield from announce.userJoin(result, result_user)

			if event == "UserLeave":
				yield from announce.userLeave(result, result_user)

			elif event == "ChatMessage":

				msg = result['data']
				msg_id = msg['id']

				user_roles = msg['user_roles']
				user_name = msg['user_name']
				user_id = msg['user_id']
				user_msg = msg['message']['message']
				meta = msg['message']['meta']

				print ('User:\t\t', user_name,
						'-', user_id)

				msg_text = ''

				if len(user_msg) > 1:	# There's an emoticon in there
					for section in user_msg:
						if section['type'] == 'text' and section['data'] != '':
							msg_text += section['data']

						elif section['type'] == 'emoticon':		# Emoticon
							msg_text += section['text']

						elif section['type'] == 'link':			# Link/URL
							msg_text += section['text']

				else:
					# Updated form /me handling - to be released Oct 18-19 by Beam
					if 'meta' in user_msg[0]:			# /me message
						if 'me' in user_msg[0]['meta']:
							msg_text += user_msg[0]['message']

					elif user_msg[0]['type'] == 'text' and user_msg[0]['data'] != '':
						msg_text += user_msg[0]['data']

				print ('Message:\t', msg_text, end='\n\n')

				if user_name not in activeChat:
					activeChat.append(user_name)

				response, goodbye = commands.prepCMD(msg, msgLocalID, websocket, user_name, user_roles, user_id)

				if goodbye:							# If goodbye is set to true, bot is supposed to turn off

					yield from messages.sendMsg(websocket, response)	# Send the message
					yield from messages.sendMsg(websocket, "See ya later!")	# Send goodbye msg
					yield from messages.close(websocket)
					print ("Bot quit", str(datetime.now().strftime('%H.%M.%S')))
					quit()

				if response == None or response == "":	# Make sure response isn't nothing
					continue
				else:
					#----------------------------------------------------------
					# Send the message
					#----------------------------------------------------------

					ret_msg = yield from messages.sendMsg(websocket, response)
					ret_msg = json.loads(ret_msg)			# Convert response to JSON

					print ('ret_msg:\t', ret_msg)
					print ('Response:\t', ret_msg['data'])

					if 'error' in ret_msg:
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
		asyncio.async(controlChannel()),
		asyncio.async(schedule.timeoutsHandler()),
		asyncio.async(keepAlive())
	]
	try:
		loop.run_until_complete(connect())		# Announce your presence!
		loop.run_until_complete(asyncio.wait(tasks))

	except Exception as e:
		print ("\033[1;31mSomething happened!\033[0m\n")
		print (e)

		messages.close(websocket)
		loop.close()
		p = subprocess.Popen(['sh', './restart.sh'])
		print ("Restarting bot")
		quit()

if __name__ == "__main__":
	global args

	parser = argparse.ArgumentParser()
	parser.add_argument('-nsm', '--nostartmsg', help="Start the bot without the startup greeting", action="store_true")

	args = parser.parse_args()

	main()
