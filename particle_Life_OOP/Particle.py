import random
import pygame

class Particle():
    #constants
    ForceVelocityNormaliser = 0.01

    #A single particle
    def __init__(self):
        colours = [(255,0,0),(0,255,0),(0,0,255)]
        self.colour_ID = random.randint(0,2) #colour ID as an identifier for the colour
        self.colour = colours[self.colour_ID]

        self.pos_x = float(random.uniform(0,1)) 
        self.pos_y = float(random.uniform(0,1)) 

        self.vel_x = float(0.0) 
        self.vel_y = float(0.0) 
    


    def drawParticle(self, screen, ssize):
        psize = ssize//600 #scale the particle to the screen size
        if psize < 1: #clamps the size of the particle to be > 1, as when it is < 1, it disappears
            psize = 1 
        pygame.draw.circle(screen, self.colour,(self.pos_x * ssize, self.pos_y * ssize), psize)

    def drawVelocityVector(self, screen, ssize):
        #draws a line representing the direction and magnitude of a particles velocity
        wrap = False
        vel_x = self.vel_x
        vel_y = self.vel_y
        x = self.pos_x
        y = self.pos_y
        x1 = x+(vel_x/5) #end pos of vector
        y1 = y + (vel_y/5) #end pos of vecto
        # finds values for start and end pos of wrapped vector
        x4 = x
        x5 = x1
        y4 = y
        y5 = y1
        if x1 > 1:
            wrap = True #indicates to draw the wrapped vector
            x4 = x - 1 #start
            x5 = x1 - 1 #end
        if x1 < 0:
            wrap = True
            x4 = x + 1
            x5 = x1 + 1

        if y1 > 1:
            wrap = True
            y4 = y - 1
            y5 = y1 - 1
        if y1 < 0:
            wrap = True
            y4 = y + 1
            y5 = y1 + 1
        x = x*ssize
        y = y*ssize
        x1 = x1*ssize
        y1 = y1*ssize
        if wrap == False:
            pygame.draw.line(screen,(100,100,100), (x,y), #starting point = particle position
                            (x1, y1)) #end point = particle position + velocity  #velocity divided by 5, as at its normal magnitude, the vectors look too big
        if wrap == True:
            x4 = x4*ssize
            y4 = y4*ssize
            x5 = x5*ssize
            y5 = y5*ssize
            pygame.draw.line(screen,(100,100,100), (x,y), #starting point = particle position
                            (x1, y1))
            pygame.draw.line(screen,(100,100,100), (x4,y4),
                        (x5,y5))



    def updateVelocity(self, frictionFactor, totalForceX, totalForceY):
        # adds friction and calculates the velocity
        self.vel_x *= frictionFactor
        self.vel_y *= frictionFactor

        self.vel_x += totalForceX * self.ForceVelocityNormaliser
        self.vel_y += totalForceY * self.ForceVelocityNormaliser


    def updatePosition(self):

        #applies the velocity to the particles position
        self.pos_x += self.vel_x * self.ForceVelocityNormaliser
        self.pos_y += self.vel_y * self.ForceVelocityNormaliser
        
        #mod the particle position for screen wrapping
        if self.pos_x < 0 or self.pos_x > 1:
            self.pos_x %= 1
        if self.pos_y < 0 or self.pos_y > 1:
            self.pos_y %= 1