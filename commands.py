"""
This module has two functions.
prepCMD prepares the raw websockets data for getResp to return the appropriate response.
This makes it even easier for modding, since you can simply pass the command from the
new code instead of having to figure out how to create the correct packet.
"""

from datetime import datetime
import responses
import callbacks

initTime = datetime.now().strftime('%H.%M.%S')

def prepCMD(msg, bannedUsers, msgLocalID, msgs_acted):

	userID = msg['user_id']
	userName = msg['user_name']
	msgID = msg['id']

	response = None					# Have to declare variable as None to avoid UnboundLocalError
	goodbye  = False 				# Have to declare variable as False to avoid UnboundLocalError

	if userName in bannedUsers:		# Is the user chatbanned?
		session = requests.session()

		login_r = session.post(
			addr + '/api/v1/users/login',
			data=_get_auth_body()
		)

		if login_r.status_code != requests.codes.ok:
			print (login_r.text)
			print ("Not Authenticated!")
			quit()

		del_r = session.delete(addr + '/api/v1/chats/' + str(channel) + '/message/' + msgID)	# Delete the message

		if del_r.status_code != requests.codes.ok:
			print ('Response:\t\t',del_r.json())
			quit()

		session.close()

	curItem = ''

	"""
	This loop goes through the message. If there is a link in the message, then it will show up every second
	part of the message.

	When there *is* a link, it won't have any text for the current part of the message, so use the "data" key
	of the current part of the message.
	"""

	for i in range(0, len(msg['message'])):
		if i % 2:		# Every 2 messages
			curItem += msg['message'][i]['text']
		else:
			curItem += msg['message'][i]['data']

	for item in msg['message']:	# Iterate through the message

		if len(curItem) >= 1:	# Just make sure it's an actual message

			if curItem[0] == '!' and msgID not in msgs_acted:	# It's a command! Pay attention!

				response, goodbye = getResp(curItem, userName, msgLocalID)

	return response, goodbye

def getResp(curItem, userName=None, msgLocalID=None):

	# ----------------------------------------------------------
	# Commands
	# ----------------------------------------------------------
	cmd = curItem[1:].split()

	if cmd[0] == "throw":			# Throw a ball at another user
		timer = callbacks.Timer(2)

		print (timer.callback())

		response = "Blargh"

	elif cmd[0][0:5] == "blame":	# Blame a user
		response = responses.blame(userName, curItem)

	elif cmd[0] == "commands":		# Get list of commands
		response = responses.cmdList(userName, curItem)

	elif cmd[0] == "hey":				# Say hey
		response = responses.hey(userName)

	elif cmd[0] == "ping":				# Ping Pong Command
		response = responses.ping(userName)

	elif cmd[0] == "dimes" or cmd[0] == "currency":			# Get user balance
		response = responses.dimes(userName, curItem)

	elif cmd[0] == "give":	# Give dimes to a user
		response = responses.give(userName, curItem)

	elif cmd[0] == "ban":	# Ban a user from chatting
		response, banUser = responses.ban(userName, curItem)
		bannedUsers.append(banUser)

		pickle.dump(bannedUsers, open('data/bannedUsers.p', "wb"))

	elif cmd[0] == "unban":	# Unban a user
		response, uBanUser = responses.unban(userName, curItem)
		bannedUsers.remove(uBanUser)

		pickle.dump(bannedUsers, open('data/bannedUsers.p', "wb"))

	elif cmd[0] == "quote":	# Get random quote from DB
		response = responses.quote(userName, curItem)

	elif cmd[0] == "tackle":# Tackle a user!
		response = responses.tackle(userName, curItem)

	elif cmd[0] == "slap":	# Slap someone
		response = responses.slap(userName)

	elif cmd[0] == "uptime":# Bot uptime
		response = responses.uptime(userName, initTime)

	elif cmd[0] == "hug":	# Give hugs!
		response = responses.hug(userName, curItem)

	elif cmd[0] == "raid":	# Go raid peoples
		response = responses.raid(userName, curItem)

	elif cmd[0] == "raided":	# You done got raided son!
		response = responses.raided(userName, curItem)

	elif cmd[0] == "twitch":	# Go raid peoples on Twitch.tv!
		response = responses.twitch(userName, curItem)

	elif cmd[0] == "whoami":	# Who am I? I'M A GOAT. DUH.
		response = responses.whoami(userName)

	elif cmd[0] == "command":	# Add command for any users
		response = responses.command(userName, curItem)

	elif cmd[0] == "command+":	# Add mod-only command
		response = responses.commandMod(userName, curItem)

	elif cmd[0] == "command-":	# Remove a command
		response = responses.commandRM(userName, curItem)

	elif cmd[0] == "whitelist":	# Whitelist a user
		if len(cmd) >= 3:	# True means it has something like `add` or `remove`
			if cmd[1] == 'add':
				response = responses.whitelist(userName, curItem)
			elif cmd[1] == 'remove':
				response = responses.whitelistRM(userName, curItem)
			else: 	# Not add or remove
				response = None
		else:		# Just get the whitelist
			response = responses.whitelistLS(userName, curItem)

	elif cmd[0] == "goodbye":	# Turn off the bot correctly

		packet = {
			"type":"method",
			"method":"msg",
			"arguments":['See you later my dear sir, wot wot!'],
			"id":msgLocalID
		}

		return packet, True	# Return the Goodbye message packet &

	else:					# Unknown or custom command
		response = responses.custom(userName, curItem)

	print ('command:\t',cmd,'\n',
		'response:\t',response,'\n')	# Console logging

	return response, False 		# Return the response to calling statement
