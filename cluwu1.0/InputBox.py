import pygame
import pygame_gui
from pygame.locals import *

class InputBox:
    def __init__(self, manager, xLoc=8, yLoc=770, width=341, height=30, container="", object_id="", text=""):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.manager = manager
        self.container = container
        self.object_id = object_id
        self.focus = 0
        self.text = text
        self.newInputBox()

    def newInputBox(self):
        if (self.container == ""):
            self.inputBox = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), manager=self.manager, object_id=self.object_id, )
        else:
            self.inputBox = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), manager=self.manager, container=self.container, object_id=self.object_id)
        self.inputBox.set_text_length_limit(32)

    def setObjectId(self, objectId=""):
        self.inputBox.kill()
        if self.object_id == "" and objectId == "":
            self.object_id = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newInputBox()

    def getText(self):
        return self.inputBox.get_text()
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
    def getInputBox(self):
        return self.inputBox

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
        self.inputBox.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.inputBox.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.inputBox.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.inputBox.set_text(self.text)

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
        self.inputBox.focus()
        self.focus = not self.focus
    
    def update(self, time_delta):
        self.inputBox.update(time_delta)

    def unfocus(self):
        self.inputBox.unfocus()

    def setManager(self, newManager):
        self.inputBox.kill()
        self.manager = newManager
        self.newInputBox()

    def kill(self):
        self.inputBox.kill()

        

