import random
import time
from datetime import datetime
import sqlite3
import pickle
import requests
import os
import json

global prevTime, custCommands, WHITELIST, commandList

prevTime = {'tackle':{}, 'slap':{}, 'quote':{}, 'ping':{}, 'hug':{}, 'give':{}, 'dimes':{}, 'hey':{}, 'uptime':{}, 'whoami':{}, 'cmdList':{}, 'blame':{}}

config = json.load(open('data/config.json', 'r'))

if os.path.exists('data/whitelist{}.p'.format(config['CHANNEL'])):
	WHITELIST = pickle.load(open('data/whitelist{}.p'.format(config['CHANNEL']), 'rb'))
else:
	WHITELIST = ['pybot']
	pickle.dump(WHITELIST, open('data/whitelist{}.p'.format(config['CHANNEL']), 'wb'))

if os.path.exists('data/commands{}.json'.format(config['CHANNEL'])):
	custCommands = json.load(open('data/commands{}.json'.format(config['CHANNEL']), 'r'))
	print ('Custom commands loaded:\n' + str(custCommands))
else:
	custCommands = []
	with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
		f.write(str(custCommands))

if os.path.exists('data/commandList.json'):
	commandList = json.load(open('data/commandList.json', 'r'))
else:
	print ('Error:')
	print ('data/commandList.json is missing! !commands will not work')
	commandList = False

# End of do responses-specific modules
# ------------------------------------------------------------------------

def _checkTime(cmd, user, custom=False):
	curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

	if cmd in prevTime:		# Make sure the command exists, so no KeyError exceptions
		if user in prevTime[cmd]:	# Make sure the user exists in that command dictionary
			if (curTime - prevTime[cmd][user]) <= 31:	# Only every 30 seconds per user
				return True			# Too soon
			elif (curTime - prevTime[cmd][user]) >= 30:	# Under 30 seconds
				prevTime[cmd][user] = curTime
				return False

	# If execution gets to this point, then either user or command does not exist and we need to create a value for that
	prevTime[cmd] = {user : curTime}
	return False

# ------------------------------------------------------------------------
# End of do responses-specific modules
# ------------------------------------------------------------------------

def blame(user_name, curItem, is_mod):
	cmd = "blame"

	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:
			return None
	else:
		if curItem[1:][5] == " ":		# Is it a space?

			if curItem[1:][6] == "@":
				return curItem[8:] + " has been duly blamed! " + curItem[7:] + \
						" you have been blamed!"
			else:
				return curItem[7:] + " has been duly blamed! @" + curItem[7:] + \
						" you have been blamed!"
		else:
			return curItem[6:] + " has been duly blamed! @" + curItem[6:] + \
					" you have been blamed!"

def cmdList(user_name, curItem, is_mod):	# Returns list of commands

	global commandList

	response = ""
	cmd = "cmdList"

	if commandList == False:		# File missing
		return None					# So no response!
	else:

		if user_name not in WHITELIST:	# Command is whitelist-only
			return None

		else:
			cmdListUsage = commandList['usage']
			cmdList = commandList['list']

			msg = curItem.split()[1:]		# Split the command up to see if there are args

			if len(msg) >= 2:				# At least 2 items, so at least one arg
				if msg[1] in cmdListUsage:	# Does a key exist with that argument's value?
					return msg[1] + " - " + cmdListUsage[msg[1]] + " - " + cmdList[msg[1]]	# Return command + usage
			else:					# Just !commands, so list commands
				response += "Commands: "
				for cmd in cmdList:
					response += cmd + ", "

				return response

		return None					# If execution gets here, then we've got no matches

