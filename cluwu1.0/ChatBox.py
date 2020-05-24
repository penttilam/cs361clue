import pygame
import pygame_gui
from pygame.locals import *


class InputBox:
        def __init__(self, xLoc=0, yLoc=0, width=120, height=15, manager):
            self.xLoc = xLoc
            self.yLoc = yLoc
            self.width = width
            self.height = height
            self.manager = manager
            self.inputBox = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((self.chatTextBoxX, self.chatTextBoxY), (self.chatTextBoxW, self.chatTextBoxH)), manager=self.manager)
            self.lastTextInput = self.chatInput.get_text()

    def newInputBox(self):
        if (self.container == ""):
            self.inputBox = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, object_id=self.object_ids)
        else:
            self.inputBox = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, container=self.container, object_id=self.object_ids)

    def setObjectId(self, objectId=""):
        self.inputBox.kill()
        if self.object_ids == "" and objectId == "":
            self.object_ids = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newInputBox()
        
    def getLocation(self):
        return self.location
    def getOccupied(self):
        return self.occupied
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
    def getRow(self):
        return self.row
    def getColumn(self):
        return self.column
    def getButton(self):
        return self.button

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

    def focus(self):
        self.inputBox.focus()
    
    def update(self, time_delta):
        self.inputBox.update(time_delta)

    def unfocus(self):
        self.inputBox.unfocus()

    def setManager(self, newManager):
        self.button.kill()
        self.manager = newManager
        self.newButton()

    def getClickedStatus(self, event):
        if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED):
            return event.ui_element.object_ids == self.button.object_ids
        elif (event.type == KEYDOWN):
            return event.key == self.shortcutKey

    def kill(self):
        self.button.kill()

        

