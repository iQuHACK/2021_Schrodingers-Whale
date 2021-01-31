import pygame
import os
import time

#  things to do:
# - title/start screen
# - create multiple colors for various tunnels?
# - colors of two other snakes
# - create "class" for snake (including the neighbor cells and the length of the snake)
# - are we having a score system?
# - create superposition, entanglement, quantum teleporting functions

pygame.init()


distance = 1000
display = pygame.display.set_mode((distance, distance))
pygame.display.set_caption("Tron")
# background = pygame.transform.scale(pygame.image.load('space.png'), (distance, distance))
# colors
GREY = (192, 192, 192)  
WHITE = (255, 255, 255)
ROSE = (255, 51, 153)
TEAL = (0, 0, 255)
BLACK = (0, 0, 0)
SKY = (158, 255, 250)
LIME = (178, 250, 102)
LAVENDER = (178, 102, 255)
FPS = 60
#player colors
p1_color = (0, 255, 255)
p2_color = (255, 0, 255)
# whale icon (player)
# WHALE_IMAGE = pygame.image.load('schrodingers_whale_1.png')

# global variable for players
players = list()
paths = list()

class Player:
    def __init__(self, x, y, b, c):
        """
        init method for class
        """
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.bearing = b  # player direction
        self.color = c
        # self.isTunnel = False  # is boost active
        # self.startTunnel = time.time()  # used to control boost length
        # self.tunnels = 2
        self.rect = pygame.Rect(self.x - 0, self.y - 1, 4, 2)  # player rect object

    def __draw__(self):
        """
        method for drawing player
        """
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 4, 2)  # redefines rect
        pygame.draw.rect(display, self.color, self.rect, 0)  # draws player onto screen

    def __move__(self):
        """
        method for moving the player
        """
        # if not self.isTunnel:  # player isn't currently boostin
        print("move method")
        self.x += self.bearing[0]
        self.y += self.bearing[1]

# tunneling function?
    # def __tunnel__(self):
    #     """
    #     starts the player boost
    #     """
    #     if self.tunnels > 0:
    #         self.tunnels -= 1
    #         self.isTunnel = True
    #         self.startTunnel = time.time()

#
def draw(win, rows, width):
    win.blit(display, (0,0)) # maybe background
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, WHITE, (0, i * gap), (width, i * gap))  # horizontal lines
        for j in range(rows):
            pygame.draw.line(win, WHITE, (j * gap, 0), (j * gap, width))  # vertical lines
    pygame.display.update()

def Player1_Movements(key, index): #NEED TO CODE THIS PART. can be implemented by moving the head of the snake to the desired location, popping the last element from the snake array
    if key == pygame.K_LEFT:  # Left
        players[index].bearing = (-2,0)
    elif key == pygame.K_RIGHT:  # right
        players[index].bearing = (2,0)
    elif key == pygame.K_UP:  # up
        players[index].bearing = (0,-2)
    elif key == pygame.K_DOWN:  # down
        players[index].bearing = (0,2)


def Player2_Movements(key, index): #NEED TO CODE THIS PART. can be implemented by moving the head of the snake to the desired location, popping the last element from the snake array
    if key == pygame.K_a:  # Left
        players[index].bearing = (-2,0)
    elif key == pygame.K_d:  # right
        players[index].bearing = (2,0)
    elif key == pygame.K_w:  # up
        players[index].bearing = (0,-2)
    elif key == pygame.K_s:  # down
        players[index].bearing = (0,2)

def main(win, width):
    rows = 40  # can change rows
    clock = pygame.time.Clock()

    p1 = Player(250,250,(0,2),p1_color)
    players.append(p1)
    paths.append((p1.rect, '1'))
    p2 = Player(distance - 250,distance - 250,(0,-2),p2_color)
    players.append(p2)
    paths.append((p2.rect,'2'))

    run = True
    new = False
    while run:
        clock.tick(FPS)
        draw(win, rows, width) #draws screen
        for event in pygame.event.get():  # check through all the events that have happened
            print("start")
            print(players[0].bearing)
            print(players[1].bearing)
            
            if event.type == pygame.QUIT:
                run = False
                break         
                
            for i in range(len(players)):
                print("in the for loop")
                if event.type == pygame.KEYDOWN:
                    print("key down")
                    print(event.key)
                    # if i % 2 != 0:
                    Player1_Movements(event.key, 0)
                    # else:
                    Player2_Movements(event.key, 1)

        for i in range(len(players)):    
            players[i].__draw__()
            print("drawn")
            players[i].__move__()
            print("moved")

        for p in paths:
            print(p)
            if new is True:  # empties the path - needs to be here to prevent graphical glitches
                path = []
                new = False
                break

            if p[1] == '1':
                pygame.draw.rect(display,p1_color,p[0],4)
            else:
                pygame.draw.rect(display,p2_color,p[0],4)

            # create if-statements for keys pressed -- move the snake in the desired direction
            # create condition for when the snakes intersect -- end game and print winner

    pygame.quit()


main(display, distance)