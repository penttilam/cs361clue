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
WIDTH = 1680
HEIGHT = 900

class LobbyStart:
    def __init__(self, netConn, lobby):
        self.lobbyStatus = lobby
        print("lobby: " + lobby.getId())
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
        # List of managers used to set themes

        manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./ourTheme.json')
        self.managerList.append(manager)
        rdyManager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./rdyTheme.json')
        self.managerList.append(rdyManager)
        notRdyManager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path='./notRdyTheme.json')
        self.managerList.append(notRdyManager)

        background = pygame.Surface((WIDTH, HEIGHT))
        # background.fill(manager.ui_theme.get_colour('dark_bg'))
        windowSurface.blit(background, (0, 0))
        #pygame surface
        Image('board.png', manager, 0, 0, WIDTH, HEIGHT)
        
        # Button that starts the game when all players are ready, NOT visible to peons
        startButton = Button('Start Game', manager)
        startButton.setXLocYLoc(int(WIDTH), int(HEIGHT/2-HEIGHT/20))
        startButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

        # Button that tells the server if player is ready and displays visuals to the player
        readyButton = Button('Not Ready', notRdyManager)
        readyButton.setXLocYLoc(int(WIDTH/17), int(HEIGHT/2))
        readyButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))

        backButton = Button('Back', manager)
        backButton.setXLocYLoc(int(WIDTH/17), int(HEIGHT/2+HEIGHT/20))
        backButton.setWidthHeight(int(WIDTH/10), int(HEIGHT/20))
        
        for each in self.managerList:
            each.draw_ui(windowSurface)
        pygame.display.update()
        clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
        clientThreads.start()
        self.lobbyPlayersStatus = TextBox(self.managerList[1], self.lobbyStatus.htmlStringify(), self.lobbyPlayersStatusX, self.lobbyPlayersStatusY, self.lobbyPlayersStatusW, self.lobbyPlayersStatusH, wrapToHeight=True)
        while True:
            time_delta = clock.tick(60) / 1000.0
            #update the text box to let players know who is ready etc...
            clientThreads.join(1/1000)
            if not clientThreads.is_alive():
                print("LobbyStatus: " + str(self.lobbyStatus))
                print(str(self.lobbyStatus.getStartGame()))
                if self.lobbyStatus.getStartGame():
                    print("did it work")
                    gameBoard = GameBoard(self.netConn)
                    print("that worked")
                    return gameBoard.gameBoard()                    
                elif type(self.lobbyStatus) != type(""):
                    print("lobbyStatus is not a string")
                    self.processClientUpdates()
                    clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
                    clientThreads.start()
                    print("updates processed")
                elif self.lobbyStatus == "lobby.leave:confirmed":
                    print("Got to the return on leave")
                    return "leave"

            if self.lobbyStatus.getLobbyHost():
                startButtonX = int(WIDTH/17)
                startButton.setXLoc(startButtonX)
                if self.lobbyStatus.getLobbyReadyStatus() and self.lobbyStatus.getNumberOfPlayers() > 0:
                    startButton.enable()
                else:
                    startButton.disable()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    if startButton.getClickedStatus(event):
                        self.netConn.send("lobby.start")

                    #events for ready button
                    elif readyButton.getClickedStatus(event):
                        #if player presses the ready button
                        self.netConn.send("lobby.ready")
                        #change color from red to green and back when button is pushed
                        if readyButton.getText() == "Not Ready":
                            readyButton.setText("Ready")
                            readyButton.setManager(rdyManager)
                        else:
                            readyButton.setText("Not Ready")
                            readyButton.setManager(notRdyManager)

                    elif backButton.getClickedStatus(event):
                        self.netConn.send("lobby.leave")
                        # return "leave"
            # Update events based on clock ticks
            for each in self.managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)
            pygame.display.update()

    def processClientUpdates(self):
        print("updatin yo box")
        #if player status changes update the information.
        self.lobbyPlayersStatus.setText(self.lobbyStatus.htmlStringify())
        print("yo box updated")


    def getUpdates(self, arg1, arg2):
        tempCatch = self.netConn.catch()
        print("In the catch1: " + tempCatch.getId())
        while type(tempCatch) == type(""):
            tempCatch = self.netConn.catch()
            print("In the catch2: " + tempCatch.getId())
        self.lobbyStatus = tempCatch