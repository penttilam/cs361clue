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
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=self.manager)

    def getText(self):
        return self.text
    
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
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (w, self.h)), text=self.text, manager=self.manager)        

    def setH(self, h):
        self.button.kill()
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, h)), text=self.text, manager=self.manager)        

    def setWH(self, w, h):
        self.button.kill()
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (w, h)), text=self.text, manager=self.manager)

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
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (self.w, self.h)), text=self.text, manager=self.manager)

    def event(self, event):
        return (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.text == self.text) or (event.type == KEYDOWN and event.key == K_ESCAPE)