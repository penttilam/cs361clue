import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui

def createNotebook(notebook, panelManager, width, height):
    d=50
    xPos = [((width*2)/12),((width*5)/12),((width*8)/12)]
    yPos = [((height*9)/d),((height*13)/d),((height*20)/d),((height*24)/d),((height*28)/d),((height*35)/d),((height*39)/d)]
    buttonsList = []
    
    for x in xPos:
            for y in yPos: 
                notebookButtonsX = x
                notebookButtonsY = y
                notebookButtonsW = 20
                notebookButtonsH = 20
                buttonsList.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((notebookButtonsX, notebookButtonsY), (notebookButtonsW, notebookButtonsH)), text=' ', manager=panelManager, container = notebook))
    return buttonsList   
    