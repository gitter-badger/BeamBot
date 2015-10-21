import time
from threading import Thread
import responses
import messages
import asyncio
import os
import random
import pickle

messages = []

def register(text, websocket):

	text = " ".join(text)
	messages.append(text)

	if os.path.exists('data/scheduled.p'):
		pickle.dump(messages, open('data/scheduled.p', 'wb'))

	return text + " registered! It will be randomly selected to appear every 5 minutes"

@asyncio.coroutine
def timeoutsHandler():
	global websocket

	prev_message = ""

	while True:
		while True:
			if len(messages) == 0:
				break

			message = random.randrange(len(messages))
			text = messages[message]

			if text != prev_message:
				yield from messages.sendMsg(websocket, text)
				prev_message = text
				break


		yield from asyncio.sleep(300)

def registerWebsocket(chat_socket):
	global websocket

	websocket = chat_socket

if os.path.exists('data/scheduled.p'):
	messages = pickle.load(open('data/scheduled.p', 'rb'))
