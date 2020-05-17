## Project Cluwu
## File clientLobby.py
## client side lobby contain client side player information

from clientPlayer import ClientPlayer

class ClientLobby:
    def __init__(self, lobbyName, playerNumber, playerNames, lobbyReady):
        self.id = lobbyName
        self.numberOfPlayers = playerNumber
        self.playerNameList = playerNames
        self.lobbyReadyStatus = lobbyReady
        
    def getId(self):
        return self.id
    
    def getNumberOfPlayers(self):
        return self.numberOfPlayers
   
    def getPlayerNameList(self):
        return self.playerNameList
    
    def getLobbyReadyStatus(self):
        return self.lobbyReadyStatus

    def htmlStringify(self):
        playerCount = 0
        htmlString = "<b>Lobby name: " + self.id + "<br></b>" 
        for player in self.playerNameList:
            playerCount += 1
            htmlString += "Player "+ playerCount + " - " 
            if player.getReady():
                htmlString +="Ready<br>"
            else:
                htmlString +="Ready up little bitch<br>"
        return htmlString

