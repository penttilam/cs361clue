## Project Cluwu
## File clientPlayer.py
## This is the players info for use on the client side

class ClientPlayer:
    def __init__(self, ready, token, cards, turn, wonLost):
        self.ready = ready
        self.myToken = token 
        self.myCards = cards
        self.myTurn = turn
        self.wonLostGame = wonLost

    def getReady(self):
        return self.ready
    
    def getGameToken(self):
        return self.myToken

    def getMyCards(self):
        return self.myCards

    def getMyTurn(self):
        return self.myTurn
    
    def getWonLostGame(self):
        return self.wonLostGame

