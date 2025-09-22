import random
import pygame

class Particle():
    #constants
    ForceVelocityNormaliser = 0.01

    #A single particle
    def __init__(self):
        colours = [(255,0,0),(0,255,0),(0,0,255)]
        self.colour_ID = random.randint(0,2)
        self.colour = colours[self.colour_ID]

        self.pos_x = float(random.uniform(0,1)) 
        self.pos_y = float(random.uniform(0,1)) 

        self.vel_x = float(0.0) 
        self.vel_y = float(0.0) 
    


    def drawParticle(self, screen, ssize):
        psize = ssize//600
        if psize < 1:
            psize = 1
        pygame.draw.circle(screen, self.colour,(self.pos_x * ssize, self.pos_y * ssize), psize)


    def updateVelocity(self, frictionFactor, totalForceX, totalForceY):
        self.vel_x *= frictionFactor
        self.vel_y *= frictionFactor

        self.vel_x += totalForceX * self.ForceVelocityNormaliser
        self.vel_y += totalForceY * self.ForceVelocityNormaliser


    def updatePosition(self):
        self.pos_x += self.vel_x * self.ForceVelocityNormaliser
        self.pos_y += self.vel_y * self.ForceVelocityNormaliser

        if self.pos_x < 0 or self.pos_x > 1:
            self.pos_x %= 1
        if self.pos_y < 0 or self.pos_y > 1:
            self.pos_y %= 1