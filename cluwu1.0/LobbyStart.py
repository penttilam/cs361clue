import pygame
import pygame_gui
import random
from pygame.locals import *
from Button import Button
from ImageButton import ImageButton
from Image import Image
from Panel import Panel
from gameBoard import GameBoard
from notebook import createNotebook
from clientPlayer import ClientPlayer
from clientLobby import ClientLobby
from clientNetwork import *
from clientCard import *
from clientGame import *
from TextBox import *
from InputBox import *
from clientChat import *
from Label import Label
import threading
import time
# set resolution as a constant, yes 1680 is weird, but the grid lines up properly at those numbers
WIDTH = 1680
HEIGHT = 900

class LobbyStart:
    def __init__(self, netConn, lobby):
        self.lobbyStatus = lobby
        self.lobbyPlayersStatus = None
        self.netConn = netConn
        #text box to display player ids and ready status 
        self.lobbyPlayersStatusX = int((WIDTH*16)/17-(WIDTH/9))
        self.lobbyPlayersStatusY = int(HEIGHT/4)
        self.lobbyPlayersStatusW = int(WIDTH/7)
        self.lobbyPlayersStatusH = int(HEIGHT/20)
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')
        self.managerList = []
        self.managerList.append(self.manager)
    
    def startLobby(self):

        clock = pygame.time.Clock()
        windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))

        # List of managers used to set themes/screen height of objects
        manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')
        self.managerList.append(manager)
        rdyManager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./rdyTheme.json')
        self.managerList.append(rdyManager)
        notRdyManager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./notRdyTheme.json')
        self.managerList.append(notRdyManager)

        # Display the background
        background = pygame.Surface((WIDTH, HEIGHT))
        windowSurface.blit(background, (0, 0))
        # Set the background image of the game board
        Image('board.png', manager, 0, 0, WIDTH, HEIGHT)
        
        # Button that starts the game when all players are ready, NOT visible to peons
        startButton = Button('Start Game', manager)
        startButton.setXLocYLoc(int(WIDTH), int(HEIGHT/2-HEIGHT/20))
        startButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

        # Button that tells the server if player is ready and displays visuals to the player
        readyButton = Button('Not Ready', notRdyManager)
        readyButton.setXLocYLoc(int(WIDTH/17), int(HEIGHT/2))
        readyButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

        # Button to return to lobby list or host game menu
        backButton = Button('Back', manager)
        backButton.setXLocYLoc(int(WIDTH/17), int(HEIGHT/2+HEIGHT/20))
        backButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))
        
        # Draw all items associated with managers
        for each in self.managerList:
            each.draw_ui(windowSurface)
        pygame.display.update()

        # Declare and start thread for getting updates from server
        clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
        clientThreads.start()

        # Display a textbox with current player status (Ready, Not Ready)
        self.lobbyPlayersStatus = TextBox(self.managerList[1], self.lobbyStatus.htmlStringify(), self.lobbyPlayersStatusX, self.lobbyPlayersStatusY, self.lobbyPlayersStatusW, self.lobbyPlayersStatusH, wrapToHeight=True)
        
        while True:
            # Set refresh rate for managers
            time_delta = clock.tick(60) / 1000.0
        
            # Attempt to re-join the thread listening for server commands
            clientThreads.join(1/1000)

            # If thread caught something from server it should not be alive
            # If it is not alive, handle the input from the server
            if not clientThreads.is_alive():
                # If server told us the game is starting, launch the game board
                if self.lobbyStatus.getStartGame():
                    gameBoard = GameBoard(self.netConn)
                    return gameBoard.gameBoard()
                # If the server returned an object, process the update then start a new thread
                elif type(self.lobbyStatus) != type(""):
                    self.processClientUpdates()
                    clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
                    clientThreads.start()
                # If server sent confirmation that player wanted to leave, return from function
                elif self.lobbyStatus == "lobby.leave:confirmed":
                    return "leave"

            # If the player is the host, display the Start Game button
            if self.lobbyStatus.getLobbyHost():
                startButtonX = int(WIDTH/17)
                startButton.setXLoc(startButtonX)
                # If there are 1 or more players that are ready, enable the start button, otherwise disable
                if self.lobbyStatus.getLobbyReadyStatus() and self.lobbyStatus.getNumberOfPlayers() > 0:
                    startButton.enable()
                else:
                    startButton.disable()

            # Check for interaction with the game
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                # If the player clicked a button or pressed a key
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    # Check if the player clicked to start the game and send command to server
                    if startButton.getClickedStatus(event):
                        self.netConn.send("lobby.start")

                    # Check if the ready button was clicked, send ready command to server and toggle the value if so
                    elif readyButton.getClickedStatus(event):
                        #if player presses the ready button
                        self.netConn.send("lobby.ready")
                        #change color from red to green and back when button is pushed
                        if readyButton.getText() == "Not Ready":
                            readyButton.setText("Ready")
                            # Change manager to change displayed color green
                            readyButton.setManager(rdyManager)
                        else:
                            readyButton.setText("Not Ready")
                            # Change manager to change displayed color to red
                            readyButton.setManager(notRdyManager)
                    
                    # Check if the back button was pressed and return from function
                    elif backButton.getClickedStatus(event):
                        self.netConn.send("lobby.leave")

            # Update events based on clock ticks
            for each in self.managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)
            pygame.display.update()

    # processClientUpdates function updates the player status information.
    def processClientUpdates(self):
        self.lobbyPlayersStatus.setText(self.lobbyStatus.htmlStringify())

    # getUpdates function takes two empty args and attempts to catch data from the server
    def getUpdates(self, arg1, arg2):
        self.lobbyStatus = self.netConn.catch()