#import needed libraries 
import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
import pygame_gui
from cLobby import CLobby
from network import Network
from notebook import createNotebook

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
    #hostButton.fill(manager.ui_theme.get_colour('pinkMF'))
    
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
                return startNewGame()
                
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #when join button is pressed starts the game list by calling the function
                return startGameList()
    
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
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    
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
                 return openMainMenu()

            if ((((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == startButton) or (event.type == pygame.KEYDOWN and event.key == K_RETURN)) and gameName.get_text() != "")):
                print(netConn.send("lobby.new:"+gameName.get_text()))
                return gameBoard(gameName.get_text(), userId)
                
            manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
        pygame.display.update()
        
#starts game selectin list
def startGameList():
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    
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
    
    #button location and initilization
    joinButtonX = width/2-width/20
    joinButtonY = height/2
    joinButtonW = width/10
    joinButtonH = height/20
    joinButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((joinButtonX, joinButtonY), (joinButtonW, joinButtonH)), text='Join Game', manager=manager)
    
    #button location and initilization
    refreshButtonX = width/2-width/20
    refreshButtonY = height/2+height/20
    refreshButtonW = width/10
    refreshButtonH = height/20
    refreshButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((refreshButtonX, refreshButtonY), (refreshButtonW, refreshButtonH)), text='Refresh', manager=manager)
    
    #button location and initilization
    backButtonX = width/2-width/20
    backButtonY = height/2+height/10
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
            
            #events for join button
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == joinButton):
                #send gameSelectList.get_single_selection() to server, make connection to the game lobby
                #if game list selection isn't valid refresh the list
                if not gameSelectList.get_single_selection():
                    return startGameList()
                #if it does not throw an error make a game of this name
                else:
                    gameName = gameSelectList.get_single_selection().split(' ')[0]
                    
                joinResponse = netConn.send("lobby.join:"+gameName)
                
                action = joinResponse.split(":")
                command = action[2].split(".")
            
                #if success start game
                if command[1] == "success":
                     gameBoard(gameName, userId)
                     
                #otherwise refresh the lobby list 
                else:
                   return startGameList()
            
            #events for refresh button 
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == refreshButton)):
                return startGameList()
            
            #events for back button
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
                return openMainMenu()
            
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
    width=1600
    height=900
    #pygame surface
    window_surface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height),'./ourTheme.json')
    
    panelManager= pygame_gui.UIManager((width, height),'./panelTheme.json')
    
    #managers used to set color 
    rdyManager = pygame_gui.UIManager((width, height),'./rdyTheme.json')
    
    #bool variable shows if the player is ready or not
    rdyFlag = True
    handFlag = True
    notebookFlag = True
    
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    gameBoard = addImage('./images/board.png', 1, background, width/2, height/2, width, height)

    #button that tells the server wether or not the user is ready and displays visuals to the user 
    readyButtonX = width/17
    readyButtonY = height/2
    readyButtonW = width/10
    readyButtonH = height/20
    readyButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((readyButtonX, readyButtonY), (readyButtonW, readyButtonH)), text='Not Ready', manager=rdyManager)

    #button that opens the hand 
    handButtonX = (width*16)/17-(width/10)
    handButtonY = height/2
    handButtonW = width/10
    handButtonH = height/20
    handButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((handButtonX, handButtonY), (handButtonW, handButtonH)), text='Hand', manager=manager)

    #button that opens the notebook 
    notebookButtonX = (width*16)/17-(width/10)
    notebookButtonY = height/2+height/20
    notebookButtonW = width/10
    notebookButtonH = height/20
    notebookButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((notebookButtonX, notebookButtonY), (notebookButtonW, notebookButtonH)), text='Notebook', manager=manager)
    
    #button that sends the user back to the main menu
    backButtonX = width/17
    backButtonY = height/2+height/20
    backButtonW = width/10
    backButtonH = height/20
    backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((backButtonX, backButtonY), (backButtonW, backButtonH)), text='Back', manager=manager)
    
    #initilization of the notebook panel
    notebookX = width
    notebookY = height/8
    notebookW = width/4
    notebookH = (3*height)/4
    notebook = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((notebookX, notebookY), (notebookW, notebookH)), starting_layer_height = 1, manager = panelManager)
    notePadImage = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 0), (notebookW, notebookH)), image_surface = pygame.image.load('./images/clueNotepad.png') , manager= panelManager, container = notebook.get_container())
    buttonsList = createNotebook(notebook, panelManager, notebookW, notebookH)
    #list that holds integers used to determine what should be displayed in each button
    buttonFlags = [0]*21
    
    #initilization of the hand panel
    handX = width
    handY = height/3
    handW = width/2
    handH = height/3
    hand = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((handX, handY), (handW, handH)), starting_layer_height = 1, manager = panelManager)
    
    
    player.game=gameName
    player.id=id
    print(player.id)
    print(player.game)

    clock = pygame.time.Clock()           
    while True:
        time_delta = clock.tick(60)/1000.0 
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()  
        
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                pygame.quit()
                sys.exit()
                
            #events for ready button
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == readyButton)):
                #if player presses the ready button 
                netConn.send("lobby.ready")
                #change color from red to green and back when button is pushed
                 
                if rdyFlag:
                    readyButton.select()
                    readyButton.set_text("Ready")
                else:
                    readyButton.unselect()
                    readyButton.set_text("Not Ready")
                rdyFlag = not rdyFlag
            
            #opens the notebook 
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == notebookButton)):
                if notebookX == width:
                    notebookButton.select()
                    notebookX= (width*3)/8   
                    handX = width
                    handButton.unselect()
                else: 
                    notebookX = width
                notebook.set_relative_position((notebookX,notebookY))
                hand.set_relative_position((handX,handY))
                
            buttonCounter = 0
            #goes through list of buttons and checks events for each button
            for button in buttonsList:
                #first time button is pressed select it and set text to X
                #"closes" the hand if it is open
                if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button)):
                    if buttonFlags[buttonCounter] == 0:
                        button.select()
                        button.set_text("X")
                        buttonFlags[buttonCounter]=1
                    #second button press set text to O
                    elif buttonFlags[buttonCounter] == 1:
                        button.select()
                        button.set_text(u'\u2713')
                        buttonFlags[buttonCounter]=2
                    #finally return button to original state
                    elif buttonFlags[buttonCounter] == 2:
                        button.set_text(" ")
                        buttonFlags[buttonCounter]=0
                buttonCounter=buttonCounter+1
                        
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == handButton)):
                #defines the notebook, image and close button 
                #"closes" the notebook if it is open
                if handX == width:
                    handButton.select()
                    handX= width/4   
                    notebookX = width
                    notebookButton.unselect()
                else: 
                    handX = width
                hand.set_relative_position((handX,handY))
                notebook.set_relative_position((notebookX,notebookY))
          
            #events for back button    
            if ((event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == backButton) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE)):
               width=1000
               height=1000
               netConn.send("lobby.leave")
               return openMainMenu()
            
            manager.process_events(event)
            manager.update(time_delta)
            rdyManager.process_events(event)
            rdyManager.update(time_delta)
            panelManager.process_events(event)
            panelManager.update(time_delta)
           
            window_surface.blit(background, (0, 0))
            #window_surface.blit(notebookSurface, (0, 0))
            rdyManager.draw_ui(window_surface)
            manager.draw_ui(window_surface)
            panelManager.draw_ui(window_surface)
            
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

