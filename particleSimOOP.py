import random
import math
import pygame



#particle class


class particle():
    def __init__(self):
        self.colour = random.randint(0,2)
        self.xpos = float(random.uniform(0,1))
        self.ypos = float(random.uniform(0,1))
        self.xvel = float(0.0)
        self.yvel = float(0.0)
        self.totalforcex = 0
        self.totalforcey = 0
    
    def force(r, a):
        beta = 0.5
        if (r < beta):
            return r / beta - 1
        elif beta < r and r < 1:
            return a * (1 - abs(2 * r - 1 - beta) / (1 - beta))
        else:
            return 8




class simulation():
    def __init__(self):
        self.colours = [(255,0,0), (0,255,0), (0,0,255)]
        self.screenwidth = 600
        self.screenheight = 600
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight),pygame.RESIZABLE)
        self.particlenum = 400
        self.particles = []
        self.matrix = self.randomMatrix()
        self.maxRadius = 0.2
        self.forceFactor = 10
        self.frictionFactor = math.pow(0.5, 0.01 / 0.040)
        self.edgeDistance = 100

        for i in range(self.particlenum):
            self.particles.append(particle())

    def draw(self, i):
        #debug print(self.particles[i].xpos, self.particles[i].ypos)
        pygame.draw.circle(self.screen, self.colours[self.particles[i].colour], (self.particles[i].xpos,self.particles[i].ypos),2)

    def simulate(self):
        for i in range(self.particlenum):
            totalforcex = 0
            totalforcey = 0

            for j in range(0, self.particlenum):
                if j == i:
                    continue

                else:
                    rx = self.particles[j].xpos - self.particles[i].xpos
                    ry = self.particles[j].ypos - self.particles[i].ypos

                    radius = math.hypot(rx, ry)

                    if 0 < radius < self.maxRadius:

                        f = particle.force(radius / self.maxRadius, self.matrix[self.particles[i].colour][self.particles[i].colour])
                        totalforcex += rx / radius * f
                        totalforcey += ry / radius * f

            #finding the force the particles are interacting with
            totalforcex *= self.maxRadius * self.forceFactor
            totalforcey *= self.maxRadius * self.forceFactor

            #decreasing velocity so they dont speed up indefinitely
            self.particles[i].xvel *= self.frictionFactor
            self.particles[i].yvel *= self.frictionFactor

            #calculating velocity
            self.particles[i].xvel += totalforcex * 0.01
            self.particles[i].yvel += totalforcey * 0.01

            #changes the position of the particle to the new position calculated
            self.particles[i].xpos += self.particles[i].xvel * 0.01
            self.particles[i].ypos += self.particles[i].yvel * 0.01

            #scales the position of the particle to the screen dimensions
            self.particles[i].xpos *= self.screenwidth
            self.particles[i].ypos *= self.screenheight


            self.draw(i)

            self.particles[i].xpos /= self.screenwidth
            self.particles[i].ypos /= self.screenheight

    def run(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.simulate()
            pygame.display.flip()



    def randomMatrix(self):
        rows = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(random.uniform(0, 1) * 2 - 1)
            rows.append(row)
        return rows

    

if __name__ == '__main__':
    sim = simulation()
    sim.run()