class MissingKey(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Missing key " + repr(self.value)

    def __repr__(self):
        return "Missing key " + repr(self.value)

class NonNoneError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Non-None Error returned " + repr(self.value)

    def __repr__(self):
        return "Non-None Error returned " + repr(self.value)

class NotAuthenticated(Exception):

    def __str__(self):
        return "Not Authenticated!"

    def __repr__(self):
        return "Not Authenticated!"
