
class ClientToken:
    def __init__(self, characterName, tokenRow, tokenColumn, tokenLocation):
        self.tokenCharacter = characterName
        self.tokenRow = tokenRow
        self.tokenColumn = tokenColumn
        self.tokenLocation = tokenLocation

    def getTokenCharacter(self):
        return self.tokenCharacter

    def getRow(self):
        return self.tokenRow

    def getColumn(self):
        return self.tokenColumn
    
    def getLocation(self):
        return self.tokenLocation

    def getLocation(self):
        return self.tokenLocation