def custom(user_name, curItem, is_mod):	# Check unknown command, might be custom one
	global custCommands

	split = curItem[1:].split()
	cmd = split[0]
	response = ""

	print ('cmd:\t\t',cmd)
	print ('split:\t\t',split)

	if user_name in WHITELIST:	# Is the user on the whitelist? If so, ignore timeout
		for e in custCommands:	# Loop through the custom commands
			if e['cmd'] == cmd:		# Does the current entry equal the command?
				eArgs = e['response'].split('[[')	 # 1 - Split on occurrences of [[

				for i in range(0, len(eArgs)):

					stringCur = eArgs[i][0:4]  # 2 - String we're going to be editing, make it separate

					# 3 - Compare stringCur to real response variables
					if stringCur == 'args':	 # Replace with remainder of arguments
						# 3a - It's the args variable so join the arguments + rest of response (sans ]])
						if len(split[1:]) >= 1:
							response += (" ".join(split[1:]) + eArgs[i][4:].strip(']'))
						else:
							response += eArgs[i][4:].strip(']')
					elif stringCur == 'user':   # Replace with sending user
						# 3b - It's the user variable, so return the sending user + rest of response (sans ]])
						response += (user_name + eArgs[i][4:].strip(']'))
					else:
						# Just append the curent string item, it's not a response variable
						response += eArgs[i]

			return response

	if _checkTime(cmd, user_name, True):
		return None				# Too soon

	else:
		for e in custCommands:	# Loop through the custom commands
			if e['cmd'] == cmd:		# Does the current entry equal the command?
				eArgs = e['response'].split('[[')	 # 1 - Split on occurrences of [[
				for i in range(0, len(eArgs)):

					stringCur = eArgs[i][0:4]  # 2 - String we're going to be editing, make it separate

					# 3 - Compare stringCur to real response variables
					if stringCur == 'args':	 # Replace with remainder of arguments
						# 3a - It's the args variable so join the arguments + rest of response (sans ]])
						response += (" ".join(split[1:]) + eArgs[i][4:].strip(']'))
					elif stringCur == 'user':   # Replace with sending user
						# 3b - It's the user variable, so return the sending user + rest of response (sans ]])
						response += (user_name + eArgs[i][4:].strip(']'))
					else:
						# Just append the curent string item, it's not a response variable
						response += eArgs[i]

			print ('response:\t',response)
			return response

	return None 		# If execution gets to this point, it's not a command, so no response

