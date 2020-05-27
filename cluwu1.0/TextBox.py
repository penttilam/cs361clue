import pygame
import pygame_gui
from pygame.locals import *

class TextBox:
    def __init__(self, manager, text="", xLoc=8, yLoc=680, width=341, height=200, container="", layer=1, wrapToHeight=False, objectId="chatlog"):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.manager = manager
        self.container = container
        self.text = text
        self.layer = layer
        self.focus = 0
        self.wrapToHeight = wrapToHeight
        self.object_id = objectId
        self.newTextBox()
        self.text = text

    def newTextBox(self):
        if (self.container == ""):
            print("no container")
            print(self.text)
            self.textBox = pygame_gui.elements.UITextBox(html_text=self.text, relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), manager=self.manager, object_id=self.object_id, wrap_to_height=self.wrapToHeight, layer_starting_height=self.layer)
            print(self.text)
        else:
            print("yes container")
            self.textBox = pygame_gui.elements.UITextBox(html_text=self.text, relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), manager=self.manager, container=self.container, object_id=self.object_id, wrap_to_height=self.wrapToHeight, layer_starting_height=self.layer)

    def setObjectId(self, objectId=""):
        self.textBox.kill()
        if self.object_id == "" and objectId == "":
            self.object_id = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_id = objectId
        self.newTextBox()

    def setWrapToText(self):
        self.textBox.wrap_to_height(True)

    def addText(self, text):
        self.text = text
        self.textBox.kill()
        self.newTextBox()

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
        return self.object_id
    def getTextBox(self):
        return self.textBox
    def getFocus(self):
        return self.focus

    def setRow(self, row):
        self.row = row
    
    def setColumn(self, column):
        self.column = column
    
    def setRowColumn(self, row, column):
        self.row = row
        self.column = column

    def setLocation(self, location):
        self.location = location

    def setOccupied(self, occupied):
        self.occupied = occupied

    def setXLoc(self,xLoc):
        self.xLoc = xLoc
        self.textBox.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.textBox.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.textBox.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.textBox.kill()
        self.newTextBox()

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

    def toggleFocus(self):
        self.focus = not self.focus

    def update(self, time_delta):
        self.textBox.update(time_delta)

    def setManager(self, newManager):
        self.textBox.kill()
        self.manager = newManager
        self.newTextBox()

    def kill(self):
        self.textBox.kill()

        

