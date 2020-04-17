import pygame
import time

print("hello world")
# Intialize pygame
pygame.init()

# Var naming: Methods should be verbs in lowerCamelCase or a multi-word name that begins 
# with a verb in lowercase; that is, with the first letter lowercase and the first letters 
# of subsequent words in uppercase.


# creat a window/screen
screen = pygame.display.set_mode((800, 600))


# Title and Icon
pygame.display.set_caption("Clue game")
icon = pygame.image.load("hiroshi-normal-icon.jpg")
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load("player.png")
playerX = 350
playerY = 300
playerX_change = 0


def player():
    screen.blit(playerImg,(playerX,playerY)) #blit(): draw one image onto another


#room
roomImg = pygame.image.load("weeb_room.jpg")
roomX = 0
roomY = 0

def room():
    screen.blit(roomImg,(roomX,roomY)) #blit(): draw one image onto another

#cave
caveImg = pygame.image.load("cave.png")
caveX = 100
caveY = 300

def cave():
    screen.blit(caveImg, (caveX,caveY))
# Game loop
running = True
while running:

    screen.fill((0,0,0)) 

    #playerX -=0.1  # The move mechanics


    for event in pygame.event.get(): # get events from users
        if event.type == pygame.QUIT:
            running = False

    
        #If the keystroke is pressed check whether its right or left 
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left is pressed\n")
                    playerX -=10
                if event.key == pygame.K_RIGHT:
                    print("right is pressed\n")
                    playerX +=10
                if event.key == pygame.K_UP:
                    print("up is pressed\n")
                    playerY -=10
                if event.key == pygame.K_DOWN:
                    print("right is pressed\n")
                    playerY +=10

        if playerX == 120 and playerY == 350:
            room()
            pygame.display.update()#to refresh the screen
            time.sleep(5)

    
        print(playerX, playerY)
        cave()
        player()
        pygame.display.update()#to refresh the screen
