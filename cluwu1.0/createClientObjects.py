from serverPlayer import *
from clientPlayer import *
from serverLobby import *
from clientLobby import *


def createClientPlayer(serverPlayer):
    print("in client player")
    print("this be the list matey!: " + str(serverPlayer.getReady()))
    print(str(serverPlayer.getMyCharacter()))
    print(str(serverPlayer.getMyCards()))
    print(str(serverPlayer.getMyTurn()))
    print(str(serverPlayer.getLostGame()))
    clientPlayer = ClientPlayer(serverPlayer.getReady(), serverPlayer.getMyCharacter(), serverPlayer.getMyCards(), serverPlayer.getMyTurn(), serverPlayer.getLostGame())

    print("in after player")
    return clientPlayer


def createClientLobby(serverLobby):
    print("Im fucking here in clobby")
    clientPlayerList = []
    serverPlayers = []
    serverPlayers = serverLobby.getPlayers()
    print("this be the list matey!: " + str(serverPlayers))
    for player in serverPlayers:
        print("these be my clientBitches: " + str(player))
        clientPlayer = createClientPlayer(player)
        print("before the append")
        clientPlayerList.append(clientPlayer)
        print("after the append")
    print("this is after the for: " + str(clientPlayerList))
    print(serverLobby.getId())
    print(serverLobby.getPNumber())
    print(clientPlayerList)
    print(serverLobby.getLobbyReady())
    clientLobby = ClientLobby(serverLobby.getId(), serverLobby.getPNumber(), clientPlayerList, serverLobby.getLobbyReady())
    print("this is the client lobby: " + str(clientLobby))
    return clientLobby





