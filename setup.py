#!/usr/bin/env python3

import os
import sqlite3
import json
import pickle
import requests

# This script just sets up the various files/variables that BeamBot needs to run

# Default values, can be changed manually if the user wants
config = {}
config['BEAM_ADDR'] = 'https://beam.pro/api/v1'

# Beam.pro account stuff
config['USERNAME'] = input ("Beam.pro username? ")
config['PASSWORD'] = input ("Beam.pro password? ")

# Do you want to auto-connect to a channel?
autoConnect = input ("Do you want to auto-connect to a channel on bot startup? [Y/n] ")

# If user just hits enter or enters y or Y, then they want to autoconnect
if autoConnect == '' or autoConnect.lower() == 'y':

	while True:		# Loop until we have a working chat ID
		CHANNEL = input ("What channel do you want to connect to? [Channel ID or Name] ")

		if CHANNEL == "":
			print ("You must enter a valid channel ID or name")
			next

		else:
			session = requests.Session()

			chan_ret = session.get(
				'https://beam.pro/api/v1/channels/' + CHANNEL
			)

			CHANNEL = chan_ret.json()['id']

			if type(CHANNEL) == int:
					config['CHANNEL'] = str(chan_ret.json()['id'])
					break # Get out of the loop, the channel ID works

			else:	# Nope, gotta ask for it again...
				print ('Sorry, that channel doesn\'t exist or Beam\'s servers are derping. Please try again!')

# Nope, don't auto-connect
elif autoConnect.lower() == 'n':
	config['CHANNEL'] = None
	config['CONTROL'] = 22085

currency_name = input ("What would you like your currency to be called? ")

while True:		# Loop until we have a numeric # for the command timeout

	cmd_timeout = input ("What would you like the command timeout to be? ")

	try:
		cmd_timeout = int(cmd_timeout)
		if cmd_timeout >= 0:
			config['cmd_timeout'] = cmd_timeout
			break
		else:
			print ("The command timeout MUST be an integer greater than or equal to 0")
	except:		# Not an integer
		print ("Sorry! That's not an integer!")
		print ("The command timeout MUST be an integer greater than or equal to 0")


announce_enter = input ("Do you want entries to be announced? [y/N] ")
if announce_enter == "" or announce_enter.lower() =="n":
	config['announce_enter'] = False

elif announce_enter.lower() == "y":
	config['announce_enter'] = True


announce_leave = input ("Do you want exits to be announced? [y/N] ")
if announce_leave == "" or announce_leave.lower() =="n":
	config['announce_leave'] = False

elif announce_leave.lower() == "y":
	config['announce_leave'] = True


announce_follow = input ("Do you want follows to be announced? [Y/n] ")
if announce_follow == "" or announce_follow.lower() =="n":
	config['announce_follow'] = False

elif announce_follow.lower() == "y":
	config['announce_follow'] = True

config['currency_name'] = currency_name

# Store the config information
with open('data/config.json', 'w') as f:
	json.dump(config, f, sort_keys=True, indent=4, separators=(',', ': '))

# Create the sqlite database
with sqlite3.connect('data/beambot.sqlite') as con:

	cur = con.cursor()

	cur.execute("""
		CREATE TABLE gears
		(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
		 name TEXT UNIQUE,
		 gears INTEGER)"""
	)

	cur.execute("""
		CREATE TABLE quotes
		(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
		 name TEXT,
		 game TEXT,
		 quote TEXT)"""
	)

# Create various pickle files that are required for user bans, command whitelist, and custom commands

bannedUsers = []
pickle.dump(bannedUsers, open('data/bannedUsers.p', 'wb'))

custCommands = []
with open('data/commands.json', 'w') as f:
	json.dump(custCommands, f)

print ("All set! Just run \"python3 beambot.py\" and you're good to go!")
