import random
from serverPlayer import *

class serverCards:
    def __init__(self, cardName, cardCategory):
        self.cardName = cardName
        self.cardCategory = cardCategory

    def getCardName(self):
        return self.cardName

    def getCardCategory(self):
        return self.cardCategory



def createDecks():

    serverCardSet = []
    serverDeck = []

    dakimakura = serverCards("dakimakura", "weapon")
    katana = serverCards("katana", "weapon")
    manga = serverCards("manga", "weapon")
    bento = serverCards("bento", "weapon")
    curse = serverCards("curse", "weapon")
    mecha = serverCards("mecha", "weapon")

    weapon = [dakimakura, katana, manga, bento, curse, mecha]

    shrine = serverCards("shrine", "location")
    library = serverCards("library", "location")
    tearoom = serverCards("tearoom", "location")
    karaoke = serverCards("karaoke", "location")
    lovehotel = serverCards("lovehotel", "location")
    mangastore = serverCards("mangastore", "location")
    school = serverCards("school", "location")
    hotsprings = serverCards("hotsprings", "location")
    beach = serverCards("beach", "location")

    location = [shrine, library, tearoom, karaoke, lovehotel, mangastore, school, hotsprings, beach]

    colonelmustard = serverCards("mustard", "people")
    mrgreen = serverCards("green", "people")
    mrswhite = serverCards("white", "people")
    mspeacock = serverCards("peacock", "people")
    msscarlet = serverCards("scarlet", "people")
    professorplum = serverCards("plum", "people")

    character = [colonelmustard, mrgreen, mrswhite, mspeacock, msscarlet, professorplum]

    guiltyCharacter = random.choice(character)
    guiltyWeapon = random.choice(weapon)
    guiltyLocation = random.choice(location)

    character.remove(guiltyCharacter)
    weapon.remove(guiltyWeapon)
    location.remove(guiltyLocation)

    guiltyCards = [guiltyCharacter, guiltyWeapon, guiltyLocation]
    serverCardSet.append(guiltyCards)

    serverDeck.extend(weapon)
    serverDeck.extend(location)
    serverDeck.extend(character)

    random.shuffle(serverDeck)
    serverCardSet.append(serverDeck)

    return serverCardSet

def dealCards(deckList, playerList):
    remCards = 18 % len(playerList)
    divCards = (18 - remCards)/len(playerList)

    for player in playerList:
        numberPlayerCards = 0
        tempHand = []
        while numberPlayerCards < divCards:
            numberPlayerCards += 1 
            tempHand.append(deckList.pop(0))
        if remCards != 0:
            tempHand.append(deckList.pop(0))
            remCards -= 1
        player.setHand(tempHand)
        





