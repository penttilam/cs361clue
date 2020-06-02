from clientToken import *
from clientWeapon import *
class ClientGame:
    def __init__(self, turnIn, tokenIn, cardsIn, chatIn, fullDeckIn):
        self.turnOrder = turnIn
        self.myToken = tokenIn
        self.myCards = cardsIn
        self.myChat = chatIn
        self.discards = None
        self.fullDeck = fullDeckIn
        self.wonLostGame = None
        self.suggestCards = None
        self.refuteCard = None
        self.weaponTokens = None

    def getTurnOrder(self):
        return self.turnOrder

    def getMyToken(self):
        return self.myToken

    def getMyCards(self):
        return self.myCards

    def getMyTurn(self):
        if(self.turnOrder[0].getGameToken().getTokenCharacter() == self.myToken.getTokenCharacter()):
            return True
        else:
            return False

    def setTurnOrder(self, turnOrder):
        self.turnOrder = turnOrder
        
    def getChat(self):
        return self.myChat

    def getDiscardedCards(self):
        return self.discards

    def setDiscardedCards(self, cards):
        self.discards = cards

    def getFullDeck(self): 
        return self.fullDeck

    def getSuggestCards(self):
        return self.suggestCards
        
    def setSuggestCards(self, suggestCards):
        self.suggestCards = suggestCards

    def getRefuteCard(self):
        return self.refuteCard

    def setRefuteCard(self, refuteCard):
        self.refuteCard = refuteCard

    def getWonLostGame(self):
        return self.wonLostGame

    def setWonLostGame(self, wonLost):
        self.wonLostGame = wonLost

    def getWeapons(self):
        return self.weaponTokens