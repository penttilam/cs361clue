from player import Player
from cPlayer import CPlayer

class CLobby:
    def __init__(self, lobbyId, pNumber, lPlayers, lReady):
        self.id = lobbyId
        self.pNumber = pNumber
        self.pList = lPlayers
        self.lReady = lReady
        
    def getId(self):
        return self.id
    
    def getPNumber(self):
        return self.pNumber
   
    def getPList(self):
        return self.pList
    
    def getLReady(self):
        return self.lReady

    def htmlStringify(self):
        htmlString = "<b>Lobby name: " + self.id + "<br></b>" 
        for player in self.pList:
                htmlString += player.getId() + " - " 
                if player.getReady():
                    htmlString +="Ready<br>"
                else:
                    htmlString +="Ready up little bitch<br>"
        return htmlString
