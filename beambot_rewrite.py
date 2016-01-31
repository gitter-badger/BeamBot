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
	Version: 	4.0.0.A
	Author: 	RPiAwesomeness
	Date:		December 12, 2015

	Changelog:	Fixed a bug where a message of just !
				would crash the bot
			Fixed a bug where running currency cmds
				within the cmd timeout would
				crash the bot
-+=============================================================+
"""

import sys
import json
import requests
import os
import logging

from twisted.python import log

from twisted.internet import reactor, ssl
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketClientProtocol, \
	WebSocketClientFactory, connectWS

# PyBot modules
from tools import _getAuthBody, _updateConfig, _checkStatus, _checkMessage
from exceptions import *

global cur_channel, cur_user_id, cur_authkey
cur_channel = ""
cur_user_id = ""
cur_authkey = ""

class Connection:
	def __init__(self, *args, **kwargs):
		global cur_channel, cur_user_id, cur_authkey

		self.addr = kwargs["addr"]			# Beam API base URL
		self.channel = kwargs["channel"]	# Channel to connect to

		self.session = kwargs["session"]	# Session for accessing REST API

		# Get user_id
		login_ret = self.session.post(
			addr + '/users/login',
			data=_getAuthBody()
		)
		if _checkStatus(login_ret):
			self.user_id = login_ret.json()["id"]	# Bot's user ID
		else:
			logging.error("ERROR:")
			logging.error(login_ret.text)
			logging.error(login_ret.status_code)
			quit()

		# Get authkey and endpoint
		chat_ret = self.session.get(
			addr + "/chats/{}".format(self.channel)
		)
		if _checkStatus(chat_ret):
			self.authkey = chat_ret.json()["authkey"]
			self.endpoint = chat_ret.json()["endpoints"][0]
		else:
			logging.error("ERROR:")
			logging.error(chat_ret.text)
			logging.error(chat_ret.status_code)
			quit()

		cur_channel = self.channel
		cur_user_id = self.user_id
		cur_authkey = self.authkey

		# create a WS server factory with our protocol
		self.factory = WebSocketClientFactory(self.endpoint, debug=False)
		self.factory.protocol = MyClientProtocol

		# SSL client context: default
		if self.factory.isSecure:
			self.contextFactory = ssl.ClientContextFactory()
		else:
			self.contextFactory = None

		connectWS(self.factory, self.contextFactory)

class MyClientProtocol(WebSocketClientProtocol):

	def onConnect(self, response):
		logging.info("Server connected: {0}".format(response.peer))

	def onOpen(self):

		logging.info("WebSocket connection opened.")

		# Register user in chat
		packet = {
			"type":"method",
			"method":"auth",
			"arguments":[chat.channel, chat.user_id, chat.authkey]
		}

		self.sendMessage(json.dumps(packet).encode("utf-8"))

	def onMessage(self, payload, isBinary):
		if isBinary:
			logging.info("Binary message received: {0} bytes".format(len(payload)))
		else:
			logging.info("Message received: {0}".format(payload.decode('utf8')))
			logging.info(chat.channel)
		try:
			_checkMessage(json.loads(payload.decode('utf-8')))
		except NonNoneError as e:
			logging.error("ERROR - NonNoneError")
			logging.error(e)
		else:
			pass

	def onClose(self, wasClean, code, reason):
		logging.info("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':

	global main_chat
	config = _updateConfig()

	session = requests.Session()

	if not config:
		logging.error('\033[1;31mConfig file missing!\033[0m\n')
		logging.error('Please run setup before launching the bot.')
		logging.error('To do so run:\tpython3 setup.py')
		quit()
	else:
		addr = "https://beam.pro/api/v1"
		if config["channel"] != None or config["channel"].strip() != "":
			main_chan = config["channel"]
		else:
			chanOwner = input("Channel [Channel owner's username]: ").lower()
			chat_channel = session.get(
				addr + '/channels/' + chanOwner
			)

			if _checkStatus(chat_channel):
				main_chan = chat_channel.json()['id']
			else:
				logging.error('ERROR!')
				logging.error('Message:\t',control_channel.json()['message'])
				quit()

	observer = log.PythonLoggingObserver(loggerName='logname')
	observer.start()
	logging.basicConfig(stream=sys.stdout,
						level=logging.INFO,
						format='%(asctime)s [-] %(levelname)s:%(message)s')

	chat = Connection(addr=addr, channel=main_chan, session=session)

	reactor.run()
