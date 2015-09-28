import asyncio
import websockets
import json

global msg_id

msg_id = 0
msg_id_control = 1

"""Used to send messages. Provide websocket to send via, message, & boolean main to tell which msg ID to use"""
@asyncio.coroutine
def sendMsg(websocket, content, is_auth=False, main=True):
    global msg_id

    if is_auth:
        channel = content[0]
        user_id = content[1]
        authkey = content[2]

        if main:    # For the main chat
            msg_id_send = msg_id
            msg_id += 1
        else:       # For the control chat
            msg_id_send = msg_id_control
            msg_id_control += 1

        packet = {
            "type":"method",
            "method":"auth",
            "arguments":[channel, user_id, authkey],
            "id":msg_id_send
        }

    else:
        if main:    # For the main chat
            msg_id_send = msg_id
            msg_id += 1
        else:       # For the control chat
            msg_id_send = msg_id_control
            msg_id_control += 1

        packet = {
            "type":"method",
            "method":"msg",
            "arguments":[content],
            "id":msg_id_send
        }

    yield from websocket.send(json.dumps(packet))
    ret = yield from websocket.recv()

    msg_id += 1

    return ret

@asyncio.coroutine
def close(websocket):
    yield from websocket.close()
    return None
