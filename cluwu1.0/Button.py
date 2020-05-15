import pygame
import pygame_gui
from pygame.locals import *

class Button:
    

    def __init__(self, buttText, manager, xLoc=0, yLoc=0, width=0, height=0, container="", object_id="", shortcutKey="None"):
        self.x = xLoc
        self.y = yLoc
        self.w = width
        self.h = height
        self.text = buttText
        self.manager = manager
        self.container = container
        self.shortcutKey = shortcutKey
        if (object_id == ""):
            self.object_ids = str(xLoc)+str(yLoc)+str(width)
        else:
            self.object_ids = object_id
        self.newButton()
        
    def newButton(self):
        if (self.container == ""):
            self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=self.manager, object_id=self.object_ids)
        else:
            self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=self.manager, container=self.container, object_id=self.object_ids)

    def getText(self):
        return self.text
    def getXLocYLoc(self):
        return "X="+str(self.x)+", Y="+str(self.y)
    def getXLoc(self):
        return self.x
    def getYLoc(self):
        return self.y

    def setX(self,x):
        self.x = x
        self.button.set_relative_position((self.x, self.y))

    def setYLoc(self,y):
        self.y = y
        self.button.set_relative_position((self.x, self.y))
    
    def setXLocYLoc(self, x, y):
        self.x = x
        self.y = y
        self.button.set_relative_position((self.x, self.y))

    def setText(self, text):
        self.text = text
        self.button.set_text(self.text)

    def setWidth(self, w):
        self.button.kill()
        self.w = w
        self.object_ids = str(self.x)+str(self.y)+str(w)
        self.newButton()
 
    def setHeight(self, h):
        self.button.kill()
        self.h = h
        self.object_ids = str(self.x)+str(self.y)+str(self.w)
        self.newButton()

    def setWidthHeight(self, w, h):
        self.button.kill()
        self.w = w
        self.h = h
        self.object_ids = str(self.x)+str(self.y)+str(w)
        self.newButton()

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
            if (self.shortcutKey == "None"):
                return (event.ui_element.object_ids == self.button.object_ids)
            else:
                return (event.ui_element.object_ids == self.button.object_ids) or (event.type == KEYDOWN and event.key == shortcutKey)
