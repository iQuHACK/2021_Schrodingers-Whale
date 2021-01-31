import pygame
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute

pygame.font.init()

distance = 800
display = pygame.display.set_mode((distance, distance))
pygame.display.set_caption("Hackathon")

font = pygame.font.SysFont('comicsans', 40)



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
gates = []

# Quantum Circuit
qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
backend_sim = Aer.get_backend('qasm_simulator')

# Tracks variables for quantum gates and state
isHadamard = False
isX = False
isMeasured = False
qState = "|0>"

counts = {}


def draw(win):
    red_health_text = font.render("Current Qubit: " + qState, 1, WHITE)
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

    def __get_x__(self):
        return self.x
    def __get_y__(self):
        return self.y
    
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


class Gate:
    def __init__(self,x,y,width,height,imgurl):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.imgurl = imgurl

        self.gate = pygame.image.load(imgurl)
    
    def __returnimg__(self):
        return self.gate

    def __getp1x__(self): 
        print(self.x)
        return self.x
    def __getp1y__(self): 
        print(self.y)
        return self.y
    def __getp2x__(self): 
        print(self.x + self.width)
        return self.x + self.width
    def __getp2y__(self): 
        print(self.y + self.height)
        return self.y + self.height


def movePlayer(key, p1):
    if key == pygame.K_LEFT:  # Left
        p1.bearing = (-5,0)
    elif key == pygame.K_RIGHT:  # right
        p1.bearing = (5,0)
    elif key == pygame.K_UP:  # up
        p1.bearing = (0,-5)
    elif key == pygame.K_DOWN:  # down
        p1.bearing = (0,5)

# yLimit = 400
# xLimit 

def checkCollision(p1):
    isCollision = False
    whichGate = None
    for gate in gates:
        if p1.__get_x__() > gate.__getp1x__() and p1.__get_x__() < gate.__getp2x__() and p1.__get_y__() > gate.__getp1y__() and p1.__get_y__() < gate.__getp2y__():
            print("in gate")
            isCollision = True
            whichGate = gate
        # if p1.__get_y__() > gate.__getp1y__() or p1.__get_y__() < gate.__getp2y__():
        #     print("in gate")
        #     return True
        else:
            print("not in gate")
            isCollision = False

        return isCollision,whichGate

def main(win):
    p1_color = WHITE
    p1 = Player(250, 250, (0, 2), p1_color)
    paths = list()
    paths.append((p1.rect, '1'))

    imgWidth = 250
    imgHeight = 200
    img_x = 30
    img_y = 400

    gate_h = Gate(img_x,img_y,imgWidth,imgHeight,'Gate_H.png')
    gates.append(gate_h)
    gate_images.append(gate_h.__returnimg__())
    gate_x = Gate(img_x,img_y,imgWidth,imgHeight,'Gate_X.png')
    gates.append(gate_x)
    gate_images.append(gate_x.__returnimg__())
    gate_m = Gate(img_x,img_y,imgWidth,imgHeight,'Gate_M.png')
    gates.append(gate_m)
    gate_images.append(gate_m.__returnimg__())

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        draw(win)

        # Tracks Quantum Gate Collision
        #for i in range(len(gates)):
            #if gates[i] == "h":
        #         circuit.h(qreg_q[0])
        #         if isHadamard is False:
        #             isHadamard = True
        #         if isHadamard is True:
        #             isHadamard = False
        #     #elif gates[i] == "x":
        #         circuit.x(qreg_q[0])
        #         if isX is False:
        #             isX = True
        #         if isX is True:
        #             isX = False
        #     #elif gates[i] == "m":
        #         circuit.measure(qreg_q[0],creg_c[0])
        #         isMeasured = True
        
        if isHadamard is True and isX is True:
            qState = "|->"
        elif isHadamard is True and isX is False:
            qState = "|+>"
        elif isHadamard is False and isX is True:
            qState = "|1>"
        else:
            qState = "|0>"
        
        # # if isMeasured is True:
        #      sim = execute(circuit,backend_sim, shots=1)
        #      result = sim.result()
        #      counts = result.get_counts(circuit)

        for img in gate_images:
            img = pygame.transform.scale(img, (imgWidth, imgHeight))
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
                movePlayer(event.key, p1)

                isCrossed,whichGate = checkCollision(p1)

                if isCrossed == False:
                    p1_color = WHITE
                else:
                    if whichGate == gate[0]:
                        p1_color = ROSE
                         circuit.h(qreg_q[0])
                        if isHadamard is False:
                            isHadamard = True
                        if isHadamard is True:
                            isHadamard = False
                    elif whichGate == gate[1]:
                        p1_color = LIME
                        circuit.x(qreg_q[0])
                      if isX is False:
                          isX = True
                      if isX is True:
                          isX = False
                    elif whichGate == gate[2]:
                        p1_color = LAVENDER
                        circuit.measure(qreg_q[0],creg_c[0])
                        isMeasured = True
                        if isMeasured is True:
                            sim = execute(circuit,backend_sim, shots=1)
                            result = sim.result()
                            counts = result.get_counts(circuit)
                
                p1.__draw__()
                print("drawn")
                
                p1.__move__()
                print("moved")

            # keyup to stop the continued movement of the line

            # create if-statements for keys pressed -- move the snake in the desired direction
            # create condition for when the snakes intersect -- end game and print winner
            
    pygame.quit()

main(display)