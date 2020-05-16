##
## This class is the Player in the Server. It represents their connection and their information
##

import pickle
import pygame
import sys
from cPlayer import CPlayer

class Player():
    def __init__(self, playerId, conn):
        self.id = playerId     ## this is the player ID stored as a string
        self.ready = False     ## this is the players status in the lobby
        self.lobbyId = 0       ## this is the players current lobby id
        self.myCards = []
        self.char = " "
        self.turn = 0

        ##remove these
        self.conn = conn       ## this is the player's conn object
        self.conn.send(pickle.dumps(str(self.id) + ":connected"))

    ##this returns the players id
    def getId(self):
        return self.id

    ##this returns the players conn
    def getConn(self):
        return self.conn

    ##this sets the players ready status in the lobby
    def setReady(self, ready):
        self.ready = ready

    ##this returns the ready status 
    def getReady(self):
        return self.ready

    ##this returns a bool value of were a player is currently in a lobby
    def getInLobby(self):
        if self.lobbyId == 0:
            return False
        return True

    ##this returns current lobby idea
    def getLobby(self):
        return self.lobbyId

    def getTurn(self):
        return self.turn

    def setTurn(self, turn):
        self.turn = turn 

    def addCard(self, newCard):
        self.myCards.append(newCard) 

    def getDeck(self): 
        return self.myCards

    def setChar(self, char):
        self.char = char

    def getChar(self):
        return self.char

    ##this sets the current lobby idea
    def setLobby(self, lobbyId):
        self.lobbyId = lobbyId

    ##not sure we need this
    def clicked_create_lobby(self):
        self.event_click_create_lobby = True
   
    ##remove player from lobby
    def leaveLobby(self, lobbyList):
        if not self.lobbyId == 0:
            lobby = self.lobbyId
            lobby.removePlayer(self, lobbyList)


    def getCPlayer(self):
        cplayer = self.id
        cplayer = CPlayer(self.id, self.ready, self.char)
        return cplayer
        


