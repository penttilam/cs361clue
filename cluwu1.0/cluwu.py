import pygame
import pygame_gui
import time
# import sys; sys.path.insert(0, "..")
from pygame.locals import *
from pygame import surface
from cPlayer import CPlayer
from cLobby import CLobby
from network import Network
from notebook import createNotebook
# from GameTile import GameTile
from Button import Button

#what does all this do?
KEYDOWN = 2
K_ESCAPE = 27
K_RETURN = 13
USEREVENT = 24
QUIT = 12
MOUSEBUTTONDOWN = 5

#was there a reason clock was here?

#runs main menu
def OpenMainMenu():
    #pygame surface
    windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')

    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    menuLabelX = int(width/2-width/20)
    menuLabelY = int(height/2-height/5)
    menuLabelW = int(width/10)
    menuLabelH = int(height/10)
    pygame_gui.elements.ui_label.UILabel(pygame.Rect((menuLabelX, menuLabelY), (menuLabelW, menuLabelH)), text="Main Menu", manager=manager)

    hostButtonX = int(width/2-width/20)
    hostButtonY = int(height/2-height/10)
    hostButtonW = int(width/10)
    hostButtonH = int(height/20)
    # Host button
    Button(hostButtonX, hostButtonY, hostButtonW, hostButtonH, 'Host', manager)
    #hostButton.fill(manager.ui_theme.get_colour('pinkMF'))

    joinButtonX = int(width/2-width/20)
    joinButtonY = int(height/2-height/20)
    joinButtonW = int(width/10)
    joinButtonH = int(height/20)
    # Join button
    Button(joinButtonX, joinButtonY, joinButtonW, joinButtonH, 'Join', manager)

    quitButtonX = int(width/2-width/20)
    quitButtonY = int(height/2)
    quitButtonW = int(width/10)
    quitButtonH = int(height/20)
    quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((quitButtonX, quitButtonY), (quitButtonW, quitButtonH)), text='Quit', manager=manager)

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                print(event.type)
                netConn.send("quit")
                raise SystemExit

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.text == "Host"):
                #when host is pressed starts the game list by calling the function
                print(event.type)
                return hostGame()

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.text == "Join"):
                #when join button is pressed starts the game list by calling the function
                print(event.type)
                return startGameList()

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == quitButton):
                netConn.send("quit")
                raise SystemExit

            manager.process_events(event)
            manager.update(time_delta)
            windowSurface.blit(background, (0, 0))
            manager.draw_ui(windowSurface)
        pygame.display.update()

#starts new game
def hostGame():
    #pygame surface
    # windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')

    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    gameNameLabelX = int(width/2-width/10)
    gameNameLabelY = int(height/2-height/5)
    gameNameLabelW = int(width/5)
    gameNameLabelH = int(height/20)
    pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((gameNameLabelX, gameNameLabelY), (gameNameLabelW, gameNameLabelH)), text="Enter name for your game", manager=manager)

    gameNameTextBoxX = int(width/2-width/10)
    gameNameTextBoxY = int(height/2-width/6)
    gameNameTextBoxW = int(width/5)
    gameNameTextBoxH = int(height/20)
    gameName = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((gameNameTextBoxX, gameNameTextBoxY), (gameNameTextBoxW, gameNameTextBoxH)), manager=manager)

    startButtonX = int(width/2-width/20)
    startButtonY = int(height/2-height/10)
    startButtonW = int(width/10)
    startButtonH = int(height/20)
    # startButton
    Button(startButtonX, startButtonY, startButtonW, startButtonH, "Start Game", manager)

    backButtonX = int(width/2-width/20)
    backButtonY = int(height/2-height/20)
    backButtonW = int(width/10)
    backButtonH = int(height/20)
    # back button
    Button(backButtonX, backButtonY, backButtonW, backButtonH, "Back", manager)
    #pygame_gui.elements.UIButton(relative_rect=pygame.Rect((backButtonX, backButtonY), (backButtonW, backButtonH)), text='Back', manager=manager)

    # Tile1 = GameTile(width/2, height/2, 50, 50, 0)

    while True:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.text == "Back") or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return OpenMainMenu()

            if (((event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.text == "Start Game") or (event.type == KEYDOWN and event.key == K_RETURN)) and gameName.get_text() != ""):
                print(netConn.send("lobby.new:"+gameName.get_text()))
                return startLobby(gameName.get_text(), userId)

            manager.process_events(event)
            manager.update(time_delta)
            windowSurface.blit(background, (0, 0))
            manager.draw_ui(windowSurface)
        pygame.display.update()

