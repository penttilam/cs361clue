import random
from serverPlayer import *

#characterChoices = [("Ms Scarlet", 16), ("Mrs White", 191), ("Colonel Mustard", 590), ("Mr Green", 585), ("Professor Plum", 432), ("Ms Peacock", 120)]
characterChoices = [("Ms Scarlet", 0, 16), ("Mrs White", 7, 23), ("Colonel Mustard", 24, 14), ("Mr Green", 24, 9), ("Professor Plum", 18, 0), ("Ms Peacock", 5, 0)]

class ServerToken:
    def __init__(self, characterName, tokenLocationX, tokenLocationY):
        self.tokenCharacter = characterName
        self.tokenXLoc = tokenLocationX
        self.tokenYLoc = tokenLocationY

    def getTokenCharacter(self):
        return self.tokenCharacter

    def getTokenXLoc(self):
        return self.tokenXLoc

    def getTokenYLoc(self):
        return self.tokenYLoc



def assignTokens(playerList):
    random.shuffle(playerList)
    tokenList = []
    for characters in characterChoices:
        objectName = characters[0]
        objectName = ServerToken(characters[0], characters[1], characters[2])
        tokenList.append(objectName)
    for x in range(len(playerList)):
        playerList[x].setMyToken(tokenList[x])

