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
from clientNetwork import Network
from clientCard import ClientCards
from clientGame import ClientGame
from clientToken import ClientToken
from TextBox import *
from InputBox import *
# from clientChat import *
from Label import Label
import threading
import time
WIDTH = 1680
HEIGHT = 900

class GameBoard:
    def __init__(self, netConn):
        self.characterTokens = []
        self.weaponTokens = []
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
        self.lostGame = False
        self.refuteHand = None
        self.windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.waitingForRefute = False

    def gameBoard(self):

        accused = [None, None, None] 

        # Set for use in updating displays
        self.clock = pygame.time.Clock()

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
        layer4 = pygame_gui.UIManager((WIDTH, HEIGHT), './notebookPanelTheme.json')
        self.managerList.append(layer4)
        
        # Display the background
        
        background = pygame.Surface((WIDTH, HEIGHT))
        self.windowSurface.blit(background, (0, 0))
        # Image('board.png', layer0, 0, 0, WIDTH, HEIGHT) # Un-comment to view grid numbers during game
        # Create the grid the player clicks to interact with the game board
        self.gameGrid = GameGrid(WIDTH, HEIGHT, layer0)
       

        # Set cards in player hand
        self.playerCards = self.clientGame.getMyCards()

        # Set full deck for player
        self.fullDeck = self.clientGame.getFullDeck()  

        # Button to display the player's notebook
        notebookButton = Button(manager=layer0, buttonText=" ")
        notebookButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10))-45, int(HEIGHT/2+HEIGHT/20))
        notebookButton.setWidthHeight(int(420), int(460))

        # ImageButton to display player's hand of cards
        handCards = len(self.playerCards)
        handButton = ImageButton(layer3, imageFile="cardback" + str(handCards) + ".png", buttonText=" ")
        handButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10))-60, int(HEIGHT/4) - 90)
        handButton.setWidthHeight(int(142), int(180))
        handButton.getButton().setManager(layer0)
        Label("Your Cards", layer1, handButton.getXLoc(), handButton.getYLoc() + 180, 142, 20)
        Image('board.png', layer0, 0, 0, WIDTH, HEIGHT) #Un-comment to display board without grid numbers for normal gameplay
        handButton.getImage().setImage("cardback" + str(handCards) + ".png")

        # Display the turn order of players and display
        self.displayTurnOrder(self.clientGame.getTurnOrder(), layer1, initial=1)

        # Set layer the chatlog and input will be displayed on
        self.chatLog = TextBox(layer1)
        chatInput = InputBox(layer1)

        # ImageButton to roll the dice
        diceButton = ImageButton(layer0, imageFile='dieRoll.png', buttonText=" ")
        diceButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10))-30, int(HEIGHT/4)+160)
        diceButton.setWidthHeight(int(80), int(80))
        Label("Roll", layer1, diceButton.getXLoc() + 10, diceButton.getYLoc() + 90, 60, 20)
        self.rollLabel = Label("Current Moves: 0", layer1, diceButton.getXLoc() - 30, diceButton.getYLoc() - 30, 142, 20)
        # myRoll should always be -1 unless it is that player's turn
        myRoll = -1

        # End turn Button
        endTurnButton = Button("End turn", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 25, 90, 30)

        # Initilization of the notebook panel
        notebook = Panel(layer4, layerHeight=2)
        notebook.setXLocYLoc(int(WIDTH), int(HEIGHT/8))
        notebook.setWidthHeight(int(WIDTH/4), int(3*HEIGHT/4))
        notebook.addImage(Image("clueNotepad.png", layer4, 0, 0, notebook.getWidth(), notebook.getHeight(), container=notebook.getContainer()))
        notebook.setVisibleLocation(int((WIDTH*3)/8))
        notebook.setHiddenLocation(WIDTH)

        # Creates a Button object to allow interaction with checkbox buttons
        checkBoxButton = createNotebook(notebook)

        # Accuse Button
        accuseButton = Button("Accuse", layer1, handButton.getXLoc(), 20, 90, 30, object_id="accuseButton")
        accuseButton.setXLoc(WIDTH) 
        # Suggest Button
        suggestButton = Button("Suggest", layer1, handButton.getXLoc(), 80, 90, 30, object_id="suggestButton")
        suggestButton.setXLoc(WIDTH) 
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
        accuseText = TextBox(layer3, "It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.", xLoc=1069, yLoc=450, width=190, height=195, container=accuseHand.getContainer(), layer=1, objectId="accuseText", wrapToHeight=True)
        # Accusation Submit Button
        submitAccuse = Button("Accuse", layer3, 1090, 535, 90, 30, container=accuseHand.getContainer())

        # Create the panel to display the suggestion cards
        suggestHand = Panel(layer3, layerHeight=2)
        suggestHand.setXLocYLoc(int(WIDTH), int(HEIGHT/3) - 225)
        suggestHand.setWidthHeight(7*142 + 105, 410)
        suggestHand.setVisibleLocation(int(WIDTH/2-suggestHand.getWidth()/2))
        suggestHand.setHiddenLocation(WIDTH)

        suggestText = TextBox(layer3, "It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.", xLoc=920, yLoc=170, width=170, height=195, container=suggestHand.getContainer(), layer=1, objectId="suggestText", wrapToHeight=True)
        # Accusation Submit Button
        submitSuggest = Button("Suggest", layer3, 955, 255, 90, 30, container=suggestHand.getContainer())

        # cardXLoc allows cards to be placed a card distance apart plus the buffer value between them
        cardXLoc = -142
        buffer = 10
        i = 0
        # For each card in the player hand
        for card in self.playerCards:
            # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
            hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card.getCardName()))
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
            # If token is player, assign token to myToken. Assigned here instead of above due 
            # to the [i] location not existing until the Image is appended above
            if tokenFileExtension == "mytoken.png":
                self.myToken = self.characterTokens[i]
            self.characterTokens[i].setLocation("outside")
            i += 1
        weaponList = ["dakimakura", "katana", "manga", "bento", "curse", "mecha"]
        # For each weapon, create a game image
        i = 0
        for weapons in weaponList:
            tokenFileExtension = "weapon.png"
            # Add the image to the character tokens
            self.weaponTokens.append(Image(str(weapons) + tokenFileExtension, layer2, 0, 0, 30, 30, object_id=weapons))
            i += 1
        self.updateWeaponPositions(self.clientGame.getWeaponTokens())

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

        y = 10
        i = 0
        # For each card in the the deck
        for cardType in reversed(self.fullDeck):
            cardXLoc = -142
            for card in cardType:
                if card.getCardCategory() == "location":
                    y -= 200
                    break
                # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
                suggestHand.addImageButton(ImageButton(suggestHand.getManager(), cardXLoc + 142 + buffer, y, 142, 190, container=suggestHand.getContainer(), object_id="suggestHandIB"+card.getCardCategory(), buttonText=card.getCardName()))
                imageFormat = ".png"
                # Set the image for the ImageButton
                suggestHand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
                cardXLoc += 142 + buffer
                i += 1
            y += 200
        weaponSuggestButton = Button("", layer3, container=suggestHand.getContainer(), object_id = "suggestHandIBweapon", xLoc=WIDTH)
        peopleSuggestButton = Button("", layer3, container=suggestHand.getContainer(), object_id = "suggestHandIBpeople", xLoc=WIDTH)
        

        

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
        Image(self.myToken.getObjectId() + "notebook.png", layer0, diceButton.getXLoc() - 120, diceButton.getYLoc() + 130, 550, 600)
        # Set starting tile to not be occupiable again on first turn
        self.myToken.addMove(self.gameGrid.grid[self.myToken.getRow()][self.myToken.getColumn()].getText())
        suggested = False
        # Game loop
        while True:

            
            time_delta = self.clock.tick(60) / 1000.0
            
            # Check to see if the server sent the client anything
            clientThreads.join(1/1000)
            # if server sent something, the thread will not be alive
            if not clientThreads.is_alive():
                # If the object sent back is not a string, process it
                if type(self.clientUpdate) != type(""):
                    # If someone refuted your suggestion, hide any panels you may have open
                    if self.clientUpdate.getRefuteCard() != None:
                        self.hidePanel(notebook)
                        self.hidePanel(hand)
                        self.hidePanel(accuseHand)
                        self.hidePanel(suggestHand)
                        if self.discardHand != None:
                            self.hidePanel(self.discardHand)
                    # If you are the closest person in turn order with a card to refute a suggestion, hide any panels you may have open
                    if self.clientUpdate.getSuggestCards() != None:
                        self.hidePanel(notebook)
                        self.hidePanel(hand)
                        self.hidePanel(accuseHand)
                        self.hidePanel(suggestHand)
                        if self.discardHand != None:
                            self.hidePanel(self.discardHand)
                    self.processClientUpdates()
                # Start the thread back up
                clientThreads = threading.Thread(target=self.getUpdates, args=(None, None))
                clientThreads.start()


            # check if it's the player's turn
            myTurn = self.clientGame.getMyTurn()
            if myTurn:
                # Display and end turn button for the player next to the die
                if not self.waitingForRefute:
                    endTurnButton.setXLoc(diceButton.getXLoc() + diceButton.getWidth() + 10)
                accuseButton.setXLoc(diceButton.getXLoc()) 
                # check if player is in a room AND that they did not start the turn in that room
                if self.myToken.getLocation() != "outside" and self.myToken.getMoveHistory()[0] != self.myToken.getLocation() and not suggested:
                    suggestButton.setXLoc(diceButton.getXLoc())
                # if they started turn in room, hide suggestion button
                elif self.myToken.getLocation() != "outside" and self.myToken.getLocation() not in self.myToken.getMoveHistory():
                    suggestButton.setXLoc(WIDTH) 
                if myRoll == -1:
                    diceButton.setImage("dieRoll.png")
                    self.rollLabel.setText("Your Turn")
            else:
                self.rollLabel.setText(self.clientGame.getTurnOrder()[0].getGameToken().getTokenCharacter() + "'s Turn")
                # Hide the end turn button off screen
                endTurnButton.setXLoc(WIDTH)
                accuseButton.setXLoc(WIDTH)
                suggestButton.setXLoc(WIDTH)
        
            # Get interactions with the game
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                
                # If the player clicked a button or pressed a key
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:

                    # If the notebook is visible, set the notebook to handle all events that come in to prevent clickthrough to the board
                    if (not self.checkHidden(notebook)):
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

                    # If the discarded cards is visible, set the discarded cards to handle all events that come in to prevent clickthrough to the board
                    elif self.discardedButtonFlag and (not self.checkHidden(self.discardHand)):
                        self.discardHand.panel.process_event(event)
                        # If the player clicks the discard image again or hits escape key, close the discarded cards
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

                    # If the accuse cards is visible, set the accuse cards to handle all events that come in to prevent clickthrough to the board
                    elif (not self.checkHidden(accuseHand)):
                        accuseHand.panel.process_event(event)
                        # If the player clicks the accuse button again or hits escape key, close the accuse cards
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
                        # If the player clicks the discard hand button, display it and hide the hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.hidePanel(accuseHand)
                            self.showPanel(self.discardHand)

                        elif peopleButton.getClickedStatus(event):
                            person = event.ui_element.text
                        elif locationButton.getClickedStatus(event):
                            location = event.ui_element.text
                        elif weaponButton.getClickedStatus(event):
                            weapon = event.ui_element.text
                        elif submitAccuse.getClickedStatus(event): 
                            if not (person == None and location == None and weapon == None):
                                self.netConn.send("game.accuse:" + person + "." + location + "." + weapon)
                                person = "_____"
                                location = "_____"
                                weapon = "_____"
                                self.hidePanel(accuseHand)
                        accuseText.addText("It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.")

                    # If the suggest cards is visible, set the accuse cards to handle all events that come in to prevent clickthrough to the board
                    elif (not self.checkHidden(suggestHand)):
                        location = self.myToken.getLocation()
                        suggestText.addText("It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.")
                        suggestHand.panel.process_event(event)
                        # If the player clicks the suggest button again or hits escape key, close the suggest hand
                        if event.type == KEYDOWN and event.key == K_ESCAPE or accuseButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                        # If the player clicks the notebook button, display it and hide the suggest hand
                        elif notebookButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                            self.showPanel(notebook)
                        # If the player clicks the hand button, display it and hide the suggest hand
                        elif handButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                            self.showPanel(hand)
                        # If the player clicks the discard hand button, display it and hide the suggest hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                            self.showPanel(self.discardHand)
                        # If the player clicks the suggest hand button, display it and hide the suggest hand
                        elif suggestButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                        # If the player clicks the accuse hand button, display it and hide the suggest hand
                        elif accuseButton.getClickedStatus(event):
                            self.hidePanel(suggestHand)
                            self.showPanel(accuseHand)
                        elif peopleSuggestButton.getClickedStatus(event):
                            person = event.ui_element.text
                        elif weaponSuggestButton.getClickedStatus(event):
                            weapon = event.ui_element.text
                        elif submitSuggest.getClickedStatus(event): 
                            if not (person == "_____" and weapon == "_____"):
                                for people in self.characterTokens:
                                    if people.getObjectId() == person:
                                        self.gameGrid.enterARoom(people, location)
                                for weapons in self.weaponTokens:
                                    if weapons.getObjectId() == weapon:
                                        self.gameGrid.enterARoom(weapons, location)
                                self.netConn.send("game.suggest:" + person + "." + location + "." + weapon)
                                person = "_____"
                                weapon = "_____"
                                # Prevent movement after making a suggestion
                                myRoll = 0
                                endTurnButton.setXLoc(WIDTH)
                                self.waitingForRefute = True
                                self.hidePanel(suggestHand)
                                suggested = True
                                suggestButton.setXLoc(WIDTH)
                        suggestText.addText("It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.")

                    else:
                        if chatInput.getText() != "" and event.type == KEYDOWN and event.key == K_RETURN:
                            self.netConn.send("game.chat.add:" + chatInput.getText())
                            # Blank out the chat input box
                            chatInput.setText("")
                        if chatInput.getInputBox().focused and event.type == KEYDOWN and (event.key == K_w or event.key == K_a or event.key == K_s or event.key == K_d):
                            pass
                        # Open the Notebook
                        elif notebookButton.getClickedStatus(event):
                            self.showPanel(notebook)
                        
                        # Open the Hand
                        elif handButton.getClickedStatus(event):
                            self.showPanel(hand)

                        # Open the discard hand
                        elif self.discardedButtonFlag and self.discardedButton.getClickedStatus(event):
                            self.showPanel(self.discardHand)

                        # Open the accuse hand
                        elif accuseButton.getClickedStatus(event):
                            self.showPanel(accuseHand)

                        # Open the suggest hand
                        elif suggestButton.getClickedStatus(event):
                            location = self.myToken.getLocation()
                            suggestText.addText("It was <b>" + person + "</b> in the <b>" + location + "</b> with the <b>" + weapon +"</b>.")
                            self.showPanel(suggestHand)
                        
                        # End player turn, send command to server
                        elif endTurnButton.getClickedStatus(event):
                            self.netConn.send("game.turn")
                            # Hide end turn button
                            endTurnButton.setXLoc(WIDTH)
                            # reset myRoll to -1
                            myRoll = -1
                            suggested = False
                            self.myToken.clearMoveHistory()
                            # Set current token location to not be movable to again on the next turn, make room not re-enterable as well if inside a room
                            if self.myToken.getLocation() != "outside":
                                self.myToken.addMove(self.myToken.getLocation())
                            else:
                                self.myToken.addMove(self.gameGrid.grid[self.myToken.getRow()][self.myToken.getColumn()].getText())
                            

                        # Roll the die
                        elif diceButton.getClickedStatus(event):
                            # If it's the player's turn and they haven't rolled yet, roll the die and store in myRoll
                            if myRoll == -1 and myTurn:
                                # myRoll = 80 # Testing remnant!
                                myRoll = random.randrange(1,7,1)
                                diceButton.setImage("die" + str(myRoll) + ".png")
                                self.rollLabel.setText("You rolled: " + str(myRoll))
                            # If player has already rolled this turn, indicate how many moves they have left
                            elif myTurn:
                                self.rollLabel.setText("Current Moves: " + str(myRoll))
                            # If it is not the player's turn, roll for fun.
                            else:
                                diceButton.setImage("die" + str(random.randrange(1,6,1)) + ".png")

                        # Moves token if it is the player's turn, they have moves left, the notebook and hand are not visible and they clicked on a valid game tile
                        elif myTurn and myRoll > 0 and self.checkHidden(notebook) and self.checkHidden(hand) and self.gameGrid.clickedTile(event, self.myToken):
                            self.netConn.send("game.move:" + str(self.myToken.getRow()) + "." + str(self.myToken.getColumn()) + "." + self.myToken.getLocation())
                            # Decrease die roll by 1
                            myRoll -= 1
                            self.rollLabel.setText("Moves Left: " + str(myRoll))
                            if myRoll > -1:
                                diceButton.setImage("die" + str(myRoll) + ".png")
            
            # Update events based on clock ticks
            for each in self.managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(self.windowSurface)
            pygame.display.update()

    # Handle events received from the server
    def processClientUpdates(self):
        # Store the current turn order
        tokenUpdates = self.clientUpdate.getTurnOrder()
        suggestionMove = self.clientUpdate.getSuggestionMove()
        weaponUpdates = self.clientUpdate.getWeaponTokens()
        # Store the character who has the current turn
        currentTurnCharacter = self.clientGame.getTurnOrder()[0].getGameToken().getTokenCharacter()
        # Update the Chatlog from the server, currently stores 10 lines of text
        self.chatLog.setText(self.clientUpdate.getChat())
        # Call function to move the tokens to locations indicated by server
        self.updateTokenPositions(tokenUpdates)
        if suggestionMove != None:
            self.updateTokenPositions(suggestionMove)
        
        self.updateWeaponPositions(weaponUpdates)

        #displays discarded cards button if a player leaves the game
        if self.clientGame.getDiscardedCards() != self.clientUpdate.getDiscardedCards() and self.discardedButtonFlag == False:
            self.discardedButton = ImageButton(self.managerList[3], imageFile="cardPile.png", buttonText=" ")
            self.discardedButton.setXLocYLoc(int((WIDTH*16)/17-(WIDTH/10)) + 115, int(HEIGHT/4) - 60)
            self.discardedButton.setWidthHeight(int(142), int(180))
            self.discardedButton.getButton().setManager(self.managerList[0])
            Label("View Discards", self.managerList[1], self.discardedButton.getXLoc(), self.discardedButton.getYLoc() + 180, 142, 20)
            self.discardedButtonFlag = True 
        
        
        for player in self.clientUpdate.getTurnOrder():
            if player.getWonLostGame() == True:
                if self.myToken.getObjectId() == player.getGameToken().getTokenCharacter():
                    print("You're a weiner")
                    # Trigger WINNER SCREEN HERE
                    winScreen = Image("win.png", self.managerList[3], width=WIDTH, height=HEIGHT)
                    self.managerList[3].draw_ui(self.windowSurface)
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            # Quit when window X button is clicked
                            if event.type == QUIT:
                                self.netConn.send("quit")
                                raise SystemExit
                            # Display menu options if splash screen is clicked
                            if event.type == KEYDOWN and event.key == K_RETURN:
                                self.netConn.send("quit")
                                raise SystemExit
                else:
                    print("You lost loser")
                    # Trigger LOSER SCREEN HERE
                    loseScreen = Image("lose.png", self.managerList[3], width=WIDTH, height=HEIGHT)
                    self.managerList[3].draw_ui(self.windowSurface)
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            # Quit when window X button is clicked
                            if event.type == QUIT:
                                self.netConn.send("quit")
                                raise SystemExit
                            # Display menu options if splash screen is clicked
                            if event.type == KEYDOWN and event.key == K_RETURN:
                                self.netConn.send("quit")
                                raise SystemExit
                        




        if self.clientGame.getDiscardedCards() != self.clientUpdate.getDiscardedCards():
            self.showDiscardedCards()

        # Update the client game turn order
        if tokenUpdates[0].getGameToken().getTokenCharacter() != currentTurnCharacter:
            self.clientGame.setTurnOrder(tokenUpdates)
            self.displayTurnOrder(self.clientGame.getTurnOrder(), self.managerList[1])

        # If someone refuted your suggestion, display the refuted card
        if self.clientUpdate.getRefuteCard() != None:
            self.showRefuteCard()

        # If you are the closest person in turn order with a card to refute a suggestion, display cards to choose to refute
        if self.clientUpdate.getSuggestCards() != None:
            self.refuteSuggestion()
            
    def showDiscardedCards(self):
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
            self.discardHand.addImageButton(ImageButton(self.discardHand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=self.discardHand.getContainer(), object_id="discardIB"+card.getCardName()))
            imageFormat = ".png"
            # Set the image for the ImageButton
            self.discardHand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
            # Move the location of the next card in the hand
            cardXLoc += 142 + buffer
            i += 1

    def refuteSuggestion(self):

        # Create the panel to display the cards to pick to show to rebut a suggestion
        refuteHand = Panel(self.managerList[3], layerHeight=2)
        refuteHand.setWidthHeight((len(self.clientUpdate.getSuggestCards()))*142 + (len(self.clientUpdate.getSuggestCards()) + 2) * 10 + 8, 304)
        refuteHand.setXLocYLoc(int(WIDTH/2-refuteHand.getWidth()/2), int(HEIGHT/2) - int(refuteHand.getHeight()/2))
        refuteCard = "_____"
        refuteText = TextBox(self.managerList[3], "You have chosen <b>" + refuteCard + "</b>.", xLoc=int(refuteHand.getWidth()/2) - 110, yLoc=10, width=140, height=30, container=refuteHand.getContainer(), layer=1, objectId="refuteText", wrapToHeight=True)
        # Accusation Submit Button
        submitRefute = Button("Refute", self.managerList[3], int(refuteHand.getWidth()/2) - 45, 250, 90, 30, container=refuteHand.getContainer())
        # cardXLoc allows cards to be placed a card distance apart plus the buffer value between them
        cardXLoc = -142
        buffer = 10
        i = 0
        # For each card in the player hand
        for card in self.clientUpdate.getSuggestCards():
            # Create an ImageButton and add it to the hand, clean up this code once all images share the same extension type
            refuteHand.addImageButton(ImageButton(refuteHand.getManager(), cardXLoc + 142 + buffer, 55, 142, 190, buttonText=card.getCardName(), container=refuteHand.getContainer(), object_id="refuteHandIB"+card.getCardName()))
            imageFormat = ".png"
            # Set the image for the ImageButton
            refuteHand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
            # Move the location of the next card in the hand
            cardXLoc += 142 + buffer
            i += 1
        while(True):
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                # If the player clicked a button or pressed a key
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    refuteHand.panel.process_event(event)
                    # If the player clicks the notebook image again or hits escape key, close the notebook
                    for x in range(len(self.clientUpdate.getSuggestCards())):
                        if refuteHand.getImageButton(x).getClickedStatus(event):
                            refuteCard = event.ui_element.text
                    refuteText.addText("You have chosen <b>" + refuteCard + "</b>.")
                    if submitRefute.getClickedStatus(event): 
                        if not (refuteCard == "_____" ):
                            self.netConn.send("game.refute:" + refuteCard)
                            refuteHand.kill()
                            submitRefute.kill()
                            refuteText.kill()
                            self.clientUpdate.setSuggestCards(None)
                            return
                # Update events based on clock ticks
                for each in self.managerList:
                    each.process_events(event)
                    each.update(time_delta)
                    each.draw_ui(self.windowSurface)
            pygame.display.update()

    def showRefuteCard(self):
        # Create the panel to display the refuted card
        refuteCard = Panel(self.managerList[3], layerHeight=2)
        refuteCard.setWidthHeight(172, 300)
        refuteCard.setXLocYLoc(int(WIDTH/2-int(refuteCard.getWidth()/2)), int(HEIGHT/2) - int(refuteCard.getHeight()/2))
        refuteImage = Image(self.clientUpdate.getRefuteCard().getCardName() + self.clientUpdate.getRefuteCard().getCardCategory() + ".png", self.managerList[3], 10, 60, 142, 190, container=refuteCard.getContainer())
        Label("This card wrong", self.managerList[3], xLoc=int(refuteCard.getWidth()/2) - 80, yLoc=10, width=160, height=20, container=refuteCard.getContainer())
        # Accusation Submit Button
        okayButton = Button("Okay", self.managerList[3], int(refuteCard.getWidth()/2-30), 250, 60, 30, container=refuteCard.getContainer())
        while(True):
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.netConn.send("quit")
                    raise SystemExit
                # If the player clicked a button or pressed a key
                if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                    refuteCard.panel.process_event(event)
                    # If the player clicks the notebook image again or hits escape key, close the notebook
                    if okayButton.getClickedStatus(event): 
                        refuteCard.kill()
                        refuteImage.kill()
                        okayButton.kill()
                        self.waitingForRefute = False
                        self.clientUpdate.setRefuteCard(None)
                        return
                # Update events based on clock ticks
                for each in self.managerList:
                    each.process_events(event)
                    each.update(time_delta)
                    each.draw_ui(self.windowSurface)
            pygame.display.update()

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
                self.turnOrderImages.append(Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id=name))
                # Set yLoc for the next card to move it down to stagger the cards
                yLoc += 60
        # For subsequent runs, kill the existing images and recreate them with new turn order
        else:
            for image in self.turnOrderImages:
                image.kill()
            for character in reversed(turnOrder):
                name = character.getGameToken().getTokenCharacter()
                # Add images to the turn order
                self.turnOrderImages[i] = Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id=name)
                # Set yLoc for the next card to move it down to stagger the cards
                yLoc += 60
                i += 1

    # Update the token positions based on server locations
    def updateTokenPositions(self, tokenUpdates):
        for player in self.characterTokens:
            for token in tokenUpdates:
                if player.getObjectId() == token.getGameToken().getTokenCharacter() and token.getGameToken().getLocation() == "outside":
                    self.gameGrid.movePlayerToken(player, int(token.getGameToken().getRow()), int(token.getGameToken().getColumn()), 0)
                elif player.getObjectId() != token.getGameToken().getTokenCharacter():
                    pass
                elif player.getObjectId() == token.getGameToken().getTokenCharacter() and token.getGameToken().getLocation() != "outside":
                    self.gameGrid.enterARoom(player, token.getGameToken().getLocation())
        
    # Update the token positions based on server locations
    def updateWeaponPositions(self, weaponUpdates):
        i=0
        for weapon in weaponUpdates:
            self.gameGrid.enterARoom(self.weaponTokens[i], weapon.getLocation())
            i += 1
    
    # Catch updates from the server                    
    def getUpdates(self, arg1, arg2):
        self.clientUpdate = self.netConn.catch()
