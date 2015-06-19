import random
import time
from datetime import datetime
import sqlite3
import config
import pickle
import requests
import os
from bs4 import BeautifulSoup

# Full list of commands
"""
!tackle - Tackle a user
!slap   - Slap a user
!quote  - Post a quote
!ping   - Ping Pong!
!hug    - Hug a user
!give   - Give gears to a user
!gears  - Get # of gears for user
!hey    - Basically say hi to the Bot
!uptime - How long the bot has been running
!whoami - Who are you - class whoami command
!command   - Create new command for anyone to use
!command+  - Create mod-only command
!command-  - Remove command
!ban    - Ban a user from chatting
!whitelist - Whitelist a user to remove command restrictions
!goodbye - Turn off the bot
"""

global prevTime
prevTime = {'tackle':{}, 'slap':{}, 'quote':{}, 'ping':{}, 'hug':{}, 'give':{}, 'gears':{}, 'hey':{}, 'uptime':{}, 'whoami':{}} 

if os.path.exists('data/whitelist.p'):
	WHITELIST = pickle.load(open('data/whitelist.p', 'rb'))
else:
	WHITELIST = []

# End of do responses-specific modules
# ------------------------------------------------------------------------

def _checkTime(cmd, user):
	curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

	if cmd == "tackle":			# Tackle command
		
		if user in prevTime['tackle'] and (curTime - prevTime['tackle'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['tackle'] and (curTime - prevTime['tackle'][user]) >= 30:	# Under 30 seconds
			prevTime['tackle'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['tackle'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "slap":			# Slap command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['slap'] and (curTime - prevTime['slap'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['slap'] and (curTime - prevTime['slap'][user]) >= 30:	# Under 30 seconds
			prevTime['slap'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['slap'][user] = curTime
			return False		# Allow it to be run		# Allow it to be run

	elif cmd == "quote":		# Quote command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))
		
		if user in prevTime['quote'] and (curTime - prevTime['quote'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['quote'] and (curTime - prevTime['quote'][user]) >= 30:	# Under 30 seconds
			prevTime['quote'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['quote'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "ping":			# Ping pong command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['ping'] and (curTime - prevTime['ping'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['ping'] and (curTime - prevTime['ping'][user]) >= 30:	# Under 30 seconds
			prevTime['ping'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['ping'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "hug":			# Hug command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['hug'] and (curTime - prevTime['hug'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['hug'] and (curTime - prevTime['hug'][user]) >= 30:	# Under 30 seconds
			prevTime['hug'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['hug'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "give":			# Give gears command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['give'] and (curTime - prevTime['give'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['give'] and (curTime - prevTime['give'][user]) >= 30:	# Under 30 seconds
			prevTime['give'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['give'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "gears":		# Check # of gears command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['gears'] and (curTime - prevTime['gears'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['gears'] and (curTime - prevTime['gears'][user]) >= 30:	# Under 30 seconds
			prevTime['gears'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['gears'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "hey":			# Hey command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['hey'] and (curTime - prevTime['hey'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['hey'] and (curTime - prevTime['hey'][user]) >= 30:	# Under 30 seconds
			prevTime['hey'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['hey'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "uptime":		# Bot uptime command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['uptime'] and (curTime - prevTime['uptime'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['uptime'] and (curTime - prevTime['uptime'][user]) >= 30:	# Under 30 seconds
			prevTime['uptime'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['uptime'][user] = curTime
			return False		# Allow it to be run

	elif cmd == "whoami":		# Whoami command
		curTime =  (int(datetime.now().strftime("%M")) * 60) + int(datetime.now().strftime("%S"))

		if user in prevTime['whoami'] and (curTime - prevTime['whoami'][user]) <= 31:	# Only every 30 seconds per user 
			return True			# Too soon
		elif user in prevTime['whoami'] and (curTime - prevTime['whoami'][user]) >= 30:	# Under 30 seconds
			prevTime['whoami'][user] = curTime
			return False		# Allow it to be run
		else:
			prevTime['whoami'][user] = curTime
			return False		# Allow it to be run

# ------------------------------------------------------------------------
# End of do responses-specific modules
# ------------------------------------------------------------------------

def custom(userName, curItem):	# Check unknown command, might be custom one
	return "Custom - Not implemented yet ;("

def commandMod(userName, curItem):		# Command available to mods only
	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		if len(curItem[1:].split()) >= 3:
			cmd = curItem[1]
			response = curItem[2]

		return "Not implemented yet ;("

	else:
		return None						# Not whitelisted

def command(userName, curItem):			# Command available to anyone
	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		if len(curItem[1:].split()) >= 3:
			cmd = curItem[1]
			response = curItem[2]

		return "Not implemented yet ;("

	else:
		return None						# Not whitelisted

def commandRM(userName, curItem):			# Remove a command
	if userName in WHITELIST:	# Make sure the user is a mod or streamer or otherwise whitelisted
		if len(curItem[1:].split()) >= 2:
			cmdRemove = curItem[1]
			return "Not implemented yet ;("

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

	if len(curItem[1:].split()) >= 2:	# Make sure we have username to ban
		banUser = curItem[1:].split()[1]
		return "Not implemented yet - Planned for 2.0 ;("

	else:
		return "Not implemented yet - Planned for 2.0 ;(" # Wrong # of args

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
		user = split[1]	# User recieving gears
		try:	# Try to convert argument to int type
			numSend = int(split[2])	# Number of gears being transferred
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
				userGearsOrig = results[0][0]

				if userName == "ParadigmShift3d":	# If it's me, ignore removal of gears & # check
					userGears = int(userGearsOrig) + int(numSend)

					command = '''UPDATE gears 
								SET gears={}
								WHERE name="{}"'''.format(userGears, user)

					cur.execute(command)

					return "@" + user + " now has " + str(userGears) + " gears!"					

				if numSend <= userGearsOrig:	# Make sure the sending user has enough gears

					userGears = int(userGearsOrig) + int(numSend)

					command = '''UPDATE gears 
								SET gears={}
								WHERE name="{}"'''.format(userGears, user)

					cur.execute(command)

					return "@" + user + " now has " + str(userGears) + " gears!"

				else:
					return None

			else:		# User not in gears database
				command = '''INSERT INTO gears
							(name, gears)
							VALUES ("{}", {})'''.format(user, str(numSend))

				cur.execute(command)	# Soooo... add 'em!

				return "@" + user + " now has " + str(numSend) + " gears!"

	else:
		return None
	
def gears(userName, curItem):
	cmd = 'gears'
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
			return "@" + user + " has " + str(results[0][0]) + " gears."
		else:
			return "@" + user + " has no gears! :o"

def hey(userName):
	cmd = 'hey'
	if _checkTime(cmd, userName) and userName not in WHITELIST:		# if _checkTime() returns True then the command is on timeout, return nothing
		return None
	return "Saluton Mondo {}!".format(userName)

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
	
	if userName == "ParadigmShift3d":	# Make sure it's me (in the future, the streamer)

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

	if userName == "ParadigmShift3d":	# Make sure it's me

		if len(curItem[1:].split()) >= 2:	# Make sure the # of args is correct

			print (curItem)
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

	if userName == "ParadigmShift3d":
		WHITELIST = pickle.load(open('data/whitelist.p', 'rb'))
		response = 'Whitelisted users: '
		for item in WHITELIST:
			response += item + ", "
		
		return response[:-2]