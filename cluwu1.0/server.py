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

server = "45.132.241.193"
# server = "localhost"
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
        newLobbyName = ServerLobby(serverThreadInfo.getServerPlayer(), newLobbyName)
        serverInfo.getLobbyList().append(newLobbyName)
        serverThreadInfo.setServerLobby(newLobbyName)
        sendUpdatedLobby(serverThreadInfo.getServerLobby())


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
    serverThreadInfo.getServerPlayer().sendClientAObject(clientLobbyList)


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
        #FIX ME MIKE I BROKED
        sendUpdatedLobby(removeLobby)


##this function initializes the game
def startCommand(serverThreadInfo, serverInfo):
    serverThreadInfo.getServerLobby().setStartGame()
    serverGame = ServerGame(serverThreadInfo.getServerLobby().getPlayers())
    serverInfo.getGameList().append(serverGame)
    serverThreadInfo.setServerGame(serverGame)
    sendUpdatedLobby(serverThreadInfo.getServerLobby())


##this function sets the player to ready
def readyCommand(serverThreadInfo):
    if serverThreadInfo.getServerPlayer().getReady() == False:
        serverThreadInfo.getServerPlayer().setReady(True)
    elif serverThreadInfo.getServerPlayer().getReady() == True:
        serverThreadInfo.getServerPlayer().setReady(False)
    sendUpdatedLobby(serverThreadInfo.getServerLobby())


def sendUpdatedLobby(serverLobbyIn):
    clientLobby = createClientLobby(serverLobbyIn)
    LobbyPlayers = serverLobbyIn.getPlayers()
    for player in LobbyPlayers:
        if player is LobbyPlayers[0]:
            clientLobby.setLobbyHost(True)
        else:
            clientLobby.setLobbyHost(False)
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
        for games in serverInfo.getGameList():
            for players in games.getPlayerTurnOrder():
                if players is serverThreadInfo.getServerPlayer():
                    serverThreadInfo.setServerGame(games)
    serverThreadInfo.getServerPlayer().sendClientAObject(createClientGame(serverThreadInfo))
    removeLobby = serverThreadInfo.getServerLobby()
    removeLobby.removePlayer(serverThreadInfo.getServerPlayer())
    serverThreadInfo.setServerLobby(None)
    if removeLobby.getPNumber() == 0:
        serverInfo.getLobbyList().remove(removeLobby)

def moveTokenCommand(serverThreadInfo, block2):
    arguments = block2.split(".")
    serverThreadInfo.getServerPlayer().getMyToken().setTokenXLocYLoc(arguments[0], arguments[1])
    serverThreadInfo.getServerPlayer().getMyToken().setTokenRoom(arguments[2])
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        if not player is serverThreadInfo.getServerPlayer():
            player.sendClientAObject(createClientGame(serverThreadInfo))


def turnCommand(serverThreadInfo):
    try:
        serverThreadInfo.getServerGame().changeTurn(serverThreadInfo.getServerPlayer())
        updateGame(serverThreadInfo)

    except:
        error_string = str(datetime.now()) + " -- error -- game.turn -- " + str(serverThreadInfo.getServerPlayer())
        logging.debug(error_string)


def chatCommand(serverThreadInfo, argumentInput):
    htmlString = "<b>" + str(serverThreadInfo.getServerPlayer().getMyToken().getTokenCharacter()) + "</b> " + str(argumentInput) + "<br>"
    serverThreadInfo.getServerGame().setGameChat(htmlString)
    updateGame(serverThreadInfo)

def updateGame(serverThreadInfo):
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        player.sendClientAObject(createClientGame(serverThreadInfo))


def accuseCommand(serverThreadInfo, block2):
    accused = block2.split(".")
    for x in range(3):
        if accused[x] != serverThreadInfo.getServerGame().getGuiltyCards()[x].getCardName():
            serverThreadInfo.getServerPlayer().setWonLostGame(False)
            break
    
    if serverThreadInfo.getServerPlayer().getWonLostGame() == None:
        serverThreadInfo.getServerPlayer().setWonLostGame(True)
        for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
            if not player == serverThreadInfo.getServerPlayer():
                player.setWonLostGame(False)
    updateGame(serverThreadInfo)

