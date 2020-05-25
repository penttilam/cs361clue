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
from UpdateThread import *
import time
from multiprocessing.pool import ThreadPool

random.seed()
width = 1680
height = 900
hiddenPanelLocation = width

def getUpdates(netConn, updates):
    clientUpdate = netConn.catch()
    print("catch 1: " + str(clientUpdate))
    clientUpdate = netConn.catch()
    print("catch 2: " + str(clientUpdate))
    return clientUpdate

def gameBoard(netConn):
    clock = pygame.time.Clock()
    updates = 0
    windowSurface = pygame.display.set_mode((width, height))
    netConn.send("game.create")
    clientThreads = ThreadPool(processes=1)
    threadResults = clientThreads.apply_async(getUpdates, (netConn, updates))
    # threading.Thread(target=getUpdates, args=(netConn))?
    clientUpdate = threadResults.get()
    clientGame = clientUpdate
    print (clientGame)
    # clientGame = netConn.catch()
    # clientGame = clientThread.join(1/1000)
    # List of managers used to set themes
    managerList = []
    layer0 = pygame_gui.UIManager((width, height), './tileTheme.json')
    managerList.append(layer0)
    layer1 = pygame_gui.UIManager((width, height), './ourTheme.json')
    managerList.append(layer1)

    layer2 = pygame_gui.UIManager((width, height), './panelTheme.json')
    managerList.append(layer2)
    layer3 = pygame_gui.UIManager((width, height), './panelTheme.json')
    managerList.append(layer3)
    
    turnOrderImages = displayTurnOrder(clientGame.getTurnOrder(), layer1, initial=1)
    chatLog = TextBox(layer1)
    chatInput = InputBox(layer1)

    gameGrid = GameGrid(width, height, layer0)

    Image('board.png', layer0, 0, 0, width, height)

    

    # Button to display player's hand of cards
    handButton = ImageButton(layer3, imageFile= 'weebcard.png', buttonText=" ")
    handButton.setXLocYLoc(int((width*16)/17-(width/10)), int(height/4) - 60)
    handButton.setWidthHeight(int(142), int(180))
    Label("Look at Hand", layer1, handButton.getXLoc(), handButton.getYLoc() + 180, 142, 20)

    # Button to roll the dice
    diceButton = ImageButton(layer0, imageFile='dice.png', buttonText=" ")
    diceButton.setXLocYLoc(int((width*16)/17-(width/10)), int(height/4)+180)
    diceButton.setWidthHeight(int(120), int(120))
    Label("Roll", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 100, 142, 20)
    rollLabel = Label("Current Moves: 0", layer1, diceButton.getXLoc(), diceButton.getYLoc() - 20, 142, 20)
    myRoll = -1
    
    # End turn Button
    endTurnButton = Button("End turn", layer1, diceButton.getXLoc(), diceButton.getYLoc() + 40 , 90, 30)
    
    # Button to display the player's notebook
    # notebookButton = Button('Notebook', layer3)
    notebookButton = ImageButton(layer3, imageFile='notepadbutton.png', buttonText=" ")
    notebookButton.setXLocYLoc(int((width*16)/17-(width/10))-60, int(height/2+height/20)+39)
    notebookButton.setWidthHeight(int(330), int(365))
    Label("Check Notes", layer3, notebookButton.getXLoc() + int(notebookButton.getWidth()/2), notebookButton.getYLoc() + int(notebookButton.getHeight()/2) + 90, 100, 20)

    #initilization of the notebook panel
    notebook = Panel(layer3, layerHeight=2)
    notebook.setXLocYLoc(int(width), int(height/8))
    notebook.setWidthHeight(int(width/4), int(3*height/4))
    notebook.addImage(Image("clueNotepad.png", layer3, 0, 0, notebook.getWidth(), notebook.getHeight(), container=notebook.getContainer()))
    notebook.setVisibleLocation(int((width*3)/8))
    notebook.setHiddenLocation(width)
    # Creates a Button object to allow interaction with checkboxe buttons
    checkBoxButton = createNotebook(notebook)

    characterList = ["scarlet", "white", "mustard", "green", "peacock", "plum"]
    characterTokens = []
    playerCards = []
    # playerCards = [("scarlet", "Card"),("white", "Card"),("mustard", "Card"),("green", "Card"),("peacock", "Card"),("plum", "Card")]
    playerCards = clientGame.getMyCards()
    #initilization of the hand panel
    hand = Panel(layer3, layerHeight=2)
    hand.setXLocYLoc(int(width), int(height/3))
    hand.setWidthHeight(len(playerCards)*142 + 20 + 10*len(playerCards), 215)
    hand.setVisibleLocation(int(width/2-hand.getWidth()/2))
    hand.setHiddenLocation(width)
    
    cardXLoc = -142
    buffer = 10
    i=0
    for card in playerCards:
        hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card.getCardName()))
        if card.getCardCategory() == "weapon":
            imageFormat = ".jpg"
        else:
            imageFormat = ".png"
        hand.getImageButton(i).setImage(card.getCardName() + card.getCardCategory() + imageFormat)
        cardXLoc += 142 + buffer
        i+=1
    
    for character in characterList:
        if clientGame.getMyToken().getTokenCharacter() == character:
            tokenFileExtension = "mytoken.png"
        else:
            tokenFileExtension = ".png"
        characterTokens.append(Image(str(character) + tokenFileExtension, layer2, 0, 0, 30, 30, object_id=character))


    
    characterTokens[0].setXLocYLoc(947, 60)
    characterTokens[0].setRowColumn(0, 16)
    gameGrid.grid[0][16].setOccupied(1)
    characterTokens[1].setXLocYLoc(1171, 270)
    characterTokens[1].setRowColumn(7, 23)
    gameGrid.grid[18][0].setOccupied(1)
    characterTokens[2].setXLocYLoc(883, 780)
    characterTokens[2].setRowColumn(24, 14)
    gameGrid.grid[24][14].setOccupied(1)
    characterTokens[3].setXLocYLoc(723, 780)
    characterTokens[3].setRowColumn(24, 9)
    gameGrid.grid[24][9].setOccupied(1)
    characterTokens[4].setXLocYLoc(435, 600)
    characterTokens[4].setRowColumn(18, 0)
    gameGrid.grid[7][23].setOccupied(1)
    characterTokens[5].setXLocYLoc(435, 210)
    characterTokens[5].setRowColumn(5, 0)
    characterTokens[5].setLocation("outside")
    gameGrid.grid[5][0].setOccupied(1)
    


    for x in range(6):
        if (clientGame.getMyToken().getTokenCharacter() == characterTokens[x].getObjectId()):
            myToken = characterTokens[x]
            break
    # gameGrid.enterARoom(characterTokens[5], "lovehotel")

    if myToken.getObjectId() != clientGame.getTurnOrder()[0].getTokenCharacter():
        rollLabel.setText(clientGame.getTurnOrder()[0].getTokenCharacter() + "'s Turn")
    else:
        rollLabel.setText("Your Turn")
    threadResults = clientThreads.apply_async(getUpdates, (netConn, updates))
    loopCounter = 0
    while True:
        myTurn = clientGame.getMyTurn()
        if myTurn:
            endTurnButton.setXLoc(diceButton.getXLoc() + diceButton.getWidth() + 10)
            time_delta = clock.tick(60) / 1000.0
        else:
            endTurnButton.setXLoc(width)
            time_delta = clock.tick(60) / 1000.0
        
        # if not clientUpdate.isAlive():
        #     clientUpdate = threading.Thread(target=getUpdates, args=(netConn, updates))
        #     clientUpdate.start()


        for event in pygame.event.get():
            if event.type == QUIT:
                netConn.send("quit")
                raise SystemExit
                                   
            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                if chatInput.getText() != "" and event.type == KEYDOWN and event.key == K_RETURN:
                    netConn.send("game.chat.add:" + chatInput.getText())
                    chatInput.setText("")
                elif (not checkHidden(notebook)):
                    notebook.panel.process_event(event)
                    # Cycles Notebook checkboxes between blank, X, and checked
                    if event.type == KEYDOWN and event.key == K_ESCAPE or notebookButton.getClickedStatus(event):
                        hidePanel(notebook)
                    elif handButton.getClickedStatus(event):
                        hidePanel(notebook)
                        showPanel(hand)
                    elif (checkBoxButton.getClickedStatus(event)): 
                        if event.ui_element.text == " ":
                            event.ui_element.set_text("X")
                        elif event.ui_element.text == "X":
                            event.ui_element.set_text(u'\u2713')
                        elif event.ui_element.text == u'\u2713':
                            event.ui_element.set_text(" ")
                        
                elif (not checkHidden(hand)):
                    hand.panel.process_event(event)
                    if event.type == KEYDOWN and event.key == K_ESCAPE or handButton.getClickedStatus(event):
                        hidePanel(hand)
                    elif notebookButton.getClickedStatus(event):
                        hidePanel(hand)
                        showPanel(notebook)
                    else:
                        for clicked in range(int(hand.getHandSize()/2)):
                            if (hand.getImageButton(clicked).getClickedStatus(event)):
                                break
                else:
                    # Open the Notebook
                    if notebookButton.getClickedStatus(event):
                        # Shows Notebook, hides Hand if it is open
                        if checkHidden(notebook):
                            showPanel(notebook)
                            hidePanel(hand)
                        else: # Hides Notebook
                            hidePanel(notebook)
                    
                    # Open the Hand
                    elif handButton.getClickedStatus(event):
                        # Shows Hand, hides Notebook if it is open
                        if checkHidden(hand):
                            showPanel(hand)
                            hidePanel(notebook)
                        else: # Hides the hand
                            hidePanel(hand)
                    
                    # End player turn
                    elif endTurnButton.getClickedStatus(event):
                        turnEnded = netConn.send("game.turn").split(":")
                        if turnEnded[2] == "success":
                            endTurnButton.setXLoc(width)
                            netConn.send("game.update")
                            # clientUpdate = netConn.catch()
                            clientGame.setTurnOrder(clientUpdate.getTurnOrder())
                            myTurn = clientGame.getMyTurn()
                            myRoll = -1
                            turnOrderImages = displayTurnOrder(clientGame.getTurnOrder(), layer1, turnOrderImages)
                            if myToken.getObjectId() != clientGame.getTurnOrder()[0].getTokenCharacter():
                                rollLabel.setText(clientGame.getTurnOrder()[0].getTokenCharacter() + "'s Turn")
                            else:
                                rollLabel.setText("Your Turn")

                    elif diceButton.getClickedStatus(event):
                        if myRoll == -1 and myTurn:
                            myRoll = 100
                            # myRoll = random.randrange(1,6,1)
                            rollLabel.setText("You rolled: " + str(myRoll))
                        elif myTurn:
                            rollLabel.setText("Current Moves: " + str(myRoll))
                        else:
                            rollLabel.setText("You rolled: " + str(myRoll))

                    # Moves token
                    elif myTurn and myRoll > 0 and checkHidden(notebook) and checkHidden(hand) and gameGrid.clickedTile(event, myToken):
                        netConn.send("game.move:"+str(myToken.getRow())+"."+str(myToken.getColumn()))
                        myRoll-=1
                        rollLabel.setText("Current Moves: " + str(myRoll))

        if not myTurn:
        # if loopCounter >= 50:

            # netConn.send("game.update")

            # clientUpdate = netConn.catch()
            clientUpdate = threadResults.get()
            tokenUpdates = clientUpdate.getTurnOrder()
            chatLog.addText(clientUpdate.getChatUpdate())
            updatePlayerPositions(characterTokens, tokenUpdates, gameGrid)
            loopCounter = 0
            if tokenUpdates[0].getTokenCharacter() != clientGame.getTurnOrder()[0].getTokenCharacter():
                print(tokenUpdates)
                clientGame.setTurnOrder(tokenUpdates)
                turnOrderImages = displayTurnOrder(clientGame.getTurnOrder(), layer1, turnOrderImages)
                if myToken.getObjectId() != clientGame.getTurnOrder()[0].getTokenCharacter():
                    rollLabel.setText(clientGame.getTurnOrder()[0].getTokenCharacter() + "'s Turn")
                else:
                    rollLabel.setText("Your Turn")
            threadResults = clientThreads.apply_async(getUpdates, (netConn, updates))



            
        # Update events based on clock ticks
        for each in managerList:
            each.process_events(event)
            each.update(time_delta)
            each.draw_ui(windowSurface)

        pygame.display.update()
        loopCounter+=1

