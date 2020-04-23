import socket
import sys

class Lobby:
    def __init__(self):
        self.players = []
        self.numberPlayers = 0

    def addPlayer(self, player):
        if self.numberPlayers == len(self.players)

        self.players.append(player)
        self.numberPlayers += 1
       
    def removePlayer(self, player):
        for
        
        self.numberPlayers -= 1
        
    def readyPlayer(self, player):
        player.Player.Ready

    def returnPNumber(self):
        return len(self.players)


