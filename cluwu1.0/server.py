import socket
import sys
import pickle
import _thread
from _thread import *


from serverConnection import Connection

####

from serverPlayer import ServerPlayer
from lobby import Lobby



from cLobby import CLobby
from sCard import * 

##Creating the server socket and listening for a connection
server = "45.132.241.193"
port = 42069

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print("Server waiting for a connection :D")


##This functions creates a new lobby and adds the current Player
def newCommand(newLobbyName, player, lobbyList):
    newLobbyName = Lobby(player, newLobbyName)
    lobbyList.append(newLobbyName)


##This function adds a user to a given lobby
def joinCommand(lobbyName, player, lobbyList):
    joinedLobby = False
    for lobby in lobbyList:
        if lobby.getId() == lobbyName:
            lobby.addPlayer(player)
            joinedLobby = True
    if joinedLobby == False:
        player.sendClientAString("lobby.join:" + lobbyName + ".failed")


##This function lists available lobbies
def listCommand(player, lobbyList):
    player.sendClientAString("lobby.list.confirmed")
    cLobbies = []
    for lobby in lobbyList:
        lobbyId = lobby.getId()
        lobbyId = CLobby(lobby.getId(), lobby.getPNumber(), lobby.getPName(), lobby.getLobbyReady())
        cLobbies.append(lobbyId)
    player.sendClientAObject(cLobbies)


##this function revomes a player from their lobby
def leaveCommand(player):
    for lobby in lobbyList:
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                lobby.removePlayer(player)

                if lobby.getPNumber <= 0:
                    lobbyList.remove(lobby)
                    print("  Server  --  " + str(lobby.getId()) + ".empty.removed")
                return

##this function initializes the game
def startCommand(player, lobbyList):
    lobby = player.getLobby()
    nameList = []
    nameList = lobby.getPlayers()
    ##createDeck(nameList)  
    startInfo = "lobby.start.confirmed"

    player.sendClient(startInfo)


##this function sets the player to ready
def readyCommand(player):
    if player.getReady() == False:
        player.setReady(True)
        player.sendClientAString("lobby.ready:" + str(player.getReady()))
    elif player.getReady() == True:
        player.setReady(False)
        player.sendClientAString("lobby.ready:" + str(player.getReady()))
    else:
        player.sendClientAString("lobby.ready:SeriouslyHowDidYouFuckItUpThisBad?")

##this function updates the current clobby for the client
def updateCommand(player, lobbyList):
    player.sendClient("lobby.update:confirmed")
    for lobby in lobbyList:
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                clientLobby = lobby.getCLobby()
    player.sendClientAObject(clientLobby)



##This is the subset of lobby actions
def lobbyCommand(block1, block2, player, lobbyList, gameList):
    arguements = block1.split(".")

    if arguements[1] == "new":
        newCommand(block2, player, lobbyList)
    elif arguements[1] == "lobbies":
        listCommand(player, lobbyList)
    elif arguements[1] == "join":
        joinCommand(block2, player, lobbyList)
    elif arguements[1] == "leave":
        leaveCommand(player, lobbyList)
    elif arguements[1] == "ready":
        readyCommand(player)
    elif arguements[1] == "start":
        startCommand(player, lobbyList, gameList)
    elif arguements[1] == "update":
        updateCommand(player, lobbyList)

##This is the command interperter from the client
def clientCommand(clientCommand, player, lobbyList, gameList):
    blocks = clientCommand.split(":")
    arguements = blocks[1].split(".")

    if arguements[0] == "lobby":
        if len(blocks) == 3:
            lobbyCommand(blocks[1], blocks[2], player, lobbyList, gameList)
            return True
        else:
            lobbyCommand(blocks[1], None, player, lobbyList, gameList)
            return True
    elif arguements[0] == "game":
        pass

    elif arguements[0] == "quit":
        player.sendClientAString("quit")
        runThread = False



##This the individual client thread that sends and recieves data from the client
def Threaded_Client(player, lobbyList, gameList):
    runThread = True

    while runThread:
        try:
            data = player.getClientMessage()

            if not data:
                break
            else:
                print("Received  --  " + data)
                runThread = clientCommand(data, player, lobbyList, gameList)

        except:
            break

    player.leaveLobby(lobbyList) 
    print("Lost connection to " + clientConnection.getId())
    clientConnection.getConn().close()


##
## this is the server listening for connections initizliaing them as players and passing them to threads
##
connectionNumber = 1
lobbyList = []
gameList = []

while True:

    connectionId = "connection" + str(connectionNumber)
    conn, addr = s.accept()
    print(str(addr) + " is connection" + str(connectionNumber))

    ## Using ServerPlayer class as middle man to Connection class to insolate it from the program
    connectionId = Connection(connectionId, conn)
    player = ServerPlayer(clientConnection)

    start_new_thread(Threaded_Client, (player, lobbyList, gameList))
    
    connectionNumber += 1

