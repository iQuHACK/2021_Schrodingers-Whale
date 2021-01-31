#this file contains the intermediate process of getting the player to move on the board

import pygame

pygame.font.init()

distance = 800
display = pygame.display.set_mode((distance, distance))
pygame.display.set_caption("Hackathon")

font = pygame.font.SysFont('comicsans', 40)

img_x = 50
img_y = 400
# colors
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
ROSE = (255, 51, 153)
TEAL = (0, 0, 255)
BLACK = (0, 0, 0)
SKY = (158, 255, 250)
LIME = (178, 250, 102)
LAVENDER = (178, 102, 255)
RED = (255,0,0)
BLUE = (0,0,255)
PURPLE = (204, 0, 204)
colors = [RED, BLUE, PURPLE]
FPS = 60

# Store gate images
gate_images = []
gate_h = pygame.image.load('Gate_H')
gate_images.append(gate_h)
gate_x = pygame.image.load('Gate_X')
gate_images.append(gate_x)
gate_m = pygame.image.load('Gate_M')
gate_images.append(gate_m)



def draw(win):
    red_health_text = font.render("Current Qubit: " , 1, BLACK)
    win.blit(red_health_text, (20, 10))

    pygame.display.update()


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
        print("move method")
        self.x += self.bearing[0]
        self.y += self.bearing[1]


def Player_Movements(key, p1): #NEED TO CODE THIS PART. can be implemented by moving the head of the snake to the desired location, popping the last element from the snake array
    if key == pygame.K_LEFT:  # Left
        p1.bearing = (-2,0)
    elif key == pygame.K_RIGHT:  # right
        p1.bearing = (2,0)
    elif key == pygame.K_UP:  # up
        p1.bearing = (0,-2)
    elif key == pygame.K_DOWN:  # down
        p1.bearing = (0,2)

def main(win):
    p1_color = RED
    p1 = Player(250, 250, (0, 2), p1_color)
    paths = list()
    paths.append((p1.rect, '1'))

    imgWidth = 250
    imgHeight = 100
    for img in gate_images:
        img = pygame.transform.scale(img, (imgWidth, imgHeight))

    run = True
    clock = pygame.time.Clock()
    img_x = 50
    img_y = 400
    while run:
        clock.tick(FPS)
        draw(win)
        for img in gate_images:
            display.blit(img, (img_x, img_y))
            img_x += imgWidth + 20

        for event in pygame.event.get():  # check through all the events that have happened
            print("start")

            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                print("key down")
                print(event.key)
                Player_Movements(event.key, p1)

                p1.__draw__()
                print("drawn")
                p1.__move__()
                print("moved")

            # keyup to stop the continued movement of the line

            # create if-statements for keys pressed -- move the snake in the desired direction
            # create condition for when the snakes intersect -- end game and print winner
    pygame.quit()

main(display)