import time
import threading
from messages import sendMsg

def register(timeout, cmd):

    if len(cmd) == 1:        # It's just a single command
        t = threading.Timer(timeout, lambda x: sendMsg(websocket, ))

    cmd = " ".join(cmd)

    return "Command " + cmd + " registered. It will run every " + timeout + " seconds"