#starts game list selection
def startGameList():
    #pygame surface
    # windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')

    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    gameSelectListX = width/2-width/10
    gameSelectListY = height/2-height/5
    gameSelectListW = width/5
    gameSelectListH = height/5
    netConn.send("lobby.lobbies")

    gameSelectListActiveGamesList = netConn.catch()

    lobbyList = []

    print(gameSelectListActiveGamesList)
    for cLobbies in gameSelectListActiveGamesList:
        lobbyList.append(str(cLobbies.getId())+" "+str(cLobbies.getPNumber())+ " players")

    gameSelectList = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((gameSelectListX, gameSelectListY), (gameSelectListW, gameSelectListH)), item_list=lobbyList, manager=manager)

    #button location and initilization
    joinButtonX = int(width/2-width/20)
    joinButtonY = int(height/2)
    joinButtonW = int(width/10)
    joinButtonH = int(height/20)
    # Join Game button
    joinButton = Button(joinButtonX, joinButtonY, joinButtonW, joinButtonH, 'Join Game', manager)

    #button location and initilization
    refreshButtonX = int(width/2-width/20)
    refreshButtonY = int(height/2+height/20)
    refreshButtonW = int(width/10)
    refreshButtonH = int(height/20)
    # Refresh button
    refreshButton = Button(refreshButtonX, refreshButtonY, refreshButtonW, refreshButtonH, 'Refresh', manager)

    #button location and initilization
    backButtonX = int(width/2-width/20)
    backButtonY = int(height/2+height/10)
    backButtonW = int(width/10)
    backButtonH = int(height/20)
    # Back button
    backButton = Button(backButtonX, backButtonY, backButtonW, backButtonH, 'Back', manager)

    while True:
        time_delta = clock.tick(60)/1000.0
        # Track the mouse movement
        # mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            #events for join button
            if joinButton.event(event):
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
                    startLobby(gameName, userId)
                #otherwise refresh the lobby list
                else:
                    return startGameList()

            #events for refresh button
            if refreshButton.event(event):
                return startGameList()

            #events for back button
            if backButton.event(event):
                return OpenMainMenu()

            manager.process_events(event)
            manager.update(time_delta)
            windowSurface.blit(background, (0, 0))
            
        pygame.display.update()

class Player:
    def __init__(self):
        self.id = "newPlayer"
        self.character = ""
        self.active = 0
        self.rolled = 0
        self.cards = ["", "", ""]
        self.game = ""

player = Player()

