"""This module returns the usage from the data/commandList.json file for
various commands."""

import json
import os
from datetime import datetime

prevTime = {}

if os.path.exists('data/commandList.json'):
	cmdList = json.load(open('data/commandList.json', 'r'))['usage']
else:
	print ('\033[1;31mCommand list file (data/commandList.json) missing!\033[0m\n')
	print ('!commands and usage will not work!')
	cmdList = None		# Set it to None so we know that it wasn't there

def _checkTime(user, is_mod, is_owner):
	if is_mod or is_owner:
		return False	# It's a mod or stream owner, no timeout

	else:
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime:	# Make sure the user exists
			if (curTime - prevTime[cmd][user]) <= int((config['cmd_timeout'] + 1)):	# Only every 30 seconds per user
				return True			# Too soon
			elif (curTime - prevTime[cmd][user]) >= int(config['cmd_timeout']):	# Under 30 seconds
				prevTime[cmd][user] = curTime
				return False

		# If execution gets to this point, then the user lacks an entry and we need to create a value for that
		prevTime[user] = curTime
		return False

def prepCmd(user, cmd, is_mod, is_owner):

	if _checkTime(user, is_mod, is_owner):	# Make sure there's no timeout
		return None

	else:
		if cmdList != None:	# It's not None, so there are custom commands
			if cmd == "set":	# Special usage for !set Command
				# Update commandList.json to include !set & specific usage
				return "Bot configuration options: currencyName, commandTimeout, announceEnter, announceLeave, announceFollow"

			if cmd in cmdList:	# We should never get any that aren't part of the list, but let's be safe
				return "Usage: " + cmdList[cmd]
			else:
				print ('No usage for command', cmd + "!")
				return None

		else:
			return "Usage currently unavailable!"
