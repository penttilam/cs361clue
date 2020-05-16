import random

class Cards:

    def __init__(self, cardName, cardCategory, cardImg):
        self.cardName = cardName
        self.cardCategory = cardCategory
        self.cardImg = cardImg

    def createDeck():

        deck = []

        dakimakura = Cards("dakimakura", "weapon", "./images/item.png")
        katana = Cards("katana", "weapon", "./images/item.png")
        manga = Cards("manga", "weapon", "./images/item.png")
        bento = Cards("bento", "weapon", "./images/item.png")
        curse = Cards("curse", "weapon", "./images/item.png")
        mecha = Cards("mecha", "weapon", "./images/item.png")

        weapon = [dakimakura, katana, manga, bento, curse, mecha]

        shrine = Cards("shrine", "location", "./images/location.png")
        library = Cards("library", "location", "./images/location.png")
        tearoom = Cards("tearoom", "location", "./images/location.png")
        karaoke = Cards("karaoke", "location", "./images/location.png")
        lovehotel = Cards("lovehotel", "location", "./images/location.png")
        mangastore = Cards("mangastore", "location", "./images/location.png")
        school = Cards("school", "location", "./images/location.png")
        hotsprings = Cards("hotsprings", "location", "./images/location.png")
        beach = Cards("beach", "location", "./images/location.png")

        location = [shrine, library, tearoom, karaoke, lovehotel, mangastore, school, hotsprings, beach]

        colonelmustard = Cards("colonelmustard", "people", "./images/people.png")
        mrgreen = Cards("mrgreen", "people", "./images/people.png")
        mrswhite = Cards("mrswhite", "people", "./images/people.png")
        mspeacock = Cards("mspeacock", "people", "./images/people.png")
        msscarlet = Cards("msscarlet", "people", "./images/people.png")
        professorplum = Cards("professorplum", "people", "./images/people.png")

        people = [colonelmustard, mrgreen, mrswhite, mspeacock, msscarlet, professorplum]

        deck.extend(weapon)
        deck.extend(location)
        deck.extend(people)

#### 