def startLobby(gameName, userId):
    width = 1600
    height = 900
    #pygame surface
    windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    #managers used to set color
    rdyManager = pygame_gui.UIManager((width, height), './rdyTheme.json')
    notRdyManager = pygame_gui.UIManager((width, height), './notRdyTheme.json')
    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    # gameBoard = 
    addImage('./images/board.png', 1, background, width/2, height/2, width, height)
    
    #button that starts the game when all players are ready, NOT visible to peons
    startButtonX = int(width)
    startButtonY = int(height/2-height/20)
    startButtonW = int(width/10)
    startButtonH = int(height/20)
    # Start button
    startButton = Button(startButtonX, startButtonY, startButtonW, startButtonH, 'Start Game', manager)

    #button that tells the server wether or not the user is ready and displays visuals to the user
    readyButtonX = int(width/17)
    readyButtonY = int(height/2)
    readyButtonW = int(width/10)
    readyButtonH = int(height/20)
    # Ready button
    readyButton = Button(readyButtonX, readyButtonY, readyButtonW, readyButtonH, 'Not Ready', notRdyManager)
    
    #button that sends the user back to the main menu
    backButtonX = int(width/17)
    backButtonY = int(height/2+height/20)
    backButtonW = int(width/10)
    backButtonH = int(height/20)
    # Back button
    backButton = Button(backButtonX, backButtonY, backButtonW, backButtonH, 'Back', manager)
    
    

    #text box to display player ids and ready status 
    playerStatusX = int((width*16)/17-(width/9))
    playerStatusY = int(height/4)
    playerStatusW = int(width/7)
    playerStatusH = int(height/20)
    netConn.send("lobby.update")
    currentLobbyPlayerStatus = netConn.catch()
    playerStatus = pygame_gui.elements.UITextBox(html_text=currentLobbyPlayerStatus.htmlStringify(), relative_rect = pygame.Rect((playerStatusX, playerStatusY), (playerStatusW, playerStatusH)), manager=manager, wrap_to_height=True, layer_starting_height=1)

    while True:
        time_delta = clock.tick(60) / 1000.0
        #update the text box to let players know who is ready etc...
        tmp = currentLobbyPlayerStatus
        netConn.send("lobby.update")
        currentLobbyPlayerStatus = netConn.catch()
        #if player number changes kill the text box and create a new one with updated information.

        if not currentLobbyPlayerStatus == tmp:
            playerStatus.kill()
            playerStatus = pygame_gui.elements.UITextBox(html_text=currentLobbyPlayerStatus.htmlStringify() ,relative_rect = pygame.Rect((playerStatusX, playerStatusY), (playerStatusW, playerStatusH)), manager=manager, wrap_to_height=True, layer_starting_height=1)

        if currentLobbyPlayerStatus.getPList()[0].getId() == netConn.getId():
            startButtonX = int(width/17)
            startButton.setX(startButtonX)
            if currentLobbyPlayerStatus.getLReady():
                startButton.enable()
            else:
                startButton.disable()

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            if startButton.event(event):
                gameBoard(gameName, userId)
            #events for ready button
            if readyButton.event(event):
                #if player presses the ready button
                netConn.send("lobby.ready")
                # netConn.send("lobby.passCards")
                #change color from red to green and back when button is pushed
                if readyButton.getText() == "Not Ready":
                    readyButton.setManager(rdyManager)
                    readyButton.setText("Ready")
                else:
                    readyButton.setManager(notRdyManager)
                    readyButton.setText("Not Ready")
            if backButton.event(event):
                    width = 1000
                    height = 1000
                    netConn.send("lobby.leave")
                    return OpenMainMenu()

            manager.process_events(event)
            manager.update(time_delta)
            rdyManager.process_events(event)
            rdyManager.update(time_delta)
            notRdyManager.process_events(event)
            notRdyManager.update(time_delta)
            windowSurface.blit(background, (0, 0))
            rdyManager.draw_ui(windowSurface)
            notRdyManager.draw_ui(windowSurface)
            manager.draw_ui(windowSurface)
        
        #netConn.send("lobby.update")
        pygame.display.update()

