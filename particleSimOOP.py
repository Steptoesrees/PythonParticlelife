import random
import math
import pygame
#particle class
class particle():

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (64, 64, 255)

    def __init__(self):
        self.colour = simulation.randomMatrix()
        self.xpos = float(random.uniform(0,1))
        self.ypos = float(random.uniform(0,1))
        self.xvel = float(0.0)
        self.yvel = float(0.0)



class simulation():
    def __init__(self):
        self.screenwidth = 800
        self.screenheight = 800
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
    def draw(self):
            pygame.draw.circle(self.screen, (255,255,255), (100,100),10)

    def run(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()

            pygame.display.flip()



    def randomMatrix():
        rows = []
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                row.append(random.uniform(0, 1) * 2 - 1)
            rows.append(row)
        return rows

    def force(r, a):
        beta = 0.5
        if (r < beta):
            return r / beta - 1
        elif beta < r and r < 1:
            return a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
        else:
            return 8

sim = simulation()
sim.run()