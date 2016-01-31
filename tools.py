import json
import os
import logging

from requests import codes
from exceptions import *

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
		logging.info(response["type"])

	if response["error"] != None:
		raise NonNoneError("error")

	if "authenticated" in response["data"]:
		if response["data"]["authenticated"] != True:
			raise NotAuthenticated

def _parseMessage(payload):
	if "authenticated" in payload["data"]:
		# We're authenticated, so return True & the user's roles
		return True, payload["data"]["roles"]
