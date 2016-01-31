import json
import os

class UserJoin:
    def __init__(self, username, roles, user_id):
        self.username = username
        self.roles = roles
        self.user_id = user_id

class UserLeave:
    def __init__(self, username, roles, user_id):
        self.username = username
        self.roles = roles
        self.user_id = user_id

class Message:
    def __init__(self, username, roles, user_id, message):
        self.username = username
        self.roles = roles
        self.user_id = user_id
        self.message = message
