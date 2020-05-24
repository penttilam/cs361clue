import pygame
import pygame_gui
from pygame.locals import *
from Button import Button

    
    # width = 1680
    # height = 900

    ##############################
    # tileManager = pygame_gui.UIManager((width, height), './tileTheme.json')
    # managerList.append(tileManager)    
    # ##################################
    # background = pygame.Surface((width, height))
    # background.fill(manager.ui_theme.get_colour('dark_bg'))
    # addImage('./images/board.png', 1, background, width/2, height/2, width, height)
    
    ###############################


class GameGrid:
    def __init__(self, windowWidth, windowHeight, manager):
        self.grid = []
        self.windowHeight = windowWidth
        self.windowWidth = windowWidth
        
        badMove = []
           
        fileIn = open('./rooms/rooms', 'r')
        badMove = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/hotelrooms.txt', 'r')
        hotelRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/beachrooms.txt', 'r')
        beachRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/libraryrooms.txt', 'r')
        libraryRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/schoolrooms.txt', 'r')
        schoolRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/mangarooms.txt', 'r')
        mangaRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/teashoprooms.txt', 'r')
        tearoomRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/shrinerooms.txt', 'r')
        shrineRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/karaokerooms.txt', 'r')
        karaokeRooms = fileIn.read().split(" ") 
        fileIn.close()
        fileIn = open('./rooms/hotspringrooms.txt', 'r')
        hotspringRooms = fileIn.read().split(" ") 
        fileIn.close()

        self.rooms = [("school", schoolRooms),("library", libraryRooms), ("lovehotel", hotelRooms), ("beach", beachRooms), ("karaoke", karaokeRooms), ("mangastore", mangaRooms), ("tearoom", tearoomRooms), ("hotspring", hotspringRooms), ("shrine", shrineRooms)]
        schoolExits = [104, 179, 180]
        libraryExits = [161, "secret143"]
        hotelExits = [209,303]
        beachExits = [427, "secret570"]
        karaokeExits = [463, 393, 398, 472]
        mangastoreExits = [461, "secret456"]
        tearoomExits = [265, 366]
        hotspringExits = [199, 267]
        shrineExits = [102, "secret72"]

        self.roomExits = [("school", schoolExits), ("library", libraryExits), ("lovehotel", hotelExits), ("beach", beachExits), ("karaoke", karaokeExits), ("mangastore", mangastoreExits), ("tearoom", tearoomExits), ("hotspring", hotspringExits), ("shrine", shrineExits)]
        buttonNumber = -1
        secretDoors = [72, 143, 456, 570]
        doors = [78,105,137,155,156,198,233,243,289, 304, 365, 417, 422, 471, 451, 460, 464]
        for row in range(25):
            self.grid.append([])
            for column in range(24):
                buttonNumber = buttonNumber + 1
                xLocation = 15*30-15+column*32
                yLocation = 60 + row*30
                buttonId = str(row) + "," + str(column)
                self.grid[row].append(Button(str(buttonNumber), manager, xLocation, yLocation, 30, 30, object_id=str(buttonId)))
                self.grid[row][column].setRowColumn(row, column)
                self.grid[row][column].setLocation("outside")
                if (int(self.grid[row][column].text) in doors):
                    for room in self.rooms:
                        if (self.grid[row][column].text in room[1]):
                            self.grid[row][column].setLocation(room[0])
                if (self.grid[row][column].text in secretDoors):
                    for room in self.rooms:
                        if (self.grid[row][column].text in room[1]):
                            self.grid[row][column].setLocation(room[0])
                if (self.grid[row][column].text in badMove):
                    for room in self.rooms:
                        if (self.grid[row][column].text in room[1]):
                            self.grid[row][column].setLocation(room[0])
                            
                    # self.grid[row][column].setWidthHeight(0, 0)
                    # self.grid[row][column].setText("")
                    self.grid[row][column].disable()

    def clickedTile(self, event, token):
        moved = False
        if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED):
            if(event.ui_element.object_ids[0]=="chatlog"):
                return moved
            # Take the object ID of the element clicked and split it out (grid tile IDs are "row,column")
            xLocYLoc = event.ui_element.object_ids[0].split(",")
            row = int(xLocYLoc[0])
            column = int(xLocYLoc[1])
            gridLocation = self.grid[row][column]
            # If the button was clicked, call the move function
            if (gridLocation.getClickedStatus(event)):
                moved = self.movePlayerToken(token, row, column)
        return moved

    def enterARoom(self, token, roomName):
        token.setLocation(roomName)
        possibleRoomPositions = self.findButtonByLocation(token.getLocation())
        for button in possibleRoomPositions:
            # If no one is occupying the square move to it and occupy it
            if not button.getOccupied():
                token.setXLocYLoc(button.getXLoc(), button.getYLoc())
                token.setRowColumn(button.getRow(), button.getColumn())
                self.grid[button.getRow()][button.getColumn()].setOccupied(1)
                moved = True
                break
        return moved

    def exitARoom(self, token, row, column):
        moved = False
        gridLocation = self.grid[row][column]
        for room in self.roomExits:
                if(token.getLocation() == room[0]):
                    if "secret" + str(gridLocation.text) in room[1]:
                        self.grid[token.getRow()][token.getColumn()].setOccupied(0)
                        if(room[0] == "beach"):
                            token.setLocation("shrine")
                        elif(room[0] == "shrine"):
                            token.setLocation("beach")
                        elif(room[0] == "mangastore"):
                            token.setLocation("library")
                        elif(room[0] == "library"):
                            token.setLocation("mangastore")
                        possibleExits = self.findButtonByLocation(token.getLocation())
                        for button in possibleExits:
                            if not button.getOccupied():
                                token.setXLocYLoc(button.getXLoc(), button.getYLoc())
                                token.setRowColumn(button.getRow(), button.getColumn())
                                button.setOccupied(1)
                                moved = True
                                break
                    elif (int(gridLocation.getText()) in room[1] and not gridLocation.getOccupied()):
                        self.grid[token.getRow()][token.getColumn()].setOccupied(0)
                        token.setLocation(gridLocation.getLocation())
                        token.setXLocYLoc(gridLocation.getXLoc(), gridLocation.getYLoc())
                        token.setRowColumn(gridLocation.getRow(), gridLocation.getColumn())
                        gridLocation.setOccupied(1)
                        moved = True
        return moved

    def movePlayerToken(self, token, row, column):
        moved = False
        gridLocation = self.grid[row][column]
        # check distance away from current location
        checkXMove = token.getRow() - row
        checkYMove = token.getColumn() - column
        # If the player accused or is not inside a room, the move is only 1 square away, the move is not diaganol, and the space is not already occupied
        if (token.getLocation() == "outside" and (-2 < checkXMove < 2) and (-2 < checkYMove < 2) and (abs(checkXMove) + abs(checkYMove) < 2) and not gridLocation.getOccupied()):
            # Free the current space that player occupied
            self.grid[token.getRow()][token.getColumn()].setOccupied(0)
            # If player is moving along a path and not entering a room, move them and occupy new space
            if (gridLocation.getLocation() == "outside"):
                token.setXLocYLoc(gridLocation.getXLoc(), gridLocation.getYLoc())
                token.setRowColumn(row, column)
                gridLocation.setOccupied(1)
                moved = True
            # If player is moving into a room, find the first non-occupied space in that room and move to it
            else:
                moved = self.enterARoom(token, gridLocation.getLocation())
        else:
            moved = self.exitARoom(token, row, column)
            
        return moved

    

    def findButtonByNumber(self, number):
        for row in range(25):
            for col in range(24):
                if (self.grid[row][col].text == number):
                    return (row, col)

    def findButtonByLocation(self, locationText):
        buttonList = []
        for row in range(25):
            for col in range(24):
                if (self.grid[row][col].getLocation() == locationText and not self.grid[row][col].button.is_enabled):
                    buttonList.append(self.grid[row][col])
        return buttonList
                        
        #  "images":
        #  {
        #     "disabled_image":
        #     {
        #         "path": "images/disabled_button.png"
        #     }
         # "normal_image":
            # {
            #     "path": "images/tile.png"
            # },
        
        #  },
            
        # for remove in badMove:
        #     for row in range(25):
        #         for column in range(24):
        #             if self.grid[row][column].text == remove:
