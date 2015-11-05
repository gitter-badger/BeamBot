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

import random
import time
from datetime import datetime
import sqlite3
import pickle
import requests
import os
import json

# PyBot Modules
import usage
import schedule as schedule_mod
import store as store_mod
import quotes
import currency

global prevTime, cust_commands, commandList, count_vars

prevTime = {'tackle':{}, 'slap':{}, 'quote':{}, 'ping':{}, 'hug':{}, 'give':{}, 'dimes':{}, 'hey':{}, 'uptime':{}, 'whoami':{}, 'cmdList':{}, 'blame':{}}

config = json.load(open('data/config.json', 'r'))

addr = config['BEAM_ADDR']

if os.path.exists('data/commands{}.json'.format(config['CHANNEL'])):
	cust_commands = json.load(open('data/commands{}.json'.format(config['CHANNEL']), 'r'))
	print ('Custom commands loaded:\n' + str(cust_commands))
	count_vars = {}
	for e in cust_commands:
		count_vars[e['cmd']] = 0

else:
	cust_commands = []
	count_vars = {}
	with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
		f.write(str(cust_commands))

if os.path.exists('data/commandList.json'):
	commandList = json.load(open('data/commandList.json', 'r'))
else:
	print ('\033[1;31mCommand list file (data/commandList.json) missing!\033[0m\n')
	print ('data/commandList.json is missing! !commands and command usage will not work')
	commandList = False

# End of do responses-specific modules
# ------------------------------------------------------------------------

def _checkTime(cmd, user, is_mod, is_owner, custom=False):

	if is_mod or is_owner:
		return False		# No need to check if it's mod/owner

	curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

	if cmd in prevTime:		# Make sure the command exists, so no KeyError exceptions
		if user in prevTime[cmd]:	# Make sure the user exists in that command dictionary
			if (curTime - prevTime[cmd][user]) <= (config['cmd_timeout'] + 1):	# Only every 30 seconds per user
				return True			# Too soon
			elif (curTime - prevTime[cmd][user]) >= config['cmd_timeout']:	# Under 30 seconds
				prevTime[cmd][user] = curTime
				return False

	# If execution gets to this point, then either user or command does not exist and we need to create a value for that
	prevTime[cmd] = {user : curTime}
	return False

# ------------------------------------------------------------------------
# End of do responses-specific modules
# ------------------------------------------------------------------------

def blame(user_name, cur_item, is_mod, is_owner):
	cmd = "blame"

	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None
	else:
		print ('cur_item:\t',cur_item[1:])
		if len(cur_item[1:]) > 5:
			if cur_item[1:][5] == " ":		# Is it a space?

				if cur_item[1:][6] == "@":	# Is it an @USERNAME?
					return cur_item[7:] + " has been duly blamed! " + cur_item[7:] + \
							" you have been blamed!"
				else:			# Nope, add the @ symbol
					return cur_item[6:] + " has been duly blamed! @" + cur_item[7:] + \
							" you have been blamed!"
			else:				# Nope, take the 6th character onward
				return cur_item[6:] + " has been duly blamed! @" + cur_item[6:] + \
						" you have been blamed!"

		else:	# It's too short to include anyone to blame, so return usage
			return usage.prepCmd(user_name, cmd, is_mod, is_owner)

def cmdList(user_name, cur_item, is_mod, is_owner):	# Returns list of commands

	global commandList

	response = ""
	cmd = "cmdList"

	if commandList == False:		# File missing
		return None					# So no response!
	else:

		if is_mod or is_owner:	# Command is elevated privledges user-only
			cmdListUsage = commandList['usage']
			cmdList = commandList['list']

			if len(cur_item.split()) >= 2:		# At least 2 items, so at least one arg
				cmdSplit = cur_item.split()[1:][0]		# Split the command up to see if there are args
				if cmdSplit in cmdListUsage:	# Does a key exist with that argument's value?
					response = "Usage: " + cmdListUsage[cmdSplit] + " - " + cmdList[cmdSplit]
					# In future, make this return Command & Usage in separate messages
					return response # Return command + usage

			else:					# Just !commands, so list commands
				response += "Commands: "
				for cmd in sorted(cmdList):
					response += cmd + ", "

				response = response[:-1]
				# In future, make this return all-access & custom commands separately - exclude mod & owner-only
				return response[:-1]
		else:
			return None

		return None					# If execution gets here, then we've got no matches

