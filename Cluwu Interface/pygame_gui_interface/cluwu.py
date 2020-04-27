#import needed libraries 
import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui
from mainMenu import openMainMenu

#initialize game screen 
pygame.init()

pygame.display.set_caption('cluwu')
#set the icon
icon = pygame.image.load('images/cluwuIcon.png')
pygame.display.set_icon(icon)

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

#create pygame area to add splash image to
window_surface = pygame.display.set_mode((width, height))

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
 
#create the window, displays splash screen on click starts the main menu 
def splash():
    while True:
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()
        #add splash screen 
        splash = addImage('images/splashScreen.jpg', 1, window_surface, width/2, height/2)
        #quit when mouse is clocked
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if splash.get_rect().collidepoint(mousePos):
                    openMainMenu()
        pygame.display.update()

#run the program
splash()