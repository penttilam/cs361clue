import pygame
# import pygame_gui
from pygame.locals import *
from Button import Button

class GameGrid:
    def __init__(self, windowWidth, windowHeight, manager):
        self.grid = []
        self.windowHeight = windowWidth
        self.windowWidth = windowWidth
        
        # Identify all locations that are not moveable to on the main board via the displayed spaces
        badMove = []
        fileIn = open('./rooms/rooms', 'r')
        badMove = fileIn.read().split(" ") 
        fileIn.close()
        # Populate the rooms with the grid locations that are inside them
        roomsIn = "233 304 258 260 262 257 330 309" 
        hotelRooms = roomsIn.split(" ") 
        roomsIn = "451 571 524 502 547 527 573 475"
        beachRooms = roomsIn.split(" ") 
        roomsIn = "137 143 90 92 23 70 67 95"
        libraryRooms = roomsIn.split(" ") 
        roomsIn = "105 155 156 61 13 11 59 117 109"
        schoolRooms = roomsIn.split(" ") 
        roomsIn = "460 456 483 531 529 505 530 532"
        mangaRooms = roomsIn.split(" ") 
        roomsIn = "289 365 364 361 337 362 314 316"
        tearoomRooms = roomsIn.split(" ") 
        roomsIn = "78 72 29 27 5 28 51 4"
        shrineRooms = roomsIn.split(" ") 
        roomsIn = "417 422 464 471 466 514 469 517 539 564"
        karaokeRooms = roomsIn.split(" ") 
        roomsIn = "198 243 168 195 216 218 197 170"
        hotspringRooms = roomsIn.split(" ") 
        self.rooms = [("school", schoolRooms),("library", libraryRooms), ("lovehotel", hotelRooms), ("beach", beachRooms), ("karaoke", karaokeRooms), ("mangastore", mangaRooms), ("tearoom", tearoomRooms), ("hotspring", hotspringRooms), ("shrine", shrineRooms)]

        # Identify all spaces that are viable exits to each room
        schoolExits = [104, 179, 180]
        libraryExits = [161, "secret143"]
        hotelExits = [209, 303]
        beachExits = [427, "secret571"]
        karaokeExits = [463, 393, 398, 472]
        mangastoreExits = [461, "secret456"]
        tearoomExits = [265, 366]
        hotspringExits = [199, 267]
        shrineExits = [102, "secret72"]

        self.roomExits = [("school", schoolExits), ("library", libraryExits), ("lovehotel", hotelExits), ("beach", beachExits), ("karaoke", karaokeExits), ("mangastore", mangastoreExits), ("tearoom", tearoomExits), ("hotspring", hotspringExits), ("shrine", shrineExits)]
        buttonNumber = -1
        # Identify spaces that act as secret doors
        secretDoors = [72, 143, 456, 571]
        # Identify spaces that are entrances to rooms
        doors = [78, 105, 137, 155, 156, 198, 233, 243, 289, 304, 365, 417, 422, 471, 451, 460, 464]
        # Build the grid
        for row in range(25):
            self.grid.append([])
            for column in range(24):
                # Used to assign single digit representation for each grid square
                buttonNumber = buttonNumber + 1
                # Space out the grid to match the graphical display
                xLocation = 15*30-15+column*32
                yLocation = 60 + row*30
                # Assign the object Id to be a comma separated tuple of the row/column location on board
                buttonId = str(row) + "," + str(column)
                self.grid[row].append(Button(str(buttonNumber), manager, xLocation, yLocation, 30, 30, object_id=str(buttonId)))
                # Set the button location to the appropriate row/column
                newGridLocation = self.grid[row][column]
                newGridLocation.setRowColumn(row, column)
                # Default all locations to "outside". "outside" is the movement squares of the main board
                newGridLocation.setLocation("outside")
                # If the grid number is identified as a door to a room, assign that button to be considered in that room
                if (int(newGridLocation.text) in doors):
                    # rooms is a tuple of a room name and a list of room grid locations
                    for room in self.rooms:
                        if (newGridLocation.text in room[1]):
                            newGridLocation.setLocation(room[0])
                # If the grid number is identified as a secret door in a room, assign that button to be considered in that room
                if (newGridLocation.text in secretDoors):
                    for room in self.rooms:
                        # rooms is a tuple of a room name and a list of room grid locations
                        if (newGridLocation.text in room[1]):
                            newGridLocation.setLocation(room[0])
                # If the grid number is identified as a location that cannot be move to, assign that button to be not be moveable to
                if (newGridLocation.text in badMove):
                    # rooms is a tuple of a room name and a list of room grid locations
                    for room in self.rooms:
                        if (newGridLocation.text in room[1]):
                            newGridLocation.setLocation(room[0])
                    # Disable the grid location so it cannot be clicked on
                    newGridLocation.disable()

    # clickedTile function takes an event variable and a token (player or weapon) and determines if the button clicked was a tile
    def clickedTile(self, event, token):
        # set return variable "moved" to false
        moved = False
        # If the button was clicked
        if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED):
            # If the clicked on the chatlog, go back and continue calling function
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

    # enterARoom function takes a token (player or weapon) and a room name. This allows the calling function to assign any token
    # to a room when an accusation occurs or in general course of game movement
    def enterARoom(self, token, roomName):
        #set return value to false
        moved = False
        # Assign the token location to the room desired
        token.setLocation(roomName)
        # Find the possible tiles in the room the token could be placed on
        possibleRoomPositions = self.findButtonByLocation(token.getLocation())
        # Check to see if the 
        for tile in possibleRoomPositions:
            # If no one is occupying the tile move to it and occupy it
            if not tile.getOccupied():
                token.setXLocYLoc(tile.getXLoc(), tile.getYLoc())
                token.setRowColumn(tile.getRow(), tile.getColumn())
                self.grid[tile.getRow()][tile.getColumn()].setOccupied(1)
                moved = True
                break
        return moved

    # exitARoom function takes a token (player) and a grid row and column number and allows player to exit a room
    def exitARoom(self, token, row, column):
        #set return value to false
        moved = False
        gridLocation = self.grid[row][column]
        # Check if the token is in a certain room
        for room in self.roomExits:
                if(token.getLocation() == room[0]):
                    # If the player clicked on a secret door, move them to the appropriate room
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
                        # Enter a room and return result to moved
                        moved = self.enterARoom(token, token.getLocation())
                        break
                    # If player clicked on one of the tiles that is a valid room exit, un-occupy current space, move to exit space and occupy it
                    elif (int(gridLocation.getText()) in room[1] and not gridLocation.getOccupied()):
                        self.grid[token.getRow()][token.getColumn()].setOccupied(0)
                        token.setLocation(gridLocation.getLocation())
                        token.setXLocYLoc(gridLocation.getXLoc(), gridLocation.getYLoc())
                        token.setRowColumn(gridLocation.getRow(), gridLocation.getColumn())
                        gridLocation.setOccupied(1)
                        moved = True
        return moved

    # movePlayerToken takes a token (player) and a grid row and column and attempts to move the player
    def movePlayerToken(self, token, row, column):
        #set return value to false
        moved = False
        newLocation = self.grid[row][column]
        currentLocation = self.grid[token.getRow()][token.getColumn()]
        # check distance away from current location
        checkXMove = token.getRow() - row
        checkYMove = token.getColumn() - column
        # If the player is not inside a room, the move is 1 square away, not diaganol, and the tile is not already occupied
        if (token.getLocation() == "outside" and (-2 < checkXMove < 2) and (-2 < checkYMove < 2) and (abs(checkXMove) + abs(checkYMove) < 2) and not newLocation.getOccupied()):
            # If player is moving along a path and not entering a room, move them and occupy new tile
            if (newLocation.getLocation() == "outside"):
                # Free the current space that player occupied
                currentLocation.setOccupied(0)
                # Move the player to the new tile
                token.setXLocYLoc(newLocation.getXLoc(), newLocation.getYLoc())
                token.setRowColumn(row, column)
                # Occupy new tile
                newLocation.setOccupied(1)
                moved = True
            # If player is moving into a room, find the first non-occupied space in that room and move to it
            else:
                for room in self.roomExits:
                    for exits in room[1]:
                        if room[0] == newLocation.getLocation() and str(currentLocation.getText()) == str(exits):
                            # Free the current space that player occupied
                            currentLocation.setOccupied(0)
                            # Enter the room and return result to moved variable
                            moved = self.enterARoom(token, newLocation.getLocation())
                            break
        else:
            moved = self.exitARoom(token, row, column)
            
        return moved

    
    # findButtonByNumer takes a tile number and returns a tuple of the row and column of the tile
    def findButtonByNumber(self, number):
        for row in range(25):
            for col in range(24):
                if (self.grid[row][col].text == number):
                    return (row, col)

    # findButtonByLocation takes a tile location and returns a list of tile locations inside that location
    def findButtonByLocation(self, locationText):
        buttonList = []
        for row in range(25):
            for col in range(24):
                if (self.grid[row][col].getLocation() == locationText and not self.grid[row][col].button.is_enabled):
                    buttonList.append(self.grid[row][col])
        return buttonList