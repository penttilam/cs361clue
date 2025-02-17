import random
from serverPlayer import *

characterChoices = [("scarlet", 0, 16), ("white", 7, 23), ("mustard", 24, 14), ("green", 24, 9), ("peacock", 18, 0), ("plum", 5, 0)]

class ServerToken:
    def __init__(self, characterName, tokenLocationX, tokenLocationY, tokenRoom):
        self.tokenCharacter = characterName
        self.tokenXLoc = tokenLocationX
        self.tokenYLoc = tokenLocationY
        self.tokenRoom = tokenRoom

    def getTokenCharacter(self):
        return self.tokenCharacter

    def getTokenXLoc(self):
        return self.tokenXLoc

    def getTokenYLoc(self):
        return self.tokenYLoc

    def setTokenXLocYLoc(self, newX, newY):
        self.tokenXLoc = newX
        self.tokenYLoc = newY

    def getTokenRoom(self):
        return self.tokenRoom

    def setTokenRoom(self, roomIn):
        self.tokenRoom = roomIn

def assignTokens(playerList):
    random.shuffle(playerList)
    tokenList = []
    for characters in characterChoices:
        objectName = characters[0]
        objectName = ServerToken(characters[0], characters[1], characters[2], "outside")
        tokenList.append(objectName)
    for x in range(len(playerList)):
        playerList[x].setMyToken(tokenList[x])

