import pygame
import pygame_gui
from Button import Button
def createNotebook(notebook):
    d = 50
    width = notebook.getWidth()
    height = notebook.getHeight()
    ##xPos = [((width*2)/12),((width*5)/12),((width*8)/12)]
    ##yPos = [((height*9)/d),((height*13)/d),((height*20)/d),((height*24)/d),((height*28)/d),((height*35)/d),((height*39)/d)]

    xPos = [58, 170, 280]
    yPos = [125, 150, 250, 275, 300, 403, 427]
    
    for x in xPos:
            for y in yPos: 
                buttX = x
                buttY = y
                buttW = 20
                buttH = 20
                button = Button(" ", notebook.getManager(), buttX, buttY, buttW, buttH, container=notebook.getPanel(), object_id="checkBoxes")
    return button