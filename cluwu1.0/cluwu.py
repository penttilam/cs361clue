import pygame
import pygame_gui
import time
# import sys; sys.path.insert(0, "..")
from pygame.locals import *
from pygame import surface
from clientPlayer import ClientPlayer
from clientLobby import ClientLobby
from clientNetwork import *
from notebook import createNotebook
from Button import Button
from ImageButton import ImageButton
from Image import Image
from Panel import Panel
from GameGrid import GameGrid
from gameBoard import gameBoard

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

    hostButton = Button('Host', manager)
    hostButton.setXLocYLoc(int(width/2-width/20), int(height/2-height/10))
    hostButton.setWidthHeight(int(width/10), int(height/20))
    
    
    joinButton = Button('Join', manager)
    joinButton.setXLocYLoc(int(width/2-width/20), int(height/2-height/20))
    joinButton.setWidthHeight(int(width/10), int(height/20))
    
    
    quitButton = Button("Quit", manager, shortcutKey=K_ESCAPE)
    quitButton.setXLocYLoc(int(width/2-width/20), int(height/2))
    quitButton.setWidthHeight(int(width/10), int(height/20))

    manager.draw_ui(windowSurface)

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                if hostButton.getClickedStatus(event):
                    #when host is pressed starts the game list by calling the function
                    return hostGame()

                if joinButton.getClickedStatus(event):
                    #when join button is pressed starts the game list by calling the function
                    return startGameList()

                if quitButton.getClickedStatus(event):
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
    managerList = []
    windowSurface = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    managerList.append(manager)    

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
    gameName.focus()

    startButton = Button("Start Game", manager, shortcutKey=K_RETURN)
    startButton.setXLocYLoc(int(width/2-width/20), int(height/2-height/10))
    startButton.setWidthHeight(int(width/10), int(height/20))
    
    backButton = Button("Back", manager, shortcutKey=K_ESCAPE)
    backButton.setXLocYLoc(int(width/2-width/20), int(height/2-height/20))
    backButton.setWidthHeight(int(width/10), int(height/20))

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                if backButton.getClickedStatus(event):
                    return OpenMainMenu()

                if startButton.getClickedStatus(event) and gameName.get_text() != "":
                    gameNameCamel = gameName.get_text()
                    if " " in gameName.get_text():
                        gameNameCamel = gameName.get_text().replace(" ", "_")
                    if "." in gameNameCamel:
                        gameNameCamel = gameNameCamel.replace(".", "*")
                    print(netConn.send("lobby.new:"+gameNameCamel))
                    return startLobby(gameName.get_text(), userId)

        # Redraw the background
        windowSurface.blit(background, (0, 0))
        # Update events based on clock ticks
        for each in managerList:
            each.process_events(event)
            each.update(time_delta)
            each.draw_ui(windowSurface)
        pygame.display.update()
        


#starts game list selection
def startGameList():
    #pygame surface
    managerList = []
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    managerList.append(manager)

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
    for clientLobby in gameSelectListActiveGamesList:
        lobbyList.append(str(clientLobby.getId())+" "+str(clientLobby.getNumberOfPlayers())+ " players")

    gameSelectList = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((gameSelectListX, gameSelectListY), (gameSelectListW, gameSelectListH)), item_list=lobbyList, manager=manager)

    # Join Game button
    joinButton = Button('Join Game', manager)
    joinButton.setXLocYLoc(int(width/2-width/20), int(height/2))
    joinButton.setWidthHeight(int(width/10), int(height/20))

    # Refresh button
    refreshButton = Button('Refresh', manager)
    refreshButton.setXLocYLoc(int(width/2-width/20), int(height/2+height/20))
    refreshButton.setWidthHeight(int(width/10), int(height/20))

    # Back button
    backButton = Button('Back', manager, shortcutKey=K_ESCAPE)
    backButton.setXLocYLoc(int(width/2-width/20), int(height/2+height/10))
    backButton.setWidthHeight(int(width/10), int(height/20))

    while True:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                #events for join button
                if joinButton.getClickedStatus(event):
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
                elif refreshButton.getClickedStatus(event):
                    return startGameList()
                
                #events for back button
                elif backButton.getClickedStatus(event):
                    return OpenMainMenu()

            # Redraw the background
            windowSurface.blit(background, (0, 0))

            # Update events based on clock ticks
            for each in managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)
        pygame.display.update()

