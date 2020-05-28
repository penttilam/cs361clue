import socket
import sys
import logging
import pickle
import _thread
from _thread import *

from datetime import datetime

from serverConnection import * 
from createClientObjects import *

from serverPlayer import *
from serverLobby import *
from clientLobby import *
from serverCard import * 
from serverGame import * 
from serverThread import * 



##sys.stdout = open("/dev/null", "w")

##Creating the server socket and listening for a connection

# server = "45.132.241.193"
server = "localhost"
port = 42069

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print("Server waiting for a connection :D")


class ServerInfo():
    def __init__(self, lobbList, gameList):
        self.serverLobbyList = lobbyList
        self.serverGameList = gameList

    def getGameList(self):
        return self.serverGameList

    def getLobbyList(self):
        return self.serverLobbyList

##This functions creates a new lobby and adds the current Player
def newCommand(newLobbyName, serverThreadInfo, serverInfo):
    try:
        newLobbyName = ServerLobby(serverThreadInfo.getServerPlayer(), newLobbyName)
    except:
        error_string = str(datetime.now()) + " -- error -- ServerLobby __init__ Failed " 
        logging.debug(error_string)
    try:
        serverInfo.getLobbyList().append(newLobbyName)
        print("lobby list: " + str(serverInfo.getLobbyList()))
    except:
        error_string = str(datetime.now()) + " -- error -- serverInfo.getLobbyList Failed " 
        logging.debug(error_string)
    try:
        serverThreadInfo.setServerLobby(newLobbyName)
        print("lobby: " + str(serverThreadInfo.getServerLobby()))
        print("lobbyName: " + str(serverThreadInfo.getServerLobby().getId()))
    except:
        error_string = str(datetime.now()) + " -- error -- serverThreadInfo.getServerLobby Failed " 
        logging.debug(error_string)
    try:
        sendUpdatedLobby(serverThreadInfo.getServerLobby())
    except:
        error_string = str(datetime.now()) + " -- error -- sendUpdatedLobby Failed " 
        logging.debug(error_string)



##This function adds a user to a given lobby
def joinCommand(lobbyName, serverThreadInfo, serverInfo):
    for serverLobby in serverInfo.getLobbyList():
        if serverLobby.getId() == lobbyName:
            if serverLobby.addPlayer(serverThreadInfo.getServerPlayer()):
                serverThreadInfo.setServerLobby(serverLobby)
                sendUpdatedLobby(serverThreadInfo.getServerLobby())
            else:
                listCommand(serverThreadInfo, serverInfo)
            break


##This function lists available lobbies
def listCommand(serverThreadInfo, serverInfo):
    clientLobbyList = []
    for serverLobby in serverInfo.getLobbyList():
        clientLobbyList.append(createClientLobby(serverLobby))
    print(clientLobbyList)
    player.sendClientAObject(clientLobbyList)


##this function revomes a player from their lobby
def leaveCommand(serverThreadInfo, serverInfo):
    try:
        removeLobby = serverThreadInfo.getServerLobby()
        removeLobby.removePlayer(player)
        serverThreadInfo.setServerLobby(None)
    except:
        pass
    else:
        serverThreadInfo.getServerPlayer().sendClientAString("lobby.leave:confimed")
        if removeLobby.getPNumber() == 0:
            serverInfo.getLobbyList().remove(removeLobby)
    finally:
        sendUpdatedLobby(removeLobby)


##this function initializes the game
def startCommand(serverThreadInfo, serverInfo):
    print("here 1")
    serverThreadInfo.getServerLobby().setStartGame()
    print("here 2")
    print(serverThreadInfo.getServerLobby())
    print(serverThreadInfo.getServerLobby().getPlayers())
    serverGame = ServerGame(serverThreadInfo.getServerLobby().getPlayers())
    print("here 2.5")
    serverInfo.getGameList().append(serverGame)
    serverThreadInfo.setServerGame(serverGame)
    print("here 3")
    sendUpdatedLobby(serverThreadInfo.getServerLobby())
    print("here 4")


##this function sets the player to ready
def readyCommand(serverThreadInfo):
    print("at the start")
    if serverThreadInfo.getServerPlayer().getReady() == False:
        serverThreadInfo.getServerPlayer().setReady(True)
    elif serverThreadInfo.getServerPlayer().getReady() == True:
        serverThreadInfo.getServerPlayer().setReady(False)
    print("in the middle")
    sendUpdatedLobby(serverThreadInfo.getServerLobby())
    print("after update")


def sendUpdatedLobby(serverLobbyIn):
    print("here1")
    clientLobby = createClientLobby(serverLobbyIn)
    print("here2")
    LobbyPlayers = serverLobbyIn.getPlayers()
    print("here3")
    for player in LobbyPlayers:
        print("here4")
        print(LobbyPlayers)
        if player is LobbyPlayers[0]:
            print("here5")
            clientLobby.setLobbyHost(True)
        else:
            print("here6")
            clientLobby.setLobbyHost(False)
        print("here7")
        player.sendClientAObject(clientLobby)


