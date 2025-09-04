import random
import math
import ctypes
import sys

import pygame #imports they pygame library




class Button():
    #A button
    def __init__(self,colour, xloc, yloc, width, height,surface):
        self.colour = colour 
        self.button_rect = pygame.Rect(xloc,yloc,width,height) 
        self.surface = surface 


    def draw(self):
        pygame.draw.rect(self.surface,self.colour,(self.button_rect)) 
        pygame.draw.rect(self.surface, (0,0,0), (self.button_rect), 1) 

    def click(self, mousepos):
        #if the mouse is over the button, return true, otherwise return false
        if self.button_rect.collidepoint(mousepos):
            return True
        else:
            return False 



class ForceGraph():
    def __init__(self,sim):
        """constructor method"""
        self.beta = sim.beta #defines beta

        self.height = 350 #sets the height of the surface the grid it blited to
        self.width = (sim.screen_width - sim.screen_height)/1.5 #sets width too


        self.full_padding = int(self.width - self.width*0.9) #sets the distance from the edge of the grid to the edge of the main surface
        self.padding = int(self.full_padding/2) #halves the padding so it can be used more easily in calculations

        self.grid_width = self.width - self.full_padding #sets the width of the grid in proportion to the width of the canvas surface
        self.grid_height = self.height - self.full_padding #sets the height of the grid in proportion to the height of the canvas surface


        self.canvas = pygame.Surface((self.width,self.height)) #defines the canvas surface
        self.canvas_rect = self.canvas.get_rect() #gets the size of the canvas surface as a rect object

        self.grids = [] #initialises the list "grids"
        for counter in range(sim.colour_num): #loop for however many types of particles there are
            self.grids.append(pygame.Surface((self.grid_width, self.grid_height))) #adds a new surface to draw the force graph on for every colour of particle
            self.current_graph = counter #sets the current graph

        self.grid_rect = self.grids[0].get_rect() #gets the size of the grid surface as a rect object

        self.font_size = int(self.width * 3/100) #sets the font size for graph labels

        self.bgcolours = [(20,0,0),(0,20,0),(0,0,20)]

        self.canvas.fill((30, 30, 30)) #sets the canvas surface to be gray

        for counter in range(sim.colour_num): #loops for the number of particle colours
            for i in range(sim.colour_num): #loops for the number of particle colours
                self.drawForceGraph(sim.matrix[counter][i], counter, i, sim)  #calls the drawForceGraph function
                self.drawGrid(self.grids[counter]) #calls the drawGrid function

        self.buttons = [] #initialises the array button objects are stored in for the force graph
        for i in range(0, sim.colour_num): #loop for the number of particle colours
            self.buttons.append(Button(sim.colours[i],                                                 # appends a new button object to the array of buttons
                                (i*self.padding+(self.width/2) - (self.padding*0.8*sim.colour_num)/2), #~
                                self.height-self.padding*0.9, (self.padding * 0.8), (self.padding * 0.8), self.canvas)) #~
            self.buttons[i].draw() #calls the button's draw function
        pygame.draw.rect(self.buttons[2].surface, (255, 255, 255), (self.buttons[2].button_rect), 1)


    def drawGrid(self, grid):
        """Draws the axis, lable, title, and values onto the graph"""
        pygame.draw.line(grid, (255,255,255), (0,0),#draws the y-axis
                         (0, self.grid_height)) #draws the y-axis


        pygame.draw.line(grid, (255,255,255), (0,self.grid_height/2),#draws the x-axis
                         (self.grid_width,self.grid_height/2))#draws the x-axis

        pygame.draw.line(grid, (255, 255, 255), (0, self.grid_height),#draws the line from -1 to beta, as this is constant for all particles
                         ((self.beta*self.grid_width), self.grid_height/2)) #draws the line from -1 to beta, as this is constant for all particles


        pygame.draw.line(self.canvas, (255, 255, 255), (self.grid_width + self.padding, self.grid_height/2+self.padding),
                        (self.grid_width+self.padding, self.grid_height/2+self.padding + (self.padding*(1/6)))) #draws the line showing where r-max is

        pygame.draw.line(self.canvas, (255, 255, 255), (self.padding,self.padding), #draws the line showing where F = 1
                         (self.padding-(self.padding*(1/6)),self.padding)) #draws the line showing where F = 1

        pygame.draw.line(self.canvas, (255, 255, 255), (self.padding, self.height-self.padding),#draws the line showing where F = -1
                         (self.padding-(self.padding*(1/6)), self.height-self.padding))#draws the line showing where F = -1

        font = pygame.font.SysFont('segoeui', self.font_size) #initialises pygame font

        ylable = font.render('F', True, (255, 255, 255)) #creates the label for the y-axis (F), which can be blited onto a surface
        xlable = font.render('r', True, (255, 255, 255)) #creates the label for the x-axis (r), which can be blited onto a surface
        one = font.render('1', True, (255, 255, 255)) #creates text showing 1, which can be blited onto a surface
        neg_one = font.render('-1', True, (255, 255, 255)) #creates text showing -1, which can be blited onto a surface
        Title = font.render("Particle Force Interactions", True, (255, 255, 255)) #creates the Title for the Graph, which can be blited onto a surface

        self.canvas.blit(ylable, (self.padding,#draws the ylable
                                  self.padding-ylable.get_rect().height)) #draws the ylabel

        self.canvas.blit(xlable, (self.width-self.padding+xlable.get_rect().width,#draws the xlable
                                  (self.height/2)-(xlable.get_rect().height/2))) #draws the xlable

        self.canvas.blit(one, (self.width-self.padding-one.get_rect().width/2,#draws 1 where r = 1
                                  (self.height/2))) #draws 1 where r = 1

        self.canvas.blit(one, (self.padding - (self.padding * 1 / 6) - one.get_rect().width,#draws 1 where F = 1
                               self.padding - one.get_rect().height / 2)) #draws 1 where F = 1

        self.canvas.blit(neg_one, (self.padding-(self.padding*1/6)-neg_one.get_rect().width,#draws -1 where F = -1
                                   self.height-self.padding-neg_one.get_rect().height/2)) #draws -1 where F = -1

        self.canvas.blit(Title, ((self.width/2 - Title.get_rect().width/2), 1)) #draws the title of the graph

    def drawForceGraph(self, a,i, j, sim):

        midr = (1 + sim.beta)/2 #midpoint between beta & 1
        pygame.draw.line(self.grids[i], sim.colours[j], (sim.beta*(self.grid_width),(self.grid_height)/2), #draws the line from beta to midr (midpoint between beta & 1)
                         (midr*(self.grid_width), (self.grid_height/2-(a)*(self.grid_height)/2)))  #where the midpoint is where the force between particles is at its max or min

        pygame.draw.line(self.grids[i], sim.colours[j], (self.grid_width,(self.grid_height) / 2),#draws the line from 1 to midr (midpoint between beta & 1)
                         (midr * (self.grid_width), (self.grid_height/2 - (a)*(self.grid_height)/2))) #where the midpoint is where the force between particles is at its max or min


        self.canvas.blit(self.grids[i], (self.padding,self.padding)) #draws the graph



