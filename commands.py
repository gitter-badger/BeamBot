"""
This module has two functions.
prepCMD prepares the raw websockets data for getResp to return the appropriate response.
This makes it even easier for modding, since you can simply pass the command from the
new code instead of having to figure out how to create the correct packet.
"""

from datetime import datetime
import os
import pickle
import json

# PyBot modules
import responses
import control
import usage

initTime = datetime.now().strftime('%H.%M.%S')

if os.path.exists('data/config.json'):
	config = json.load(open('data/config.json', 'r'))
else:
	print ('\033[1;31mConfig file (data/config.json) missing!\033[0m\n')
	print ('Please run setup before launching the bot.')
	print ('To do so run:\tpython3 setup.py')
	quit()

if os.path.exists('data/bannedUsers{}.p'.format(config['CHANNEL'])):
	bannedUsers = pickle.load(open('data/bannedUsers{}.p'.format(config['CHANNEL']), 'rb'))
else:
	bannedUsers = []
	pickle.dump(bannedUsers, open('data/bannedUsers{}.p'.format(config['CHANNEL']), 'wb'))

def prepCMD(msg, msg_local_id, websocket):

	global is_owner

	user_id = msg['user_id']
	user_name = msg['user_name']
	msg_id = msg['id']
	user_roles = msg['user_roles']

	msg = msg['message']

	is_mod = False
	is_owner = False

	if 'Owner' in user_roles:
		is_mod = True
		is_owner = True
	elif 'Mod' in user_roles:
		is_mod = True

	response = None					# Have to declare variable as None to avoid UnboundLocalError
	goodbye  = False 				# Have to declare variable as False to avoid UnboundLocalError

	if user_name in bannedUsers:		# Is the user chatbanned?
		session = requests.session()

		login_r = session.post(
			addr + '/api/v1/users/login',
			data=_get_auth_body()
		)

		if login_r.status_code != requests.codes.ok:
			print (login_r.text)
			print ("Not Authenticated!")
			quit()

		del_r = session.delete(addr + '/api/v1/chats/' + str(channel) + '/message/' + msg_id)	# Delete the message

		if del_r.status_code != requests.codes.ok:
			print ('Response:\t\t',del_r.json())
			quit()

		session.close()

	cur_item = ''

	"""
	This loop goes through the message. If there is a link in the message, then it will show up every second
	part of the message.

	When there *is* a link, it won't have any text for the current part of the message, so use the "data" key
	of the current part of the message.
	"""

	for i in range(0, len(msg['message'])):
		msg_cur = msg['message'][i]

		if i % 2:		# Every 2 messages
			cur_item += msg_cur['text']
		else:
			if 'data' in msg_cur:
				cur_item += msg_cur['data']

			elif 'me' in msg_cur:
				cur_item += msg_cur['text']

	for item in msg['message']:	# Iterate through the message

		if len(cur_item) >= 1:	# Just make sure it's an actual message

			if cur_item[0] == '!':	# It's a command! Pay attention!

				response, goodbye = getResp(cur_item, user_name, user_id, msg_local_id, is_mod, is_owner, websocket)

	return response, goodbye

