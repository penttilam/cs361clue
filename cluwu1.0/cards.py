class Cards:
    def __init__(self, cardName, cardCategory, cardPic):
        self.cardName = cardName
        self.cardCategory = cardCategory
        self.cardPic = cardPic

    def createSCard(self):
        tempCard = sCard(self.cardName, self.cardCategory)
        return tempCard


