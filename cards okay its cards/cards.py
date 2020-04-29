import pygame as pygame
import sys
from pygame.locals import *

# UWU SCREEN RES

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# UWU COLORZ ???
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# run it bitch

pygame.init()

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Aizawa Card <3')

clock = pygame.time.Clock()
done = False
cardImg = pygame.image.load('card.png')


def card(x,y):
    gameDisplay.blit(cardImg, (x,y))


x = (SCREEN_WIDTH * 0.04)
y = (SCREEN_HEIGHT * 0.04)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    gameDisplay.fill(BLACK)
    card(x,y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
