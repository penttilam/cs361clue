from serverPlayer import *
from clientPlayer import *
from serverLobby import *
from clientLobby import *
from serverToken import *
from clientToken import *
from serverGame import *
from clientGame import *
from serverCard import *
from clientCard import *
from serverChat import *

def createClientPlayer(serverPlayer):
    clientPlayer = ClientPlayer(serverPlayer.getReady(), serverPlayer.getMyToken(), serverPlayer.getMyCards(), serverPlayer.getMyTurn(), serverPlayer.getLostGame())
    return clientPlayer


def createClientLobby(serverLobby):
    clientPlayerList = []
    serverPlayers = []
    serverPlayers = serverLobby.getPlayers()
    for player in serverPlayers:
        clientPlayer = createClientPlayer(player)
        clientPlayerList.append(clientPlayer)
    clientLobby = ClientLobby(serverLobby.getId(), serverLobby.getPNumber(), clientPlayerList, serverLobby.getLobbyReady(), serverLobby.getStartGame())
    return clientLobby

def createClientToken(serverToken):
    clientToken = ClientToken(serverToken.getTokenCharacter(), serverToken.getTokenXLoc(), serverToken.getTokenYLoc())
    return clientToken

def createClientCards(serverCards):
    clientHand = []
    for cards in serverCards:
        clientCard = ClientCards(cards.getCardName(), cards.getCardCategory())
        clientHand.append(clientCard)
    return clientHand


def createClientChat(serverChat):
    htmlString = ""
    for lines in serverChat:
        htmlString += "<b>" + str(lines[0].getMyToken().getTokenCharacter()) + "</b> " + str(lines[1]) + "<br>"
    return htmlString





def createClientGame(serverThreadInfo):
    clientTurnOrder = []
    for players in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        clientTurnOrder.append(createClientPlayer(players))
    clientPlayerToken = createClientToken(serverThreadInfo.getServerPlayer().getMyToken())
    clientCards = createClientCards(serverThreadInfo.getServerPlayer().getMyCards())
    clientChat = createClientChat(serverThreadInfo.getServerPlayer().getGameChat())
    clientGame = ClientGame(clientTurnOrder, clientPlayerToken, clientCards, clientChat)
    return clientGameInit


def updateClientGame(serverGame):
    clientTurnOrder = []
    print("before the string")
    htmlChatLine = ""
    print("after the string")
    for players in serverGame.getPlayerTurnOrder():
        print("in loop")
        clientTurnOrder.append(createClientToken(players.getMyToken()))
        print("in ploop")
    for chatlines in serverGame.getGameChat().getChatlog():
        print("in loop2")
        htmlChatLine + "<b>" +  str(chatlines[0].getMyToken().getTokeCharacter()) + "</b> " + str(chatlines[1]) + "<br>"
    print("after before")
    updateClientGame = UpdateClientGame(clientTurnOrder, htmlChatLine)
    print("after")
    return updateClientGame
    




