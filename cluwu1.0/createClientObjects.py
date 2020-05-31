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
    print(serverPlayer.getMyToken())
    print(createClientToken(serverPlayer.getMyToken()))
    clientPlayer = ClientPlayer(serverPlayer.getReady(), createClientToken(serverPlayer.getMyToken()), serverPlayer.getMyCards(), serverPlayer.getMyTurn(), serverPlayer.getLostGame())
    print("after clientPlayer")
    print(clientPlayer)
    return clientPlayer


def createClientLobby(serverLobby):
    clientPlayerList = []
    serverPlayers = []
    serverPlayers = serverLobby.getPlayers()
    for player in serverPlayers:
        print("before")
        clientPlayer = createClientPlayer(player)
        print("After")
        clientPlayerList.append(clientPlayer)
    print(clientPlayerList)
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
    print("ClientGameStart")
    clientTurnOrder = []
    for players in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        print("ClientGameFor")
        clientTurnOrder.append(createClientPlayer(players))
    print("ClientGameAfterFor")
    clientPlayerToken = createClientToken(serverThreadInfo.getServerPlayer().getMyToken())
    print("ClientGameAfterToken")
    clientCards = createClientCards(serverThreadInfo.getServerPlayer().getMyCards())
    print("ClientGameAfterCards")
    clientChat = createClientChat(serverThreadInfo.getServerGame().getGameChat())
    print("ClientGameAfterChar")
    clientGame = ClientGame(clientTurnOrder, clientPlayerToken, clientCards, clientChat, serverThreadInfo.getServerGame().getFullDeck())
    print("print the deck after clientGame =")
    print(serverThreadInfo.getServerGame().getFullDeck())
    print("ClientGameAfterCLIENTGAME")
    clientGame.setDiscardedCards(serverThreadInfo.getServerGame().getDiscardedCards())
    print("returning clientGame")
    return clientGame


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
    