##This is the subset of lobby actions
def lobbyCommand(block1, block2, serverThreadInfo, serverInfo):
    arguments = block1.split(".")

    if arguments[1] == "new":
        try:
            newCommand(block2, serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.new(" + str(block2) + ", " + str(serverThreadInfo) + ", " + str(serverInfo) +",  Failed " 
            logging.debug(error_string)
    elif arguments[1] == "lobbies":
        try:
            listCommand(serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.lobbies Failed " 
            logging.debug(error_string)
    elif arguments[1] == "join":
        try:
            joinCommand(block2, serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.join Failed " 
            logging.debug(error_string)
    elif arguments[1] == "leave":
        try:
            leaveCommand(serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.ready Failed " 
            logging.debug(error_string)
    elif arguments[1] == "ready":
        try:
            readyCommand(serverThreadInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.start Failed " 
            logging.debug(error_string)
    elif arguments[1] == "start":
        try:
            startCommand(serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- lobby.start Failed " 
            logging.debug(error_string)


def createCommand(serverThreadInfo, serverInfo):
    if serverThreadInfo.getServerGame() == None:
        print("Not the host!")
        for games in serverInfo.getGameList():
            print("Which Game?")
            for players in games.getPlayerTurnOrder():
                print("Which Player?")
                if players is serverThreadInfo.getServerPlayer():
                    print("Found My Game!")
                    serverThreadInfo.setServerGame(games)
                    print("Saved My GAME!")
    print("here1")
    serverThreadInfo.getServerPlayer().sendClientAObject(createClientGame(serverThreadInfo))
    print("here12")
    removeLobby = serverThreadInfo.getServerLobby()
    print("here123")
    removeLobby.removePlayer(serverThreadInfo.getServerPlayer())
    print("here1234")
    serverThreadInfo.setServerLobby(None)
    print("here12345")
    if removeLobby.getPNumber() == 0:
        serverInfo.getLobbyList().remove(removeLobby)
    print("here-6")

def moveTokenCommand(serverThreadInfo, block2):
    arguments = block2.split(".")
    serverThreadInfo.getServerPlayer().getMyToken().setTokenXLocYLoc(arguments[0], arguments[1])
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        player.sendClientAObject(createClientGame(serverThreadInfo))


def turnCommand(serverThreadInfo):
    try:
        serverThreadInfo.getServerGame().changeTurn(serverThreadInfo.getServerPlayer())
        for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
            player.sendClientAObject(createClientGame(serverThreadInfo))
    except:
        error_string = str(datetime.now()) + " -- error -- game.turn -- " + str(serverThreadInfo.getServerPlayer())
        logging.debug(error_string)


def chatCommand(serverThreadInfo, argumentInput):
    htmlString = "<b>" + str(serverThreadInfo.getServerPlayer().getMyToken().getTokenCharacter()) + "</b> " + str(argumentInput) + "<br>"
    serverGame.setGameChat(htmlString)
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        player.sendClientAObject(createClientGame(serverThreadInfo))


def gameCommand(block1, block2, serverThreadInfo, serverInfo):
    arguments = block1.split(".")

    if arguments[1] == "create":
        try:
            createCommand(serverThreadInfo, serverInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- game.create Failed " 
            logging.debug(error_string)
    elif arguments[1] == "move":
        try:
            moveTokenCommand(serverThreadInfo, block2)
        except:
            error_string = str(datetime.now()) + " -- error -- game.move Failed " 
            logging.debug(error_string)
    elif arguments[1] == "turn":
        try:
            turnCommand(serverThreadInfo)
        except:
            error_string = str(datetime.now()) + " -- error -- game.turn Failed " 
            logging.debug(error_string)
    elif arguments[1] == "chat":
        try:
            chatCommand(serverThreadInfo, arguments[2])
        except:
            error_string = str(datetime.now()) + " -- error -- game.chat Failed " 
            logging.debug(error_string)



##This is the command interperter from the client
def clientCommand(clientCommand, serverThreadInfo, serverInfo):
    blocks = clientCommand.split(":")
    arguments = blocks[1].split(".")

    if arguments[0] == "lobby":
        if len(blocks) == 3:
            lobbyCommand(blocks[1], blocks[2], serverThreadInfo, serverInfo)
            return True
        else:
            lobbyCommand(blocks[1], None, serverThreadInfo, serverInfo)
            return True

    elif arguments[0] == "game":
        if len(blocks) == 3:
            gameCommand(blocks[1], blocks[2], serverThreadInfo, serverInfo)
            return True
        else:
            gameCommand(blocks[1], None, serverThreadInfo, serverInfo)
            return True

    elif arguments[0] == "quit":
        return False



##This the individual client thread that sends and recieves data from the client
def Threaded_Client(serverThreadInfo, serverInfo):
    runThread = True

    while runThread:
        try:
            data = serverThreadInfo.getServerPlayer().getClientMessage()

            if not data:
                break
            else:
                print("Received  --  " + data)
                runThread = clientCommand(data, serverThreadInfo, serverInfo)

        except:
            error_string = str(datetime.now()) + " -- error -- " + str(data)
            logging.debug(error_string)
            break

    try:
        if not serverThreadInfo.getServerLobby() == None:
            removeLobby = serverThreadInfo.getServerLobby()
            removeLobby.removePlayer(serverThreadInfo.getServerPlayer())
            serverThreadInfo.setServerLobby(None)
            print("Removed from Lobby")
            if removeLobby.getPNumber() == 0:
                serverInfo.getLobbyList().remove(removeLobby)
                print("Lobby Removed")
    except:
        pass
        
    print("Lost connection to " + serverThreadInfo.getServerPlayer().getConnectionId())
    serverThreadInfo.getServerPlayer().closeConnection()
##
## this is the server listening for connections initizliaing them as players and passing them to threads
##
connectionNumber = 1
lobbyList = []
gameList = []
serverInfo =  ServerInfo(lobbyList, gameList)
logging.basicConfig(filename='Epic_Server_Fails', level=logging.DEBUG)

while True:

    connectionId = "connection" + str(connectionNumber)
    conn, addr = s.accept()
    print(str(addr) + " is connection" + str(connectionNumber))

    ## Using ServerPlayer class as middle man to Connection class to insolate it from the program
    connectionId = Connection(connectionId, conn)
    player = ServerPlayer(connectionId)
    serverThreadInfo = ServerThread(player)

    start_new_thread(Threaded_Client, (serverThreadInfo, serverInfo))
    
    connectionNumber += 1