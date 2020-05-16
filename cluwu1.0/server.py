import socket
import sys
import pickle
import _thread
from _thread import *


from serverConnection import * 
from createClientObjects import *

######

from serverPlayer import ServerPlayer
from serverLobby import *



from clientLobby import *
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
    print("fucking here bro")
    print("newLobbyName: " + newLobbyName)
    print("player: " + str(player))
    print("lobbyList: " + str(lobbyList))
    newLobbyName = ServerLobby(player, newLobbyName)
    print("No its fucking here bro")
    lobbyList.append(newLobbyName)
    print("Wait wait wait Its fucking here bro")


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
def leaveCommand(player, lobbyList):
    for lobby in lobbyList:
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                playerLobby = lobby

    playerLobby.removePlayer(player)
    if playerLobby.getPNumber() == 0:
        lobbyList.remove(playerLobby)
        print("FUCKING GUCKING DUCKS2")
    print("after the If")


##this function initializes the game
def startCommand(player, lobbyList):
    lobby = player.getLobby()
    nameList = []
    nameList = lobby.getPlayers()
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
    player.sendClientAString("lobby.update:confirmed")
    for lobby in lobbyList:
        print("fuck your lobbies!")
        for lobbyPlayer in lobby.getPlayers():
            print("no fuck the players!")
            if lobbyPlayer == player:
                print("this is right before clobby")
                clientLobby = createClientLobby(lobby)
                print("this is a clobby: " + str(clientLobby))
                player.sendClientAObject(clientLobby)
                return


def hostCommand(player, lobbyList):
    print("did i make it here?")
    hostFlag = False
    print("this is the fucking LobbyList: " + str(lobbyList))
    for lobby in lobbyList:
        print("Im in the lobbyList")
        playerList = lobby.getPlayers()
        if playerList[0] == player:
             print("is anything ever true?")
             hostFlag = True
         
    print("nothing is real!")
    player.sendClientAString("lobby.host:" + str(hostFlag))



##This is the subset of lobby actions
def lobbyCommand(block1, block2, player, lobbyList, gameList):
    print("player print 4: " + str(player))
    arguements = block1.split(".")

    if arguements[1] == "new":
        newCommand(block2, player, lobbyList)
    elif arguements[1] == "lobbies":
        listCommand(player, lobbyList)
    elif arguements[1] == "join":
        joinCommand(block2, player, lobbyList)
    elif arguements[1] == "leave":
        print("before teh command?")
        leaveCommand(player, lobbyList)
        print("after teh command?")
    elif arguements[1] == "ready":
        readyCommand(player)
    elif arguements[1] == "start":
        startCommand(player, lobbyList, gameList)
    elif arguements[1] == "update":
        updateCommand(player, lobbyList)
    elif arguements[1] == "host":
        hostCommand(player, lobbyList)

    print("Before I go to Bed")

##This is the command interperter from the client
def clientCommand(clientCommand, player, lobbyList, gameList):
    print("player print 3: " + str(player))
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

    return True



##This the individual client thread that sends and recieves data from the client
def Threaded_Client(player, lobbyList, gameList):
    runThread = True

    print("player print 2: " + str(player))
    while runThread:
        try:
            data = player.getClientMessage()

            if not data:
                break
            else:
                print("Received  --  " + data)
                runThread = clientCommand(data, player, lobbyList, gameList)

        except:
            print("this is the except: " + str(data))
            break
    
    leaveCommand(player, lobbyList)
    print("its running the wrong leave?")
    print("Lost connection to " + player.getConnectionId())


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
    player = ServerPlayer(connectionId)
    print("player print 1: " + str(player))

    start_new_thread(Threaded_Client, (player, lobbyList, gameList))
    
    connectionNumber += 1

