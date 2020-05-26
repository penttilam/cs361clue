
class ClientToken:
    def __init__(self, characterName, tokenRow, tokenColumn):
        self.tokenCharacter = characterName
        self.tokenRow = int(tokenRow)
        self.tokenColumn = int(tokenColumn)

    def getCharacter(self):
        return self.tokenCharacter

    def getRow(self):
        return self.tokenRow

    def getColumn(self):
        return self.tokenColumn

