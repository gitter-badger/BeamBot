import time
from threading import Thread
import responses
import messages
import asyncio
import os
import pickle

timeouts = []

class Timeout:
	def __init__(self, timeout, text):
		self.timeout = timeout
		self.text = text

	def __str__(self):
		return str(self.timeout) + ':' + self.text

def register(timeout, text, websocket):

	text = " ".join(text)

	try:
		timeout = int(timeout)

	except ValueError as e:
		print (e)
		return "Error: The timout must be an integer greater than 1"

	if timeout > 0:
		scheduled = Timeout(timeout, text)
		timeouts.append(scheduled)

		if os.path.exists('data/scheduled.p'):
			pickle.dump(timeouts, open('data/scheduled.p', 'wb'))

	return text + " registered. It will run every " + str(timeout) + " seconds"

@asyncio.coroutine
def timeoutsHandler():
	global websocket

	initial = True	# Set to True initially to keep messages from being sent on startup
	seconds = 0

	while True:
		for i in timeouts:
			if seconds % i.timeout == 0 and not initial:
				# print ('i:\t\t',i)
				# print (seconds % i.timeout)
				yield from messages.sendMsg(websocket, i.text)

		yield from asyncio.sleep(1)
		seconds += 1
		initial = False	# Not initial run

def registerWebsocket(chat_socket):
	global websocket

	websocket = chat_socket

if os.path.exists('data/scheduled.p'):
	timeouts = pickle.load(open('data/scheduled.p', 'rb'))
