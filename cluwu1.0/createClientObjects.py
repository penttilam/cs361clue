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
from clientWeapon import *
from serverWeapon import *

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
        clientToken = ClientToken(serverToken.getTokenCharacter(), serverToken.getTokenXLoc(), serverToken.getTokenYLoc(), serverToken.getTokenRoom())
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


def createClientWeapon(serverWeapon):
    weaponList = []
    for weapon in serverWeapon:
        clientWeapon = ClientWeapon(weapon.getName(), weapon.getLocation())
        weaponList.append(clientWeapon)
    return weaponList


def createClientGame(serverThreadInfo):
    clientTurnOrder = []
    for players in serverThreadInfo.getServerGame().getPlayerTurnOrder():
        clientTurnOrder.append(createClientPlayer(players))
    clientPlayerToken = createClientToken(serverThreadInfo.getServerPlayer().getMyToken())
    clientCards = createClientCards(serverThreadInfo.getServerPlayer().getMyCards())
    clientChat = createClientChat(serverThreadInfo.getServerGame().getGameChat())
    clientWeapon = createClientWeapon(serverThreadInfo.getServerGame().getServerWeapons())
    clientGame = ClientGame(clientTurnOrder, clientPlayerToken, clientCards, clientChat, serverThreadInfo.getServerGame().getFullDeck(), clientWeapon)
    clientGame.setDiscardedCards(serverThreadInfo.getServerGame().getDiscardedCards())
    clientGame.setSuggestCards(serverThreadInfo.getServerGame().getSuggestCards())
    clientGame.setRefuteCard(serverThreadInfo.getServerGame().getRefuteCard())
    return clientGame