def hidePanel(panel):
    panel.setXLoc(panel.getHiddenLocation())
        
def showPanel(panel):
    panel.setXLoc(panel.getVisibleLocation())

def checkHidden(panel):
    return (panel.getXLoc() == panel.getHiddenLocation())

def displayTurnOrder(turnOrder, manager, turnOrderImages=[], initial=0):
    yLoc = 0
    i = 0
    if initial:
        for character in reversed(turnOrder):
            name = character.getTokenCharacter()
            turnOrderImages.append(Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name))
            yLoc += 60
    else:
        for image in turnOrderImages:
            image.kill()
        for character in reversed(turnOrder):
            name = character.getTokenCharacter()
            turnOrderImages[i] = Image(name + "Head.png", manager, 90, yLoc + 90, 142, 190, object_id="turn"+name)
            yLoc += 60
            i += 1
    return turnOrderImages

def updatePlayerPositions(playerList, tokenUpdates, gameGrid):
    for player in playerList:
        for updatePlayer in tokenUpdates:
            if (player.getObjectId() == updatePlayer.getTokenCharacter()):
                gameGrid.grid[player.getRow()][player.getColumn()].setOccupied(0)
                player.setXLocYLoc(gameGrid.grid[int(updatePlayer.getTokenXLoc())][int(updatePlayer.getTokenYLoc())].getXLoc(), gameGrid.grid[int(updatePlayer.getTokenXLoc())][int(updatePlayer.getTokenYLoc())].getYLoc())
                player.setRowColumn(int(updatePlayer.getTokenXLoc()), int(updatePlayer.getTokenYLoc()))
                gameGrid.grid[player.getRow()][player.getColumn()].setOccupied(1)
