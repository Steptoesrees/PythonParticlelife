import pygame
from Button import Button
from Slider import Sliders
from matrixView import matrixView
from forceGraph import ForceGraph
class Menu:
    def __init__(self,screen, screen_width, screen_height, physics):
        self.screen = screen

        self.sliderdrag =  False

        self.menu = pygame.Surface((screen_height/2,screen_height))
        self.menu_rect = self.menu.get_rect() #for collision
        
        self.visible = False
        self.graph_or_matrix = 0 #1 for graph, 0 for matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.create_sliders()

        self.physics_engine = physics

        self.force_graph = ForceGraph(self.menu, 0, 20, screen_height/4, screen_height/2, physics)
        self.matrix_view = matrixView(self.menu, 0, 20, screen_height/4, screen_height/2, physics)

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
                self.matrix_view.draw()
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
        self.particle_num_slider = Sliders(self, (pos[0],pos[1]), whole_width=self.screen_height/2 - 20, max_val=5000, slider_val=300, Name='Particles:')
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
        self.particle_num_slider.slider_value = round(self.particle_num_slider.slider_value,0)
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

        

    def input_event(self, event):
        mpos = pygame.mouse.get_pos()

        

        self.particle_num_slider.Input(event, mpos)
        self.force_factor_slider.Input(event, mpos)
        self.beta_slider.Input(event, mpos)
        self.radius_slider.Input(event, mpos)

        self.matrix_view.input_event(event, mpos)
        


    





                
                
                