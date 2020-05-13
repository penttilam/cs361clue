##
## This is a Class for creating a lobby it will hold palyers before directing them into a game
##

from cLobby import CLobby


class Lobby:
    def __init__(self, host_player, lobbyId):
        self.id = lobbyId                 ## This is the lobby ID stored as a string
        self.players = []                 ## This is the list holding the players in the lobby 
        self.players.append(host_player)  ## This adds the host directly into the lobby
        self.numberPlayers = 1            ## The lobby starts with the a player in it.. the host
        host_player.sendClient("lobby.created:" + str(self.id)) ## Sends a message to the client
        host_player.setLobby(self)        ## Sets the players current lobby

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
            player.setLobby(self)
            player.sendClient("lobby.join:" + str(self.id) + ".success")
     
    ##this removes a player from the lobby
    def removePlayer(self, player, lobbyList):
        self.players.remove(player)
        self.numberPlayers -= 1
        player.setLobby(0)
        if self.numberPlayers == 0:
            print("  Server  --  " + str(self.id) + ".empty")
            print("  Server  --  " + str(self.id) + ".removed")
            lobbyList.remove(self)
        player.sendClient("lobby.remove:" + str(self.id) + "." + str(player.getId()))

    ##this this returns a list of the player names
    def getPName(self):
        names = []
        for x in self.players:
            names.append(x.getId())
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

    def getCLobby(self):
        cPlayerList = []
        for players in self.players:
            cPlayerList.append(players.getCPlayer())
        clobby = self.id
        clobby = cLobby(self.id, self.numberPlayers ,cPlayerList)
        return clobby





