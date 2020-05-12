import random
from player import *

class sCards:

    def __init__(self, cardName, cardCategory):
        self.cardName = cardName
        self.cardCategory = cardCategory

def createDeck(nameList):

    numPlayers = 0

    for y in nameList:
        numPlayers += 1

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

    print("Guilty Cards: ") 
    guilty = [mPeople, mWeapon, mLocation]

    print(mPeople.cardName, mWeapon.cardName, mLocation.cardName)

    sDeck.extend(weapon)
    sDeck.extend(location)
    sDeck.extend(people)

    print("\nShuffling remaining cards...")

    random.shuffle(sDeck)

    print("Shuffled Cards: \n") 

    for card in sDeck:
        print(card.cardName)

    remCards = 18 % numPlayers
    divCards = (18 - remCards)/numPlayers

    print("\nDividing up cards...") 
    for x in nameList:
        y = 0
        while y < divCards:
            y += 1 
            tempCard = sDeck[0] 
            x.addCard(tempCard)
            sDeck.pop(0) 
        

    print("Dividing remainder cards...")         
    if divCards > 0:
        y = 0 
        while y < remCards:
            y += 1 
            extraCard = sDeck[0]
            nameList[0].addCard(extraCard) 
            sDeck.pop(0)

    print("\n\nPlayer Decks") 
    for z in nameList:
        print("\nCURRENT PLAYER: ")
        print(z.getId())
        deckList = [] 
        deckList = z.getDeck() 
        for q in deckList:
            print(q.cardName)

    charChoices = ["Mrs White", "Colonel Mustard", "Mr Green", "Professor Plum", "Ms Peacock"]
    
    assignChar = ["Ms Scarlet"] 

    random.shuffle(charChoices)
    
    x = 0
    while x < numPlayers - 1:
        randChar = charChoices[x]
        assignChar.append(randChar) 
        x += 1

    random.shuffle(assignChar)

    c = 0
    for p in nameList:
        p.setChar(assignChar[c])
        c += 1


    for x in nameList:
        print("\n\nCharacter for " + x.getId()) 
        print(x.getChar())


    h = 2
    for x in nameList: 
        tempChar = x.getChar() 

        if tempChar == "Ms Scarlet":
            x.setTurn(1)
        else:
            x.setTurn(h)
            h += 1
        

    print("\nPlayer Turns: ") 

    for x in nameList: 
        print(x.getId() ,"'s turn is ", x.getTurn()) 







