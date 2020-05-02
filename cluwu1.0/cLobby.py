from player import Player

class CLobby:
    def __init__(self, lobbyId, pNumber, lPlayers):
        self.id=lobbyId
        self.pNumber=pNumber
        self.pList=lPlayers
        
    def getId(self):
        return self.id
    
    def getPNumber(self):
        return self.pNumber
    