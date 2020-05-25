import pygame
import pygame_gui
from pygame.locals import *

class Label:
    def __init__(self, labelText, manager, xLoc=0, yLoc=0, width=0, height=0, container="", object_id=""):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.text = labelText
        self.manager = manager
        self.container = container
        self.object_ids = object_id
        self.newLabel()
        
    def newLabel(self):
        if (self.container == ""):
            self.label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, object_id=self.object_ids)
        else:
            self.label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, container=self.container, object_id=self.object_ids)

    def setObjectId(self, objectId=""):
        self.label.kill()
        if self.object_ids == "" and objectId == "":
            self.object_ids = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newLabel()

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
    def getObjectId(self):
        return self.object_ids
    def getLabel(self):
        return self.label

    def setRow(self, row):
        self.row = row
    
    def setColumn(self, column):
        self.column = column
    
    def setRowColumn(self, row, column):
        self.row = row
        self.column = column

    def setXLoc(self,xLoc):
        self.xLoc = xLoc
        self.label.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.label.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.label.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.label.set_text(self.text)

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

    def setManager(self, newManager):
        self.label.kill()
        self.manager = newManager
        self.newLabel()

    def kill(self):
        self.label.kill()
