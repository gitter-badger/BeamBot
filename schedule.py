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

	return text + " registered! It will be randomly selected to appear every 5 minutes"

@asyncio.coroutine
def timeoutsHandler():
	global websocket

	prev_message = ""
	initial = True

	while True:
		if len(scheduled_list) != 0:
			message = random.randrange(len(scheduled_list))
			text = scheduled_list[message]

			if text != prev_message and not initial:
				yield from messages.sendMsg(websocket, text)
				prev_message = text
				break


		yield from asyncio.sleep(3)
		initial = False

def registerWebsocket(chat_socket):
	global websocket

	websocket = chat_socket

if os.path.exists('data/scheduled.p'):
	scheduled_list = pickle.load(open('data/scheduled.p', 'rb'))
