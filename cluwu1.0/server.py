import socket
import sys
import pickle
import _thread
from _thread import *

from serverConnection import * 
from createClientObjects import *

from serverPlayer import *
from serverLobby import *
from clientLobby import *
from serverCard import * 
from serverGame import * 

####
##sys.stdout = open("/dev/null", "w")

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
    newLobbyName = ServerLobby(player, newLobbyName)
    lobbyList.append(newLobbyName)


##This function adds a user to a given lobby
def joinCommand(lobbyName, player, lobbyList):
    joinedLobby = False
    for serverLobby in lobbyList:
        if serverLobby.getId() == lobbyName:
            serverLobby.addPlayer(player)
            joinedLobby = True
    if joinedLobby == False:
        player.sendClientAString("lobby.join:" + lobbyName + ".failed")


##This function lists available lobbies
def listCommand(player, lobbyList):
    player.sendClientAString("lobby.list.confirmed")
    clientLobbyList = []
    for serverLobby in lobbyList:
        clientLobbyList.append(createClientLobby(serverLobby))
    player.sendClientAObject(clientLobbyList)


##this function revomes a player from their lobby
def leaveCommand(player, lobbyList):
    for lobby in lobbyList:
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                playerLobby = lobby
    try:
        playerLobby.removePlayer(player)
        if playerLobby.getPNumber() == 0:
            lobbyList.remove(playerLobby)

    except:
        pass

##this function initializes the game
def startCommand(player, lobbyList, gameList):
    for lobby in lobbyList:
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                playerLobby = lobby
    print("is it here")
    playerLobby.setStartGame()
    startInfo = "lobby.start.confirmed"
    player.sendClientAString(startInfo)
    serverGame(playerLobby.getPlayers())


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
        for lobbyPlayer in lobby.getPlayers():
            if lobbyPlayer == player:
                clientLobby = createClientLobby(lobby)
                player.sendClientAObject(clientLobby)
                return


def hostCommand(player, lobbyList):
    hostFlag = False
    for lobby in lobbyList:
        playerList = lobby.getPlayers()
        if playerList[0] == player:
             hostFlag = True
    player.sendClientAString("lobby.host:" + str(hostFlag))



##This is the subset of lobby actions
def lobbyCommand(block1, block2, player, lobbyList, gameList):
    arguments = block1.split(".")

    if arguments[1] == "new":
        newCommand(block2, player, lobbyList)
    elif arguments[1] == "lobbies":
        listCommand(player, lobbyList)
    elif arguments[1] == "join":
        joinCommand(block2, player, lobbyList)
    elif arguments[1] == "leave":
        leaveCommand(player, lobbyList)
    elif arguments[1] == "ready":
        readyCommand(player)
    elif arguments[1] == "start":
        startCommand(player, lobbyList, gameList)
    elif arguments[1] == "update":
        updateCommand(player, lobbyList)
    elif arguments[1] == "host":
        hostCommand(player, lobbyList)


def createCommand(player, lobbyList, gameList):
#    create a clientGame object
#    we need remove player from lobby
#   player.sendAObject(clienGameobject of some kind) 
    pass

def gameCommand(block1, block2, player, lobbyList, gameList):
    arguments = block1.split(".")

    if arguments[1] == "create":
        createCommand(player, lobbyList, gameList)



##This is the command interperter from the client
def clientCommand(clientCommand, player, lobbyList, gameList):
    blocks = clientCommand.split(":")
    arguments = blocks[1].split(".")

    if arguments[0] == "lobby":
        if len(blocks) == 3:
            print("before?")
            lobbyCommand(blocks[1], blocks[2], player, lobbyList, gameList)
            return True
        else:
            print("before?")
            lobbyCommand(blocks[1], None, player, lobbyList, gameList)
            return True
    elif arguments[0] == "game":
        pass

    elif arguments[0] == "quit":
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

    start_new_thread(Threaded_Client, (player, lobbyList, gameList))
    
    connectionNumber += 1


