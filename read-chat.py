import requests
import config
import json
import time

addr = config.BEAM_ADDR

session = requests.Session()

get_msg = session.get(
	addr + '/api/v1/chats/' + str(config.CHANNEL_PARA) + '/message'
)

for msg in get_msg.json():
	
	user_id = msg['user_id']
	user_name = msg['user_name']

	for item in msg['message']:
		
		iterable = iter(item.keys())
		text = False

		for i in iterable:
			
			if i == "data":
				curItem = str(item[i])
				if item[i] == '':	# Empty data, indicating a link
					next
				if curItem[0] == '!':	# It's a command! Pay attention!
					if curItem[1:] == "hey":		# Hello command
						print ("Saluton Mondo", user_name + "!")
					elif curItem[1:] == "ping":	# Ping Pong Command
						print ("Pong!")
					elif curItem[1:] == "urmom":	# No U!
						print ("No U!")
					elif curItem[1:] == "gears":	# User balance, need to get user ID for
						print ("Not implemented yet")
			elif i == "type":				# The type of message, either link or text
				if item[i] == 'text':	# It's text, check for commands
					text = True
				if item[i] == 'link':	# It's a link
					pass
