import random


weaponChoices = ["dakimakura", "katana", "manga", "bento", "curse", "mecha"]
locationChoices = ["shrine", "library", "tearoom", "karaoke", "lovehotel", "mangastore", "school", "hotspring", "beach"]


class ServerWeapon:
    def __init__(self, weaponName, weaponRoom):
        self.name = weaponName
        self.location = weaponRoom

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def setLocation(self, locationIn):
        self.location = locationIn


def assignWeapons():
    random.shuffle(locationChoices)
    weaponList = []
    for x in range(len(weaponChoices)):
        serverWeapon = ServerWeapon(weaponChoices[x], locationChoices[x])
        weaponList.append(serverWeapon)
    return weaponList