def custom(user_name, cur_item, is_mod, is_owner):	# Check unknown command, might be custom one
	global cust_commands

	split = cur_item[1:].split()
	cmd = split[0]
	response = ""

	if _checkTime(cmd, user_name, True, is_mod, is_owner):
		print ('checkTime')
		return None				# Too soon

	else:		# Not mod or owner, but not time-out, so let it run
		for e in cust_commands:	# Loop through the custom commands
			if e['cmd'] == cmd:		# Does the current entry equal the command?
				eArgs = e['response'].split('[[')	 # 1 - Split on occurrences of [[

				toDel = []

				for i in range(0, len(eArgs)):
					if eArgs[i] == "":
						toDel.append(i)

				for i in toDel:
					del eArgs[i]

				for i in range(0, len(eArgs)):

					string_cur = eArgs[i]  # 2 - String we're going to be editing, make it separate

					# 3 - Compare string_cur to real response variables
					if string_cur[0:4] == 'args':	 # Replace with remainder of arguments
						# 3a - Join the arguments + rest of response (sans ]])
						if len(split[1:]) >= 1:
							response += (" ".join(split[1:]) + eArgs[i][4:].strip(']'))
						else:
							response += eArgs[i][4:].strip(']')
					elif string_cur[0:4] == 'user':   # Replace with sending user
						# 3b - Return the sending user + rest of response (sans ]])
						response += (user_name + eArgs[i][4:].strip(']'))

					elif string_cur[0:5] == "count":	# Replace with a incremental variable
						# 3c - Return that counter + iterate it or create it if it doesn't exist
						if cmd in count_vars:
							count_vars[cmd] += 1
							response += str(count_vars[cmd]) + " ".join(eArgs[i][5:].split(']')[1:])
						else:
							count_vars[cmd] = 0
							response += str(count_vars[cmd]) + " ".join(eArgs[i][5:].split(']')[1:])

					elif string_cur[0:8] == "currency":
						# 3d - Return the users' currency total and possibly change the total
						currency_ret, user = dimes(user_name, user_name, is_mod, is_owner)		# Username, username for currency, is_mod, is_owner

						response += currency_ret

					else:
						# Just append the curent string item, it's not a response variable
						response += eArgs[i]

		if response != "":
			return response
		else:
			return None

def editCommand(user_name, cur_item, is_mod, is_owner, is_mod_only):
	global cust_commands

	if is_mod or is_owner:	# Make sure the user is a mod or streamer
		split = cur_item[1:].split()
		print ('split:\t',split)

		if len(split) >= 2:
			command = split[2]
			response = " ".join(split[3:])

			print ('response:\t',response)

			for cmd in cust_commands:			# Loop through the list of custom commands JSON objects
				if cmd['cmd'] == command:		# Does the JSON object's command match the command we're making/updating?

					if is_mod_only:				# Checks if it's OP-only
						cmd['op'] = 'True'		# Update the OP-only value to True
					else:
						cmd['op'] = 'False'		# Update the OP-only value to False

					cmd['response'] = response 	# Update the response

					with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
						cmd['cmd'] = cmd['cmd']
						f.write(json.dumps(cust_commands, sort_keys=True))

					# Command exists, so it has been updated
					return 'Command \'' + cmd['cmd'] + '\' updated! ' + cmd['response']
		else:
			return None	 	# Return None because the command lacks a response

	else:
		return None			# Return None because the user isn't mod or owner

