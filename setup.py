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

		if type(CHANNEL) == int:
			config['CHANNEL'] = str(chan_ret.json()['id'])
			break				# If we're this far, then it was a numeric ID

		else:		# Nope, gotta do it manually
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

# Store the config information
with open('data/config.json', 'w') as f:
	f.write(json.dumps(config))

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

WHITELIST = ['pybot']
pickle.dump(WHITELIST, open('data/whitelist.p', 'wb'))

custCommands = []
with open('data/commands.json', 'w') as f:
	f.write(str(custCommands))

commandList = {}
with open('data/commandList.json', 'w') as f:
	f.write(str(commandList))

print ("All set! Just run \"python3 beambot.py\" and you're good to go!")
