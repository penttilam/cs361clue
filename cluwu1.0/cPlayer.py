class CPlayer:
    def __init__(self, playerId, ready, character):
        self.id = playerId
        self.ready = ready
        self.char = character

    def getId(self):
        return self.id

    def getReady(self):
        return self.ready
    
    def getChar(self):
        return self.char

