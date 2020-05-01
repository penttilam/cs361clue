##
## This class is the Player in the Server. It represents their connection and their information
##

import pickle
import pygame
import sys

class Player():
    def __init__(self, playerId, conn):
        ##basic info
        self.id = playerId     ## this is the player ID stored as a string
        self.conn = conn       ## this is the player's conn object
        ##lobby info
        self.ready = False     ## this is the players status in the lobby
        self.lobbyId = 0       ## this is the players current lobby id
        ##game info

        ##events
        self.event_click_create_lobby = False

        ##send a message on initilization
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

    ##send a message to player client
    def sendClient(self, message):
        self.conn.send(pickle.dumps(str(self.id) + ":" + str(message)))
        print("    Sent  --  " + str(self.id) + ":" + str(message))

