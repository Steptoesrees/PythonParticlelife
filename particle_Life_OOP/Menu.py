import pygame
from Button import Button
from Slider import Sliders
from matrixView import matrixView
from forceGraph import ForceGraph

class Menu:
    def __init__(self,screen, screen_width, screen_height, physics):
        #constructro function

        self.screen = screen

        self.sliderdrag =  False

        self.menu = pygame.Surface((screen_height/2,screen_height))
        self.menu_rect = self.menu.get_rect() #for collision
        
        self.visible = False
        self.graph_or_matrix = 0 #1 for graph, 0 for matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.create_sliders()

        self.physics_engine = physics #passes in the physics engine object

        self.force_graph = ForceGraph(self.menu, 0, 20, screen_height/4, screen_height/2, physics) #creates forcegraph and matrix view objects.
        self.matrix_view = matrixView(self.menu, self.screen, 0, 20, screen_height/4, screen_height/2, physics)

        self.create_buttons()

        
    def mouse_in_menu(self, mousepos):#checks if the mouse is over the menu
        if self.visible:
            return self.menu_rect.collidepoint(mousepos)
        else:
            return False

    def draw(self):
        #draws the menu
        self.menu.fill((43,42,51)) #fills the background

        if self.visible:
            
            self.update_slider_values()
            self.draw_sliders()
            self.draw_buttons()

            #checks the value of graph_or_matrix and draws the graph or the matrix
            if self.graph_or_matrix == 1:
                self.force_graph.draw()
            else:
                self.matrix_view.draw()
            
            self.screen.blit(self.menu, (0,0)) #draws menu to the main screen
            self.matrix_view.save.draw()#draws the save/loading menus to the screen
    
    def toggle_graph_matrix(self): #switches the value of graph_or_matrix
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

    def slide(self, mousepos, dx): #updates the position of the slider buttons
        self.particle_num_slider.button_click(mousepos, dx)
        self.particle_num_slider.slider_value = round(self.particle_num_slider.slider_value,0)
        self.force_factor_slider.button_click(mousepos, dx)
        self.beta_slider.button_click(mousepos, dx)
        self.radius_slider.button_click(mousepos, dx)

        #updates the values in physics engine based on the slider values
        self.physics_engine.changeParticleCount(int(self.particle_num_slider.slider_value))
        self.physics_engine.force_Factor = self.force_factor_slider.slider_value
        self.physics_engine.beta = self.beta_slider.slider_value
        self.physics_engine.max_Radius = self.radius_slider.slider_value

        

    def update_slider_values(self):
        #updates the values of the slider
        self.particle_num_slider.slider_value = len(self.physics_engine.particles)+1
        self.force_factor_slider.slider_value = self.physics_engine.force_Factor
        self.beta_slider.slider_value = self.physics_engine.beta
        self.radius_slider.slider_value = self.physics_engine.max_Radius

        #updates the position of the slider
        self.particle_num_slider.updateslider()
        self.force_factor_slider.updateslider()
        self.beta_slider.updateslider()
        self.radius_slider.updateslider()

        

    def input_event(self, event):
        mpos = pygame.mouse.get_pos()

        #calls the input event functions for the sliders
        self.particle_num_slider.Input(event, mpos)
        self.force_factor_slider.Input(event, mpos)
        self.beta_slider.Input(event, mpos)
        self.radius_slider.Input(event, mpos)

        #adn the matrix visualiser
        self.matrix_view.input_event(event, mpos)
        

class Taskbar():

    def __init__(self,screen, screen_width, screen_height, menu, physics_engine, cam):
        #constructor function
        self.cam = cam

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.main_menu = menu
        self.physics_engine = physics_engine

        self.screen = screen
        self.taskbar = pygame.Surface((screen_width, 20))
        self.taskbar_rect = self.taskbar.get_rect() #for collision

        #creates buttons for the taskbar
        self.menu_button = Button((100,100,100), 0, 0, 40, 20, self.taskbar, self.toggle_menu, None,text='M')
        self.add_particle_button = Button((100,100,100), 100, 0, 100, 20, self.taskbar, self.physics_engine.addParticle, None,text='+')
        self.remove_particle_button = Button((100,100,100), 210, 0, 100, 20, self.taskbar, self.physics_engine.removeParticle, None,text='-')
        self.reset_matrix_button = Button((100,100,100), 320, 0, 100, 20, self.taskbar, self.physics_engine.randomMatrix, None, text='R')
        self.pause_button = Button((100,100,100), 430, 0, 100, 20, self.taskbar, self.pause_simulation, None,text='Pause')
        self.exit_button = Button((200,0,0), self.screen_width-40, 0, 40, 20, self.taskbar, self.exit, None,text='×')
        self.vector_vis = Button((100,100,100), 540,0,100,20,self.taskbar,self.toggle_vectors,None,text='Vector')

        #creates font for the text on buttons
        self.font = pygame.font.SysFont('segoeui', 15)


    def draw(self, clock):
        #clears taskbar
        self.taskbar.fill((20,20,20))

        #draws the fps at the top right of the taskbar
        fps = int(clock.get_fps())
        fps_text = f'FPS: {fps}'
        fps_label = self.font.render(fps_text, True, (255,255,255))
        self.taskbar.blit(fps_label, (self.screen_width - 100, 0))

        #draws the buttons
        self.menu_button.draw(BR=3)
        self.add_particle_button.draw(BR=3)
        self.remove_particle_button.draw(BR=3)
        self.reset_matrix_button.draw(BR=3)
        self.pause_button.draw(BR=3)
        self.exit_button.draw(text_pos=(10,-5))
        self.vector_vis.draw(BR=3)
        self.screen.blit(self.taskbar, (0,0))

    def click_buttons(self):
        #calls the click function for all the buttons
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.click(mouse_pos)
        self.add_particle_button.click(mouse_pos)
        self.remove_particle_button.click(mouse_pos)
        self.reset_matrix_button.click(mouse_pos)
        self.pause_button.click(mouse_pos)
        self.exit_button.click(mouse_pos)
        self.vector_vis.click(mouse_pos)

    def toggle_menu(self):
        self.main_menu.visible = not self.main_menu.visible
    
    def toggle_vectors(self):
        self.cam.velocityV = not self.cam.velocityV

    def pause_simulation(self):
        self.physics_engine.paused = not self.physics_engine.paused

    def exit(self):
        pygame.quit()
        quit()
    
    def mouse_in_taskbar(self, mousepos):
        #checks if the mouse is over the taskbar
        return self.taskbar_rect.collidepoint(mousepos)
    





                
                
                