
class ClientToken:
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


