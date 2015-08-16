#!/usr/bin/env python3

import os
import sqlite3
import json
import pickle

# This script just sets up the various files/variables that BeamBot needs to run

# Default values, can be changed manually if the user wants
config = {}
config['BEAM_ADDR'] = 'https://beam.pro'

# Beam.pro account stuff
config['USERNAME'] = input ("Beam.pro username? ")
config['PASSWORD'] = input ("Beam.pro password? ")

# Do you want to auto-connect to a channel?
autoConnect = input ("Do you want to auto-connect to a channel on bot startup? [Y/n] ")

# If user just hits enter or enters y or Y, then they want to autoconnect
if autoConnect == '' or autoConnect.lower() == 'y':
	config['CHANNEL'] = input ("What channel do you want to connect to? [Channel ID] ")

# Nope, don't auto-connect
elif autoConnect.lower() == 'n':
	config['CHANNEL'] = None

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

# Create various pickle files that are required for blacklist, user bans, command whitelist, and custom commands

msgs_acted = []
pickle.dump(msgs_acted, open('data/blacklist.p', 'wb'))

bannedUsers = []
pickle.dump(bannedUsers, open('data/bannedUsers.p', 'wb'))

WHITELIST = ['ParadigmShift3d','pybot']
pickle.dump(WHITELIST, open('data/whitelist.p', 'wb'))

custCommands = []
with open('data/commands.json', 'w') as f:
	f.write(str(custCommands))

commandList = {}
with open('data/commandList.json', 'w') as f:
	f.write(str(commandList))

print ("All set! Just run \"python3 beambot.py\" and you're good to go!")
