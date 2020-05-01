import socket
from _thread import *
import sys
from player import Player
import pickle
from lobby import Lobby
from cLobby import CLobby

##this is the IPV4 connection
server = "45.132.241.193"
port = 42069

##this sets up the IPV4 socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#setting up the server named s

##this actively binds the server to a port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

##this allows the server to accept a connection limited to: 6
s.listen(6)
print("Server waiting for a connection :D")

##this is the individual thread for a player
def Threaded_Client(player, lobbyList):

    while True:
        try:

            ##this is listening for information from the client
            data = pickle.loads(player.getConn().recv(2048))
           
            if not data:
                break

            ##if the connection is valid and data is recieved
            else:

                ##prints the message recieved
                print("Received  --  " + data)
                
                ##this takes in data from the client and splits it by :'s and .'s
                action = data.split(":")
                command = action[1].split(".")

                ##This analyzes the data thats come in from the client and pushes a command
                ## based on the string recieved from the client

                ##Base-command lobby checked
                if command[0] == "lobby":

                    ##Sub-command new checked
                    if command[1] == "new":

                        ##run command to create a lobby and place it in the lobbylist
                        action[2] = Lobby(player, action[2])
                        lobbyList.append(action[2])

                    ##Sub-command getLobbies checked
                    if command[1] == "lobbies":

                        ##run command to compile a string of arguements composed of
                        ## lobbyname:numberPlayers
                        lobbyInfo = "lobby.list"
                        cLobbies = []
                        for x in lobbyList:
                            lId = x.getId()
                            cLobbies.append((lId = CLobby(x.getId(), x.getPNumber(), x.getPName())))
                            #lobbyInfo += ":"
                            #lobbyInfo += x.getId()
                            #lobbyInfo += "."
                            #lobbyInfo += str(x.getPNumber())

                        #player.sendClient(lobbyInfo)

                    ##Sub-command join check
                    if command[1] == "join":

                        ##run command to find a lobby object based on the name given
                        ## once an object name matches the lobby name the player is added to the object
                        for x in lobbyList:
                            if x.getId() == action[2]:
                                x.addPlayer(player)

                    ##Sub-command get players names in lobby
                    if command[1] == "players":
                        lobby = player.getLobby()
                        namelist = []
                        namelist = lobby.getPName()
                        lobbyInfo = "lobby.players:"
                        for x in namelist:
                            lobbyInfo += x
                            lobbyInfo += "."

                        player.sendClient(lobbyInfo)

                ##Base-command quit checked
                elif command[0] == "quit":
                    player.sendClient("quit")

        except:
            break

    ##If the player disconnects and is a lobby they are removed
    player.leaveLobby(lobbyList) 

    ##Prints diconnect and close the connection
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
    
