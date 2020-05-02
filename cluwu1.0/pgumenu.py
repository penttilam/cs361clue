# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:37:05 2020

@author: LEhlert
"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")
import pygame_gui

pygame.init()

class Player:
    def __init__(self):
        self.id = "newPlayer"
        self.character = ""
        self.active = 0
        self.rolled = 0
        self.cards = ["","",""]
        self.game = ""

#colors
black = 0, 0, 0
white = 255, 255, 255

#screen set up
width = 1000
height = 1000

#set the font
#set font for text in program and text size
title = pygame.font.SysFont(None, int(height/20))
font = pygame.font.SysFont(None, int(height/40))

#function takes
#text as a string
#font is the font defined
#color is your choice of color
#location int 
#surface the screen object you are adding this to
# x and y locations, integer pixel positions
#locations can be updated in the future to add other alignments,center, left right etc.... 
def addImage(img, location, surface, x, y):
    imgObj=pygame.image.load(img)
    imgRect = imgObj.get_rect()
    if location == 1:
       imgRect.center = (int(x), int(y))
    surface.blit(imgObj, imgRect)
    return imgObj

#function takes
#text as a string
#font is the font defined
#color is your choice of color
#location int 
#surface the screen object you are adding this to
# x and y locations, integer pixel positions
#locations can be updated in the future to add other alignments,center, left right etc.... 
def addText(text, font, color, location, surface, x, y):
    textObj=font.render(text,1,color)
    textRect=textObj.get_rect()
    if location == 1:
        textRect.center = (int(x), int(y))
    surface.blit(textObj, textRect)
    
pygame.display.set_caption('cluwu')
window_surface = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width, height), 'data/themes/quick_theme.json')

background = pygame.Surface((width, height))

#add background image and text
addImage('splashscreen.jpg', 1, background, width/2, height/2)
addText('Main Menu', title, black, 1, background, width/2, height/8)

#background.fill(manager.ui_theme.get_colour(None, None, 'dark_bg'))

hostButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((int(width/2)-int(width/20), int(height/2)-int(width/5)), (int(width/10), int(height/20))), text='Host', manager=manager)

joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((int(width/2)-int(width/20), int(height/2)-int(width/10)), (int(width/10), int(height/20))), text='Join', manager=manager)

quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((int(width/2)-int(width/20), int(height/2)), (int(width/10), int(height/20))), text='Quit', manager=manager)

clock = pygame.time.Clock()


def splash():
    while True:
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()
        #add splash screen 
        splash = addImage("splashscreen.jpg", 1, window_surface, width/2, height/2)
        #quit when mouse is clocked
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if splash.get_rect().collidepoint(mousePos):
                    mainMenu()

def hostGame():
    manager = pygame_gui.UIManager((width, height), 'data/themes/quick_theme.json')
    gameName = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((int(width/2)-int(width/20), int(height/2)), (int(width/10), int(height/20))), manager=manager)
    window_surface.blit(gameName, (0, 0))

def mainMenu():
    clock = pygame.time.Clock()
    is_running = True            
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
    
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == quitButton):
                 pygame.quit()
                 sys.exit()
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hostButton):
                 hostGame()
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()
        
splash()