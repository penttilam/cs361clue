from clientToken import *

class ClientGameInit:
    def __init__(self, turnIn, tokenIn, cardsIn):
        self.turnOrder = turnIn
        self.myToken = tokenIn
        self.myCards = cardsIn
        

    def getTurnOrder(self):
        return self.turnOrder

    def getMyToken(self):
        return self.myToken

    def getMyCards(self):
        return self.myCards

    def getMyTurn(self):
        if(str(self.turnOrder[0].getTokenCharacter()) == str(self.myToken.getTokenCharacter())):
            return True
        else:
            return False

    def setTurnOrder(self, turnOrder):
        self.turnOrder = turnOrder

class updateClientGame:
    def __init__(self, turnIn, chatText):
        self.turnOrder = turnIn
        self.chatText = chatText

    def getTurnOrder(self):
        return self.turnOrder

    def getChatUpdate(self):
        return self.chatText



