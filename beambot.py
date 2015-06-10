import requests
import config
import json
import asyncio
import websockets

global authkey, endpoint, channel

@asyncio.coroutine
def connect():
	websocket = yield from websockets.connect(endpoint)
	
	packet = {
		"type":"method",
		"method":"auth",
		"arguments":[channel, user_id, authkey],
		"id":0
	}
	
	yield from websocket.send(json.dumps(packet))
	ret = yield from websocket.recv()
	ret = json.loads(ret)
	print (ret)
	
	if ret["error"] != None:
		print ("EEEK!")
		quit()

	# If the message doesn't send initially, send it again. The bot just needs to wake up chat
	msg_send = input("Please enter your message: ")

	packet = {
		"type":"method",
		"method":"msg",
		"arguments":[str(msg_send)],
		"id":2
	}

	yield from websocket.send(json.dumps(packet))
	ret_msg = yield from websocket.recv()
	ret_msg = json.loads(ret_msg)

	print (ret_msg)

# ----------------------------------------------------------------------
# Main Code
# ----------------------------------------------------------------------

def _get_auth_body():
	return {
		'username': config.USERNAME,
		'password': config.PASSWORD
	}
	
addr = config.BEAM_ADDR

session = requests.Session()

login_r = session.post(
	addr + '/api/v1/users/login',
	data=_get_auth_body()
)

if login_r.status_code != requests.codes.ok:
	print ("Not Authenticated!")
	quit()

print (login_r.json())

user_id = login_r.json()['id']

channel = input("Channel? ")

if channel == 'p':		# Paradigm, me
	channel = config.CHANNEL_PARA
elif channel == 'du':	# Duke
	channel = config.CHANNEL_DUKE
elif channel == 'de':	# Deci
	channel = config.CHANNEL_DECI

chat_r = session.get(
	addr + '/api/v1/chats/%s' % channel
)
if chat_r.status_code != requests.codes.ok:
	print ('Unknown error!')
	quit()

chat_details = chat_r.json()

endpoint = chat_details['endpoints'][0]

authkey = chat_details['authkey']

print ('authkey:\t',authkey)
print ('endpoint:\t',endpoint)

asyncio.get_event_loop().run_until_complete(connect())