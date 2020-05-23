import pygame
import pygame_gui
from Button import Button
from Image import Image
from pygame.locals import *

class ImageButton:
    def __init__(self, manager, xLoc=0, yLoc=0, width=0, height=0, imageFile="tile.png", buttonText="", imagePath="./images/", container="", object_id="", button=""):
        self.image = Image(imageFile, manager, xLoc, yLoc, width, height, imagePath, container, object_id)
        if button == "":
            self.button = Button(buttonText, manager, xLoc, yLoc, width, height, container, object_id)
        else:
            self.button = button
        if object_id == "":
            self.objectId = "IB" + self.button.getObjectId()
        else:
            self.objectId = object_id

    def getText(self):
        return self.button.getText()
    def getXLocYLoc(self):
        return (self.button.xLoc, self.button.yLoc)
    def getXLoc(self):
        return self.button.xLoc
    def getYLoc(self):
        return self.button.yLoc
    def getWidth(self):
        return self.button.width
    def getHeight(self):
        return self.button.height
    def getContainer(self):
        return self.image.getContainer()
    def getObjectId(self):
        return self.objectId

    def setXLoc(self,xLoc):
        self.button.setXLoc(xLoc)
        self.image.setXLoc(xLoc)
        
    def setYLoc(self,yLoc):
        self.button.setYLoc(yLoc)
        self.image.setYLoc(yLoc)
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.button.setXLocYLoc(xLoc, yLoc)
        self.image.setXLocYLoc(xLoc, yLoc)

    def setText(self, text):
        self.button.setText(text)

    def setWidth(self, width):
        self.button.setWidth(width)
        self.image.setWidth(width)
 
    def setHeight(self, height):
        self.button.setHeight(height)
        self.image.setHeight(height)

    def setWidthHeight(self, width, height):
        self.button.setWidthHeight(width, height)
        self.image.setWidthHeight(width, height)

    def setImage(self, imageFile, imagePath="./images/"):
        self.image.setImage(imageFile, imagePath)

    def enable(self):
        self.button.enable()

    def disable(self):
        self.button.disable()

    def select(self):
        self.button.select()
    
    def unselect(self):
        self.button.unselect()

    def setManager(self, newManager):
        self.button.setManager(newManager)
        self.image.setManager(newManager)

    def setContainer(self, newContainer):
        self.button.setContainer(newContainer)
        self.image.setContainer(newContainer)

    def getClickedStatus(self, event):
        return self.button.getClickedStatus(event)

    def kill(self):
        self.button.kill()
        self.image.kill()