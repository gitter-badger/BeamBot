import random
import time
from datetime import datetime
import sqlite3
import pickle
import requests
import os
import json

# Full list of commands
"""
!tackle - Tackle a user
!slap   - Slap a user
!quote  - Post a quote
!ping   - Ping Pong!
!hug    - Hug a user
!give   - Give dimes/currency to a user
!dimes/currency  - Get # of dimes/currency for user
!hey    - Basically say hi to the Bot
!uptime - How long has the bot been running?
!raid 	- End of Stream command, provides link to Beam.pro channel
!raided - Thank a raider who raided you
!whoami - Who are you - classic whoami command
!command   - Create new command for anyone to use
!command+  - Create mod-only command
!command-  - Remove command
!ban       - Ban a user from chatting
!whitelist - Whitelist a user to remove command restrictions
!goodbye   - Turn off the bot
"""

global prevTime, custCommands

prevTime = {'tackle':{}, 'slap':{}, 'quote':{}, 'ping':{}, 'hug':{}, 'give':{}, 'dimes':{}, 'hey':{}, 'uptime':{}, 'whoami':{}}

if os.path.exists('data/whitelist.p'):
	WHITELIST = pickle.load(open('data/whitelist.p', 'rb'))
else:
	WHITELIST = ['ParadigmShift3d','pybot']
	pickle.dump(WHITELIST, open('data/whitelist.p', 'wb'))

if os.path.exists('data/commands.json'):
	custCommands = json.load(open('data/commands.json', 'r'))
	print ('Custom commands loaded:\n' + str(custCommands))
else:
	custCommands = []
	with open('data/commands.json', 'w') as f:
		f.write(str(custCommands))

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

def custom(userName, curItem):	# Check unknown command, might be custom one
	global custCommands

	cmd = curItem[1:].split()[0]

	if userName in WHITELIST:	# Is the user on the whitelist?
		for e in custCommands:	# Loop through the custom commands
			print ('e:\t\t',str(e))
			if e['cmd'] == cmd:		# Does the current entry equal the command?
				eArgs = e['cmd'].split("[[")
				print ('eArgs:\t',eArgs)
				if len(eArgs) >= 1:		# Make sure there's actually some args
					print ('here')
					for i in range(0, len(eArgs)):
						print ('eArags[i]:\t',eArgs[i])
						eArgs[i] = eArgs[i].replace(']]', '')
						print ('eArags[i]:\t',eArgs[i])
						if eArgs[i][0:3] == 'args':		# Use all the arguments
							eArgs[i] = eArgs[i].replace(response[i][4:], '')
							print ('eArgs[i]:\t',eArgs[i])
						elif eArgs[i][0:3] == 'user':	# Use the sending user
							pass

				return e['response']		# If op, then just automatically return response

	if _checkTime(cmd, userName, True):

		for e in custCommands:	# Loop through the custom commands
			if e['op']:			# Is it op-only?
				return None		# Return nothing because user is not whitelisted because program execution is here
			else:				# Not op-only
				return e['response']	# Return proper response

	return None 		# If execution gets to this point, it's not a command, so no response

