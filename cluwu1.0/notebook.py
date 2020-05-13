import pygame
import pygame_gui

def createNotebook(notebook, panelManager, width, height):
    d = 50
    xPos = [((width*2)/12),((width*5)/12),((width*8)/12)]
    yPos = [((height*9)/d),((height*13)/d),((height*20)/d),((height*24)/d),((height*28)/d),((height*35)/d),((height*39)/d)]
    
    for x in xPos:
            for y in yPos: 
                buttX = x
                buttY = y
                buttW = 20
                buttH = 20
                pygame_gui.elements.UIButton(relative_rect=pygame.Rect((buttX, buttY), (buttW, buttH)), text=' ', manager=panelManager, container=notebook, object_id="checkBoxes")
    