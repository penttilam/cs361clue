#import needed libraries 
import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui
from cLobby import CLobby
from network import Network

#runs main menu
def openMainMenu():
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    
    menuLabelX = width/2-width/20
    menuLabelY = height/2-height/5
    menuLabelW = width/10
    menuLabelH = height/10
    pygame_gui.elements.ui_label.UILabel(pygame.Rect((menuLabelX, menuLabelY), (menuLabelW, menuLabelH)),text="Main Menu", manager=manager)
    
    hostButtonX = width/2-width/20
    hostButtonY = height/2-height/10
    hostButtonW = width/10
    hostButtonH = height/20
    hostButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((hostButtonX, hostButtonY), (hostButtonW, hostButtonH)), text='Host', manager=manager)
    
    joinButtonX = width/2-width/20
    joinButtonY = height/2-height/20
    joinButtonW = width/10
    joinButtonH = height/20
    joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((joinButtonX, joinButtonY), (joinButtonW, joinButtonH)), text='Join', manager=manager)
    
    quitButtonX = width/2-width/20
    quitButtonY = height/2
    quitButtonW = width/10
    quitButtonH = height/20
    quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((quitButtonX, quitButtonY), (quitButtonW, quitButtonH)), text='Quit', manager=manager)

    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                netConn.send("quit")
                pygame.quit()
                sys.exit()
    
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hostButton):
                #when host is pressed starts the game list by calling the function
                startNewGame()
                
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #when join button is pressed starts the game list by calling the function
                startGameList()
    
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == quitButton):
                 netConn.send("quit")
                 pygame.quit()
                 sys.exit()
    
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()

#starts new game
def startNewGame():
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height))
    
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    
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

    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                pygame.quit()
                sys.exit()
            
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
                 return

            if ((((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == startButton) or (event.type == pygame.KEYDOWN and event.key == K_RETURN)) and gameName.get_text() != "")):
                gameBoard(gameName.get_text(), userId)
                
                
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()
        
#starts game list selection
def startGameList():
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height))
    
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    # background.fill(white)
    
    gameSelectListX = width/2-width/10
    gameSelectListY = height/2-height/5
    gameSelectListW = width/5
    gameSelectListH = height/5
    netConn.send("lobby.lobbies")
    
    gameSelectListActiveGamesList=netConn.catch()
    
    lobbyList = []
    
    print(gameSelectListActiveGamesList)
    for cLobbies in gameSelectListActiveGamesList:
        lobbyList.append(str(cLobbies.getId())+" "+str(cLobbies.getPNumber())+ " players")
    
    gameSelectList = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((gameSelectListX, gameSelectListY), (gameSelectListW, gameSelectListH)), item_list=lobbyList, manager=manager)
    
    joinButtonX = width/2-width/20
    joinButtonY = height/2
    joinButtonW = width/10
    joinButtonH = height/20
    joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((joinButtonX, joinButtonY), (joinButtonW, joinButtonH)), text='Join Game', manager=manager)
    
    backButtonX = width/2-width/20
    backButtonY = height/2+height/20
    backButtonW = width/10
    backButtonH = height/20
    backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((backButtonX, backButtonY), (backButtonW, backButtonH)), text='Back', manager=manager)
    
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
                netConn.send("quit")
                pygame.quit()
                sys.exit()

            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #send gameSelectList.get_single_selection() to server, make connection to the game lobby
                print("Selected game: " + gameSelectList.get_single_selection())      
            
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
                return
            
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()        
 
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
    print(netConn.send("lobby.new:"+gameName))
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height))
    
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    gameBoard = addImage('images/board.jpg', 1, background, width/2, height/2, width, height)

    # background.fill(white)
    
    player.game=gameName
    player.id=id
    print(player.id)
    print(player.game)
    
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
                netConn.send("quit")
                pygame.quit()
                sys.exit()
            
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()
       
#initialize game screen 
pygame.init()

pygame.display.set_caption('cluwu')
#set the icon
icon = pygame.image.load('images/cluwuIcon.png')
pygame.display.set_icon(icon)

#colors
black = 0, 0, 0
white = 255, 255, 255

#set up network connection
netConn = Network()
userId = netConn.getId()

#screen set up
width = 1000
height = 1000

#set the font
#set font for text in program and text size
title = pygame.font.SysFont(None, int(height/20))
font = pygame.font.SysFont(None, int(height/40))

#create pygame area to add splash image to
window_surface = pygame.display.set_mode((width, height))

#function takes
#text as a string
#font is the font defined
#color is your choice of color
#location int 
#surface the screen object you are adding this to
# x and y locations, integer pixel positions
#locations can be updated in the future to add other alignments,center, left right etc.... 
def addImage(img, location, surface, x, y, xRes, yRes):
    imgObj=pygame.image.load(img)
    imgObj = pygame.transform.scale(imgObj, (xRes,yRes))
    imgRect = imgObj.get_rect()
    if location == 1:
       imgRect.center = (int(x), int(y))
    surface.blit(imgObj, imgRect)
    return imgObj
 
#create the window, displays splash screen on click starts the main menu 
def splash():
    while True:
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()
        #add splash screen 
        splash = addImage('images/splashScreen.jpg', 1, window_surface, width/2, height/2, width, height)
        #quit when mouse is clocked
        
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if splash.get_rect().collidepoint(mousePos):
                    openMainMenu()
        pygame.display.update()

#run the program
splash()

