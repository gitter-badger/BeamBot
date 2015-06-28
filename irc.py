#!/usr/bin/env python3

import sys
import socket
import string
import time
import config

readbuffer="" 			# We need this to hold messages in a buffer, so we can make sure we can read them all

# Commands
SETNICK = ("NICK {}\r\n".format(config.NICK)).encode()
LOGIN = ("USER {} {} {} :{}\r\n".format(config.IDENT, config.HOST, config.REALNAME, config.IRC_PASSWORD)).encode()
JOINCHAN = ("JOIN {}\r\n".format(config.IRC_CHANNEL)).encode()

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 					# Creates a new socket
s.connect((config.HOST, config.PORT)) 			# Connect to the host IRC network through port 6667
s.send(SETNICK)				# Send the NICK command to set our nickname
s.send(LOGIN)				# Send the USER command to log in
s.send((("PRIVMSG {} /msg NickServ identify olander99\r\n").format(config.IRC_CHANNEL)).encode())	# Identify with NickServ
s.send(JOINCHAN)			# Join the #BeamProCommand IRC_CHANNEL
s.send((("PRIVMSG {} {}\r\n").format(config.IRC_CHANNEL, "Hai. Ima bot.")).encode())	# Send the online notification message
data = s.recv(1024)

while 1: # Loop forever because 1 == always True (keeps us connected to IRC)
	# Make buffer to hold strings - Unfortunately have to use ISO-8859-1
	readbuffer = readbuffer + s.recv(1024).decode('ISO-8859-1')
	temp = readbuffer.split("\n") 	# Parses strings into a readable form
	readbuffer = temp.pop() 					# Removes and returns last item in list

	for line in temp: 						# This loop allows the buffer to be read line-by-line until no more is left
		line = line.rstrip()
		line = line.split()

		print ('line:',line)

		if len(line) >= 4	:
			print ('line[1]:',line[1])
			if line[3][2:] == "PING": 				# If someone pings us, we will pong back
				# Take the first item in the line and split it on the !, then take the first element of THAT list
				# and take the characters after the first character. This is our PINGer
				pinger = line[0].split('!')[0][1:]
				PONG = (("PONG {}\r\n").format(pinger).encode())
				s.send(PONG)
			elif line[1] == "PRIVMSG":				# It's a command
				cmd = line[3][1:].lower()
				print ('Command:\t', cmd)

				# Have to accomodate for the result that checkCMD is expecting
				#cmd = 