import asyncio
import time

class Timer(object):
    """docstring for Timer
    Timer just takes a certain number of seconds to wait, then returns once
    that time has expired.
    Usage: Timer(<NUMOFSECONDS>)"""
    def __init__(self, timeSleep):
        self.timeSleep = timeSleep
        self.loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def sleep(self):
        time.sleep(self.timeSleep)

    def callback(self):
        self.loop.run_until_complete(self.sleep())
