import sys, pygame
from pygame.locals import *
import pygame_textinput

pygame.init()

black = 0, 0, 0
white = 255, 255, 255
class Background:
    def __init__(self, image):
        self.img = image
        self.rect = image.get_rect()

class Button:
    def __init__(self, image, position):
        #position determines where in the button display order the button appears
        self.img = image
        self.rect = image.get_rect()
        self.position = position

def MainMenu():
   while True:
    # used to calculate where to put buttons, centered on screen
    numButtons = 2
    
    # Track the mouse movement
    mouseX, mouseY = pygame.mouse.get_pos()


    # Make window size of splash screen graphic
    splashScreen = Background(pygame.image.load("Splash_Screen.jpg"))
    size = width, height = splashScreen.img.get_width(), splashScreen.img.get_height()
    screen = pygame.display.set_mode(size)
    screen.fill(white)

    # Populate displayInfo with... display info... extra comment is extra
    displayInfo = pygame.display.Info() 
        
    # Center splash screen
    splashScreenRect = splashScreen.img.get_rect(center=(displayInfo.current_w / 2, (displayInfo.current_h / 2)))

    #Make buttons
    buttonJoin = Button(pygame.image.load("join_button.png"),0)
    buttonQuit = Button(pygame.image.load("quit_button.png"),1)

    buttonJoin.rect = buttonJoin.img.get_rect(center=(displayInfo.current_w / 2, (displayInfo.current_h / numButtons - buttonJoin.img.get_height()) + buttonJoin.img.get_height() * buttonJoin.position))
    buttonQuit.rect = buttonQuit.img.get_rect(center=(displayInfo.current_w / 2, (displayInfo.current_h / numButtons - buttonQuit.img.get_height()) + buttonQuit.img.get_height() * buttonQuit.position))

    # Draw surfaces to screen
    screen.blit(splashScreen.img, splashScreenRect)
    screen.blit(buttonJoin.img, buttonJoin.rect)
    screen.blit(buttonQuit.img, buttonQuit.rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if buttonJoin.rect.collidepoint((mouseX, mouseY)):
                lobby()
            if buttonQuit.rect.collidepoint((mouseX, mouseY)):
                pygame.quit()
                sys.exit()

def lobby():
    
    # Track the mouse movement
    textInput = pygame_textinput.TextInput()
    
    clock = pygame.time.Clock()

    # Make window size of lobby graphic
    lobbyScreen = Background(pygame.image.load("lobby_background.png"))
    size = width, height = lobbyScreen.img.get_width(), lobbyScreen.img.get_height()
    screen = pygame.display.set_mode(size)
    
    screen.fill(white)
    screen.blit(lobbyScreen.img, lobbyScreen.rect)

    while True:
        screen.blit(lobbyScreen.img, lobbyScreen.rect)
        events = pygame.event.get()    
        
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        
        
        # if textInput.update(events):
            # print(textInput.get_text())
        textInput.update(events)
        screen.blit(textInput.get_surface(),(lobbyScreen.rect.left + 12, lobbyScreen.rect.bottom - 32))
        pygame.display.update()
        clock.tick(30)



MainMenu()

