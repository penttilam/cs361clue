import pygame
import pygame_gui
import random
from pygame.locals import *
from Button import Button
from ImageButton import ImageButton
from Image import Image
from Panel import Panel
from GameGrid import GameGrid
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
from multiprocessing.pool import ThreadPool


class GameBoard:
    def __init__(self, netConn):
        self.characterTokens = []
        self.playerCards = []
        self.managerList = []
        self.chatLog = None
        self.gameGrid = None
        self.turnOrderImages = []
        self.clientGame = None
        random.seed()
        self.width = 1680
        self.height = 900
        self.hiddenPanelLocation = self.width
        self.rollLabel = None
        self.netConn = netConn
        self.clientUpdate = UpdateClientGame(None, None)

    def gameBoard(self):
        clock = pygame.time.Clock()
        updates = 0
        windowSurface = pygame.display.set_mode((self.width, self.height))
        clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))

        self.netConn.send("game.create")
        self.netConn.catch()
        self.clientGame = self.netConn.catch()
        
        clientThreads.start()

        print("ClientGame:")
        print(self.clientGame)
        
        # List of managers used to set themes
        layer0 = pygame_gui.UIManager((self.width, self.height), './tileTheme.json')
        self.managerList.append(layer0)
        layer1 = pygame_gui.UIManager((self.width, self.height), './ourTheme.json')
        self.managerList.append(layer1)

        layer2 = pygame_gui.UIManager((self.width, self.height), './panelTheme.json')
        self.managerList.append(layer2)
        layer3 = pygame_gui.UIManager((self.width, self.height), './panelTheme.json')
        self.managerList.append(layer3)
        
        self.displayTurnOrder(self.clientGame.getTurnOrder(), layer1, initial=1)
        self.chatLog = TextBox(layer1)
        chatInput = InputBox(layer1)

        self.gameGrid = GameGrid(self.width, self.height, layer0)
        Image('board.png', layer0, 0, 0, self.width, self.height)

        # Button to display player's hand of cards
        handButton = ImageButton(layer3, imageFile= 'weebcard.png', buttonText=" ")
        handButton.setXLocYLoc(int((self.width*16)/17-(self.width/10)), int(self.height/4) - 60)
        handButton.setWidthHeight(int(142), int(180))
        Label("Look at Hand", layer1, handButton.getXLoc(), handButton.getYLoc() + 180, 142, 20)

        # Button to roll the dice
        diceButton = ImageButton(layer0, imageFile='dice.png', buttonText=" ")
        diceButton.setXLocYLoc(int((self.width*16)/17-(self.width/10)), int(self.height/4)+180)
        diceButton.setWidthHeight(int(120), int(120))
        Label("Roll", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 100, 142, 20)
        self.rollLabel = Label("Current Moves: 0", layer1, diceButton.getXLoc(), diceButton.getYLoc() - 20, 142, 20)
        myRoll = -1
        # End turn Button
        endTurnButton = Button("End turn", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 40 , 90, 30)
        
        # Button to display the player's notebook
        # notebookButton = Button('Notebook', layer3)
        notebookButton = ImageButton(layer3, imageFile='cluwuNotebook.png', buttonText=" ")
        notebookButton.setXLocYLoc(int((self.width*16)/17-(self.width/10))-70, int(self.height/2+self.height/20)+34)
        notebookButton.setWidthHeight(int(450), int(475))
        notebookButton.getButton().setManager(layer0)
        # Label("Check Notes", layer3, notebookButton.getXLoc() + int(notebookButton.getWidth()/2), notebookButton.getYLoc() + int(notebookButton.getHeight()/2) + 90, 100, 20)

        #initilization of the notebook panel
        notebook = Panel(layer3, layerHeight=2)
        notebook.setXLocYLoc(int(self.width), int(self.height/8))
        notebook.setWidthHeight(int(self.width/4), int(3*self.height/4))
        notebook.addImage(Image("clueNotepad.png", layer3, 0, 0, notebook.getWidth(), notebook.getHeight(), container=notebook.getContainer()))
        notebook.setVisibleLocation(int((self.width*3)/8))
        notebook.setHiddenLocation(self.width)
        # Creates a Button object to allow interaction with checkboxe buttons
        checkBoxButton = createNotebook(notebook)
        characterList = ["scarlet", "white", "mustard", "green", "peacock", "plum"]
 
        # playerCards = [("scarlet", "Card"),("white", "Card"),("mustard", "Card"),("green", "Card"),("peacock", "Card"),("plum", "Card")]
        self.playerCards = self.clientGame.getMyCards()
        #initilization of the hand panel
        hand = Panel(layer3, layerHeight=2)
        hand.setXLocYLoc(int(self.width), int(self.height/3))
        hand.setWidthHeight(len(self.playerCards)*142 + 20 + 10*len(self.playerCards), 215)
        hand.setVisibleLocation(int(self.width/2-hand.getWidth()/2))
        hand.setHiddenLocation(self.width)
        
        cardXLoc = -142
        buffer = 10
        i=0
        for card in self.playerCards:
            hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card.getCardName()))
            if card.getCardCategory() == "weapon":
                imageFormat = ".jpg"
            else:
                imageFormat = ".png"
            hand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
            cardXLoc += 142 + buffer
            i+=1
        
        for character in characterList:
            if self.clientGame.getMyToken().getTokenCharacter() == character:
                tokenFileExtension = "mytoken.png"
            else:
                tokenFileExtension = ".png"
            self.characterTokens.append(Image(str(character) + tokenFileExtension, layer2, 0, 0, 30, 30, object_id=character))

        self.characterTokens[0].setXLocYLoc(947, 60)
        self.characterTokens[0].setRowColumn(0, 16)
        self.gameGrid.grid[0][16].setOccupied(1)
        self.characterTokens[1].setXLocYLoc(1171, 270)
        self.characterTokens[1].setRowColumn(7, 23)
        self.gameGrid.grid[18][0].setOccupied(1)
        self.characterTokens[2].setXLocYLoc(883, 780)
        self.characterTokens[2].setRowColumn(24, 14)
        self.gameGrid.grid[24][14].setOccupied(1)
        self.characterTokens[3].setXLocYLoc(723, 780)
        self.characterTokens[3].setRowColumn(24, 9)
        self.gameGrid.grid[24][9].setOccupied(1)
        self.characterTokens[4].setXLocYLoc(435, 600)
        self.characterTokens[4].setRowColumn(18, 0)
        self.gameGrid.grid[7][23].setOccupied(1)
        self.characterTokens[5].setXLocYLoc(435, 210)
        self.characterTokens[5].setRowColumn(5, 0)
        self.characterTokens[5].setLocation("outside")
        self.gameGrid.grid[5][0].setOccupied(1)
        
        for x in range(6):
            if (self.clientGame.getMyToken().getTokenCharacter() == self.characterTokens[x].getObjectId()):
                self.myToken = self.characterTokens[x]
                break

        # gameGrid.enterARoom(characterTokens[5], "lovehotel")

        if self.myToken.getObjectId() != self.clientGame.getTurnOrder()[0].getTokenCharacter():
            self.rollLabel.setText(self.clientGame.getTurnOrder()[0].getTokenCharacter() + "'s Turn")
        else:
            self.rollLabel.setText("Your Turn")

        while True:
            myTurn = self.clientGame.getMyTurn()
            if myTurn:
                endTurnButton.setXLoc(diceButton.getXLoc() + diceButton.getWidth() + 10)
                time_delta = clock.tick(60) / 1000.0
            else:
                endTurnButton.setXLoc(self.width)
                time_delta = clock.tick(60) / 1000.0
            
            clientThreads.join(1/1000)
            if not clientThreads.is_alive():
                if type(self.clientUpdate) != type(""):
                    self.processClientUpdates()
                clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
                clientThreads.start()


            for event in pygame.event.get():
                if event.type == QUIT:
                    # self.netConn.send("quit")
                    raise SystemExit
                                    
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    if chatInput.getText() != "" and event.type == KEYDOWN and event.key == K_RETURN:
                        self.netConn.send("game.chat.add:" + chatInput.getText())
                        self.netConn.catch()
                        chatInput.setText("")
                    elif (not self.checkHidden(notebook)):
                        notebook.panel.process_event(event)
                        # Cycles Notebook checkboxes between blank, X, and checked
                        if event.type == KEYDOWN and event.key == K_ESCAPE or notebookButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                        elif handButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                            self.showPanel(hand)
                        elif (checkBoxButton.getClickedStatus(event)): 
                            if event.ui_element.text == " ":
                                event.ui_element.set_text("X")
                            elif event.ui_element.text == "X":
                                event.ui_element.set_text(u'\u2713')
                            elif event.ui_element.text == u'\u2713':
                                event.ui_element.set_text(" ")
                            
                    elif (not self.checkHidden(hand)):
                        hand.panel.process_event(event)
                        if event.type == KEYDOWN and event.key == K_ESCAPE or handButton.getClickedStatus(event):
                            self.hidePanel(hand)
                        elif notebookButton.getClickedStatus(event):
                            self.hidePanel(hand)
                            self.showPanel(notebook)
                        else:
                            for clicked in range(int(hand.getHandSize()/2)):
                                if (hand.getImageButton(clicked).getClickedStatus(event)):
                                    break
                    else:
                        # Open the Notebook
                        if notebookButton.getClickedStatus(event):
                            # Shows Notebook, hides Hand if it is open
                            if self.checkHidden(notebook):
                                self.showPanel(notebook)
                                self.hidePanel(hand)
                            else: # Hides Notebook
                                self.hidePanel(notebook)
                        
                        # Open the Hand
                        elif handButton.getClickedStatus(event):
                            # Shows Hand, hides Notebook if it is open
                            if self.checkHidden(hand):
                                self.showPanel(hand)
                                self.hidePanel(notebook)
                            else: # Hides the hand
                                self.hidePanel(hand)
                        
                        # End player turn
                        elif endTurnButton.getClickedStatus(event):
                            self.netConn.send("game.turn")
                            endTurnButton.setXLoc(self.width)
                            myRoll = -1

                        elif diceButton.getClickedStatus(event):
                            if myRoll == -1 and myTurn:
                                myRoll = 100
                                # myRoll = random.randrange(1,6,1)
                                self.rollLabel.setText("You rolled: " + str(myRoll))
                            elif myTurn:
                                self.rollLabel.setText("Current Moves: " + str(myRoll))
                            else:
                                self.rollLabel.setText("You rolled: " + str(myRoll))

                        # Moves token
                        elif myTurn and myRoll > 0 and self.checkHidden(notebook) and self.checkHidden(hand) and self.gameGrid.clickedTile(event, self.myToken):
                            self.netConn.send("game.move:"+str(self.myToken.getRow())+"."+str(self.myToken.getColumn()))
                            myRoll-=1
                            self.rollLabel.setText("Current Moves: " + str(myRoll))
            
            # Update events based on clock ticks
            for each in self.managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)

            pygame.display.update()

    def processClientUpdates(self):
        tokenUpdates = self.clientUpdate.getTurnOrder()
        # self.chatLog.addText(self.clientUpdate.getChatUpdate())
        self.updateTokenPositions(tokenUpdates)
        if tokenUpdates[0].getTokenCharacter() != self.clientGame.getTurnOrder()[0].getTokenCharacter():
            self.clientGame.setTurnOrder(tokenUpdates)
            self.displayTurnOrder(self.clientGame.getTurnOrder(), self.managerList[1])
            if self.myToken.getObjectId() != self.clientGame.getTurnOrder()[0].getTokenCharacter():
                self.rollLabel.setText(self.clientGame.getTurnOrder()[0].getTokenCharacter() + "'s Turn")
            else:
                self.rollLabel.setText("Your Turn")


    def hidePanel(self, panel):
        panel.setXLoc(panel.getHiddenLocation())
            
    def showPanel(self, panel):
        panel.setXLoc(panel.getVisibleLocation())

    def checkHidden(self, panel):
        return (panel.getXLoc() == panel.getHiddenLocation())

    def displayTurnOrder(self, turnOrder, manager, initial=0):
        yLoc = 0
        i = 0
        if initial:
            for character in reversed(turnOrder):
                name = character.getTokenCharacter()
                self.turnOrderImages.append(Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name))
                yLoc += 60
        else:
            for image in self.turnOrderImages:
                image.kill()
            for character in reversed(turnOrder):
                name = character.getTokenCharacter()
                self.turnOrderImages[i] = Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name)
                yLoc += 60
                i += 1

    def updateTokenPositions(self, tokenUpdates):
        for player in self.characterTokens:
            for token in tokenUpdates:
                if (player.getObjectId() == token.getTokenCharacter()):
                    self.gameGrid.grid[player.getRow()][player.getColumn()].setOccupied(0)
                    player.setXLocYLoc(self.gameGrid.grid[int(token.getTokenXLoc())][int(token.getTokenYLoc())].getXLoc(), self.gameGrid.grid[int(token.getTokenXLoc())][int(token.getTokenYLoc())].getYLoc())
                    player.setRowColumn(int(token.getTokenXLoc()), int(token.getTokenYLoc()))
                    self.gameGrid.grid[player.getRow()][player.getColumn()].setOccupied(1)

    def getUpdates(self, arg1, arg2):
        tempCatch = self.netConn.catch()
        while (type(tempCatch) == type("")):
            tempCatch = self.netConn.catch()
        self.clientUpdate = tempCatch