class Particle():
    """A single particle"""
    def __init__(self):
        """creates new Particle object"""
        self.colour = random.randint(0,2) #the number corresponding to the colour in the colour list (held in simulation)

        self.xpos = float(random.uniform(0,1)) #random x position chosen to spawn
        self.ypos = float(random.uniform(0,1))#random y position chosen to spawn

        self.xvel = float(0.0) #velocity starts at zero
        self.yvel = float(0.0) #velocity starts at zero


    def drawVelocityVector(self):
        """draws a line representing the direction and magnitude of a particles velocity"""
        xvel = self.xvel*sim.screen_height #scales the magnitude
        yvel = self.yvel*sim.screen_height #scales the magnitude
        pygame.draw.line(sim.simBox, (100,100,100), (self.xpos, self.ypos),#start pos is the position of the particle
                         (self.xpos + (xvel/5), self.ypos + (yvel/5))) #end pos is the velocity vectors added to the original position


    def draw(self, radius):
        """draws a particle"""
        pygame.draw.circle(sim.simBox, sim.colours[self.colour],
                           (self.xpos, self.ypos),
                           radius) #draws a particle



class Simulation():
    """Calculates the interactions between particles"""
    def __init__(self):

        self.colour_num = 3
        self.colours = [(255,0,0), (0,255,0), (0,0,255), (255/2,255/2,0), (0,255/2,255/2), (255/2,0,255/2)] #A list of colours which corresponds to a particles colour number

        self.beta = 0.25

        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0) #gets the width of the computer's monitor
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1) #gets the height of the computer's monitor
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height)) #initiallizes the display for rendering

        self.simBox = pygame.Surface((self.screen_height,self.screen_height))
        self.menu_Box = pygame.Surface((self.screen_width-self.screen_height, self.screen_height))
        self.menu_Box.fill((10, 10, 10))

        self.particle_num = 300 #the number of particles which will spawn
        self.particles = [] #a list which will be populated with Particle objects
        for i in range(self.particle_num): #populates particles with Particle objects
            self.particles.append(Particle()) #populates particles with Particle objects

        self.matrix = self.randomMatrix()#attraction matrix for how the colours interact

        self.max_radius = 0.2 #the distance at which particles can interact
        self.force_factor = 10 #increases the magnitude of reactions
        self.friction_factor = math.pow(0.5, 0.01 / 0.040) #friction
        self.edge_distance =20/self.screen_height #padding

        self.graph_vis = ForceGraph(self) #graph of force diagram


        self.clock = pygame.time.Clock() #clock


    def force(self, r, a):
        """Force Function"""
        if (r < self.beta):
            return ((r / self.beta) - 1) #pushes particles away from each other when they get too close, so they don't all converge into a single point

        elif self.beta < r and r < 1:
            return a*(1-abs(-(2*r-2)/(1-self.beta)-1)) #returns the force to apply to the particle according to the force matrix

        else:
            return 0 #if the distance between the two points are more than 1 or less than zero, it returns 0


    def padding(self,i):
        if self.particles[i].xpos < self.edge_distance:
            self.particles[i].xvel += (self.edge_distance - self.particles[
                i].xpos) / 0.4  # when within the cushion border, takes the size of the cushion from the position of the particle, so the number is larger the closer to the edge the particle is, then this number is squared to make the increase exponential, divided by 10^4 for a more reasonable amount of force

        if self.particles[i].xpos > 1 - self.edge_distance:
            self.particles[i].xvel -= (self.particles[i].xpos - (
                        1 - self.edge_distance)) / 0.4

        if self.particles[i].ypos < self.edge_distance:
            self.particles[i].yvel += (self.edge_distance - self.particles[
                i].ypos) / 0.4  # when within the cushion border, takes the size of the cushion from the position of the particle, so the number is larger the closer to the edge the particle is, then this number is squared to make the increase exponential, divided by 10^4 for a more reasonable amount of force

        if self.particles[i].ypos > 1 - self.edge_distance:
            self.particles[i].yvel -= (self.particles[i].ypos - (1 - self.edge_distance)) / 0.4

    def particleOnParticle(self):
        """calculates the forces for particles & applies them"""
        for i in range(self.particle_num): #loops through all the particles


            total_force_x = 0 #sets total force applied this frame to this particle on the x-axis to 0
            total_force_y = 0 #sets total force applied this frame to this particle on the y-axis to 0

            for j in range(0, self.particle_num): #loops through all the particles
                if j == i: #if the particles are the same particle
                    continue #skip this loop

                else: #otherwise
                    dx = (self.particles[j].xpos - self.particles[i].xpos) #distance between the points horizontally
                    dy = (self.particles[j].ypos - self.particles[i].ypos) #distance between the points vertically

                    # Wrap distances
                    if abs(dx) > 0.5:
                        dx -= math.copysign(1.0, dx)
                    if abs(dy) > 0.5:
                        dy -= math.copysign(1.0, dy)

                    radius = math.sqrt(dx**2 + dy**2) #finds the distance between the points (no screen wrapping yet)

                    if 0 < radius < self.max_radius: #checks if the particles are within the radius to apply force

                        f = self.force(radius / self.max_radius,
                                    self.matrix[self.particles[i].colour][self.particles[j].colour]) #calls the force function to return the force

                        total_force_x += dx / radius * f
                        total_force_y += dy / radius * f


            #finding the force the particles are interacting with
            total_force_x *= self.max_radius * self.force_factor
            total_force_y *= self.max_radius * self.force_factor


            #decreasing velocity so they don't speed up indefinitely
            self.particles[i].xvel *= self.friction_factor
            self.particles[i].yvel *= self.friction_factor

            #calculating velocity
            self.particles[i].xvel += total_force_x * 0.01
            self.particles[i].yvel += total_force_y * 0.01

            #self.padding(i)

            #changes the position of the particle to the new position calculate
            self.particles[i].xpos += self.particles[i].xvel * 0.01
            self.particles[i].ypos += self.particles[i].yvel * 0.01




            # scales the position of the particle to the screen dimensions
            self.particles[i].xpos = (self.screen_height * self.particles[i].xpos)
            self.particles[i].ypos *= self.screen_height

            # screen wrapping
             # checks if the particle is off the right side of the simulation area
            self.particles[i].xpos = (self.particles[i].xpos % self.screen_height)


            self.particles[i].ypos = (self.particles[i].ypos % self.screen_height)

            # self.particles[i].drawVelocityVector()
            self.particles[i].draw(2)

            self.particles[i].xpos /= self.screen_height
            self.particles[i].ypos /= self.screen_height


    def run(self):
        running = True
        while running:
            self.simBox.fill((0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i in range(self.colour_num):
                        if self.graph_vis.buttons[i].click(mouse_pos):
                            self.graph_vis.canvas.blit(self.graph_vis.grids[i],
                                                       (self.graph_vis.padding, self.graph_vis.padding))
                            self.graph_vis.drawGrid(self.graph_vis.grids[i])
                            self.graph_vis.current_graph = i

                if self.graph_vis.canvas_rect.collidepoint(mouse_pos):
                    for i in range (self.colour_num):
                        if i != self.graph_vis.current_graph:
                            self.graph_vis.buttons[i].colour = self.colours[i]
                            self.graph_vis.buttons[i].draw()
                        else:
                            continue
            self.particleOnParticle()
            self.screen.blit(self.simBox, ((self.screen_width-self.screen_height),0))
            self.screen.blit(self.menu_Box, (0,0))
            self.menu_Box.blit(self.graph_vis.canvas, (0, 0))
            self.clock.tick(30)
            pygame.display.update()


    def randomMatrix(self):
        rows = []
        for i in range(0,3):
            row = []
            for j in range(0,3):
                row.append(round((random.uniform(0, 1) * 2 - 1),3))
            rows.append(row)
        print(rows)
        return rows



if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    sim = Simulation()
    sim.run()