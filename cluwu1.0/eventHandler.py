import pygame
import pygame_gui
from pygame.locals import *

def gameBoard(gameName, userId):
  
    width = 1680
    height = 900

    # List of managers used to set themes
    managerList = []
    windowSurface = pygame.display.set_mode((width, height))
    # Catch the game data and populate list of objects
    # gameInfo = netConn.catch()
    # characterList = 

    manager = pygame_gui.UIManager((width, height), './ourTheme.json')
    managerList.append(manager)
    tileManager = pygame_gui.UIManager((width, height), './tileTheme.json')
    managerList.append(tileManager)
    hideManager = pygame_gui.UIManager((width, height), './panelTheme.json')
    managerList.append(hideManager)
    playerManager = pygame_gui.UIManager((width, height), './panelTheme.json')
    managerList.append(playerManager)
    panelManager = pygame_gui.UIManager((width, height), './panelTheme.json')
    managerList.append(panelManager)

    gameGrid = GameGrid(width, height, windowSurface, tileManager)

    Image('board.png', manager, 0, 0, width, height)
    preventClickingBoard = Image('board.png', hideManager, width, 0, width, height)

    # Button to display player's hand of cards
    handButton = Button('Hand', panelManager)
    handButton.setXLocYLoc(int((width*16)/17-(width/10)), int(height/2))
    handButton.setWidthHeight(int(width/10), int(height/20))

    # Button to display the player's notebook
    # notebookButton = Button('Notebook', panelManager)
    notebookButton = ImageButton(panelManager, imageFile='notepadbutton.png', buttonText=" ")
    notebookButton.setXLocYLoc(int((width*16)/17-(width/10))-60, int(height/2+height/20)+40)
    notebookButton.setWidthHeight(int(330), int(365))

    #initilization of the notebook panel
    notebook = Panel(panelManager, layerHeight=2)
    notebook.setXLocYLoc(int(width), int(height/8))
    notebook.setWidthHeight(int(width/4), int(3*height/4))
    notebook.addImage(Image("clueNotepad.PNG", panelManager, 0, 0, notebook.getWidth(), notebook.getHeight(), container=notebook.getContainer()))
    
    # Creates a Button object to allow interaction with checkboxe buttons
    checkBoxButton = createNotebook(notebook)


    characterList = ["scarlet", "white", "mustard", "green", "peacock", "plum"]
    characterTokens = []
    playerCards = [("scarlet", "Card"),("white", "Card"),("mustard", "Card"),("green", "Card"),("peacock", "Card"),("plum", "Card")]
    #initilization of the hand panel
    hand = Panel(panelManager, layerHeight=2)
    hand.setXLocYLoc(int(width), int(height/3))
    hand.setWidthHeight(len(playerCards)*142 + 20 + 10*len(playerCards), 215)
    handVisibleLocation = int(width/2-(len(playerCards)/2)*142)
    
    cardXLoc = -142
    buffer = 10
    i=0
    for card in playerCards:
        hand.addImageButton(ImageButton(hand.getManager(), cardXLoc + 142 + buffer, 10, 142, 190, container=hand.getContainer(), object_id="HandIB"+card[0]))
        hand.getImageButton(i).setImage(card[0] + card[1] + ".jpg")
        cardXLoc += 142 + buffer
        i+=1
    
    for character in characterList:
        characterTokens.append(Image(str(character) +".png", playerManager, 0, 0, 30, 30, object_id=character))
    
    characterTokens[0].setXLocYLoc(947, 60)
    characterTokens[1].setXLocYLoc(435, 600)
    characterTokens[2].setXLocYLoc(883, 780)
    characterTokens[3].setXLocYLoc(723, 780)
    characterTokens[4].setXLocYLoc(1171, 270)
    characterTokens[5].setXLocYLoc(435, 210)
    myToken = characterTokens[5]

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

            if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED) or event.type == KEYDOWN:
                if (not checkHidden(notebook)):
                    print("notebook took it")
                    notebook.panel.process_event(event)
                    # Cycles Notebook checkboxes between blank, X, and checked
                    if event.type == KEYDOWN and event.key == K_ESCAPE or notebookButton.getClickedStatus(event):
                        hidePanel(notebook)
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
                    else:
                        for clicked in range(int(hand.getHandSize()/2)):
                            if (hand.getImageButton(clicked).getClickedStatus(event)):
                                print("Clicked on "+ hand.getImageButton(clicked).getObjectId())
                                break
                    
                else:
                    # Open the Notebook
                    if notebookButton.getClickedStatus(event):
                        # Shows Notebook, hides Hand if it is open
                        if checkHidden(notebook):
                            showPanel(notebook, int((width*3)/8))
                            hidePanel(hand)
                            handButton.unselect()
                        else: # Hides Notebook
                            hidePanel(notebook)
                    
                    # Open the Hand
                    elif handButton.getClickedStatus(event):
                        # Shows Hand, hides Notebook if it is open
                        if checkHidden(hand):
                            handButton.select()
                            showPanel(hand, handVisibleLocation)
                            hidePanel(notebook)
                        else: # Hides the hand
                            hidePanel(hand)
                    
                    # Moves token
                    elif checkHidden(notebook) and checkHidden(hand) and gameGrid.clickedTile(event, myToken):
                        pass

            # Update events based on clock ticks
            for each in managerList:
                each.process_events(event)
                each.update(time_delta)
                each.draw_ui(windowSurface)

        pygame.display.update()