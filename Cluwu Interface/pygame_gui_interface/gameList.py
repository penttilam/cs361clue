#import libraries 
import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui

pygame.init()

#colors
black = 0, 0, 0
white = 255, 255, 255

#screen set up
width = 1000
height = 1000

#pygame surface
window_surface = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width, height), 'data/themes/quick_theme.json')

background = pygame.Surface((width, height))
background.fill(manager.ui_theme.get_colour(None, None, 'dark_bg'))
# background.fill(white)

gameSelectListX = width/2-width/20
gameSelectListY = height/2-height/5
gameSelectListW = width/10
gameSelectListH = height/10
gameSelectListActiveGames = ["test", "test1", "test2"]
gameSelectList = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((gameSelectListX, gameSelectListY), (gameSelectListW, gameSelectListH)), item_list=gameSelectListActiveGames, manager=manager)

joinButtonX = width/2-width/20
joinButtonY = height/2-height/10
joinButtonW = width/10
joinButtonH = height/20
joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((joinButtonX, joinButtonY), (joinButtonW, joinButtonH)), text='Join Game', manager=manager)

backButtonX = width/2-width/20
backButtonY = height/2-height/20
backButtonW = width/10
backButtonH = height/20
backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((backButtonX, backButtonY), (backButtonW, backButtonH)), text='Back', manager=manager)


def startGameList():
    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0 
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()  
        
        #do stuff here
        #do stuff here
        #do stuff here
        #do stuff here
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #send gameSelectList.get_single_selection() to server, make connection to the game lobby
                print("Selected game: " + gameSelectList.get_single_selection())      
            
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
                 from mainMenu import openMainMenu
                 openMainMenu()
            
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()