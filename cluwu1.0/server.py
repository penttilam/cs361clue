import socket
import sys
import pickle
from _thread import *


from player import Player
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
        player.sendClient("lobby.join:" + lobbyName + ".failed")


##This function lists available lobbies
def listCommand(player, lobbyList):
    player.sendClient("lobby.list.confirmed")
    cLobbies = []
    for lobby in lobbyList:
        lobbyId = lobby.getId()
        lobbyId = CLobby(lobby.getId(), lobby.getPNumber(), lobby.getPName())
        cLobbies.append(lobbyId)
    player.sendClientLobby(cLobbies)


##This function lists all the players in the lobby
def playerCommand(player, lobbyList):
    lobby = player.getLobby()
    namelist = []
    namelist = lobby.getPName()
    lobbyInfo = "lobby.players:"
    for playerName in namelist:
        lobbyInfo += playerName
        lobbyInfo += "."
    player.sendClient(lobbyInfo)


##this function revomes a player from their lobby
def leaveCommand(player, lobbyList):
    player.leaveLobby(lobbyList) 


##this function initializes the game
def startCommand(player, lobbyList):
    lobby = player.getLobby()
    nameList = []
    nameList = lobby.getPlayers()
    createDeck(nameList)  
    startInfo = "lobby.start:"
    startInfo += player.getChar()
    player.sendClient(startInfo)


##this function sets the player to ready
def readyCommand(player):
    if player.getReady() == False:
        player.setReady(True)
        player.sendClient("lobby.ready:" + str(player.getReady()))
    elif player.getReady() == True:
        player.setReady(False)
        player.sendClient("lobby.ready:" + str(player.getReady()))
    else:
        player.sendClient("lobby.ready:SeriouslyHowDidYouFuckItUpThisBad?")


##This is the subset of lobby actions
def lobbyCommand(block1, block2, player, lobbyList):
    arguements = block1.split(".")

    if arguements[1] == "new":
        newCommand(block2, player, lobbyList)
    elif arguements[1] == "lobbies":
        listCommand(player, lobbyList)
    elif arguements[1] == "join":
        joinCommand(block2, player, lobbyList)
    elif arguements[1] == "players":
        playerCommand(player, lobbyList)
    elif arguements[1] == "leave":
        leaveCommand(player, lobbyList)
    elif arguements[1] == "ready":
        readyCommand(player)
    elif arguements[1] == "start":
        startCommand(player, lobbyList)


##This is the command interperter from the client
def clientCommand(clientCommand, player, lobbyList):
    blocks = clientCommand.split(":")
    arguements = blocks[1].split(".")

    if arguements[0] == "lobby":
        if len(blocks) == 3:
            lobbyCommand(blocks[1], blocks[2], player, lobbyList)
            return True
        else:
            lobbyCommand(blocks[1], None, player, lobbyList)
            return True
    elif arguements[0] == "game":
        pass

    elif arguements[0] == "quit":
        player.sendClient("quit")
        runThread = False



##This the individual client thread that sends and recieves data from the client
def Threaded_Client(player, lobbyList):
    runThread = True

    while runThread:
        try:
            data = pickle.loads(player.getConn().recv(2048))

            if not data:
                break
            else:
                print("Received  --  " + data)
                runThread = clientCommand(data, player, lobbyList)

        except:
            break

    player.leaveLobby(lobbyList) 
    print("Lost connection to " + player.getId())
    player.getConn().close()


##
## this is the server listening for connections initizliaing them as players and passing them to threads
##
##initialize players id number and the lobby list
playerNumber = 1
lobbyList = []

##begin a loop to listen for connections from players
while True:

    ##create a playerId string
    playerId = "p" + str(playerNumber)
    ##create a connection and assign the values to conn and addr
    conn, addr = s.accept()
    ##document the connection
    print(str(addr) + " connected as player " + str(playerId))

    ##create a player object with current playerId
    playerId = Player(playerId, conn)

    ##start a new running thread
    start_new_thread(Threaded_Client, (playerId, lobbyList))
    ##increase id for next connection
    playerNumber += 1









