import pygame
import pygame_gui
from pygame.locals import *

class Panel:
    def __init__(self, manager, xLoc=0, yLoc=0, width=0, height=0, layerHeight=1, container="", object_id=""):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.width = width
        self.height = height
        self.layerHeight = layerHeight
        self.container = container
        self.manager = manager
        self.object_ids = object_id
        self.images = []
        self.newPanel()
                
    def newPanel(self):
        if (self.container == ""):
            self.panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), starting_layer_height=self.layerHeight, manager=self.manager)
        else:
            self.panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.width, self.height)), starting_layer_height=self.layerHeight, manager=self.manager, container=self.container)
 
    def setObjectId(self, objectId=""):
        self.panel.kill()
        if self.object_ids == "" and objectId == "":
            self.object_ids = str(self.xLoc)+str(self.yLoc)+str(self.width)
        elif objectId != "":
            self.object_ids = objectId
        self.newPanel()

    def addImage(self, imageObject):
        self.images.append(imageObject)

    def getText(self):
        return self.text
    def getXLocYLoc(self):
        return (self.xLoc, self.yLoc)
    def getXLoc(self):
        return self.xLoc
    def getYLoc(self):
        return self.yLoc
    def getContainer(self):
        return self.panel.get_container()
    def getPanel(self):
        return self.panel
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height

    def setXLoc(self,xLoc):
        self.xLoc = xLoc
        self.panel.set_relative_position((self.xLoc, self.yLoc))

    def setYLoc(self,yLoc):
        self.yLoc = yLoc
        self.panel.set_relative_position((self.xLoc, self.yLoc))
    
    def setXLocYLoc(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.panel.set_relative_position((self.xLoc, self.yLoc))

    def setText(self, text):
        self.text = text
        self.panel.set_text(self.text)

    def setWidth(self, width):
        self.width = width
        self.setObjectId()
 
    def setHeight(self, height):
        self.height = height
        self.setObjectId()

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height
        self.setObjectId()

    def enable(self):
        self.panel.enable()

    def disable(self):
        self.panel.disable()

    def select(self):
        self.panel.select()
    
    def update(self, time_delta):
        self.panel.update(time_delta)

    def unselect(self):
        self.panel.unselect()

    def setManager(self, newManager):
        self.panel.kill()
        self.manager = newManager
        self.newPanel()

    # def getClickedStatus(self, event):
    #     if (event.type == MOUSEBUTTONDOWN):
    #         return event.ui_element.object_ids == self.panel.object_ids

    def kill(self):
        self.panel.kill()