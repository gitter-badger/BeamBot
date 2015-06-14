import random
import time
from datetime import datetime
import sqlite3

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
!live   - Tell the bot the stream is live
"""

global prevTime
prevTime = {'tackle':{}, 'slap':{}, 'quote':{}, 'ping':{}, 'hug':{}, 'give':{}, 'gears':{}, 'hey':{}, 'uptime':{}, 'whoami':{}} 

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
			prevTime['give'][user] = curTimegive
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
	if len(curItem[1:].split()) >= 3:
		cmd = curItem[1]
		response = curItem[2]

		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def command(userName, curItem):			# Command available to anyone
	if len(curItem[1:].split()) >= 3:
		cmd = curItem[1]
		response = curItem[2]

		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def commandRM(userName, curItem):			# Remove a command
	if len(curItem[1:].split()) >= 2:
		cmdRemove = curItem[1]
		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def tackle(userName, curItem):
	cmd = 'tackle'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
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
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return ":o Why on earth would I want to do that?"

def quote(userName, curItem):
	cmd = 'quote'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return

	if len(curItem[1:].split()) >= 2:
		userName = curItem[1:].split()[1]
	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ban(userName, curItem):

	if len(curItem[1:].split()) >= 2:
		banUser = curItem[1:].split()[1]
		return "Not implemented yet ;("

	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ping(userName):
	cmd = 'ping'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "(>^.^)>-O ____|____ ° Q(^.^<) pong!"

def hug(userName, curItem):
	cmd = 'hug'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return

	if len(curItem[1:].split()) >= 2:
		hugUser = curItem[1:].split()[1]
		return "{} gives a great big hug to {}! <3".format(userName, hugUser)
	else:
		return		# Wrong # of args
	
def give(userName, curItem):
	cmd = 'give'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return

	if len(curItem[0].split()) >= 3:
		reciever = curItem[1:].split()[1]	# User recieving gears
		numSend = curItem[1:].split()[2]	# Number of gears being transferred
		return "Not implemented yet ;("
	else:
		return "Not implemented yet ;("
	
def gears(userName, curItem):
	cmd = 'gears'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[0].split()) >= 2:
		pass
		
	return "Not implemented yet ;("

def hey(userName):
	cmd = 'hey'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "Saluton Mondo {}!".format(userName)

def uptime(userName, initTime):
	cmd = 'uptime'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(userName):
	cmd = 'whoami'
	if _checkTime(cmd, userName):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "Uh...you're {}. Are you all right? :)".format(userName)

def live(userName):
	return "Not implemented yet ;("