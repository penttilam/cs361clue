import pygame
import pygame_gui
from Button import Button
def createNotebook(notebook):
    d = 50
    width = notebook.getWidth()
    height = notebook.getHeight()
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