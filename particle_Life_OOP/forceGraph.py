import pygame
from Button import Button

class ForceGraph():
    def __init__(self, screen, xloc, yloc, height, width, Physics):
        self.screen = screen


        self.graph = pygame.Surface((width,height))
        self.axis = pygame.Surface((width-120,height-70))

        self.xloc = xloc
        self.yloc = yloc
        self.width = width
        self.height = height
        self.axis_width = width-120
        self.axis_height = height-70

        self.physics_engine = Physics

        self.graph1_b = Button((255,0,0), 10, self.height-30, 20, 20, self.graph, self.set_graph, 0)
        self.graph2_b = Button((0,255,0), 40, self.height-30, 20, 20, self.graph, self.set_graph, 1)
        self.graph3_b = Button((0,0,255), 70, self.height-30, 20, 20, self.graph, self.set_graph, 2)

        self.colour_ID = 0
        self.colours = [(255,0,0),(0,255,0),(0,0,255)]

        #text
        self.font=pygame.font.SysFont('segoeui',20)

    def set_graph(self, id):
        self.colour_ID = id


    def click_buttons(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]-self.xloc, mouse_pos[1]-self.yloc)
        self.graph1_b.click(mouse_pos)
        self.graph2_b.click(mouse_pos)
        self.graph3_b.click(mouse_pos)



    def draw(self):
        
        self.graph.fill((40,40,40))
        self.drawAxes()
        self.graph.blit(self.axis, (80,10))
        self.plotGraph()

        self.screen.blit(self.graph, (self.xloc,self.yloc))
        
    def drawAxes(self):
        
        #axis 
        self.graph1_b.draw()
        self.graph2_b.draw()
        self.graph3_b.draw()

        pygame.draw.line(self.axis, (255,255,255), (0,self.axis_height/2), (self.width,self.axis_height/2), 2) #x
        
        pygame.draw.line(self.axis, (255,255,255), (0,self.axis_height), (0,0), 2) #y

        #labels
        x_label = self.font.render('Distance (r)', True, (255,255,255))
        y_label = self.font.render('Force', True, (255,255,255))    
        minx_label = self.font.render('0', True, (255,255,255))
        maxx_label = self.font.render('1', True, (255,255,255))
        miny_label = self.font.render('-1', True, (255,255,255))
        maxy_label = self.font.render('1', True, (255,255,255))

        #draw labels
        self.graph.blit(x_label, (self.width//2 - x_label.get_width()//2, self.height-60))
        self.graph.blit(y_label, (20, self.height//2 - y_label.get_height()//2))
        self.graph.blit(minx_label, (70 - minx_label.get_width()//2, self.height-(60+((self.height-70)/2))- minx_label.get_height()//2))
        self.graph.blit(maxx_label, (self.width-30 - maxx_label.get_width()//2, self.height-(60+((self.height-70)/2))-maxx_label.get_height()//2))
        self.graph.blit(miny_label, (70 - miny_label.get_width()//2, self.height-60 - maxy_label.get_height()//2))
        self.graph.blit(maxy_label, (70 - maxy_label.get_width()//2, 10 - maxy_label.get_height()//2))

        


    def plotGraph(self):
        if self.colour_ID == 0:
            self.axis.fill((40,0,0))
        elif self.colour_ID == 1:
            self.axis.fill((0,40,0))
        else:
            self.axis.fill((0,0,40))
        midr = (1+self.physics_engine.beta)/2

        pygame.draw.line(self.axis, (255,255,255), (0,self.axis_height), 
                             (self.physics_engine.beta * self.axis_width, self.axis_height/2))

        for counter in range(3):
            a = self.physics_engine.matrix[self.colour_ID][counter]
            pygame.draw.line(self.axis, self.colours[counter], ((self.physics_engine.beta * self.axis_width), self.axis_height/2), 
                             (midr * self.axis_width, self.axis_height/2 - (a * (self.axis_height/2))))
            
            pygame.draw.line(self.axis, self.colours[counter], (midr * self.axis_width, self.axis_height/2 - (a * (self.axis_height/2))), 
                             (self.axis_width, self.axis_height/2))