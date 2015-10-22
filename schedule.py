import time
from threading import Thread
import responses
import messages
import asyncio
import os
import random
import pickle

scheduled_list = []

def register(text, websocket):

	text = " ".join(text)
	scheduled_list.append(text)

	if os.path.exists('data/scheduled.p'):
		pickle.dump(scheduled_list, open('data/scheduled.p', 'wb'))

	return "Message #" + len(scheduled_list) + "registered! It will be randomly selected to appear every 5 minutes"

@asyncio.coroutine
def timeoutsHandler():
	global websocket

	prev_messages = []
	initial = True

	while True:
		if len(scheduled_list) != 0:
			message = random.randrange(0, len(scheduled_list))
			text = scheduled_list[message]

			if not initial:
				yield from messages.sendMsg(websocket, text)
				print ('Scheduled message:\t', text)
				prev_messages.append(text)

		yield from asyncio.sleep(300)
		initial = False

def registerWebsocket(chat_socket):
	global websocket

	websocket = chat_socket

if os.path.exists('data/scheduled.p'):
	scheduled_list = pickle.load(open('data/scheduled.p', 'rb'))
