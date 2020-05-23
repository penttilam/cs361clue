import random
from serverPlayer import *
##

#characterChoices = [("Ms Scarlet", 16), ("Mrs White", 191), ("Colonel Mustard", 590), ("Mr Green", 585), ("Professor Plum", 432), ("Ms Peacock", 120)]
characterChoices = [("scarlet", 0, 16), ("white", 7, 23), ("mustard", 24, 14), ("green", 24, 9), ("plum", 18, 0), ("peacock", 5, 0)]

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

    def setTokenXLocYLoc(self, newX, newY):
        self.tokenXLoc = newX
        self.tokenYLoc = newY


def assignTokens(playerList):
    random.shuffle(playerList)
    tokenList = []
    for characters in characterChoices:
        objectName = characters[0]
        objectName = ServerToken(characters[0], characters[1], characters[2])
        tokenList.append(objectName)
    for x in range(len(playerList)):
        playerList[x].setMyToken(tokenList[x])

