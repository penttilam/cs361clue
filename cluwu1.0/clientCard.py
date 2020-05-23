
class ClientCards:
    def __init__(self, cardName, cardCategory):
        print("in init")
        self.cardName = cardName
        self.cardCategory = cardCategory
        print("before get image")
        self.cardImg = self.getCardImage(cardName, cardCategory)

    def getCardImage(self, cardName, cardCategory):
        print("in get card")

        deck = []

        dakimakura = ("dakimakura", "weapon", "./images/item.png")
        katana = ("katana", "weapon", "./images/item.png")
        manga = ("manga", "weapon", "./images/item.png")
        bento = ("bento", "weapon", "./images/item.png")
        curse = ("curse", "weapon", "./images/item.png")
        mecha = ("mecha", "weapon", "./images/item.png")

        weapon = [dakimakura, katana, manga, bento, curse, mecha]

        shrine = ("shrine", "location", "./images/location.png")
        library = ("library", "location", "./images/location.png")
        tearoom = ("tearoom", "location", "./images/location.png")
        karaoke = ("karaoke", "location", "./images/location.png")
        lovehotel = ("lovehotel", "location", "./images/location.png")
        mangastore = ("mangastore", "location", "./images/location.png")
        school = ("school", "location", "./images/location.png")
        hotsprings = ("hotsprings", "location", "./images/location.png")
        beach = ("beach", "location", "./images/location.png")

        location = [shrine, library, tearoom, karaoke, lovehotel, mangastore, school, hotsprings, beach]

        colonelmustard = ("colonelmustard", "people", "./images/people.png")
        mrgreen = ("mrgreen", "people", "./images/people.png")
        mrswhite = ("mrswhite", "people", "./images/people.png")
        mspeacock = ("mspeacock", "people", "./images/people.png")
        msscarlet = ("msscarlet", "people", "./images/people.png")
        professorplum = ("professorplum", "people", "./images/people.png")

        people = [colonelmustard, mrgreen, mrswhite, mspeacock, msscarlet, professorplum]

        deck.append(weapon)
        deck.append(location)
        deck.append(people)

        for cardType in deck:
            if cardType[0][1] == cardCategory:
                for card in cardType:
                    if card[0] == cardName:
                        return card[2]

         


