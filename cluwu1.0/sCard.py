import random

class sCards:

    def __init__(self, cardName, cardCategory):
        self.cardName = cardName
        self.cardCategory = cardCategory

def createDeck(numPlayers):
    print("hello from server sCards")

    sDeck = []

    dakimakura = sCards("dakimakura", "weapon")
    katana = sCards("katana", "weapon")
    manga = sCards("manga", "weapon")
    bento = sCards("bento", "weapon")
    curse = sCards("curse", "weapon")
    mecha = sCards("mecha", "weapon")

    weapon = [dakimakura, katana, manga, bento, curse, mecha]

    shrine = sCards("shrine", "location")
    library = sCards("library", "location")
    tearoom = sCards("tearoom", "location")
    karaoke = sCards("karaoke", "location")
    lovehotel = sCards("lovehotel", "location")
    mangastore = sCards("mangastore", "location")
    school = sCards("school", "location")
    hotsprings = sCards("hotsprings", "location")
    beach = sCards("beach", "location")

    location = [shrine, library, tearoom, karaoke, lovehotel, mangastore, school, hotsprings, beach]

    colonelmustard = sCards("colonelmustard", "people")
    mrgreen = sCards("mrgreen", "people")
    mrswhite = sCards("mrswhite", "people")
    mspeacock = sCards("mspeacock", "people")
    msscarlet = sCards("msscarlet", "people")
    professorplum = sCards("professorplum", "people")

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

    print("Remaining sCards:")

    for card in sDeck:
        print(card.cardName)

    print(" ")
    print("Shuffled: ")

    random.shuffle(sDeck)

    for card in sDeck:
        print(card.cardName)





