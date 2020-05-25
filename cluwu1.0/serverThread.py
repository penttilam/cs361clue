from serverPlayer.py import *
from serverLobby.py import *
from serverGame.py import *

class ServerThread():
    def __init__(self, player):
        self.serverPlayer = player
        self.serverLobby = None
        self.serverGame = None

    def getServerPlayer(self):
        return self.serverPlayer

    def getServerLobby(self):
        return self.serverLobby

    def setServerLobby(self, lobbyIn):
        self.serverLobby = lobbyIn

    def getServerGame(self):
        return self.serverGame

    def setServerGame(self, gameIn):
        self.serverGame = gameIn