def commandMod(userName, curItem):		# Command available to mods only

	global custCommands

	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
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
					with open('data/commands.json', 'w') as f:
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

			with open('data/commands.json', 'w') as f:
				f.write(json.dumps(custCommands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		return None	 	# Return None because the command lacks a response

	else:
		return None		# Not whitelisted

def command(userName, curItem):			# Command available to anyone
	global custCommands

	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
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
					with open('data/commands.json', 'w') as f:
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

			with open('data/commands.json', 'w') as f:
				f.write(json.dumps(custCommands))		# Update the stored JSON file

			return 'Command \'' + newCMD['cmd'] + '\' created! ' + newCMD['response']

		return None	 	# Return None because the command lacks a response

	else:
		return None		# Not whitelisted

def commandRM(userName, curItem):			# Remove a command
	global custCommands

	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		split = curItem[1:].split()
		if len(split) >= 2:
			cmd = split[1]
			for e in range(len(custCommands)):
				if custCommands[e]['cmd'] == cmd:
					print ('e:\t\t',custCommands[e]['cmd'])
					del custCommands[e]
					break

			with open('data/commands.json', 'w') as f:
				print (custCommands)
				f.write(json.dumps(custCommands))

			return 'Command \'' + cmd + '\' removed!'

	else:
		return None						# Not whitelisted

def tackle(userName, curItem):
	cmd = 'tackle'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
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

def slap(userName):
	cmd = 'slap'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None
	return ":o Why on earth would I want to do that?"

def quote(userName, curItem):
	cmd = 'quote'
	"""
	If _checkTime() returns True then the command is on timeout, return nothing
	also, if the user is in the whitelist (mod or streamer or otherwise whitelisted)
	then just let them run it as much as they want
	"""

	if _checkTime(cmd, userName) and userName not in WHITELIST:
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
	elif len(split) >= 3:		# It's add quote
		cmd = split[1]

		print ('split:\t\t',split)

		if cmd == "add":

			# Joins together with spaces all the items in the split list, then split it on the " marks
			split = " ".join(split[2:]).split('"')

			user = split[0]

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

def ban(userName, curItem):
	if userName in WHITELIST:		# Make sure it's a whitelisted user
		if len(curItem[1:].split()) >= 2:	# Make sure we have username to ban
			banUser = curItem[1:].split()[1]
			return banUser + " has been chatbanned!", banUser

		else:
			return None # Wrong # of args
	else:			# Not whitelisted
		return None

def unban(userName, curItem):
	if userName in WHITELIST:		# Make sure it's a whitelisted user
		if len(curItem[1:].split()[1]) >= 2:
			uBanUser = curItem[1:].split()[1]
			return uBanUser + " has been un-banned!", uBanUser
	else:			# Not whitelisted
		return None

def ping(userName):
	cmd = 'ping'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None
	return "(>^.^)>-O ____|____ ° Q(^.^<) pong!"

def hug(userName, curItem):
	cmd = 'hug'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	if len(curItem[1:].split()) >= 2:
		hugUser = curItem[1:].split()[1]
		return "{} gives a great big hug to {}! <3".format(userName, hugUser)
	else:
		return None	# Wrong # of args

def give(userName, curItem):
	cmd = 'give'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	split = curItem[1:].split()
	if len(split) >= 3:
		user = split[1]	# User recieving dimes
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

				if userName == "pybot" or userName == "ParadigmShift3d":	# If it's me/bot, ignore removal of dimes & # check
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

def dimes(userName, curItem):
	cmd = 'dimes'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		user = split[1]
	else:
		user = userName

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

def hey(userName):
	cmd = 'hey'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None
	return "Saluton Mondo {}!".format(userName)

def raid(userName, curItem):
	cmd = 'raid'
	if userName not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		return "Stream's over everyone!"\
				" Thanks for stopping by, let's go raid @{} at beam.pro/{}!".format(raid, raid)

def twitch(userName, curItem):
	cmd = 'raid'
	if userName not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		return "Stream's over everyone!"\
				" Thanks for stopping by, let's go raid {} at twitch.tv/{}!".format(raid, raid)


def raided(userName, curItem):
	cmd = 'raided'
	if userName not in WHITELIST:	# Check if user is whitelisted/allowed to run command
		return None

	split = curItem[1:].split()
	if len(split) >= 2:
		raid = split[1]
		return "Thank you so much @{} for the raid!"\
				" Everyone go give them some love at beam.pro/{}!".format(raid, raid)

def uptime(userName, initTime):
	cmd = 'uptime'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(userName):
	cmd = 'whoami'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None

	return "Uh...you're {}. Are you all right? :)".format(userName)

def whitelist(userName, curItem):		# Add user to command timeout whitelist

	if userName not in WHITELIST:	# Make sure it's me (in the future, the streamer)

		if len(curItem[1:].split()) >= 2:	# Make sure the # of args is correct
			WHITELIST.append(curItem[1:].split()[2])	# Append the new user to the whitelist!
			pickle.dump(WHITELIST, open('data/whitelist.p', 'wb'))
			response = str("User " + curItem[1:].split()[2] + " added to whitelist!")
			return response
		else:
			return None
	else:			# Not me/streamer, ignored
		return None

def whitelistRM(userName, curItem):		# Add user to command timeout whitelist

	if userName not in WHITELIST:	# Make sure it's me

		if len(curItem[1:].split()) >= 2:	# Make sure the # of args is correct

			print ('curItem:\t',curItem)
			WHITELIST = pickle.load(open('data/whitelist.p', 'rb'))
			if curItem[1:].split()[2] in WHITELIST:		# Make sure user being removed really is removable!
				WHITELIST.remove(curItem[1:].split()[2])	# Append the new user to the whitelist!
				pickle.dump(WHITELIST, open('data/whitelist.p', 'wb'))
				response = str("User " + curItem[1:].split()[2] + " removed from whitelist!")
				return response

			else:
				return "User " + curItem[1:].split()[2] + " not in whitelist!"
		else:
			return None
	else:
		return None

def whitelistLS(userName, curItem):

	if userName not in WHITELIST:
		WHITELIST = pickle.load(open('data/whitelist.p', 'rb'))
		response = 'Whitelisted users: '
		for item in WHITELIST:
			response += item + ", "

		return response[:-2]
