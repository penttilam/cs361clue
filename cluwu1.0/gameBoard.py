"gameBoard contains the functions that control player movement and display of pertinent game items"
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
from clientToken import *
from TextBox import *
from InputBox import *
from clientChat import *
from Label import Label
import threading
import time
WIDTH = 1680
HEIGHT = 900

class GameBoard:
    def __init__(self, netConn):
        self.characterTokens = []
        self.playerCards = []
        self.fullDeck = None
        self.managerList = []
        self.discardedButtonFlag = False 
        self.discardedButton = None
        self.discardHand = None
        self.chatLog = None
        self.gameGrid = None
        self.turnOrderImages = []
        self.clientGame = None
        random.seed()
        self.hiddenPanelLocation = WIDTH
        self.rollLabel = None
        self.netConn = netConn
        self.clientUpdate = None

    # def showDiscardedCards(self): 
    #     # ImageButton to display discarded cards from players that have left
    #     print("Trying to make the discarded card button!!!!!!!!!!!!!!!!!!")
    #     discardedButton = ImageButton(self.managerList[3], imageFile="cardPile.png", buttonText=" ")
    #     discardedButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10)) + 125, int(HEIGHT/4) - 60)
    #     discardedButton.setWidthHeight(int(175), int(180))
    #     discardedButton.getButton().setManager(self.managerList[0])
    #     Label("Discarded", self.managerList[1], discardedButton.getXLoc(), discardedButton.getYLoc() + 180, 142, 20)
    #     print("MADE THE BUTTON YAY")

    def gameBoard(self):

        accused = [None, None, None] 

        # Set for use in updating displays
        clock = pygame.time.Clock()

        # Send command to start game and catch the response
        self.netConn.send("game.create")
        time.sleep(random.randrange(1,6,1)/1000)
        self.clientGame = self.netConn.catch()

        # Create and start thread to handle server updates
        clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
        clientThreads.start()

        # List of managers used to set themes
        layer0 = pygame_gui.UIManager((WIDTH, HEIGHT), './tileTheme.json')
        self.managerList.append(layer0)
        layer1 = pygame_gui.UIManager((WIDTH, HEIGHT), './ourTheme.json')
        self.managerList.append(layer1)
        layer2 = pygame_gui.UIManager((WIDTH, HEIGHT), './panelTheme.json')
        self.managerList.append(layer2)
        layer3 = pygame_gui.UIManager((WIDTH, HEIGHT), './panelTheme.json')
        self.managerList.append(layer3)
        
        # Display the background
        windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
        background = pygame.Surface((WIDTH, HEIGHT))
        windowSurface.blit(background, (0, 0))
        Image('board.png', layer0, 0, 0, WIDTH, HEIGHT)

        # Set cards in player hand
        self.playerCards = self.clientGame.getMyCards()

        # Set full deck for player
        self.fullDeck = self.clientGame.getFullDeck()  

        print("This is the full deck")
        print(self.fullDeck) 

        # Display the turn order of players and display
        self.displayTurnOrder(self.clientGame.getTurnOrder(), layer1, initial=1)

        # Set layer the chatlog and input will be displayed on
        self.chatLog = TextBox(layer1)
        chatInput = InputBox(layer1)
        
        # Create the grid the player clicks to interact with the game board
        self.gameGrid = GameGrid(WIDTH, HEIGHT, layer0)

        # ImageButton to display player's hand of cards
        handCards = len(self.playerCards)
        handButton = ImageButton(layer3, imageFile="cardBack" + str(handCards) + ".png", buttonText=" ")
        handButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10)), int(HEIGHT/4) - 60)
        handButton.setWidthHeight(int(142), int(180))
        handButton.getButton().setManager(layer0)
        Label("Look at Hand", layer1, handButton.getXLoc(), handButton.getYLoc() + 180, 142, 20)

        # ImageButton to roll the dice
        diceButton = ImageButton(layer0, imageFile='die6.png', buttonText=" ")
        diceButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10)), int(HEIGHT/4)+180)
        diceButton.setWidthHeight(int(80), int(80))
        Label("Roll", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 100, 142, 20)
        self.rollLabel = Label("Current Moves: 0", layer1, diceButton.getXLoc(), diceButton.getYLoc() - 20, 142, 20)
        # myRoll should always be -1 unless it is that player's turn
        myRoll = -1

        # End turn Button
        endTurnButton = Button("End turn", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 40, 90, 30)

        # ImageButton to display the player's notebook
        notebookButton = ImageButton(layer3, imageFile='cluwuNotebook.png', buttonText=" ")
        notebookButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10))-70, int(HEIGHT/2+HEIGHT/20)+34)
        notebookButton.setWidthHeight(int(450), int(475))
        notebookButton.getButton().setManager(layer0)

        # Initilization of the notebook panel
        notebook = Panel(layer3, layerHeight=2)
        notebook.setXLocYLoc(int(WIDTH), int(HEIGHT/8))
        notebook.setWidthHeight(int(WIDTH/4), int(3*HEIGHT/4))
        notebook.addImage(Image("clueNotepad.png", layer3, 0, 0, notebook.getWidth(), notebook.getHeight(), container=notebook.getContainer()))
        notebook.setVisibleLocation(int((WIDTH*3)/8))
        notebook.setHiddenLocation(WIDTH)

        # Accuse Button
        accuseButton = Button("Accuse", layer1, handButton.getXLoc(), 20, 90, 30, object_id="accuseButton")

        # Suggest Button
        suggestButton = Button("Suggest", layer1, handButton.getXLoc(), 80, 90, 30, object_id="suggestButton")




        # Creates a Button object to allow interaction with checkbox buttons
        checkBoxButton = createNotebook(notebook)

        # List of characters used to create tokens
        characterList = ["scarlet", "white", "mustard", "green", "peacock", "plum"]
        
        # Create the panel to display the player cards
        hand = Panel(layer3, layerHeight=2)
        hand.setXLocYLoc(int(WIDTH), int(HEIGHT/3))
        hand.setWidthHeight(len(self.playerCards)*142 + 20 + 10*len(self.playerCards), 215)
        hand.setVisibleLocation(int(WIDTH/2-hand.getWidth()/2))
        hand.setHiddenLocation(WIDTH)

        # Create the panel to display the accuse cards
        accuseHand = Panel(layer3, layerHeight=2)
        accuseHand.setXLocYLoc(int(WIDTH), int(HEIGHT/3) - 225)
        accuseHand.setWidthHeight(len(self.fullDeck[1])*142 + 105, 615)
        accuseHand.setVisibleLocation(int(WIDTH/2-accuseHand.getWidth()/2))
        accuseHand.setHiddenLocation(WIDTH)
        person = "_____"
        location = "_____"
        weapon = "_____"
        accuseText = TextBox(layer3, "It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.", xLoc=1069, yLoc=450, width=145, height=195, container=accuseHand.getContainer(), layer=1, objectId="accuseText", wrapToHeight=True)
        # Accusation Submit Button
        submitAccuse = Button("Accuse", layer3, 1090, 550, 90, 30, container=accuseHand.getContainer())
        
        # cardXLoc allows cards to be placed a card distance apart plus the buffer value between them
        cardXLoc = -142
        buffer = 10
        i = 0
        # For each card in the player hand
        for card in self.playerCards:
            # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
            hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card.getCardName()))
            if card.getCardCategory() == "weapon":
                imageFormat = ".jpg"
            else:
                imageFormat = ".png"
            # Set the image for the ImageButton
            hand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
            # Move the location of the next card in the hand
            cardXLoc += 142 + buffer
            i += 1


        
        # For each character check if it is the player's token, if it is use the token with the purple highlight around it
        i = 0
        for character in characterList:
            if self.clientGame.getMyToken().getTokenCharacter() == character:
                tokenFileExtension = "mytoken.png"
            # If it's not the player, use the regular token
            else:
                tokenFileExtension = ".png"
            # Add the image to the character tokens
            self.characterTokens.append(Image(str(character) + tokenFileExtension, layer2, 0, 0, 30, 30, object_id=character))
            # If token is player, assign token to myToken. Assigned here instead of above due to the [i] location not existing untit the Image is appended above
            if tokenFileExtension == "mytoken.png":
                self.myToken = self.characterTokens[i]
            self.characterTokens[i].setLocation("outside")
            
            i += 1

        y = 10
        i = 0
        j = 1
        # For each card in the the deck
        for cardType in reversed(self.fullDeck):
            if j != 1:
                cardXLoc = -142
            else:
                cardXLoc = 10
            for card in cardType:
                # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
                accuseHand.addImageButton(ImageButton(accuseHand.getManager(), cardXLoc + 142 + buffer, y, 142, 190, container=accuseHand.getContainer(), object_id="accuseHandIB"+card.getCardCategory(), buttonText=card.getCardName()))
                if card.getCardCategory() == "weapon":
                    imageFormat = ".jpg"
                else:
                    imageFormat = ".png"
                # Set the image for the ImageButton
                accuseHand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
                cardXLoc += 142 + buffer
                i += 1
            j = not j
            y += 200
        weaponButton = Button("", layer3, container=accuseHand.getContainer(), object_id = "accuseHandIBweapon", xLoc=WIDTH)
        locationButton = Button("", layer3, container=accuseHand.getContainer(), object_id = "accuseHandIBlocation", xLoc=WIDTH)
        peopleButton = Button("", layer3, container=accuseHand.getContainer(), object_id = "accuseHandIBpeople", xLoc=WIDTH)
            
        # Set the starting locations of each character
        # Scarlet
        self.characterTokens[0].setXLocYLoc(947, 60)
        self.characterTokens[0].setRowColumn(0, 16)
        self.gameGrid.grid[0][16].setOccupied(1)
        # White
        self.characterTokens[1].setXLocYLoc(1171, 270)
        self.characterTokens[1].setRowColumn(7, 23)
        self.gameGrid.grid[18][0].setOccupied(1)
        # Mustard
        self.characterTokens[2].setXLocYLoc(883, 780)
        self.characterTokens[2].setRowColumn(24, 14)
        self.gameGrid.grid[24][14].setOccupied(1)
        # Green
        self.characterTokens[3].setXLocYLoc(723, 780)
        self.characterTokens[3].setRowColumn(24, 9)
        self.gameGrid.grid[24][9].setOccupied(1)
        # Peacock
        self.characterTokens[4].setXLocYLoc(435, 600)
        self.characterTokens[4].setRowColumn(18, 0)
        self.gameGrid.grid[7][23].setOccupied(1)
        # Plum
        self.characterTokens[5].setXLocYLoc(435, 210)
        self.characterTokens[5].setRowColumn(5, 0)
        self.gameGrid.grid[5][0].setOccupied(1)

        # Set the current player
        currentTurnCharacter = self.clientGame.getTurnOrder()[0].getGameToken().getTokenCharacter()
        # If is not the player's turn, set the label under the die to identify the player whose turn it is
        if self.myToken.getObjectId() != currentTurnCharacter:
            self.rollLabel.setText(currentTurnCharacter + "'s Turn")
        else:
            self.rollLabel.setText("Your Turn") 

        # Game loop
        while True:
            # check if it's the player's turn
            myTurn = self.clientGame.getTurnOrder()[0].getGameToken().getTokenCharacter() == self.myToken.getObjectId()
            if myTurn:
                # Display and end turn button for the player next to the die
                endTurnButton.setXLoc(diceButton.getXLoc() + diceButton.getWidth() + 10)
            else:
                # Hide the end turn button off screen
                endTurnButton.setXLoc(WIDTH)
            
            time_delta = clock.tick(60) / 1000.0
            
            # Check to see if the server sent the client anything
            clientThreads.join(1/1000)
            # if server sent something, the thread will not be alive
            if not clientThreads.is_alive():
                # If the object sent back is not a string, process it
                if type(self.clientUpdate) != type(""):
                    self.processClientUpdates()
                # Start the thread back up
                clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
                clientThreads.start()

        

            # Get interactions with the game
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                
                # If the player clicked a button or pressed a key
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    # If they hit the return key and the chat box is not empty, send the chat to the server
                    if chatInput.getText() != "" and event.type == KEYDOWN and event.key == K_RETURN:
                        self.netConn.send("game.chat.add:" + chatInput.getText())
                        # Blank out the chat input box
                        chatInput.setText("")
                    # If the notebook is visible, set the notebook to handle all events that come in to prevent clickthrough to the board
                    elif (not self.checkHidden(notebook)):
                        notebook.panel.process_event(event)
                        # If the player clicks the notebook image again or hits escape key, close the notebook
                        if event.type == KEYDOWN and event.key == K_ESCAPE or notebookButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                        # If the player clicks the hand button, display it and hide the notebook
                        elif handButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                            self.showPanel(hand)
                        # If the player clicks the dsicard hand button, display it and hide the notebook
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                            self.showPanel(self.discardHand)
                        # If the player clicks the accuse hand button, display it and hide the notebook
                        elif accuseButton.getClickedStatus(event):
                            self.hidePanel(notebook)
                            self.showPanel(accuseHand)
                            
                        # Cycle notebook checkboxes between blank, X, and checked
                        elif (checkBoxButton.getClickedStatus(event)): 
                            if event.ui_element.text == " ":
                                event.ui_element.set_text("X")
                            elif event.ui_element.text == "X":
                                event.ui_element.set_text(u'\u2713')
                            elif event.ui_element.text == u'\u2713':
                                event.ui_element.set_text(" ")

                    # If the hand is visible, set the hand to handle all events that come in to prevent clickthrough to the board
                    elif (not self.checkHidden(hand)):
                        hand.panel.process_event(event)
                        # If the player clicks the hand image again or hits escape key, close the hand
                        if event.type == KEYDOWN and event.key == K_ESCAPE or handButton.getClickedStatus(event):
                            self.hidePanel(hand)
                        # If the player clicks the notebook button, display it and hide the hand
                        elif notebookButton.getClickedStatus(event):
                            self.hidePanel(hand)
                            self.showPanel(notebook)
                        # If the player clicks the dsicard hand button, display it and hide the hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.hidePanel(hand)
                            self.showPanel(self.discardHand)
                        # If the player clicks the accuse hand button, display it and hide the hand cards
                        elif accuseButton.getClickedStatus(event):
                            self.hidePanel(hand)
                            self.showPanel(accuseHand)
                        else:
                            # Check if the cards in the hand are clicked, used for accusations/suggestions NOT CURRENTLY IMPLEMENTED TO DO ANYTHING
                            for clicked in range(int(hand.getHandSize()/2)):
                                if (hand.getImageButton(clicked).getClickedStatus(event)):
                                    
                                    break

                    # If the discarded cards is visible, set the discarded cards to handle all events that come in to prevent clickthrough to the board
                    elif self.discardedButtonFlag and (not self.checkHidden(self.discardHand)):
                        self.discardHand.panel.process_event(event)
                        # If the player clicks the hand image again or hits escape key, close the discarded cards
                        if event.type == KEYDOWN and event.key == K_ESCAPE or self.discardedButton.getClickedStatus(event):
                            self.hidePanel(self.discardHand)
                        # If the player clicks the notebook button, display it and hide the discarded cards
                        elif notebookButton.getClickedStatus(event):
                            self.hidePanel(self.discardHand)
                            self.showPanel(notebook)
                        # If the player clicks the hand button, display it and hide the discarded cards
                        elif handButton.getClickedStatus(event):
                            self.hidePanel(self.discardHand)
                            self.showPanel(hand)
                        # If the player clicks the accuse hand button, display it and hide the discarded cards
                        elif accuseButton.getClickedStatus(event):
                            self.hidePanel(self.discardHand)
                            self.showPanel(accuseHand)
                        # else:
                        #     # Check if the cards in the hand are clicked, used for accusations/suggestions NOT CURRENTLY IMPLEMENTED TO DO ANYTHING
                        #     for clicked in range(int(self.discardHand.getHandSize()/2)):
                        #         if (self.discardHand.getImageButton(clicked).getClickedStatus(event)):
                        #             break

                    # If the accuse cards is visible, set the accuse cards to handle all events that come in to prevent clickthrough to the board
                    elif (not self.checkHidden(accuseHand)):
                        accuseHand.panel.process_event(event)
                        # If the player clicks the hand image again or hits escape key, close the accuse cards
                        if event.type == KEYDOWN and event.key == K_ESCAPE or accuseButton.getClickedStatus(event):
                            self.hidePanel(accuseHand)
                        # If the player clicks the notebook button, display it and hide the accuse cards
                        elif notebookButton.getClickedStatus(event):
                            self.hidePanel(accuseHand)
                            self.showPanel(notebook)
                        # If the player clicks the hand button, display it and hide the accuse cards
                        elif handButton.getClickedStatus(event):
                            self.hidePanel(accuseHand)
                            self.showPanel(hand)
                        # If the player clicks the dsicard hand button, display it and hide the hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.hidePanel(accuseHand)
                            self.showPanel(self.discardHand)
                        elif weaponButton.getClickedStatus(event):
                            accused[0] = event.ui_element.text
                            weapon = event.ui_element.text
                        elif locationButton.getClickedStatus(event):
                            accused[1] = event.ui_element.text
                            location = event.ui_element.text
                        elif peopleButton.getClickedStatus(event):
                            accused[2] = event.ui_element.text
                            person = event.ui_element.text
                        elif submitAccuse.getClickedStatus(event): 
                            if not (accused[0] == None and accused[1] == None and accused[2] == None):
                                self.netConn.send("game.accuse:" + str(accused[0]) + "." + str(accused[1]) + "." + str(accused[2]))
                                self.hidePanel(accuseHand)
                        accuseText.addText("It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.")
                    else:
                        # Open the Notebook
                        if notebookButton.getClickedStatus(event):
                            self.showPanel(notebook)
                        
                        # Open the Hand
                        elif handButton.getClickedStatus(event):
                            self.showPanel(hand)

                        # Open the discard hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.showPanel(self.discardHand)

                        # Open the accuse hand
                        elif accuseButton.getClickedStatus(event):
                            print(" Showed accuse")
                            self.showPanel(accuseHand)
                        
                        # End player turn, send command to server
                        elif endTurnButton.getClickedStatus(event):
                            print("Clicked end turn")
                            self.netConn.send("game.turn")
                            # Hide end turn button
                            endTurnButton.setXLoc(WIDTH)
                            # reset myRoll to -1
                            myRoll = -1


                        # Roll the die
                        elif diceButton.getClickedStatus(event):
                            # If it's the player's turn and they haven't rolled yet, roll the die and store in myRoll
                            if myRoll == -1 and myTurn:
                                myRoll = 100
                                # myRoll = random.randrange(1,6,1)
                                diceButton.setImage("die" + str(myRoll) + ".png")
                                self.rollLabel.setText("You rolled: " + str(myRoll))
                            # If player has already rolled this turn, indicate how many moves they have left
                            elif myTurn:
                                self.rollLabel.setText("Current Moves: " + str(myRoll))
                            # If it is not the player's turn, roll for fun.
                            else:
                                self.rollLabel.setText("You rolled: " + str(random.randrange(1,6,1)))

                        # Moves token if it is the player's turn, they have moves left, the notebook and hand are not visible and they clicked on a valid game tile
                        elif myTurn and myRoll > 0 and self.checkHidden(notebook) and self.checkHidden(hand) and self.gameGrid.clickedTile(event, self.myToken):
                            self.netConn.send("game.move:"+str(self.myToken.getRow())+"."+str(self.myToken.getColumn()))
                            # Decrease die roll by 1
                            myRoll -= 1
                            self.rollLabel.setText("Current Moves: " + str(myRoll))
            
            # Update events based on clock ticks
            for each in self.managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)
            pygame.display.update()

    # Handle events received from the server
    def processClientUpdates(self):
        # Store the current turn order
        tokenUpdates = self.clientUpdate.getTurnOrder()
        # Store the character who has the current turn
        currentTurnCharacter = self.clientGame.getTurnOrder()[0].getGameToken().getTokenCharacter()
        # Update the Chatlog from the server, currently stores 10 lines of text
        self.chatLog.setText(self.clientUpdate.getChat())
        # Call function to move the tokens to locations indicated by server
        self.updateTokenPositions(tokenUpdates)

        #displays discarded cards button if a player leaves the game
        if self.clientGame.getDiscardedCards() != self.clientUpdate.getDiscardedCards() and self.discardedButtonFlag == False:
            self.discardedButton = ImageButton(self.managerList[3], imageFile="cardPile.png", buttonText=" ")
            self.discardedButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10)) + 125, int(HEIGHT/4) - 60)
            self.discardedButton.setWidthHeight(int(175), int(180))
            self.discardedButton.getButton().setManager(self.managerList[0])
            Label("Discarded", self.managerList[1], self.discardedButton.getXLoc(), self.discardedButton.getYLoc() + 180, 142, 20)
            self.discardedButtonFlag = True 

        for player in self.clientGame.getTurnOrder():
            if self.clientGame.getMyToken() == player.getGameToken():
                if player.getLostGame() == True:
                    print("You lost loser") 
                    pass


        if self.clientGame.getDiscardedCards() != self.clientUpdate.getDiscardedCards():
            self.clientGame.setDiscardedCards(self.clientUpdate.getDiscardedCards())

            if self.discardHand != None:
                self.discardHand.kill()

            # Create the panel to display the discarded cards
            self.discardHand = Panel(self.managerList[3], layerHeight=2)
            self.discardHand.setXLocYLoc(int(WIDTH), int(HEIGHT/3))
            self.discardHand.setWidthHeight(len(self.clientGame.getDiscardedCards())*142 + 20 + 10*len(self.clientGame.getDiscardedCards()), 215)
            self.discardHand.setVisibleLocation(int(WIDTH/2-self.discardHand.getWidth()/2))
            self.discardHand.setHiddenLocation(WIDTH)

            # cardXLoc allows cards to be placed a card distance apart plus the buffer value between them
            cardXLoc = -142
            buffer = 10
            i = 0


            # For each card in the player hand
            for card in self.clientGame.getDiscardedCards():
                # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
                print(str(card.getCardName()))
                self.discardHand.addImageButton(ImageButton(self.discardHand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190,container=self.discardHand.getContainer(), object_id="discardIB"+card.getCardName()))
                # hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card.getCardName()))
                if card.getCardCategory() == "weapon":
                    imageFormat = ".jpg"
                else:
                    imageFormat = ".png"
                # Set the image for the ImageButton
                self.discardHand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
                # Move the location of the next card in the hand
                cardXLoc += 142 + buffer
                i += 1

        # self.clientGame = self.clientUpdate
        # Update the client game turn order
        if tokenUpdates[0].getGameToken().getTokenCharacter() != currentTurnCharacter:
            self.clientGame.setTurnOrder(tokenUpdates)
            self.displayTurnOrder(self.clientGame.getTurnOrder(), self.managerList[1])
            # Identify whose turn it is and update label accordingly
            if self.myToken.getObjectId() != currentTurnCharacter:
                self.rollLabel.setText(currentTurnCharacter + "'s Turn")
            else:
                self.rollLabel.setText("Your Turn")
        

    # Hide the passed panel offscreen
    def hidePanel(self, panel):
        panel.setXLoc(panel.getHiddenLocation())
    
    # Move passed panel back on screen
    def showPanel(self, panel):
        panel.setXLoc(panel.getVisibleLocation())

    # Check if passed panel is hidden
    def checkHidden(self, panel):
        return panel.getXLoc() == panel.getHiddenLocation()

    # Update the displayed turn order images
    def displayTurnOrder(self, turnOrder, manager, initial=0):
        yLoc = 0
        i = 0
        # If this is the initial turn order creation, create the images
        if initial:
            for character in reversed(turnOrder):
                name = character.getGameToken().getTokenCharacter()
                # Add images to the turn order
                self.turnOrderImages.append(Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name))
                # Set yLoc for the next card to move it down to stagger the cards
                yLoc += 60
        # For subsequent runs, kill the existing images and recreate them with new turn order
        else:
            for image in self.turnOrderImages:
                image.kill()
            for character in reversed(turnOrder):
                name = character.getGameToken().getTokenCharacter()
                # Add images to the turn order
                self.turnOrderImages[i] = Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name)
                # Set yLoc for the next card to move it down to stagger the cards
                yLoc += 60
                i += 1

    # Update the token positions based on server locations
    def updateTokenPositions(self, tokenUpdates):
        for player in self.characterTokens:
            for token in tokenUpdates:
                if player.getObjectId() == token.getGameToken().getTokenCharacter():
                    currentLocation = self.gameGrid.grid[player.getRow()][player.getColumn()]
                    # Leave current location
                    currentLocation.setOccupied(0)
                    tokenRow = int(token.getGameToken().getRow())
                    tokenColumn = int(token.getGameToken().getColumn())
                    newLocation = self.gameGrid.grid[tokenRow][tokenColumn]
                    # Move token to new location
                    player.setXLocYLoc(newLocation.getXLoc(), newLocation.getYLoc())
                    player.setRowColumn(tokenRow, tokenColumn)
                    # Occupy new tile
                    newLocation.setOccupied(1)
    
    # Catch updates from the server                    
    def getUpdates(self, arg1, arg2):
        self.clientUpdate = self.netConn.catch()
