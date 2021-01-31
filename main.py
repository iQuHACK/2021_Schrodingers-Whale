#Base Code Credits to Stanely Godfrey
#https://github.com/stanley-godfrey/Tron-Pygame/

import pygame
import time
pygame.init()

BLACK = (0, 0, 0)  # colours for use in window
P1_COLOUR = (0, 255, 255)  # player 1 trail colour
P2_COLOUR = (255, 0, 255)  # player 2 trail colour


class Player:
    def __init__(self, x, y, b, c):
        """
        init method for class
        """
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.bearing = b  # player direction
        self.colour = c
        self.boost = False  # is boost active
        self.start_boost = time.time()  # used to control boost length
        self.boosts = 3
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # player rect object

    def __draw__(self):
        """
        method for drawing player
        """
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # redefines rect
        pygame.draw.rect(screen, self.colour, self.rect, 0)  # draws player onto screen

    def __move__(self):
        """
        method for moving the player
        """
        if not self.boost:  # player isn't currently boosting
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2

    def __boost__(self):
        """
        starts the player boost
        """
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


def new_game():
    new_p1 = Player(50, height / 2, (2, 0), P1_COLOUR)
    new_p2 = Player(width - 50, height / 2, (-2, 0), P2_COLOUR)
    return new_p1, new_p2


width, height = 600, 660  # window dimensions
offset = height - width  # vertical space at top of window
screen = pygame.display.set_mode((width, height))  # creates window
pygame.display.set_caption("Tron")  # sets window title

font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()  # used to regulate FPS
check_time = time.time()  # used to check collisions with rects

objects = list()  # list of all the player objects
path = list()  # list of all the path rects in the game
p1 = Player(50, (height- offset) / 2, (2, 0), P1_COLOUR)  # creates player
p2 = Player(width - 50, (height- offset) / 2, (-2, 0), P2_COLOUR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))

player_score = [0, 0]  # current player score

wall_rects = [pygame.Rect([0, offset, 15, height]) , pygame.Rect([0, offset, width, 15]),\
              pygame.Rect([width - 15, offset, 15, height]),\
              pygame.Rect([0, height - 15, width, 15])]  # outer walls of window

done = False
new = False

while not done:
    for event in pygame.event.get():  # gets all event in last tick
        if event.type == pygame.QUIT:  # close button pressed
            done = True
        elif event.type == pygame.KEYDOWN:  # keyboard key pressed
            # === Player 1 === #
            if event.key == pygame.K_w:
                objects[0].bearing = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].bearing = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].bearing = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].bearing = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            # === Player 2 === #
            if event.key == pygame.K_UP:
                objects[1].bearing = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].bearing = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].bearing = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].bearing = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()

    screen.fill(BLACK)  # clears the screen

    for r in wall_rects: pygame.draw.rect(screen, (42, 42, 42), r, 0)  # draws the walls

    for o in objects:
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False

        if (o.rect, '1') in path or (o.rect, '2') in path \
           or o.rect.collidelist(wall_rects) > -1:  # collided with path or wall
            # prevent player from hitting the path they just made
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()

                if o.colour == P1_COLOUR:
                    player_score[1] += 1
                else: player_score[0] += 1

                new = True
                new_p1, new_p2 = new_game()
                objects = [new_p1, new_p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
                break
        else:  # not yet traversed
            path.append((o.rect, '1')) if o.colour == P1_COLOUR else path.append((o.rect, '2'))

        o.__draw__()
        o.__move__()

    for r in path:
        print(r)
        if new is True:  # empties the path - needs to be here to prevent graphical glitches
            path = []
            new = False
            break
        if r[1] == '1': pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
        else: pygame.draw.rect(screen, P2_COLOUR, r[0], 0)

    # display the current score on the screen
    score_text = font.render('{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 153, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(width / 2)
    score_text_pos.centery = int(offset / 2)
    screen.blit(score_text, score_text_pos)

    pygame.display.flip()  # flips display
    clock.tick(60)  # regulates FPS

pygame.quit()