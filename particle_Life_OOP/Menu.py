import pygame
from Button import Button
from Slider import Sliders
class Menu:
    def __init__(self,screen, screen_width, screen_height, physics):
        self.screen = screen

        self.sliderdrag =  False

        self.menu = pygame.Surface((screen_height/2,screen_height))
        self.menu_rect = self.menu.get_rect() #for collision
        
        self.visible = False
        self.graph_or_matrix = 1 #1 for graph, 0 for matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.create_sliders()

        self.physics_engine = physics

        self.force_graph = ForceGraph(self.menu, 0, 20, screen_height/4, screen_height/2, physics)

        self.create_buttons()

        
    def mouse_in_menu(self, mousepos):
        if self.visible:
            return self.menu_rect.collidepoint(mousepos)
        else:
            return False

    def draw(self):
        self.menu.fill((43,42,51))
        if self.visible:
            if self.graph_or_matrix == 1:
                self.force_graph.draw()
                
            else:
                pass
            self.update_slider_values()
            self.draw_sliders()
            self.draw_buttons()
            self.screen.blit(self.menu, (0,0))
    
    def toggle_graph_matrix(self):
        if self.graph_or_matrix == 1:
            self.graph_or_matrix = 0
        else:
            self.graph_or_matrix = 1

    def create_buttons(self):
        self.graph_matrix_button = Button((100,100,100), (self.screen_height/2)-80,(self.screen_height/4)-20, 80, 40, self.menu, self.toggle_graph_matrix, None, text="G/M")

    def draw_buttons(self):
        self.graph_matrix_button.draw()




    def create_sliders(self):
        pos = (10, 40 + self.screen_height/4 + 20)
        self.particle_num_slider = Sliders(self, (pos[0],pos[1]), whole_width=self.screen_height/2 - 20, max_val=400, slider_val=300, Name='Particles:')
        self.force_factor_slider = Sliders(self, (pos[0],pos[1]+50), whole_width=self.screen_height/2 - 20, neg=True, max_val=20, slider_val=10, Name='Force Factor: ')
        self.beta_slider = Sliders(self, (pos[0],pos[1]+100), whole_width=self.screen_height/2 - 20, max_val=1, slider_val=0.25, Name='Beta: ')
        self.radius_slider = Sliders(self, (pos[0],pos[1]+150), whole_width=self.screen_height/2 - 20, max_val=1, slider_val=0.25, Name='Radius: ')

    def draw_sliders(self):
        self.particle_num_slider.draw(self.menu)
        self.force_factor_slider.draw(self.menu)
        self.beta_slider.draw(self.menu)
        self.radius_slider.draw(self.menu)

    def slide(self, mousepos, dx):
        self.particle_num_slider.button_click(mousepos, dx)
        self.force_factor_slider.button_click(mousepos, dx)
        self.beta_slider.button_click(mousepos, dx)
        self.radius_slider.button_click(mousepos, dx)

        self.physics_engine.changeParticleCount(int(self.particle_num_slider.slider_value))
        self.physics_engine.force_Factor = self.force_factor_slider.slider_value
        self.physics_engine.beta = self.beta_slider.slider_value
        self.physics_engine.max_Radius = self.radius_slider.slider_value

    def update_slider_values(self):

        self.particle_num_slider.slider_value = len(self.physics_engine.particles)+1
        self.force_factor_slider.slider_value = self.physics_engine.force_Factor
        self.beta_slider.slider_value = self.physics_engine.beta
        self.radius_slider.slider_value = self.physics_engine.max_Radius


        self.particle_num_slider.updateslider()
        self.force_factor_slider.updateslider()
        self.beta_slider.updateslider()
        self.radius_slider.updateslider()

class Taskbar():

    def __init__(self,screen, screen_width, screen_height, menu, physics_engine):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.main_menu = menu
        self.physics_engine = physics_engine

        self.screen = screen
        self.taskbar = pygame.Surface((screen_width, 20))
        self.taskbar_rect = self.taskbar.get_rect() #for collision
        print(self.physics_engine)

        
        self.menu_button = Button((100,100,100), 0, 0, 40, 20, self.taskbar, self.toggle_menu, None,text='M')
        self.add_particle_button = Button((100,100,100), 100, 0, 100, 20, self.taskbar, self.physics_engine.addParticle, None,text='+')
        self.remove_particle_button = Button((100,100,100), 210, 0, 100, 20, self.taskbar, self.physics_engine.removeParticle, None,text='-')
        self.reset_matrix_button = Button((100,100,100), 320, 0, 100, 20, self.taskbar, self.physics_engine.randomMatrix, None, text='R')
        self.pause_button = Button((100,100,100), 430, 0, 100, 20, self.taskbar, self.pause_simulation, None,text='Pause')
        self.exit_button = Button((200,0,0), self.screen_width-40, 0, 40, 20, self.taskbar, self.exit, None,text='×')


    def draw(self):
        self.taskbar.fill((20,20,20))
        self.menu_button.draw(BR=3)
        self.add_particle_button.draw(BR=3)
        self.remove_particle_button.draw(BR=3)
        self.reset_matrix_button.draw(BR=3)
        self.pause_button.draw(BR=3)
        self.exit_button.draw(text_pos=(10,-5))
        self.screen.blit(self.taskbar, (0,0))

    def click_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.click(mouse_pos)
        self.add_particle_button.click(mouse_pos)
        self.remove_particle_button.click(mouse_pos)
        self.reset_matrix_button.click(mouse_pos)
        self.pause_button.click(mouse_pos)
        self.exit_button.click(mouse_pos)

    def toggle_menu(self):
        self.main_menu.visible = not self.main_menu.visible

    def pause_simulation(self):
        self.physics_engine.paused = not self.physics_engine.paused

    def exit(self):
        pygame.quit()
        quit()
    
    def mouse_in_taskbar(self, mousepos):
        return self.taskbar_rect.collidepoint(mousepos)
    

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


    def click_buttons(self):
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
            