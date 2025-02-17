## Project Cluwu
## File clientLobby.py
## client side lobby contain client side player information
##

from clientPlayer import ClientPlayer

class ClientLobby:
    def __init__(self, lobbyName, playerNumber, playerNames, lobbyReady, start):
        self.id = lobbyName
        self.numberOfPlayers = playerNumber
        self.playerNameList = playerNames
        self.lobbyReadyStatus = lobbyReady
        self.startGame = start
        self.lobbyHost = False
        
    def getId(self):
        return self.id
    
    def getNumberOfPlayers(self):
        return self.numberOfPlayers
   
    def getPlayerNameList(self):
        return self.playerNameList
    
    def getLobbyReadyStatus(self):
        return self.lobbyReadyStatus

    def getStartGame(self):
        return self.startGame

    def getLobbyHost(self):
        return self.lobbyHost

    def setLobbyHost(self, hostIn):
        self.lobbyHost = hostIn

    def htmlStringify(self):
        playerCount = 0
        htmlString = "<b>Lobby name: " + self.id + "<br></b>" 
        for player in self.playerNameList:
            playerCount += 1
            htmlString += "Player "+ str(playerCount) + " - " 
            if player.getReady():
                htmlString +="Ready<br>"
            else:
                htmlString +="Not Ready<br>"
        return htmlString

