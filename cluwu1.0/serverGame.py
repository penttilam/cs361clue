from serverPlayer import *

characterChoices = ["Ms Scarlet", "Mrs White", "Colonel Mustard", "Mr Green", "Professor Plum", "Ms Peacock"]

class serverGame:
    def __init__(self, playerList):
        self.playerTurnOrder = playerList
        self.numberPlayers = len(playerList)
        assignChar()
    
    #for x in self.playerTurnOrder: 
    #    print(x.getId() ,"'s turn is ", x.getTurn()) 
    
    def assignChar(self):
        random.shuffle(self.playersList)
        for x in range(self.numberPlayers):
            self.playerTurnOrder[x].setChar(characterChoices[x])
        

    def createClientGame(self):
        pass



    





















