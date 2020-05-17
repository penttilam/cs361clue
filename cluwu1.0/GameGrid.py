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
    def clickedTile(self, event):

        if (event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED):
            xLocYLoc = str(event.ui_element.object_ids[0]).split(",")
            print("Button is Row:" + xLocYLoc[0] + ", column: " + xLocYLoc[1])
            print("is at pixels: " + str(self.grid[int(xLocYLoc[0])][int(xLocYLoc[1])].getXLoc())  + ", " + str(self.grid[int(xLocYLoc[0])][int(xLocYLoc[1])].getYLoc()))

            return self.grid[int(xLocYLoc[0])][int(xLocYLoc[1])].getClickedStatus(event)

    def __init__(self, windowWidth, windowHeight, screen, manager):
        self.grid = []
        self.windowHeight = windowWidth
        self.windowWidth = windowWidth
        badMove = []
        buttonNumber = -1
        for row in range(25):
            self.grid.append([])
            for column in range(24):
                buttonNumber = buttonNumber + 1
                xLocation = 15*30-3+column*32
                yLocation = 55 + row*31
                buttonId = str(row) + "," + str(column)
                # self.grid[row].append(Button("", manager, 17*30+column*30, 150 + row*30, 35, 35, object_id=str(buttonNumber)))
                self.grid[row].append(Button(str(buttonNumber), manager, xLocation, yLocation, 30, 30, object_id=str(buttonId)))
        #### SHRINE
        for x in range(7):
            badMove.append(str(x))            
        for x in range(25, 31):
            badMove.append(str(x))
        for x in range(49, 55):
            badMove.append(str(x))
        for x in range(74, 79):
            badMove.append(str(x))
        
        ### SCHOOL
        for x in range(8, 16):
            badMove.append(str(x))
        for x in range(33, 39):
            badMove.append(str(x))
        for x in range(57, 63):
            badMove.append(str(x))
        for x in range(81, 87):
            badMove.append(str(x))
        for x in range(105, 111):
            badMove.append(str(x))
        for x in range(129, 135):
            badMove.append(str(x))
        for x in range(153, 159):
            badMove.append(str(x))
        
        ###### CENTER
        for x in range(201, 206):
            badMove.append(str(x))
        for x in range(225, 230):
            badMove.append(str(x))
        for x in range(249, 254):
            badMove.append(str(x))        
        for x in range(273, 278):
            badMove.append(str(x))
        for x in range(297, 302):
            badMove.append(str(x))
        for x in range(321, 326):
            badMove.append(str(x))
        for x in range(345, 350):
            badMove.append(str(x))

        ###### LOVE HOTEL
        for x in range(215, 216):
            badMove.append(str(x))
        for x in range(232, 240):
            badMove.append(str(x))        
        for x in range(256, 264):
            badMove.append(str(x))
        for x in range(280, 288):
            badMove.append(str(x))
        for x in range(304, 312):
            badMove.append(str(x))
        for x in range(328, 336):
            badMove.append(str(x))
        for x in range(352, 360):
            badMove.append(str(x))
        for x in range(379, 384):
            badMove.append(str(x))
        for x in range(407, 408):
            badMove.append(str(x))
        
        #### Library
        for x in range(17, 25):
            badMove.append(str(x))
        for x in range(41, 49):
            badMove.append(str(x))
        for x in range(65, 74):
            badMove.append(str(x))
        for x in range(89, 97):
            badMove.append(str(x))
        for x in range(113, 120):
            badMove.append(str(x))
        for x in range(137, 144):
            badMove.append(str(x))
        for x in range(167, 168):
            badMove.append(str(x))
        
        ###### HOT SPRING
        for x in range(144, 150):
            badMove.append(str(x))
        for x in range(168, 175):
            badMove.append(str(x))
        for x in range(192, 199):
            badMove.append(str(x))
        for x in range(216, 223):
            badMove.append(str(x))
        for x in range(240, 246):
            badMove.append(str(x))
        for x in range(264, 265):
            badMove.append(str(x))

        ##############
        for x in range(416, 424):
            badMove.append(str(x))
        for x in range(440, 448):
            badMove.append(str(x))
        for x in range(464, 472):
            badMove.append(str(x))
        for x in range(488, 496):
            badMove.append(str(x))
        for x in range(512, 520):
            badMove.append(str(x))
        for x in range(536, 544):
            badMove.append(str(x))
        for x in range(562, 566):
            badMove.append(str(x))
        for x in range(586, 590):
            badMove.append(str(x))

        ####  MANGA SHOP
        for x in range(456, 461):
            badMove.append(str(x))
        for x in range(480, 486):
            badMove.append(str(x))
        for x in range(504, 510):
            badMove.append(str(x))
        for x in range(528, 534):
            badMove.append(str(x))
        for x in range(552, 559):
            badMove.append(str(x))
        for x in range(577, 585):
            badMove.append(str(x))


        ########### 
        for x in range(288, 294):
            badMove.append(str(x))
        for x in range(312, 318):
            badMove.append(str(x))
        for x in range(336, 342):
            badMove.append(str(x))
        for x in range(360, 366):
            badMove.append(str(x))
        for x in range(384, 390):
            badMove.append(str(x))
        for x in range(408, 409):
            badMove.append(str(x))


        ########## BEACH        
        for x in range(450, 456):
            badMove.append(str(x))
        for x in range(474, 480):
            badMove.append(str(x))
        for x in range(498, 504):
            badMove.append(str(x))
        for x in range(522, 528):
            badMove.append(str(x))
        for x in range(546, 552):
            badMove.append(str(x))
        for x in range(569, 577):
            badMove.append(str(x))
        for x in range(591, 600):
            badMove.append(str(x))
        
        for remove in badMove:
            for row in range(25):
                for column in range(24):
                    if self.grid[row][column].text == remove:
                        self.grid[row][column].setXLocYLoc(windowWidth, windowHeight)