def command(user_name, cur_item, is_mod, is_owner):			# Command available to anyone
	global cust_commands

	if is_mod or is_owner:	# Make sure the user is a mod or streamer
		split = cur_item[1:].split()
		print ('split:\t',split)

		if len(split) >= 2:
			command = split[2]
			response = " ".join(split[3:])

			print ('response:\t',response)

			# If we make it past the for loop, then the command doesn't exist, so make a new one
			newCMD = {
				'cmd':command,
				'op':'False',
				'response':response
			}

			cust_commands.append(newCMD)

			print ('cust_commands:\t',json.dumps(cust_commands))

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				f.write(json.dumps(cust_commands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		return None	 	# Return None because the command lacks a response

	else:
		return None		# Not mod or owner

def commandMod(user_name, cur_item, is_mod, is_owner):		# Command available to mods only

	global cust_commands

	if is_mod or is_owner:	# Make sure the user is a mod or streamer
		split = cur_item[1:].split()
		if len(split) >= 2:
			command = split[2]
			response = " ".join(split[3:])

			print ('response:\t',response)

			for cmd in cust_commands:			# Loop through the list of custom commands JSON objects
				print ('cmd[\'cmd\']:\t',cmd['cmd'])
				if cmd['cmd'] == command:	# Does the JSON object's command match the command we're making/updating?
					cmd['response'] = response 	# Update the response
					cmd['op'] = 'True'			# Update the OP-only value to True
					with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
						f.write(json.dumps(cust_commands, sort_keys=cmd))

					# Command exists, so it has been updated
					return 'Command \'' + cmd['cmd'] + '\' updated! ' + cmd['response']

			# If we make it past the for loop, then the command doesn't exist, so make a new one

			newCMD = {
				'cmd':command,
				'op':'True',
				'response':response
			}

			cust_commands.append(newCMD)

			print ('cust_commands:\t',json.dumps(cust_commands))

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				f.write(json.dumps(cust_commands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		response = usage.prepCmd(user, "command+", is_mod, is_owner) # Return None because the command lacks a response
		return response

	else:
		return None		# Not mod or owner

def commandRM(user_name, cur_item, is_mod, is_owner):			# Remove a command
	global cust_commands

	if is_mod or is_owner:	# Make sure the user is a mod or streamer
		split = cur_item[1:].split()
		if len(split) >= 2:
			cmd = split[2]
			for e in range(len(cust_commands)):
				if cust_commands[e]['cmd'] == cmd:
					print ('e:\t\t',cust_commands[e]['cmd'])
					del cust_commands[e]

					break

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				print (cust_commands)
				f.write(json.dumps(cust_commands))

			return 'Command \'' + cmd + '\' removed!'

	else:
		return None						# Not whitelisted

def tackle(user_name, cur_item, is_mod, is_owner):
	cmd = 'tackle'
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	if len(cur_item[1:].split()) >= 2:
		rand = random.randrange(0, 51)
		if rand >= 45:	# Super rare response!
			return "pybot decides to be a momentary pacifist."
		else:			# Normal response
			rand = random.randrange(0, 31)
			if rand <= 5:
				return "pybot {} {}.".format("tackles", cur_item[1:].split()[1])
			elif rand >= 6 and rand <= 10:
				return "pybot {} {}.".format("clobbers", cur_item[1:].split()[1])
			elif rand >= 11 and rand <= 15:
				return "pybot {} {}.".format("creams", cur_item[1:].split()[1])
			elif rand >= 16 and rand <= 20:
				return "pybot {} {}.".format("wallops", cur_item[1:].split()[1])
			elif rand >= 21 and rand <= 25:
				return "pybot {} {}.".format("bashes", cur_item[1:].split()[1])
			elif rand >= 26 and rand <= 31:
				return "pybot {} {}.".format("besets", cur_item[1:].split()[1])
			else:
				return "pybot {} {}.".format("tackles", cur_item[1:].split()[1])

	else:		# Too short, no user supplied
		return usage.prepCmd(user_name, "tackle", is_mod, is_owner)

def slap(user_name, is_mod, is_owner):
	cmd = 'slap'
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	return ":o Why on earth would I want to do that?"

def set(user_name, user_id, cur_item, is_mod, is_owner):

	if not is_owner:	# Don't want anyone other than the owner running this
		return None

	if len(cur_item) > 2:	# SET SETTINGNAME SETTING

		if cur_item[1] == "currencyName":	# Set the currency name
			config['currency_name'] = cur_item[2]
			response = "Currency name is now " + config['currency_name']

		elif cur_item[1] == "commandTimeout":	# Set the command time-out
			try:
				timeout = int(cur_item[2])
			except:		# If that conversion failed, it's not a clean integer
				return "The command timeout must be an integer (Usage: !set commandTimeout [integer])"

			config['cmd_timeout'] == cur_item[2]

			response = "Command timeout is now " + str(config['cmd_timeout'])

		elif cur_item[1] == "announceEnter":	# Announce user entering
			if cur_item[2].lower() == "true":
				config['announce_enter'] = True
				response = "Users joining the stream will now be announced"
			elif cur_item[2].lower() == "false":
				config['announce_enter'] = False
				response = "Users joining the stream will not be announced"
			else:
				response = "Usage: !set announceEnter [true/false]"

		elif cur_item[1] == "announceLeave":	# Announce user leaving
			if cur_item[2].lower() == "true":
				config['announce_leave'] = True
				response = "Users leaving the stream will now be announced"
			elif cur_item[2].lower() == "false":
				config['announce_leave'] = False
				response = "Users leaving the stream will not be announced"
			else:
				response = "Usage: !set announceLeave [true/false]"

		else:
			return usage.prepCmd(user_name, "set", is_mod, is_owner)

		if os.path.exists('data/config.json'):
			with open('data/config.json', 'w') as f:
				json.dump(config, f, sort_keys=True, indent=4, separators=(',', ': '))

		return response

	else:
		return usage.prepCmd(user_name, "set", is_mod, is_owner)

def schedule(user_name, cur_item, is_mod, is_owner, websocket):
	cmd = "schedule"

	if not is_mod or not is_owner:
		return None 	# Mod/owner only

	if len(cur_item) < 3:
		return usage.prepCmd(user_name, "schedule", is_mod, is_owner)

	cmd_cmd = cur_item[1]

	if cmd_cmd.lower() == "add":
		if len(cur_item) >= 3:
			text = cur_item[2:]
			response = schedule_mod.register(text, websocket)
		else:
			 return "Usage: !schedule add MESSAGEHERE"

	elif cmd_cmd.lower() == "remove":
		try:
			schedule_id = int(cur_item[2])
		except:
			return "Usage: !schedule remove MESSAGEIDHERE"

		response = schedule_mod.msg_rm(schedule_id, websocket)

	elif cmd_cmd.lower() == "update":
		try:
			schedule_id = int(cur_item[2])
		except:
			return "Usage: !schedule update MESSAGEIDHERE MESSAGETEXTHERE"

		if len(cur_item) >= 3:
			text = cur_item[3:]
			response = schedule_mod.edit_msg(text, schedule_id, websocket)
		else:
			return "Usage: !schedule update MESSAGEIDHERE MESSAGETEXTHERE"
	else:
		return usage.prepCmd(user_name, "schedule", is_mod, is_owner)

	return response

def store(user_name, cur_item, is_mod, is_owner):
	cmd = "store"

	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None

	if is_mod or is_owner:
		if len(cur_item) >= 2:
			if cur_item[1] == "add" or cur_item[1] == "remove" or cur_item[1] == "edit":
				return store_mod.storeEdit(user_name, cur_item, is_mod, is_owner)
			else:
				return usage.prepCmd(user_name, "store", is_mod, is_owner)

	return store_mod.storeList(user_name, is_mod, is_owner)

def store_buy(user_name, cur_item, is_mod, is_owner):
	cmd = "buy"

	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None

	return store_mod.storeBuy(user_name, cur_item, is_mod, is_owner)

def quote(user_name, cur_item, is_mod, is_owner):
	cmd = 'quote'

	"""
	If _checkTime() returns True then the command is on timeout, return nothing
	also, if the user is mod or streamer then just let them run it as much as
	they want.
	"""
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	split = cur_item[1:].split()

	if len(split) == 1:		# It's just 1 string, get random quote
		command = '''SELECT name
					FROM quotes'''

		with sqlite3.connect('data/beambot.sqlite') as con:
			cur = con.cursor()

			cur.execute(command)

			results = cur.fetchall()

			if len(results) < 1:
				return None
			else:
				rand = random.randrange(len(results))

			user = results[rand][0]

	elif len(split) == 2:		# If it's just 2 strings, get quote for user
		user = split[1]		# Set the user to be the second string

		if user[0] == "@":	# The first character is the @ character - remove that
			user = user[1:]

		# This code checks if it's someone failing at the !quote command
		elif user == "add" or user == "remove" or user == "update":
			return usage.prepCmd(user_name, "quote", is_mod, is_owner)

	elif len(split) >= 3:		# It's add/remove quote
		if is_mod or is_owner:

			cmd_cmd = split[1]

			if cmd_cmd == "add" or cmd_cmd == "remove":

				quote_user = split[2]

				if quote_user[0] == '@':
					quote_user = quote_user[1:]	# Remove the @ sign, we work without them

				if cmd_cmd == "add":
					response = quotes.addQuote(user_name, quote_user, split, is_mod, is_owner)
					return response

				elif cmd_cmd == "remove":
					response = quotes.removeQuote(user_name, split, is_mod, is_owner)
					return response

		else:
			return None

	else:
		return usage.prepCmd(user_name, "quote", is_mod, is_owner)

	with sqlite3.connect('data/beambot.sqlite') as con:
		cur = con.cursor()

		command = '''SELECT quote, id
					FROM quotes
					WHERE name LIKE \"%''' + user + '%\"'''

		cur.execute(command)

		results = cur.fetchall()

		print ("results:\t\t",results)

	if len(results) >= 1:	# Make sure there's at least 1 quote
		rand = random.randrange(len(results))

		quote = results[rand][0]
		quote_id = results[rand][1]

		response = quote + " - " + user

		return response

	else:		# No quotes in the database for user!
		return "Oh noes! There are no quotes :( Try adding some via !quote add!"

def ban(user_name, cur_item, is_mod, is_owner):
	if is_mod or is_owner:		# Only want mods/owners to have ban control
		if len(cur_item[1:].split()) >= 2:	# Make sure we have username to ban
			ban_user = cur_item[1:].split()[1]
			if ban_user[0] == "@":
				ban_user = ban_user[1:]	# Remove the @ character
			return ban_user + " has been chatbanned!", ban_user

		else:	# Wrong # of args
			ban_user = ""
			return usage.prepCmd(user_name, "ban", is_mod, is_owner), ban_user
	else:			# Not mod/owner
		return None

def unban(user_name, cur_item, is_mod, is_owner):
	if is_mod or is_owner:		# Only want mods/owners to have ban control

		if len(cur_item[1:].split()) >= 2:
			uban_user = cur_item[1:].split()[1]
			if uban_user[0] == "@":
				uban_user = ban_user[1:]	# Remove the @ character

			return uban_user + " has been un-banned!", uban_user

		else:	# Wrong # of args
			uban_user = ""
			return usage.prepCmd(user_name, "unban", is_mod, is_owner), uban_user
	else:			# Not owner/mod
		return None

def ping(user_name, is_mod, is_owner):
	cmd = 'ping'
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	return "Pong!"

def hug(user_name, cur_item, is_mod, is_owner):
	cmd = 'hug'

	if _checkTime(cmd, user_name, is_mod, is_owner):		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	if len(cur_item[1:].split()) >= 2:

		hugUser = cur_item[1:].split()[1]

		return "{} gives a great big hug to {}! <3".format(user_name, hugUser)

	else:	# Wrong # of args
		return usage.prepCmd(user_name, "hug", is_mod, is_owner)

def give(user_name, cur_item, is_mod, is_owner):
	cmd = 'give'

	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None

	if cur_item[0] == "auto":
		return currency.autoCurrency(cur_item[1], cur_item[2])
	else:
		return currency.give(user_name, cur_item, is_mod, is_owner)

def dimes(user_name, cur_item, is_mod, is_owner):
	cmd = 'dimes'

	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None, user_name

	return currency.dimes(user_name, cur_item, is_mod, is_owner)

def hey(user_name, is_mod, is_owner):
	cmd = 'hey'
	if _checkTime(cmd, user_name, is_mod, is_owner):
		return None
	return "Hey! {}! Listen!".format(user_name)

def raid(user_name, cur_item, is_mod, is_owner):
	cmd = 'raid'

	if is_mod or is_owner:	# Check if mod or owner
		split = cur_item[1:].split()
		if len(split) >= 2:
			raid = split[1]
			if raid[0] == "@":
				raid = raid[1:]	# Remove the @ character
			return "Stream's over everyone!"\
					" Thanks for stopping by, let's go raid @{} at beam.pro/{}!".format(raid, raid)

		else:		# Wrong # of args
			return usage.prepCmd(user_name, "raid", is_mod, is_owner)

	else:
		return None

def twitch(user_name, cur_item, is_mod, is_owner):
	cmd = 'twitch'

	if is_mod or is_owner:	# Check if user is owner/mod

		split = cur_item[1:].split()
		if len(split) >= 2:
			raid = split[1]
			if raid[0] == "@":
				raid = raid[1:]			# Remove the @ character
			return "Stream's over everyone!"\
				" Thanks for stopping by, let's go raid {} at twitch.tv/{}!".format(raid, raid)

		else:		# Wrong # of args
			return usage.prepCmd(user_name, "twitch", is_mod, is_owner)

	else:
		return None

def raided(user_name, cur_item, is_mod, is_owner):
	cmd = 'raided'

	if not is_mod or not is_owner:	# Check if user is owner/mod
		return None

	split = cur_item[1:].split()
	print ("responses637:\t",split)
	if len(split) >= 2:
		raid = split[1]
		if raid[0] == "@":
			return "Thank you so much {} for the raid!"\
				" Everyone go give them some love at beam.pro/{}!".format(raid, raid)
		else:
			return "Thank you so much @{} for the raid!"\
				" Everyone go give them some love at beam.pro/{}!".format(raid, raid)

	else:		# Wrong # of args
		return usage.prepCmd(user_name, "raided", is_mod, is_owner)

def commands(user_name, is_mod, is_owner):
	if os.path.exists('data/commands{}.json'.format(config['CHANNEL'])):
		commandList = json.loads(open('data/commands{}.json'.format(config['CHANNEL']), 'r'))
		return ", ".join(commandList)
	else:
		return "Command list missing!"

def uptime(user_name, initTime, is_mod, is_owner):
	cmd = 'uptime'
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(user_name, is_mod, is_owner):
	cmd = 'whoami'
	if _checkTime(cmd, user_name, is_mod, is_owner):
			return None

	return "Uh...you're {}. Are you all right? :)".format(user_name)