def getResp(cur_item, user_name=None, user_id=None, msg_local_id=None, is_mod=False, is_owner=False, websocket=None):

	goodbye = False

	# ----------------------------------------------------------
	# Commands
	# ----------------------------------------------------------
	cmd = cur_item[1:].split()

	if cmd[0][0:5] == "blame":	# Blame a user
		response = responses.blame(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "commands":		# Get list of commands
		response = responses.cmdList(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "hey":				# Say hey
		response = responses.hey(user_name, is_mod, is_owner)

	elif cmd[0] == "ping":				# Ping Pong Command
		response = responses.ping(user_name, is_mod, is_owner)

	elif cmd[0] == config["currency_name"] or cmd[0] == "currency":			# Get user balance
		currency_ret, user = responses.dimes(user_name, cur_item, is_mod, is_owner)

		if currency_ret != False:
			response = "@" + user + " has " + currency_ret + " " + config['currency_name'] + "!"
		else:
			response = "@" + user + " has no " + config['currency_name'] + "! :o"

	elif cmd[0] == "give":	# Give dimes to a user
		response = responses.give(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "ban":	# Ban a user from chatting
		response, banUser = responses.ban(user_name, cur_item, is_mod, is_owner)
		if banUser != "":
			bannedUsers.append(banUser)

		print ("bannedUsers",bannedUsers)

		pickle.dump(bannedUsers, open('data/bannedUsers{}.p'.format(config['CHANNEL']), "wb"))

	elif cmd[0] == "unban":	# Unban a user
		response, uBanUser = responses.unban(user_name, cur_item, is_mod, is_owner)
		if uBanUser != "":
			bannedUsers.remove(uBanUser)

		print ("bannedUsers",bannedUsers)

		pickle.dump(bannedUsers, open('data/bannedUsers{}.p'.format(config['CHANNEL']), "wb"))

	elif cmd[0] == "quote":	# Get random quote from DB
		response = responses.quote(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "tackle":# Tackle a user!
		response = responses.tackle(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "slap":	# Slap someone
		response = responses.slap(user_name, is_mod, is_owner)

	elif cmd[0] == "set":	# Bot configuration - Uses cmd instead of cur_item
		response = responses.set(user_name, user_id, cmd, is_mod, is_owner)

	elif cmd[0] == "schedule":	# Run commands at set intervals
		response = responses.schedule(user_name, cmd, is_mod, is_owner, websocket)

	elif cmd[0] == "uptime":# Bot uptime
		response = responses.uptime(user_name, initTime, is_mod, is_owner)

	elif cmd[0] == "hug":	# Give hugs!
		response = responses.hug(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "raid":	# Go raid peoples
		response = responses.raid(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "raided":	# You done got raided son!
		response = responses.raided(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "twitch":	# Go raid peoples on Twitch.tv!
		response = responses.twitch(user_name, cur_item, is_mod, is_owner)

	elif cmd[0] == "whoami":	# Who am I? I'M A GOAT. DUH.
		response = responses.whoami(user_name, is_mod, is_owner)

	elif cmd[0] == "command":	# Add command for any users
		if len(cmd) <= 3:	# It's not long enough to have a response
			return usage.prepCmd(user_name, "command", is_mod, is_owner), False

		if cmd[1] == "add":
			response = responses.command(user_name, cur_item, is_mod, is_owner)
		elif cmd[1] == "remove":
			response = responses.commandRM(user_name, cur_item, is_mod, is_owner)
		elif cmd[1] == "update":
			response = responses.editCommand(user_name, cur_item, is_mod, is_owner)
		else:					# Not add or remove, return usage
			response = usage.prepCmd(user_name, "command", is_mod, is_owner)

	elif cmd[0] == "command+":	# Add mod-only command
		if len(cmd) <= 3:	# It's not long enough to have a response
			return usage.prepCmd(user_name, "command", is_mod, is_owner), False
			
		if cmd[1] == "add":
			response = responses.commandMod(user_name, cur_item, is_mod, is_owner)
		elif cmd[1] == "remove":
			response = responses.commandRM(user_name, cur_item, is_mod, is_owner)
		else:					# Not add or remove, return usage
			response = usage.prepCmd(user_name, "command+", is_mod, is_owner)

	elif cmd[0] == "goodbye":	# Turn off the bot correctly

		return control.goodbye(user_name, is_owner, msg_local_id)

	else:					# Unknown or custom command
		response = responses.custom(user_name, cur_item, is_mod, is_owner)

	print ('command:\t',cmd,'\n',
		'response:\t',response,'\n')	# Console logging

	return response, False 		# Return the response to calling statement
