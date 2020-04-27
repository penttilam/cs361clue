#import libraries 
import pygame
from pygame.locals import *
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

player = Player()

def gameBoard(gameName, id):
    player.game=gameName
    player.id=id
    print(player.id)
    print(player.game)


