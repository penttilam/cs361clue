class ClientWeapon:
    def __init__(self, weaponName, weaponRoom):
        self.name = weaponName
        self.location = weaponRoom

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location


