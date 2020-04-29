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

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Aizawa Card <3')

clock = pygame.time.Clock()
done = False
cardImg = pygame.image.load('card.png')


# this will eventually become ze card class
def card(x, y):
    win.blit(cardImg, (x, y))


x = (SCREEN_WIDTH * 0.04)
y = (SCREEN_HEIGHT * 0.04)

x_change = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        ############################
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
        ######################
    ##
    x += x_change

    win.fill(BLACK)
    card(x, y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()


##################
