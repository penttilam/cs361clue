##
## This is a Class for creating a lobby it will hold palyers before directing them into a game
##
from serverPlayer import *


class ServerLobby:
    def __init__(self, host_player, lobbyId):
        self.id = lobbyId                 ## This is the lobby ID stored as a string
        self.players = []                 ## This is the list holding the players in the lobby 
        self.players.append(host_player)  ## This adds the host directly into the lobby
        self.numberPlayers = 1            ## The lobby starts with the a player in it.. the host
        host_player.sendClientAString("lobby.created:" + str(self.id)) ## Sends a message to the client
        self.startGame = False

    ##this returns the a list of the players
    def getPlayers(self):
        return self.players

    ##this adds a player into the lobby
    def addPlayer(self, player):
        if self.numberPlayers == 6:
            player.sendClient("lobby.join:" + str(self.id) + ".error.full" )
        else:
            self.players.append(player)
            self.numberPlayers += 1
            player.sendClientAString("lobby.join:" + str(self.id) + ".success")
     
    ##this removes a player from the lobby
    def removePlayer(self, player):
        self.players.remove(player)
        self.numberPlayers -= 1
        player.sendClientAString("lobby.remove:" + str(self.id))

    ##this this returns a list of the player names
    def getPName(self):
        print("Am i in the PNAME?")
        names = []
        for x in self.players:
            names.append(x.getConnectionId())
        return names

    ##this returns the number of players
    def getPNumber(self):
        return self.numberPlayers

    ##this returns the lobby id
    def getId(self):
        return self.id

    ##this returns a bool based on all members ready
    def getLobbyReady(self):
        for x in self.players:
            if not x.getReady():
                return False
        return True

    def getStartGame(self):
        return self.startGame

    def setStartGame(self):
        self.startGame = True




