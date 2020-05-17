import pygame
import pygame_gui
from pygame.locals import *

class Image:
    def __init__(self, imageFile, manager, xLoc=0, yLoc=0, width=0, height=0, imagePath="./images/", container="", object_id=""):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.imageFile = imageFile
        self.imagePath = imagePath
        self.height = height
        self.manager = manager
        self.container = container
        self.object_ids = object_id
        self.newImage()
        
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

    def getText(self):
        return self.text
    def getXLocYLoc(self):
        return (self.xLoc, self.yLoc)
    def getXLoc(self):
        return self.xLoc
    def getYLoc(self):
        return self.yLoc

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

    def enable(self):
        self.image.enable()

    def disable(self):
        self.image.disable()

    def select(self):
        self.image.select()
    
    def update(self, time_delta):
        self.image.update(time_delta)

    def unselect(self):
        self.image.unselect()

    def setManager(self, newManager):
        self.image.kill()
        self.manager = newManager
        self.newImage()

    def setManager(self, newContainer):
        self.image.kill()
        self.manager = newContainer
        self.newImage()


    def getClickedStatus(self, event):
        if (event.type == MOUSEBUTTONDOWN):
            return event.ui_element.object_ids == self.image.object_ids

    def kill(self):
        self.image.kill()