import pygame
from clueNetwork import Network
import cluwu_interface_testing.py

## runs the main program
def main():
    run = True
    n = Network()

    while run:
       pass

    for event in pygame.even.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

main()











