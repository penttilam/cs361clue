from cards import Cards
import random

class sCard:

    def __init__(self, cardName, cardCategory):
        self.cardName = cardName
        self.cardCategory = cardCategory

    def createDeck():

        sDeck = []

        dakimakura = Cards("dakimakura", "weapon")
        katana = Cards("katana", "weapon")
        manga = Cards("manga", "weapon")
        bento = Cards("bento", "weapon")
        curse = Cards("curse", "weapon")
        mecha = Cards("mecha", "weapon")

        weapon = [dakimakura, katana, manga, bento, curse, mecha]

        shrine = Cards("shrine", "location")
        library = Cards("library", "location")
        tearoom = Cards("tearoom", "location")
        karaoke = Cards("karaoke", "location")
        lovehotel = Cards("lovehotel", "location")
        mangastore = Cards("mangastore", "location")
        school = Cards("school", "location")
        hotsprings = Cards("hotsprings", "location")
        beach = Cards("beach", "location")

        location = [shrine, library, tearoom, karaoke, lovehotel, mangastore, school, hotsprings, beach]

        colonelmustard = Cards("colonelmustard", "people")
        mrgreen = Cards("mrgreen", "people")
        mrswhite = Cards("mrswhite", "people")
        mspeacock = Cards("mspeacock", "people")
        msscarlet = Cards("msscarlet", "people")
        professorplum = Cards("professorplum", "people")

        people = [colonelmustard, mrgreen, mrswhite, mspeacock, msscarlet, professorplum]

        mPeople = random.choice(people)
        mWeapon = random.choice(weapon)
        mLocation = random.choice(location)

        people.remove(mPeople)
        weapon.remove(mWeapon)
        location.remove(mLocation)

        guilty = [mPeople, mWeapon, mLocation]

        print(mPeople.cardName, mWeapon.cardName, mLocation.cardName)

        print(" ")

        for card in weapon:
            print(card.cardName)

        print(" ")

        for card in location:
            print(card.cardName)

        print(" ")

        for card in people:
            print(card.cardName)

        sDeck.extend(weapon)
        sDeck.extend(location)
        sDeck.extend(people)

        print(" ")

        print("Remaining Cards:")

        for card in sDeck:
            print(card.cardName)

        print(" ")
        print("Shuffled: ")

        random.shuffle(sDeck)

        for card in sDeck:
            print(card.cardName)