def startLobby(gameName, userId):
    width = 1680
    height = 900
    
    # List of managers used to set themes
    managerList = []
    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    managerList.append(manager)
    rdyManager = pygame_gui.UIManager((width, height), './rdyTheme.json')
    managerList.append(rdyManager)
    notRdyManager = pygame_gui.UIManager((width, height), './notRdyTheme.json')
    managerList.append(notRdyManager)

    #pygame surface
    windowSurface = pygame.display.set_mode((width, height))
    Image('board.png', manager, 0, 0, width, height)
    
    # Button that starts the game when all players are ready, NOT visible to peons
    startButton = Button('Start Game', manager)
    startButton.setXLocYLoc(int(width), int(height/2-height/20))
    startButton.setWidthHeight(int(width/10), int(height/20))

    # Button that tells the server if player is ready and displays visuals to the player
    readyButton = Button('Not Ready', notRdyManager)
    readyButton.setXLocYLoc(int(width/17), int(height/2))
    readyButton.setWidthHeight(int(width/10), int(height/20))

    backButton = Button('Back', manager)
    backButton.setXLocYLoc(int(width/17), int(height/2+height/20))
    backButton.setWidthHeight(int(width/10), int(height/20))

    #text box to display player ids and ready status 
    playerStatusX = int((width*16)/17-(width/9))
    playerStatusY = int(height/4)
    playerStatusW = int(width/7)
    playerStatusH = int(height/20)
    netConn.send("lobby.update")
    
    currentLobbyPlayerStatus = netConn.catch()
    playerStatus = pygame_gui.elements.UITextBox(html_text=currentLobbyPlayerStatus.htmlStringify(), relative_rect = pygame.Rect((playerStatusX, playerStatusY), (playerStatusW, playerStatusH)), manager=manager, wrap_to_height=True, layer_starting_height=1)

    for each in managerList:
        each.draw_ui(windowSurface)

    while True:
        time_delta = clock.tick(60) / 1000.0
        #update the text box to let players know who is ready etc...
        tmp = currentLobbyPlayerStatus

        netConn.send("lobby.update")
        currentLobbyPlayerStatus = netConn.catch()

        if currentLobbyPlayerStatus.getStartGame():
            gameBoard(netConn)

        #if player number changes kill the text box and create a new one with updated information.
        if not currentLobbyPlayerStatus == tmp:
            playerStatus.kill()
            playerStatus = pygame_gui.elements.UITextBox(html_text=currentLobbyPlayerStatus.htmlStringify(),relative_rect = pygame.Rect((playerStatusX, playerStatusY), (playerStatusW, playerStatusH)), manager=manager, wrap_to_height=True, layer_starting_height=1)

        isHost = netConn.send("lobby.host").split(":")
        
        if isHost[2] == "True":
            startButtonX = int(width/17)
            startButton.setXLoc(startButtonX)
            if currentLobbyPlayerStatus.getLobbyReadyStatus() and currentLobbyPlayerStatus.getNumberOfPlayers() > 0:
                startButton.enable()
            else:
                startButton.disable()

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                if startButton.getClickedStatus(event):
                    netConn.send("lobby.start")
                    gameBoard(netConn)

                #events for ready button
                elif readyButton.getClickedStatus(event):
                    #if player presses the ready button
                    netConn.send("lobby.ready")
                    # netConn.send("lobby.passCards")
                    #change color from red to green and back when button is pushed
                    if readyButton.getText() == "Not Ready":
                        readyButton.setText("Ready")
                        readyButton.setManager(rdyManager)
                    else:
                        readyButton.setText("Not Ready")
                        readyButton.setManager(notRdyManager)

                elif backButton.getClickedStatus(event):
                        width = 1000
                        height = 1000
                        netConn.send("lobby.leave")
                        return OpenMainMenu()

            # Update events based on clock ticks
            for each in managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)

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

# Create the window, displays splash screen on click starts the main menu
def splash():
    while True:
        # Track the mouse movement
        mousePos = pygame.mouse.get_pos()
        
        # Add splash screen
        splash = addImage('images/splashScreen.jpg', 1, windowSurface, width/2, height/2, width, height)
        
        for event in pygame.event.get():
            # Quit when window X button is clicked
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            # Display menu options if splash screen is clicked
            if event.type == MOUSEBUTTONDOWN:
                if splash.get_rect().collidepoint(mousePos):
                    OpenMainMenu()
        pygame.display.update()

def testingFunction():
    netConn.send("lobby.new:TRASH")
    netConn.send("lobby.start")
    gameBoard(netConn)

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
width = 1680
height = 900

#create pygame area to add splash image to
windowSurface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# TESTING 
testingFunction()
#run the program
splash()

print("print after splash :D ")