def commandMod(user_name, curItem, is_mod):		# Command available to mods only

	global custCommands

	if user_name in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		split = curItem[1:].split()
		if len(split) >= 2:
			command = split[1]
			response = " ".join(split[2:])

			print ('cmd:\t',command)
			print ('response:\t',response)

			for cmd in custCommands:			# Loop through the list of custom commands JSON objects
				print ('cmd:\t\t',custCommands)
				print ('cmd[\'cmd\']:\t',cmd['cmd'])
				if cmd['cmd'] == command:	# Does the JSON object's command match the command we're making/updating?
					cmd['response'] = response 	# Update the response
					cmd['op'] = 'True'			# Update the OP-only value to True
					with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
						f.write(json.dumps(custCommands, sort_keys=cmd))

					# Command exists, so it has been updated
					return 'Command \'' + cmd['cmd'] + '\' updated! ' + cmd['response']

			# If we make it past the for loop, then the command doesn't exist, so make a new one

			newCMD = {
				'cmd':command,
				'op':'True',
				'response':response
			}

			custCommands.append(newCMD)

			print ('custCommands:\t',json.dumps(custCommands))

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				f.write(json.dumps(custCommands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		return None	 	# Return None because the command lacks a response

	else:
		return None		# Not whitelisted

def command(user_name, curItem, is_mod):			# Command available to anyone
	global custCommands

	if user_name in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		split = curItem[1:].split()
		if len(split) >= 2:
			command = split[1]
			response = " ".join(split[2:])

			print ('cmd:\t',command)
			print ('response:\t',response)

			for cmd in custCommands:			# Loop through the list of custom commands JSON objects
				if cmd['cmd'] == command:		# Does the JSON object's command match the command we're making/updating?
					cmd['op'] = 'False'			# Update the OP-only value to False
					cmd['response'] = response 	# Update the response
					with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
						cmd['cmd'] = cmd['cmd']
						f.write(json.dumps(custCommands, sort_keys=True))

					# Command exists, so it has been updated
					return 'Command \'' + cmd['cmd'] + '\' updated! ' + cmd['response']

			# If we make it past the for loop, then the command doesn't exist, so make a new one

			newCMD = {
				'cmd':command,
				'op':'False',
				'response':response
			}

			custCommands.append(newCMD)

			print ('custCommands:\t',json.dumps(custCommands))

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				f.write(json.dumps(custCommands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		return None	 	# Return None because the command lacks a response

	else:
		return None		# Not whitelisted

def commandRM(user_name, curItem, is_mod):			# Remove a command
	global custCommands

	if user_name in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		split = curItem[1:].split()
		if len(split) >= 2:
			cmd = split[1]
			for e in range(len(custCommands)):
				if custCommands[e]['cmd'] == cmd:
					print ('e:\t\t',custCommands[e]['cmd'])
					del custCommands[e]
					break

			with open('data/commands{}.json'.format(config['CHANNEL']), 'w') as f:
				print (custCommands)
				f.write(json.dumps(custCommands))

			return 'Command \'' + cmd + '\' removed!'

	else:
		return None						# Not whitelisted

def tackle(user_name, curItem, is_mod):
	cmd = 'tackle'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None
	if len(curItem[1:].split()) >= 2:
		rand = random.randrange(0, 51)
		if rand >= 45:	# Super rare response!
			return "pybot decides to be a momentary pacifist."
		else:			# Normal response
			rand = random.randrange(0, 31)
			if rand <= 5:
				return "pybot {} {}.".format("tackles", curItem[1:].split()[1])
			elif rand >= 6 and rand <= 10:
				return "pybot {} {}.".format("clobbers", curItem[1:].split()[1])
			elif rand >= 11 and rand <= 15:
				return "pybot {} {}.".format("creams", curItem[1:].split()[1])
			elif rand >= 16 and rand <= 20:
				return "pybot {} {}.".format("wallops", curItem[1:].split()[1])
			elif rand >= 21 and rand <= 25:
				return "pybot {} {}.".format("bashes", curItem[1:].split()[1])
			elif rand >= 26 and rand <= 31:
				return "pybot {} {}.".format("besets", curItem[1:].split()[1])
			else:
				return "pybot {} {}.".format("tackles", curItem[1:].split()[1])

def slap(user_name, is_mod):
	cmd = 'slap'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None
	return ":o Why on earth would I want to do that?"

def quote(user_name, curItem, is_mod):
	cmd = 'quote'
	"""
	If _checkTime() returns True then the command is on timeout, return nothing
	also, if the user is in the whitelist (mod or streamer or otherwise whitelisted)
	then just let them run it as much as they want
	"""

	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:
			return None

	split = curItem[1:].split()

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

	elif len(split) >= 3:		# It's add quote
		cmd = split[1]

		print ('split:\t\t',split)

		if cmd == "add":

			# Joins together with spaces all the items in the split list, then split it on the " marks
			split = " ".join(split[2:]).split('"')

			user = split[0]

			if user[0] == '@':
				user = user[1:]	# Remove the @ sign, we work without them

			# The user is the first item after !quote add
			if len(user.split()) != 1:	# It's just a username, anything more indicates an incorrect command
				return None

			# The quote is the second item(s) in the list
			quote = split[1]
			# The game is the third item in the list, but may have spaces on either side
			game = split[2].lstrip().rstrip()

			command = '''INSERT INTO quotes
						(name, game, quote)
						VALUES ("{}", "{}", "{}")'''.format(user, game, quote)

			with sqlite3.connect('data/beambot.sqlite') as con:
				cur = con.cursor()

				cur.execute(command)

			con = None

	with sqlite3.connect('data/beambot.sqlite') as con:
		cur = con.cursor()

		command = '''SELECT quote, game
					FROM quotes
					WHERE name LIKE \"%''' + user + '%\"'''

		print ('command:\t',command)

		cur.execute(command)

		results = cur.fetchall()

		print ("results:\t\t",results)
		print ("len(results):\t\t",len(results))

	if len(results) >= 1:	# Make sure there's at least 1 quote
		rand = random.randrange(len(results))

		quote = results[rand][0]
		game = results[rand][1]

		response = "\"" + quote + "\" - " + game + " - " + user

		return response
	else:		# No quotes in the database for user!
		return None

def ban(user_name, curItem, is_mod):
	if user_name in WHITELIST:		# Make sure it's a whitelisted user
		if len(curItem[1:].split()) >= 2:	# Make sure we have username to ban
			banUser = curItem[1:].split()[1]
			if banUser[0] == "@":
				banUser = banUser[1:]	# Remove the @ character
			return banUser + " has been chatbanned!", banUser

		else:
			return None # Wrong # of args
	else:			# Not whitelisted
		return None

def unban(user_name, curItem, is_mod):
	if user_name in WHITELIST:		# Make sure it's a whitelisted user
		if len(curItem[1:].split()[1]) >= 2:
			uBanUser = curItem[1:].split()[1]
			if uBanUser[0] == "@":
				uBanUser = banUser[1:]	# Remove the @ character

			return uBanUser + " has been un-banned!", uBanUser
	else:			# Not whitelisted
		return None

def ping(user_name, is_mod):
	cmd = 'ping'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None
	return "(>^.^)>-O ____|____ ° Q(^.^<) pong!"

def hug(user_name, curItem, is_mod):
	cmd = 'hug'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None

	if len(curItem[1:].split()) >= 2:
		hugUser = curItem[1:].split()[1]
		if hugUser[0] == "@":
			return "{} gives a great big hug to {}! <3".format(user_name, hugUser)
		else:	# Difference adds @ symbol if not included in the argument
			return "{} gives a great big hug to @{}! <3".format(user_name, hugUser)
	else:
		return None	# Wrong # of args

def give(user_name, curItem, is_mod):
	cmd = 'give'

	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None

	split = curItem[1:].split()
	if len(split) >= 3:
		user = split[1]	# User recieving dimes
		if user[0] == '@':
			user = user[1:]			# Remove the @ character
		try:	# Try to convert argument to int type
			numSend = int(split[2])	# Number of dimes being transferred
		except:	# Oops! User didn't provide an integer
			return None

		with sqlite3.connect('data/beambot.sqlite') as con:
			cur = con.cursor()

			command = '''SELECT gears
						FROM gears
						WHERE name=\"''' + user + '\"'

			cur.execute(command)
			results = cur.fetchall()

			if len(results) >= 1:
				userDimesOrig = results[0][0]

				if user_name == "pybot":	# If it's bot, ignore removal of dimes & # check
					userDimes = int(userDimesOrig) + int(numSend)

					command = '''UPDATE gears
								SET gears={}
								WHERE name="{}"'''.format(userDimes, user)

					cur.execute(command)

					return "@" + user + " now has " + str(userDimes) + " dimes!"

				if numSend <= userGearsOrig:	# Make sure the sending user has enough dimes

					userDimes = int(userDimesOrig) + int(numSend)

					command = '''UPDATE gears
								SET gears={}
								WHERE name="{}"'''.format(userDimes, user)

					cur.execute(command)

					return "@" + user + " now has " + str(userDimes) + " dimes!"

				else:
					return None

			else:		# User not in dimes database
				command = '''INSERT INTO gears
							(name, gears)
							VALUES ("{}", {})'''.format(user, str(numSend))

				cur.execute(command)	# Soooo... add 'em!

				return "@" + user + " now has " + str(numSend) + " dimes!"

	else:
		return None

def dimes(user_name, curItem, is_mod):
	cmd = 'dimes'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None

	split = curItem[1:].split()
	if len(split) >= 2:
		if split[1][0] == "@":
			user = split[1][1:]		# Remove @ character
		else:
			user = split[1]
	else:
		user = user_name

	with sqlite3.connect('data/beambot.sqlite') as con:
		cur = con.cursor()

		command = '''SELECT gears
					FROM gears
					WHERE name LIKE \"%''' + user + '%\"'''

		cur.execute(command)

		results = cur.fetchall()

		if len(results) >= 1:
			return "@" + user + " has " + str(results[0][0]) + " dimes."
		else:
			return "@" + user + " has no dimes! :o"

def hey(user_name, is_mod):
	cmd = 'hey'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None
	return "Saluton Mondo {}!".format(user_name)

def raid(user_name, curItem, is_mod):
	cmd = 'raid'
	if user_name not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		if raid[0] == "@":
			raid = raid[1:]	# Remove the @ character
		return "Stream's over everyone!"\
				" Thanks for stopping by, let's go raid @{} at beam.pro/{}!".format(raid, raid)

def twitch(user_name, curItem, is_mod):
	cmd = 'raid'
	if user_name not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		if raid[0] == "@":
			raid = raid[1:]			# Remove the @ character
		return "Stream's over everyone!"\
			" Thanks for stopping by, let's go raid {} at twitch.tv/{}!".format(raid, raid)

def raided(user_name, curItem, is_mod):
	cmd = 'raided'
	if user_name not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		if raid[0] == "@":
			return "Thank you so much {} for the raid!"\
				" Everyone go give them some love at beam.pro/{}!".format(raid, raid)
		else:
			return "Thank you so much @{} for the raid!"\
				" Everyone go give them some love at beam.pro/{}!".format(raid, raid)

def commands(user_name, is_mod):
	commandList = json.loads(open('data/commands{}.json'.format(config['CHANNEL']), 'r'))

	return ", ".join(commandList)

# def throw(user_name, curItem):
# 	cmd = 'throw'
# 	if user_name in WHITELIST:
#

def uptime(user_name, initTime, is_mode):
	cmd = 'uptime'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None

	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(user_name, is_mod):
	cmd = 'whoami'
	if _checkTime(cmd, user_name) and user_name not in WHITELIST:
		if not is_mod:		# if _checkTime() returns True then the command is on timeout, return nothing
			return None

	return "Uh...you're {}. Are you all right? :)".format(user_name)

def whitelist(user_name, curItem, is_mod):		# Add user to command timeout whitelist
	global WHITELIST

	if user_name not in WHITELIST:	# Make sure it's me (in the future, the streamer)

		if len(curItem[1:].split()) >= 2:	# Make sure the # of args is correct
			WHITELIST.append(curItem[1:].split()[2])	# Append the new user to the whitelist!
			pickle.dump(WHITELIST, open('data/whitelist{}.p'.format(config['CHANNEL']), 'wb'))
			response = str("User " + curItem[1:].split()[2] + " added to whitelist!")
			return response
		else:
			return None
	else:			# Not me/streamer, ignored
		return None

def whitelistRM(user_name, curItem, is_mod):		# Add user to command timeout whitelist
	global WHITELIST

	if user_name not in WHITELIST:	# Make sure it's me

		if len(curItem[1:].split()) >= 2:	# Make sure the # of args is correct

			print ('curItem:\t',curItem)
			WHITELIST = pickle.load(open('data/whitelist{}.p'.format(config['CHANNEL']), 'rb'))
			if curItem[1:].split()[2] in WHITELIST:		# Make sure user being removed really is removable!
				WHITELIST.remove(curItem[1:].split()[2])	# Append the new user to the whitelist!
				pickle.dump(WHITELIST, open('data/whitelist{}.p'.format(config['CHANNEL']), 'wb'))
				response = str("User " + curItem[1:].split()[2] + " removed from whitelist!")
				return response

			else:
				return "User " + curItem[1:].split()[2] + " not in whitelist!"
		else:
			return None
	else:
		return None

def whitelistLS(user_name, curItem, is_mod):
	global WHITELIST

	WHITELIST = pickle.load(open('data/whitelist{}.p'.format(config['CHANNEL']), 'rb'))
	response = 'Whitelisted users: '
	for item in WHITELIST:
		response += item + ", "

	return response[:-2]
