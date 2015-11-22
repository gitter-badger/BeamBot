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
	Version: 	3.3.2b
	Author: 	RPiAwesomeness
	Date:		November 4th, 2015

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

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

# PyBot modules
from tools import _get_auth_body, _update_config

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            # self.sendMessage(u"Hello, world!".encode('utf8'))
            # self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

	config = _update_config()

	if not config:
		print ('\033[1;31mConfig file missing!\033[0m\n')
		print ('Please run setup before launching the bot.')
		print ('To do so run:\tpython3 setup.py')
		quit()
	else:
		addr = config["beam_addr"]

	session = requests.Session()

	loginRet = session.post(
		addr + '/users/login',
		data=_get_auth_body()
	)

	if loginRet.status_code != requests.codes.ok:
		print (loginRet.text)

		user_id = loginRet.json()["id"]

	channel = config["channel"]

	chat_ret = session.get(
		addr + "/chats/{}".format(channel)
	)

	if chat_ret.status_code != requests.codes.ok:
		print ('ERROR!')
		print ('Message:\t',control_ret.json())
		print(control_ret.json())
		quit()

	chat_details = chat_ret.json()
	endpoint = chat_details["endpoints"][0]
	authkey = chat_details["authkey"]

	log.startLogging(sys.stdout)

	factory = WebSocketClientFactory(endpoint, debug=False)
	factory.protocol = MyClientProtocol

	reactor.connectTCP("127.0.0.1", 4001, factory)
	reactor.run()
