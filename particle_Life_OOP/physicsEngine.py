import math
import random
import pygame
from Particle import Particle

class PhysicsEngine():
    #Handles the particle interactions
    def __init__(self):
        self.particles = []
        self.max_Radius = 0.25
        self.friction_Factor = math.pow(0.5, 0.01 / 0.040)
        self.force_Factor = 10
        self.matrix = [[],[],[]]
        self.beta = 0.15
        self.randomMatrix()
        self.paused = False

        self.simarea = pygame.Surface((800,800))

    def addParticle(self):
        self.particles.append(Particle())
        
    def removeParticle(self):
        if len(self.particles) > 0:
            self.particles.pop()

    def changeParticleCount(self, amount):
        if amount > len(self.particles)+1:
            for i in range(amount-len(self.particles)):
                self.addParticle()
        elif amount < len(self.particles)+1:
            for i in range(len(self.particles)-amount):
                self.removeParticle()
    
    def randomMatrix(self): 
        rows = [] 
        for i in range(0,3): 
            row = [] 
            for j in range(0,3): 
                row.append(round((random.uniform(0, 1) * 2 - 1),3)) 
            rows.append(row) 
        self.matrix = rows
    

    def force(self, r, a):
        #Force Function
        if (r < self.beta):
            return ((r / self.beta) - 1) #pushes particles away from each other when they get too close, so they don't all converge into a single point

        elif self.beta < r and r < 1:
            return a*(1-abs(-(2*r-2)/(1-self.beta)-1)) #returns the force to apply to the particle according to the force matrix

        else:
            return 0 #if the distance between the two points are more than 1 or less than zero, it returns 0
        
    
    
    def interactions(self): 
        if self.paused:
            return
        #handles the interactions between particles
        for i in range(len(self.particles)):
            total_force_x = 0 
            total_force_y = 0 

            for j in range(len(self.particles)):
                if i == j:
                    continue
                else:
                    dx = (self.particles[j].pos_x - self.particles[i].pos_x) 
                    dy = (self.particles[j].pos_y - self.particles[i].pos_y)


                    if dx > 0.5:
                        dx -= 1.0
                    if dx < -0.5:
                        dx += 1.0
                    if dy > 0.5:
                        dy -= 1.0
                    if dy < -0.5:
                        dy += 1.0

                    radius = math.sqrt(dx**2 + dy**2) 

                    if 0 < radius < self.max_Radius: 

                        f = self.force(radius / self.max_Radius,self.matrix[self.particles[i].colour_ID][self.particles[j].colour_ID]) 

                        total_force_x += dx / radius * f
                        total_force_y += dy / radius * f

            total_force_x *= self.max_Radius * self.force_Factor
            total_force_y *= self.max_Radius * self.force_Factor

            self.particles[i].updateVelocity(self.friction_Factor, total_force_x, total_force_y)

            self.particles[i].updatePosition()
            

    
            