import pygame
import pygame_gui
from pygame.locals import *

class Button:
    def __init__(self, buttonText, manager, xLoc=0, yLoc=0, width=0, height=0, container="", object_id="", shortcutKey="None"):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.text = buttonText
        self.manager = manager
        self.container = container
        self.shortcutKey = shortcutKey
        self.object_ids = object_id
        self.newButton()
        
    def newButton(self):
        if (self.container == ""):
            self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, object_id=self.object_ids)
        else:
            self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), text=self.text, manager=self.manager, container=self.container, object_id=self.object_ids)

    def setObjectId(self, objectId=""):
        self.button.kill()
        if self.object_ids == "" and objectId == "":
            self.object_ids = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newButton()

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
        self.button.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.button.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.button.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.button.set_text(self.text)

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
        self.button.enable()

    def disable(self):
        self.button.disable()

    def select(self):
        self.button.select()
    
    def update(self, time_delta):
        self.button.update(time_delta)

    def unselect(self):
        self.button.unselect()

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