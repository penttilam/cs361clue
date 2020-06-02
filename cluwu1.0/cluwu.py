import pygame
import pygame_gui
import time
from pygame.locals import *
from pygame import surface
from clientPlayer import ClientPlayer
from clientLobby import ClientLobby
from clientNetwork import *
from Button import Button
from ImageButton import ImageButton
from Image import Image
from Panel import Panel
from Label import Label
from InputBox import InputBox
from TextBox import *
from LobbyStart import LobbyStart
from GameGrid import GameGrid
from gameBoard import GameBoard
import threading

#initialize game screen
pygame.init()

pygame.display.set_caption('cluwu')
#set the icon
icon = pygame.image.load('images/cluwuIcon.png')
pygame.display.set_icon(icon)

#set up network connection
netConn = Network()

#screen set up
WIDTH = 1680
HEIGHT = 900

#create pygame area to add splash image to
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#runs main menu
def OpenMainMenu():
    #pygame surface
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    mainMenu = Label("Main Menu", manager, width=72, height=20)
    mainMenu.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2-HEIGHT/5))
    mainMenu.setWidthHeight(int(WIDTH/10), int(HEIGHT/10))

    hostButton = Button('Host', manager)
    hostButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2-HEIGHT/10))
    hostButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))
    
    joinButton = Button('Join', manager)
    joinButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2-HEIGHT/20))
    joinButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))
    
    quitButton = Button("Quit", manager, shortcutKey=K_ESCAPE)
    quitButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2))
    quitButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

    manager.draw_ui(windowSurface)

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                
                if quitButton.getClickedStatus(event):
                    netConn.send("quit")
                    raise SystemExit

                elif hostButton.getClickedStatus(event):
                    #when host is pressed starts the game list by calling the function
                    hostGame()

                elif joinButton.getClickedStatus(event):
                    #when join button is pressed starts the game list by calling the function
                    startGameList()

            manager.process_events(event)
            manager.update(time_delta)
            windowSurface.blit(background, (0, 0))
            manager.draw_ui(windowSurface)
        pygame.display.update()

#starts new game
def hostGame():
    #pygame surface
    managerList = []
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')
    managerList.append(manager)    

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    gameNameLabel = Label("Enter name for your game", manager, width=192, height=20)
    gameNameLabel.setXLocYLoc(int(WIDTH/2-WIDTH/10), int(HEIGHT/2-HEIGHT/5))
    gameNameLabel.setWidthHeight(int(WIDTH/5), int(HEIGHT/20))

    gameName = InputBox(manager)
    gameName.setXLocYLoc(int(WIDTH/2-WIDTH/10), int(HEIGHT/2-WIDTH/6))
    gameName.setWidthHeight(int(WIDTH/5), int(HEIGHT/20))
    gameName.toggleFocus()

    startButton = Button("Start Game", manager, shortcutKey=K_RETURN)
    startButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2-HEIGHT/10))
    startButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))
    
    backButton = Button("Back", manager, shortcutKey=K_ESCAPE)
    backButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2-HEIGHT/20))
    backButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

    while True:
        time_delta = clock.tick(60)/1000.0
        event = None
        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
          
            if event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED or event.type == KEYDOWN:
                if backButton.getClickedStatus(event):
                    return 

                if startButton.getClickedStatus(event) and gameName.getText() != "":
                    gameNameCamel = gameName.getText()
                    if " " in gameName.getText():
                        gameNameCamel = gameName.getText().replace(" ", "_")
                    if "." in gameNameCamel:
                        gameNameCamel = gameNameCamel.replace(".", "*")
                    netConn.send("lobby.new:"+gameNameCamel)
                    newLobby = netConn.catch()
                    startLobby = LobbyStart(netConn, newLobby)
                    startedLobby = startLobby.startLobby()
                    return

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
    
    managerList = []
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')
    managerList.append(manager)

    #pygame surface
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(manager.ui_theme.get_colour('dark_bg'))

    gameSelectListX = int(WIDTH/2-WIDTH/10)
    gameSelectListY = int(HEIGHT/2-HEIGHT/5)
    gameSelectListW = int(WIDTH/5)
    gameSelectListH = int(HEIGHT/5)
    netConn.send("lobby.lobbies")
    gameSelectListActiveGamesList = netConn.catch()

    lobbyList = []

    for clientLobby in gameSelectListActiveGamesList:
        lobbyList.append(str(clientLobby.getId())+" "+str(clientLobby.getNumberOfPlayers())+ " players")

    gameSelectList = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((gameSelectListX, gameSelectListY), (gameSelectListW, gameSelectListH)), item_list=lobbyList, manager=manager)

    # Join Game button
    joinButton = Button('Join Game', manager)
    joinButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2))
    joinButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

    # Refresh button
    refreshButton = Button('Refresh', manager)
    refreshButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2+HEIGHT/20))
    refreshButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

    # Back button
    backButton = Button('Back', manager, shortcutKey=K_ESCAPE)
    backButton.setXLocYLoc(int(WIDTH/2-WIDTH/20), int(HEIGHT/2+HEIGHT/10))
    backButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

    while True:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                #events for join button
                if joinButton.getClickedStatus(event):
                    # send gameSelectList.get_single_selection() to server,
                    # make connection to the game lobby
                    # if game list selection isn't valid refresh the list
                    if not gameSelectList.get_single_selection():
                        return startGameList()
                    #if it does not throw an error make a game of this name
                    else:
                        gameName = gameSelectList.get_single_selection().split(' ')[0]

                    netConn.send("lobby.join:" + gameName)
                    joinResponse = netConn.catch()
                    joinLobby = LobbyStart(netConn, joinResponse)
                    joinedLobby = joinLobby.startLobby()
                    return

                #events for refresh button 
                elif refreshButton.getClickedStatus(event):
                    return startGameList()
                
                #events for back button
                elif backButton.getClickedStatus(event):
                    return 

            # Redraw the background
            windowSurface.blit(background, (0, 0))

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
        splash = addImage('images/splashScreen.jpg', 1, windowSurface, WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)

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
    netConn.catch()
    netConn.send("lobby.start")
    netConn.catch()
    gameBoard = GameBoard(netConn)
    gameBoard.gameBoard()

# TESTING FUNCTION ENSURE COMMENTED OUT IF NEED TO TEST ANYTHING BEFORE THE GAME BOARD
# testingFunction()
# run the program
splash()

print("print after splash :D ")
