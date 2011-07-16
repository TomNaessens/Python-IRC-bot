import utils

class PrivMSG:
    def __init__(self, data):
        self.full, self.info, self.text, self.user, self.channel, self.char, self.cmd = utils.parse(data)
