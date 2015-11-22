import json
import os

if os.path.exists('data/config.json'):
	config = json.load(open('data/config.json', 'r'))
else:
	print ('\033[1;31mConfig file missing!\033[0m\n')
	print ('Please run setup before launching the bot.')
	print ('To do so run:\tpython3 setup.py')
	quit()

def _update_config():
	if os.path.exists('data/config.json'):
		config = json.load(open('data/config.json', 'r'))
		return config
	else:
		return False

def _get_auth_body():

	return {
		'username': config['username'],
		'password': config['password']
	}
