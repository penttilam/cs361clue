import pygame
import pygame_gui
from pygame.locals import *
from Button import Button

    #############################
    # width = 1600
    # height = 900
    ###############################
    # tileManager = pygame_gui.UIManager((width, height), './tileTheme.json')
    ###################################
    # background = pygame.Surface((width, height))
    # background.fill(manager.ui_theme.get_colour('dark_bg'))
    # addImage('./images/board.png', 1, background, width/2, height/2, width, height)
    
    ################################

    # testGrid = GameGrid(width, height, windowSurface, tileManager)

class GameGrid:
    def __init__(self, windowWidth, windowHeight, screen, manager):
        self.grid = []
        badMove = []
        buttonNumber = -1
        for row in range(24):
            self.grid.append([])
            for column in range(24):
                buttonNumber = buttonNumber + 1
                # self.grid[row].append(Button("", manager, 17*30+column*30, 150 + row*30, 35, 35, object_id=str(buttonNumber)))
                self.grid[row].append(Button(str(buttonNumber), manager, 17*30+column*30, 150 + row*30, 35, 35, object_id=str(buttonNumber)))
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
        for x in range(8, 15):
            badMove.append(str(x))
        for x in range(33, 38):
            badMove.append(str(x))
        for x in range(57, 62):
            badMove.append(str(x))
        for x in range(81, 86):
            badMove.append(str(x))
        for x in range(105, 110):
            badMove.append(str(x))
        for x in range(129, 134):
            badMove.append(str(x))
        for x in range(153, 158):
            badMove.append(str(x))
        
        ###### CENTER
        for x in range(225, 229):
            badMove.append(str(x))
        for x in range(249, 253):
            badMove.append(str(x))        
        for x in range(273, 277):
            badMove.append(str(x))
        for x in range(297, 301):
            badMove.append(str(x))
        for x in range(321, 325):
            badMove.append(str(x))
        for x in range(345, 349):
            badMove.append(str(x))

        ###### LOVE HOTEL
        for x in range(191, 192):
            badMove.append(str(x))
        for x in range(214, 216):
            badMove.append(str(x))
        for x in range(231, 240):
            badMove.append(str(x))        
        for x in range(255, 264):
            badMove.append(str(x))
        for x in range(279, 288):
            badMove.append(str(x))
        for x in range(303, 312):
            badMove.append(str(x))
        for x in range(327, 336):
            badMove.append(str(x))
        for x in range(354, 360):
            badMove.append(str(x))
        for x in range(382, 384):
            badMove.append(str(x))
        for x in range(407, 408):
            badMove.append(str(x))

        #### Library
        for x in range(16, 25):
            badMove.append(str(x))
        for x in range(40, 49):
            badMove.append(str(x))
        for x in range(64, 74):
            badMove.append(str(x))
        for x in range(88, 97):
            badMove.append(str(x))
        for x in range(112, 120):
            badMove.append(str(x))
        for x in range(136, 144):
            badMove.append(str(x))
        for x in range(166, 168):
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

        ##############
        for x in range(416, 421):
            badMove.append(str(x))
        for x in range(440, 445):
            badMove.append(str(x))
        for x in range(464, 469):
            badMove.append(str(x))
        for x in range(488, 493):
            badMove.append(str(x))
        for x in range(512, 517):
            badMove.append(str(x))
        for x in range(538, 539):
            badMove.append(str(x))
        for x in range(562, 563):
            badMove.append(str(x))

        ####  MANGA SHOP
        for x in range(432, 437):
            badMove.append(str(x))
        for x in range(456, 462):
            badMove.append(str(x))
        for x in range(480, 486):
            badMove.append(str(x))
        for x in range(504, 510):
            badMove.append(str(x))
        for x in range(528, 535):
            badMove.append(str(x))
        for x in range(552, 561):
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
        for x in range(384, 385):
            badMove.append(str(x))


        ########## BEACH        
        for x in range(423, 432):
            badMove.append(str(x))
        for x in range(447, 456):
            badMove.append(str(x))
        for x in range(471, 480):
            badMove.append(str(x))
        for x in range(495, 504):
            badMove.append(str(x))
        for x in range(519, 528):
            badMove.append(str(x))
        for x in range(543, 552):
            badMove.append(str(x))
        for x in range(564, 577):
            badMove.append(str(x))
        
        for remove in badMove:
            for row in range(24):
                for column in range(24):
                    if self.grid[row][column].object_ids == remove:
                        self.grid[row][column].kill()
        for row in range(24):
            for column in range(24):
                color = (255, 255, 255)
                pygame.draw.rect(screen, color, [windowWidth*column, windowHeight*row, windowWidth, windowHeight])



        


# 17,9 17,10