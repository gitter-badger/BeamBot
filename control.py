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
"""

"""
The control.py module takes care of monitoring the beam.pro/pybot channel for
commands & provides bot control.
"""

import pickle
from datetime import datetime
import json
import os
import asyncio, websockets, requests
import subprocess

import responses, commands
import messages

global WHITELIST, config, loop
global local_msg_id

local_msg_id = 0

try:
	config = json.load(open('data/config.json', 'r'))
except:
	print ('Configuration file (data/config.json) missing!')
	print ("You need to run 'python3 setup.py' to set up the bot if you haven't already.")
	print ("If you have set up the bot before, then please make sure data/config.json exists & has the proper information in it.")
	print ("Quiting.")
	quit()

if os.path.exists('data/whitelist{}.p'.format(config['CHANNEL'])):
	WHITELIST = pickle.load(open('data/whitelist{}.p'.format(config['CHANNEL']), 'rb'))
else:
	WHITELIST = ['pybot']
	pickle.dump(WHITELIST, open('data/whitelist{}.p'.format(config['CHANNEL']), 'wb'))

def _get_auth_body():

	return {
		'username': config['USERNAME'],
		'password': config['PASSWORD']
	}

@asyncio.coroutine
def controlChannel():

	global user_id
	global websocket

	addr = config['BEAM_ADDR']

	session = requests.Session()

	loginRet = session.post(
		addr + '/users/login',
		data=_get_auth_body()
	)

	if loginRet.status_code != requests.codes.ok:
		print (loginRet.text)

	user_id = loginRet.json()['id']

	channel = config['CHANNEL']

	control_ret = session.get(
		addr + '/chats/22085'
	)

	if control_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',control_ret.json())
		quit()

	chat_details_control = control_ret.json()

	endpoint_control = chat_details_control['endpoints'][0]

	authkey_control = chat_details_control['authkey']

	websocket = yield from websockets.connect(endpoint_control)

	content = [22085, user_id, authkey_control]

	ret = yield from messages.sendMsg(websocket, content, is_auth=True)
	ret = ret.split('"id"')[0][:-1] + "}"
	ret = json.loads(ret)

	if ret["error"] != None:
		print (ret["error"])
		print ("Error - Non-None error returned!")
		quit()

	while True:
		result = yield from websocket.recv()

		if type(result) == None:
			next

		result = json.loads(result)

		if result['event'] == 'ChatMessage':
			print ('Control channel:')

			result = result['data']
			msg = result['message']['message'][0]

			print ('User:\t\t',result['user_name'],
					'-', result['user_id'])

			print ('Message:\t', msg['data'], end='\n\n')

def goodbye(user_name, is_owner, msgLocalID):

	# Make sure to have the most updated user whitelist
	if os.path.exists('data/whitelist{}.p'.format(config['CHANNEL'])):
		WHITELIST = pickle.load(open('data/whitelist{}.p'.format(config['CHANNEL']), 'rb'))

	if is_owner or user_name in WHITELIST:
		packet = {
			"type":"method",
			"method":"msg",
			"arguments":['See you later my dear sir, wot wot!'],
			"id":msgLocalID
		}

		return packet, True	# Return the Goodbye message packet &
	else:		# Don't want anyone but owner killing the bot
		return None, False

@asyncio.coroutine
def keepAlive():
	global websocket

	initial = True

	while True:
		if not initial:
			yield from websocket.ping()

		yield from asyncio.sleep(180)
		initial = False

def restart(user_name, websocket):
	print ('Restarting bot in 10 seconds...')
	subprocess.Popen(['sh','restart.sh'])
	closeSocket(websocket)
