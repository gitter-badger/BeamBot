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

	return "Message #" + str(len(scheduled_list) - 1) + " registered! It will be randomly selected to appear every 5 minutes"

def msg_rm(schedule_id, websocket):

	if schedule_id <= len(scheduled_list):
		rm_cmd = scheduled_list[schedule_id]

		del scheduled_list[schedule_id]

		if os.path.exists('data/scheduled.p'):
			pickle.dump(scheduled_list, open('data/scheduled.p', 'wb'))

		return "Message #" + str(schedule_id) + ": " + rm_cmd + " removed! It will no longer be sent"
	else:
		return "There is no registered message by that ID!"

def edit_msg(text, schedule_id, websocket):

	if schedule_id <= len(scheduled_list):	# Check if it actually exists
		scheduled_list[schedule_id] = text

		if os.path.exists('data/scheduled.p'):
			pickle.dump(scheduled_list, open('data/scheduled.p', 'wb'))

		return "Message #" + str(schedule_id) + " updated!"
	else:
		return "There is no registered message by that ID!"

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
