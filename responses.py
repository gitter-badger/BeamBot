import random
import time
from datetime import datetime

def tackle(curItem):
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
	return ":o Why on earth would I want to do that?"

def quote(curItem):
	if len(curItem[1:].split()) >= 2:
		userName = curItem[1:].split()[1]

	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ban(curItem):
	if len(curItem[1:].split()) >= 2:
		banUser = curItem[1:].split()[1]

	else:
		return "Not implemented yet ;(" # Wrong # of args

	return "Not implemented yet ;("

def ping():
	return "(>^.^)>-O ____|____ ° Q(^.^<) pong!"

def hug(hugee, curItem):
	if len(curItem[1:].split()) >= 2:
		hugUser = curItem[1:].split()[1]

	else:
		return		# Wrong # of args

	return "{} gives a great big hug to {}! <3".format(hugee, hugUser)

def give(curItem):
	if len(curItem[0].split()) >= 3:
		reciever = curItem[1:].split()[1]	# User recieving gears
		numSend = curItem[1:].split()[2]	# Number of gears being transferred
		return "Not implemented yet ;("

	else:
		return "Not implemented yet ;("
	
def gears(userName, curItem):
	if len(curItem[0].split()) >= 2:
		pass
		
	return "Not implemented yet ;("

def hey(userName):
	return "Saluton Mondo {} !".format(userName)

def uptime(initTime):
	initTime = initTime.split('.')
	timeHr = int(datetime.now().strftime("%H")) - int(initTime[0])
	timeMin = int(datetime.now().strftime("%M")) - int(initTime[1])
	timeSec = int(datetime.now().strftime("%S")) - int(initTime[2])
	response = "I've been alive for {} hours, {} minutes, and {} seconds!".format(timeHr, timeMin, timeSec)

	return response

def whoami(userName):
	return "Uh...you're {}. Are you all right? :)".format(userName)

def live():
	return "Not implemented yet ;("