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
        if(self.turnOrder[0].getTokenCharacter() == self.myToken.getTokenCharacter()):
            return True
        else:
            return False

class UpdateClientGame:
    def __init__(self, turnIn, chatLineIn):
        print("this is in init")
        self.turnOrder = turnIn
        self.chat = chatLineIn

    def getTurnOrder(self):
        return self.turnOrder

    def getChatUpdate(self):
        return self.chat


