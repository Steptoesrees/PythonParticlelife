import pygame
from Button import Button
from Main import main
from physicsEngine import PhysicsEngine

class Menu:
    def __init__(self,screen, screen_width, screen_height):
        self.screen = screen
        self.menu = pygame.Surface((screen_height/2,screen_height))
        self.visible = False
        self.graph_or_matrix = 1 #1 for graph, 0 for matrix
        self.force_graph = ForceGraph(self.menu, 0, 40, screen_height/4, screen_height/2)

    def draw(self):
        self.menu.fill((43,42,51))
        if self.visible:
            self.screen.blit(self.menu, (0,0))
            if self.graph_or_matrix == 1:
                self.force_graph.draw()

    
        
class Taskbar():

    def __init__(self,screen, screen_width, screen_height, menu, physics_engine):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.main_menu = menu
        self.physics_engine = physics_engine

        self.screen = screen
        self.taskbar = pygame.Surface((screen_width, 40))
        print(self.physics_engine)

        #create buttons
        self.menu_button = Button((100,100,100), 0, 0, 40, 40, self.taskbar, 'M', self.toggle_menu)
        self.add_particle_button = Button((100,100,100), 100, 0, 100, 40, self.taskbar, '+', self.physics_engine.addParticle)
        self.remove_particle_button = Button((100,100,100), 210, 0, 100, 40, self.taskbar, '-', self.physics_engine.removeParticle)
        self.reset_matrix_button = Button((100,100,100), 320, 0, 100, 40, self.taskbar, 'R', self.physics_engine.randomMatrix)
        self.pause_button = Button((100,100,100), 430, 0, 100, 40, self.taskbar, 'Pause', self.pause_simulation)
        self.exit = Button((200,0,0), self.screen_width-40, 0, 40, 40, self.taskbar, 'X', self.exit)


    def draw(self):
        self.taskbar.fill((20,20,20))
        self.menu_button.draw()
        self.add_particle_button.draw()
        self.remove_particle_button.draw()
        self.reset_matrix_button.draw()
        self.pause_button.draw()
        self.exit.draw()
        self.screen.blit(self.taskbar, (0,0))

    def click_buttons(self):
        self.menu_button.click()
        self.add_particle_button.click()
        self.remove_particle_button.click()
        self.reset_matrix_button.click()
        self.pause_button.click()
        self.exit.click()

    def toggle_menu(self):
        self.main_menu.visible = not self.main_menu.visible

    def pause_simulation(self):
        self.physics_engine.paused = not self.physics_engine.paused

    def exit(self):
        pygame.quit()
        quit()
    
        
    

class ForceGraph():
    def __init__(self, screen, xloc, yloc, width, height):
        self.screen = screen
        self.graph = pygame.Surface((width,height))
        self.xloc = xloc
        self.yloc = yloc
        self.width = width
        self.height = height
        self.font=pygame.font.SysFont('segoeui',20)
    
    def draw(self):
        self.graph.fill((43,42,51))
        self.screen.blit(self.graph, (self.xloc,self.yloc))
        
    def drawAxes(self):
        pygame.draw.line(self.graph, (255,255,255), (40,self.height-20), (self.width-10,self.height-20), 2)
        pygame.draw.line(self.graph, (255,255,255), (40,self.height-20), (40,10), 2)

    def drawGraph(self, force_data):
        pass
        