def suggestCommand(serverThreadInfo, block2):
    suggestion = block2.split(".")
    suggestCards = []
    for weapon in serverThreadInfo.getServerGame().getServerWeapons():
        if weapon.getName() == suggestion[2]:
            weapon.setLocation(suggestion[1])
    token_changed = False 
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        if suggestion[0] == player.getMyToken().getTokenCharacter():
            player.getMyToken().setTokenRoom(suggestion[1])
            break
    suggestedToken = ClientToken(suggestion[0], None, None, suggestion[1])
    suggestedPlayer = ClientPlayer(None, suggestedToken, None, None, None)
    suggestedTokenList = []
    suggestedTokenList.append(suggestedPlayer)
    firstPlayerFound = False
    for player in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        if not player == serverThreadInfo.getServerPlayer():
            for i in range(3):
                for j in range(len(player.getMyCards())):
                    if suggestion[i] == player.getMyCards()[j].getCardName():
                        firstPlayerFound = True
                        suggestCards.append(player.getMyCards()[j])
        if firstPlayerFound:
            serverThreadInfo.getServerGame().setSuggestCards(suggestCards)
            clientPackage = createClientGame(serverThreadInfo)
            clientPackage.setSuggestionMove(suggestedTokenList)
            player.sendClientAObject(clientPackage)
            serverThreadInfo.getServerGame().setSuggestCards(None)
            clientPackage = createClientGame(serverThreadInfo)
            clientPackage.setSuggestionMove(suggestedTokenList)
            for otherPlayer in serverThreadInfo.getServerGame().getPlayerTurnOrder():
                if player != otherPlayer:
                    otherPlayer.sendClientAObject(clientPackage)
            break

def refuteCommand(serverThreadInfo, block2):
    refute = block2
    cards = serverThreadInfo.getServerPlayer().getMyCards()
    for card in cards:
        if card.getCardName() == refute:
            serverThreadInfo.getServerGame().setRefuteCard(card)
            break
    player = serverThreadInfo.getServerGame().getPlayerTurnOrder()[0]
    player.sendClientAObject(createClientGame(serverThreadInfo))
    serverThreadInfo.getServerGame().setRefuteCard(None)

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
            chatCommand(serverThreadInfo, block2)
        except:
            error_string = str(datetime.now()) + " -- error -- game.chat Failed " 
            logging.debug(error_string)
    elif arguments[1] == "accuse":
        try:
            accuseCommand(serverThreadInfo, block2)
        except:
            error_string = str(datetime.now()) + " -- error -- game.accuse Failed " 
            logging.debug(error_string)
    elif arguments[1] == "suggest":
        try:
            suggestCommand(serverThreadInfo, block2)
        except:
            error_string = str(datetime.now()) + " -- error -- game.suggest Failed " 
            logging.debug(error_string)
    elif arguments[1] == "refute":
        try:
            refuteCommand(serverThreadInfo, block2)
        except:
            error_string = str(datetime.now()) + " -- error -- game.refute Failed " 
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
        if not serverThreadInfo.getServerGame() == None:
            serverThreadInfo.getServerGame().setDiscardedCards(serverThreadInfo.getServerPlayer())
            removeGame = serverThreadInfo.getServerGame()
            removeGame.removePlayer(serverThreadInfo.getServerPlayer())
            updateGame(serverThreadInfo)
            serverThreadInfo.setServerGame(None)
            if len(removeGame.getPlayerTurnOrder()) == 0:
                serverInfo.getGameList().remove(removeGame)
    except:
        pass


    try:
        if not serverThreadInfo.getServerLobby() == None:
            removeLobby = serverThreadInfo.getServerLobby()
            removeLobby.removePlayer(serverThreadInfo.getServerPlayer())
            serverThreadInfo.setServerLobby(None)
            if removeLobby.getPNumber() == 0:
                serverInfo.getLobbyList().remove(removeLobby)
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
