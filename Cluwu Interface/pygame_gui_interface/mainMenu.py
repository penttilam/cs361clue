# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:07:20 2020

@author: LEhlert
"""
import pygame
from pygame.locals import *
from newGame import startNewGame
from gameList import startGameList


# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")
import pygame_gui

pygame.init()

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

pygame.display.set_caption('cluwu')
window_surface = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width, height), 'data/themes/quick_theme.json')

background = pygame.Surface((width, height))

#function takes
#text as a string
#font is the font defined
#color is your choice of color
#location int 
#surface the screen object you are adding this to
# x and y locations, integer pixel positions
#locations can be updated in the future to add other alignments,center, left right etc.... 


#add background image and text
#addImage('images/splashScreen.jpg', 1, background, width/2, height/2)
background.fill(manager.ui_theme.get_colour(None, None, 'dark_bg'))

menuLabelX = width/2-width/20
menuLabelY = height/2-height/5
menuLabelW = width/10
menuLabelH = height/10
pygame_gui.elements.ui_label.UILabel(pygame.Rect((menuLabelX, menuLabelY), (menuLabelW, menuLabelH)),text="Main Menu", manager=manager)

hostButtonX = width/2-width/20
hostButtonY = height/2-height/10
hostButtonW = width/10
hostButtonH = height/20
hostButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((hostButtonX, hostButtonY), (hostButtonW, hostButtonH)), text='Host', manager=manager)

joinButtonX = width/2-width/20
joinButtonY = height/2-height/20
joinButtonW = width/10
joinButtonH = height/20
joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((joinButtonX, joinButtonY), (joinButtonW, joinButtonH)), text='Join', manager=manager)

quitButtonX = width/2-width/20
quitButtonY = height/2
quitButtonW = width/10
quitButtonH = height/20
quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((quitButtonX, quitButtonY), (quitButtonW, quitButtonH)), text='Quit', manager=manager)

def openMainMenu():
    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hostButton):
                #when host is pressed starts the game list by calling the function
                startNewGame()
                
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #when join button is pressed starts the game list by calling the function
                startGameList()
    
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == quitButton):
                 pygame.quit()
                 sys.exit()
    
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()