import json
import os
import logging

from requests import codes
from exceptions import *
from messageClasses import *

global Parent

if os.path.exists('data/config.json'):
	config = json.load(open('data/config.json', 'r'))
else:
	print ('\033[1;31mConfig file missing!\033[0m\n')
	print ('Please run setup before launching the bot.')
	print ('To do so run:\tpython3 setup.py')
	quit()

def _updateConfig():
	if os.path.exists('data/config.json'):
		config = json.load(open('data/config.json', 'r'))
		return config
	else:
		return False

def _getAuthBody():

	return {
		'username': config['username'],
		'password': config['password']
	}

def _checkStatus(response):
	if response.status_code != codes.ok:
		return False
	else:
		return True

def _checkMessage(response):

	if "type" in response:
		logging.info("Response type:\t" + response["type"])
	else:
		logging.warning("Totally confused here - no type key")

	if "error" in response:
		if response["error"] != None:
			raise NonNoneError("error")

	if "authenticated" in response["data"]:
		if response["data"]["authenticated"] != True:
			raise NotAuthenticated
		else:
			return True
	else:
		logging.info("tools51:\t" + str(response))

		return None

def _parseMessage(payload):
	if "type" in payload:
		if payload["type"] == "event:
			if "event" in payload:
				if payload["event"] == "ChatMessage":
					data = payload["data"]
					# Iterate through the message section
					for segment in data["message"]:
						segment
					msg = Message(data["user_name"], data["user_roles"], data["user_id"], msg_text)
	pass

def _setParent(parent):
	global Parent

	Parent = parent

def _getParent():
	global Parent

	return Parent
