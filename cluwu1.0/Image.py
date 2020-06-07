import pygame
import pygame_gui
from pygame.locals import *

class Image:
    def __init__(self, imageFile, manager, xLoc=0, yLoc=0, width=0, height=0, imagePath="./images/", container="", object_id=""):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.imageFile = imageFile
        self.imagePath = imagePath
        self.manager = manager
        self.container = container
        self.object_ids = object_id
        self.column = 0
        self.row = 0
        self.location = "outside"
        self.newImage()
        self.moveHistory = []

    def newImage(self):
        if (self.container == ""):
            self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), image_surface=pygame.image.load(self.imagePath+self.imageFile), manager=self.manager)
        else:
            self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), image_surface=pygame.image.load(self.imagePath+self.imageFile), manager=self.manager, container=self.container)

    def setObjectId(self, objectId=""):
        self.image.kill()
        if self.object_ids == "" and objectId == "":
            self.object_ids = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newImage()

    def getLocation(self):
        return self.location
    def getText(self):
        return self.text
    def getXLocYLoc(self):
        return (self.xLoc, self.yLoc)
    def getXLoc(self):
        return self.xLoc
    def getYLoc(self):
        return self.yLoc
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getContainer(self):
        return self.image.get_container()
    def getObjectId(self):
        return self.object_ids
    def getRow(self):
        return self.row
    def getColumn(self):
        return self.column

    def setLocation(self, location):
        self.location = location

    def setRow(self, row):
        self.row = row
    
    def setColumn(self, column):
        self.column = column

    def setRowColumn(self, row, column):
        self.row = row
        self.column = column

    def setXLoc(self,xLoc):
        self.xLoc = xLoc
        self.image.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.image.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.image.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.image.set_text(self.text)

    def setWidth(self, width):
        self.width = width
        self.setObjectId()
 
    def setHeight(self, height):
        self.height = height
        self.setObjectId()

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height
        self.setObjectId()

    def setImage(self, imageFile, imagePath="./images/"):
        self.image.kill()
        self.imageFile = imageFile
        self.imagePath = imagePath
        self.newImage()

    def setManager(self, newManager):
        self.image.kill()
        self.manager = newManager
        self.newImage()

    def setContainer(self, newContainer):
        self.image.kill()
        self.manager = newContainer
        self.newImage()
        
    def getMoveHistory(self):
        return self.moveHistory
    def addMove(self, move):
        self.moveHistory.append(move)
    def clearMoveHistory(self):
        self.moveHistory = []

    def kill(self):
        self.image.kill()