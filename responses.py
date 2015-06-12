import random
import time
from datetime import datetime
import sqlite3

def _checkTime(cmd, user=None):
	time = (datetime.now().strftime("%M") * 60) + (datetime.now().strftime("%S"))

	if cmd == "cmd":			# Add command command
		

	if cmd == "cmdMod":			# Add mod command command
		

	if cmd == "cmdRM":			# Remove command command
		

	if cmd == "tackle":			# Tackle command
		

	if cmd == "slap":			# Slap command
		

	if cmd == "quote":			# Quote command
		

	if cmd == "ban":			# Ban command
		

	if cmd == "ping":			# Ping pong command
		

	if cmd == "hug":			# Hug command
		

	if cmd == "give":			# Give gears command
		

	if cmd == "gears":			# Check # of gears command
		

	if cmd == "hey":			# Hey command
		

	if cmd == "uptime":			# Bot uptime command
		

	if cmd == "whoami":			# Whoami command
		

	if cmd == "live":			# Tell bot stream is live command
		

def custom(userName, curItem):	# Check unknown command, might be custom one
	return "Not implemented yet ;("

def commandMod(userName, curItem):		# Command available to mods only
	cmd = 'cmdMod'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[1:].split()) >= 3:
		cmd = curItem[1]
		response = curItem[2]

		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def command(userName, curItem):			# Command available to anyone
	cmd = 'cmd'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[1:].split()) >= 3:
		cmd = curItem[1]
		response = curItem[2]

		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def commandRM(userName, curItem):			# Remove a command
	cmd = 'cmdRM'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[1:].split()) >= 2:
		cmdRemove = curItem[1]
		return "Not implemented yet ;("

	return "Not implemented yet ;("	# Incorrect # Args - won't return anything

def tackle(curItem):
	cmd = 'tackle'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
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

def slap():
	cmd = 'slap'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return ":o Why on earth would I want to do that?"

def quote(curItem):
	cmd = 'quote'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[1:].split()) >= 2:
		userName = curItem[1:].split()[1]

	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ban(curItem):
	cmd = 'ban'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return

	if len(curItem[1:].split()) >= 2:
		banUser = curItem[1:].split()[1]
		return "Not implemented yet ;("

	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ping():
	cmd = 'ping'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "(>^.^)>-O ____|____ ° Q(^.^<) pong!"

def hug(hugee, curItem):
	cmd = 'hug'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[1:].split()) >= 2:
		hugUser = curItem[1:].split()[1]

	else:
		return		# Wrong # of args

	return "{} gives a great big hug to {}! <3".format(hugee, hugUser)

def give(curItem):
	cmd = 'give'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[0].split()) >= 3:
		reciever = curItem[1:].split()[1]	# User recieving gears
		numSend = curItem[1:].split()[2]	# Number of gears being transferred
		return "Not implemented yet ;("

	else:
		return "Not implemented yet ;("
	
def gears(userName, curItem):
	cmd = 'gears'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	if len(curItem[0].split()) >= 2:
		pass
		
	return "Not implemented yet ;("

def hey(userName):
	cmd = ''
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "Saluton Mondo {} !".format(userName)

def uptime(initTime):
	cmd = 'uptime'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(userName):
	cmd = 'whoami'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "Uh...you're {}. Are you all right? :)".format(userName)

def live():
	cmd = 'live'
	if _checkTime(cmd):		# if _checkTime() returns True then the command is on timeout, return nothing
		return
	return "Not implemented yet ;("