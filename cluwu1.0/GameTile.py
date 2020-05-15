import pygame
import pygame_gui

class GameTile:
    def __init__(self, xLoc, yLoc, width, height, occupied):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.occupied = occupied
        self.w = width
        self.h = height
        manager = pygame_gui.UIManager((self.w, self.h), './tileTheme.json')
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.xLoc, self.yLoc), (self.w, self.h)), text="", manager=manager)

    def getXLoc(self):
        return self.xLoc
    def getYLoc(self):
        return self.yLoc
    def getOccupant(self):
        return self.occupied