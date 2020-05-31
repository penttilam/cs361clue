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
    clientPlayer = ClientPlayer(serverPlayer.getReady(), createClientToken(serverPlayer.getMyToken()), serverPlayer.getMyCards(), serverPlayer.getMyTurn(), serverPlayer.getWonLostGame())
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
    try:
        clientToken = ClientToken(serverToken.getTokenCharacter(), serverToken.getTokenXLoc(), serverToken.getTokenYLoc())
    except:
        clientToken = None
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
        htmlString += lines
    return htmlString





def createClientGame(serverThreadInfo):
    clientTurnOrder = []
    for players in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        clientTurnOrder.append(createClientPlayer(players))
    clientPlayerToken = createClientToken(serverThreadInfo.getServerPlayer().getMyToken())
    clientCards = createClientCards(serverThreadInfo.getServerPlayer().getMyCards())
    clientChat = createClientChat(serverThreadInfo.getServerGame().getGameChat())
    clientGame = ClientGame(clientTurnOrder, clientPlayerToken, clientCards, clientChat, serverThreadInfo.getServerGame().getFullDeck())
    clientGame.setDiscardedCards(serverThreadInfo.getServerGame().getDiscardedCards())
    return clientGame


def updateClientGame(serverGame):
    clientTurnOrder = []
    htmlChatLine = ""
    for players in serverGame.getPlayerTurnOrder():
        clientTurnOrder.append(createClientToken(players.getMyToken()))
    for chatlines in serverGame.getGameChat().getChatlog():
        htmlChatLine + "<b>" +  str(chatlines[0].getMyToken().getTokeCharacter()) + "</b> " + str(chatlines[1]) + "<br>"
    updateClientGame = UpdateClientGame(clientTurnOrder, htmlChatLine)
    return updateClientGame
    




