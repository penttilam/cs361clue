#import libraries 
import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui
from gameBoard import gameBoard

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

gameNameLabelX = width/2-width/10
gameNameLabelY = height/2-height/5
gameNameLabelW = width/5
gameNameLabelH = height/20
pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((gameNameLabelX, gameNameLabelY), (gameNameLabelW, gameNameLabelH)),text="Enter name for your game", manager=manager)

gameNameTextBoxX = width/2-width/10
gameNameTextBoxY = height/2-width/6
gameNameTextBoxW = width/5
gameNameTextBoxH = height/20
gameName = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((gameNameTextBoxX, gameNameTextBoxY), (gameNameTextBoxW, gameNameTextBoxH)), manager=manager)

startButtonX = width/2-width/20
startButtonY = height/2-height/10
startButtonW = width/10
startButtonH = height/20
startButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((startButtonX, startButtonY), (startButtonW, startButtonH)), text='Start Game', manager=manager)

backButtonX = width/2-width/20
backButtonY = height/2-height/20
backButtonW = width/10
backButtonH = height/20
backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((backButtonX, backButtonY), (backButtonW, backButtonH)), text='Back', manager=manager)

def startNewGame():
    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
                 from mainMenu import openMainMenu
                 openMainMenu()

            if ((((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == startButton) or (event.type == pygame.KEYDOWN and event.key == K_RETURN)) and gameName.get_text() != "")):
                #send gameName.get_text() to server, if game name is not is use, reserve name and return id# for user
                #if duplicate name, return "dup" give error message that name exists, exit this section and wait for button again
                #pass gameName.get_text() and server returned id number to 
                userID = 1
                gameBoard(gameName.get_text(), userID)
                print(gameName.get_text())
                
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()