def gameBoard(gameName, userId):
    width = 1600
    height = 900
    #pygame surface
    windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')

    panelManager = pygame_gui.UIManager((width, height), './panelTheme.json')
    tileManager = pygame_gui.UIManager((width, height), './tileTheme.json')
    #managers used to set color
    rdyManager = pygame_gui.UIManager((width, height), './rdyTheme.json')

    background = pygame.Surface((width, height))
    background.fill(manager.ui_theme.get_colour('dark_bg'))
    # gameBoard = 
    addImage('./images/board.png', 1, background, width/2, height/2, width, height)

    # Tile buttonnnnnnns
    # for x in range(60):
    #     for y in range(30):
    #         tileButtonX = 15+int((width/60)*(x))
    #         tileButtonY = int(((height*y)/30))
    #         tileButtonW = 30
    #         tileButtonH = 15
    #         tileButton = []
    #         tileButton.append(Button(tileButtonX, tileButtonY, tileButtonW, tileButtonH, "", tileManager))


    #button that opens the hand
    handButtonX = int((width*16)/17-(width/10))
    handButtonY = int(height/2)
    handButtonW = int(width/10)
    handButtonH = int(height/20)
    handButton = Button(handButtonX, handButtonY, handButtonW, handButtonH, 'Hand', manager)

    #button that opens the notebook
    notebookButtonX = int((width*16)/17-(width/10))
    notebookButtonY = int(height/2+height/20)
    notebookButtonW = int(width/10)
    notebookButtonH = int(height/20)
    notebookButton = Button(notebookButtonX, notebookButtonY, notebookButtonW, notebookButtonH, 'Notebook', manager)

    #initilization of the notebook panel
    notebookX = int(width)
    notebookY = int(height/8)
    notebookW = int(width/4)
    notebookH = int((3*height)/4)
    notebook = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((notebookX, notebookY), (notebookW, notebookH)), starting_layer_height=1, manager=panelManager)
    # notePadImage =
    pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 0), (notebookW, notebookH)), image_surface=pygame.image.load('./images/clueNotepad.png'), manager=panelManager, container=notebook.get_container())
    createNotebook(notebook, panelManager, notebookW, notebookH)
    #list that holds integers used to determine what should be displayed in each button

    #initilization of the hand panel
    handX = int(width)
    handY = int(height/3)
    handW = int(width/2)
    handH = int(height/3)
    hand = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((handX, handY), (handW, handH)), starting_layer_height=1, manager=panelManager)
    pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 0), (handW, handH)), image_surface=pygame.image.load('./images/character.png'), manager=panelManager, container=hand.get_container())
    
    player.game = gameName
    player.id = userId
    print(player.id)
    print(player.game)

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            
            # for butt in tileButton:
            #     if butt.event(event):
            #         print(butt.getXY())
            #opens the notebook
            if notebookButton.event(event):
                if notebookX == width:
                    notebookButton.select()
                    notebookX = (width*3)/8
                    handX = width
                    handButton.unselect()
                else:
                    notebookX = width
                notebook.set_relative_position((notebookX, notebookY))
                hand.set_relative_position((handX, handY))

            #Cycles checkboxes between blank, X, and checked
            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.object_ids == [None, 'checkBoxes']):
                if event.ui_element.text == " ":
                    event.ui_element.set_text("X")
                elif event.ui_element.text == "X":
                    event.ui_element.set_text(u'\u2713')
                elif event.ui_element.text == u'\u2713':
                    event.ui_element.set_text(" ")
            
            if handButton.event(event):
                #defines the notebook, image and close button
                #"closes" the notebook if it is open
                if handX == width:
                    handButton.select()
                    handX = width/4
                    notebookX = width
                    notebookButton.unselect()
                else:
                    handX = width
                hand.set_relative_position((handX, handY))
                notebook.set_relative_position((notebookX, notebookY))
            manager.process_events(event)
            manager.update(time_delta)
            rdyManager.process_events(event)
            rdyManager.update(time_delta)
            panelManager.process_events(event)
            panelManager.update(time_delta)
            tileManager.update(time_delta)
            tileManager.process_events(event)
            manager.draw_ui(windowSurface)
            windowSurface.blit(background, (0, 0))
            rdyManager.draw_ui(windowSurface)
            
            manager.draw_ui(windowSurface)
            panelManager.draw_ui(windowSurface)
            tileManager.draw_ui(windowSurface)

        pygame.display.update()

#function takes
#text as a string
#font is the font defined
#color is your choice of color
#location int
#on the screen object you are adding this to
# x and y locations, integer pixel positions
#locations can be updated in the future to add other alignments,center, left right etc....
def addImage(img, location, on, x, y, xRes, yRes):
    imgObj = pygame.image.load(img)
    imgObj = pygame.transform.scale(imgObj, (xRes, yRes))
    imgRect = imgObj.get_rect()
    if location == 1:
        imgRect.center = (int(x), int(y))
    on.blit(imgObj, imgRect)
    return imgObj

#create the window, displays splash screen on click starts the main menu
def splash():
    while True:
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()
        #add splash screen
        splash = addImage('images/splashScreen.jpg', 1, windowSurface, width/2, height/2, width, height)
        #quit when mouse is clocked

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            if event.type == MOUSEBUTTONDOWN:
                if splash.get_rect().collidepoint(mousePos):
                    OpenMainMenu()
        pygame.display.update()

#initialize game screen
pygame.init()

pygame.display.set_caption('cluwu')
#set the icon
icon = pygame.image.load('images/cluwuIcon.png')
pygame.display.set_icon(icon)

#set up network connection
netConn = Network()
userId = netConn.getId()

#screen set up
width = 1000
height = 1000

#create pygame area to add splash image to
windowSurface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#run the program
splash()