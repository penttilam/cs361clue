import pygame
import pygame_gui
from pygame.locals import *

class Button:
    def __init__(self, xLoc, yLoc, width, height, buttText, manager):
        self.x = xLoc
        self.y = yLoc
        self.w = width
        self.h = height
        self.text = buttText
        self.manager = manager
        self.object_ids = str(self.x)+str(self.y)+str(self.w)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=self.manager, object_id=self.object_ids)

    def getText(self):
        return self.text
    def getXY(self):
        return "X="+str(self.x)+", Y="+str(self.y)
    def getX(self):
        return self.x
    def getY(self):
        return self.y


    def setX(self,x):
        self.button.set_relative_position((x,self.y))

    def sety(self,y):
        self.button.set_relative_position((self.x,y))
    
    def setXY(self, x, y):
        self.button.set_relative_position((x,y))

    def setText(self, text):
        self.text = text
        self.button.set_text(self.text)

    def setW(self, w):
        self.button.kill()
        self.object_ids = str(self.x)+str(self.y)+str(w)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (w, self.h)), text=self.text, manager=self.manager, object_id=self.object_ids)

    def setH(self, h):
        self.button.kill()
        self.object_ids = str(self.x)+str(self.y)+str(self.w)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, h)), text=self.text, manager=self.manager, object_id=self.object_ids)

    def setWH(self, w, h):
        self.button.kill()
        self.object_ids = str(self.x)+str(self.y)+str(w)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (w, h)), text=self.text, manager=self.manager, object_id=self.object_ids)

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

    def setManager(self, manager):
        self.button.kill()
        self.manager = manager
        self.object_ids = str(self.x)+str(self.y)+str(self.w)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=manager, object_id=self.object_ids)

    def event(self, event):
        return (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.object_ids == self.button.object_ids) or (event.type == KEYDOWN and event.key == K_ESCAPE)