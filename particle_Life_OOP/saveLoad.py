from input_box import InputBox
from Button import Button
import json
import pygame

class save:
    def __init__(self, screen, main_screen, physics):
        self.physics_engine = physics
        self.toggle_dropdown = False
        self.toggle_input = False
        try:
            with open("SavedMatrix.json", "r") as file:
                matrixes = json.load(file)
                self.MatrixNames =   [item['name'] for item in matrixes]
                self.MatrixMatrix =  [item['matrix'] for item in matrixes]
        except:
            with open("particle_Life_OOP//SavedMatrix.json", "r") as file:
                matrixes = json.load(file)
                self.MatrixNames =   [item['name'] for item in matrixes]
                self.MatrixMatrix =  [item['matrix'] for item in matrixes]

        self.dropdown_pos = (0, 0)
        self.input_pos = (0, 0)

        self.dropdown_buttons = []

        self.main_screen = main_screen
        self.dropdown = pygame.Surface((0, 0))

        padding = 5
        button_height = 20
        button_width = 80
        self.input_area = pygame.Surface((button_width*3 + padding*3, button_height + padding*2))
        self.name_box = InputBox((padding,padding), (button_height,button_width*2), text='name')
        self.confirm_button = Button((155,155,155), padding*2+button_width*2, padding, button_width, button_height, self.input_area, self.update_matrix, None, text = "confirm")

    def save_input(self):
        self.toggle_input = not self.toggle_input
        
        self.input_pos = pygame.mouse.get_pos()

        
        self.name_box.draw(self.input_area)
        self.confirm_button.draw()
        
       
# click Button
# update dropdown <- will call toggle dropdown in the function
# draw dropdown
# event handler
# on click:
#  if mpos outside dropdown toggle dropdown off
#  run button.click for all buttons
#
    def update_dropdown(self):
        self.toggle_dropdown = not self.toggle_dropdown
        mpos = pygame.mouse.get_pos()
        padding = 5
        button_height = 20
        button_width = 80

        width = button_width + padding*2
        height = padding*(len(self.MatrixNames)+1) + button_height*len(self.MatrixNames)
        self.dropdown_pos = mpos


        self.dropdown = pygame.Surface((width,height))
        
        i = 1
        self.dropdown_buttons
        for i in range (len(self.MatrixNames)):
            self.dropdown_buttons.append(Button((155,155,155), padding, (button_height*i + padding*(i+1)), button_width, button_height, self.dropdown, 
                                  self.update_matrix, self.MatrixMatrix[i], text = f'{self.MatrixNames[i]}'))
            self.dropdown_buttons[i].surface = self.dropdown
            self.dropdown_buttons[i].draw()
    


    def event_handler(self, event,mpos):
        mpos = mpos
        rel_mpos = (mpos[0] - self.dropdown_pos[0], mpos[1] - self.dropdown_pos[1] + 20 )#20 to adjust for taskbar
        print(rel_mpos)
        
        if self.dropdown.get_rect().collidepoint(rel_mpos) == False:
            self.toggle_dropdown = False

        if self.toggle_dropdown and self.dropdown.get_rect().collidepoint(rel_mpos) == True:
            for counter in range (len(self.dropdown_buttons)):
                self.dropdown_buttons[counter].click(rel_mpos)
        
        rel_mpos = (mpos[0] - self.input_pos[0], mpos[1] - self.input_pos[1] + 20 )
        if self.toggle_input and self.input_area.get_rect().collidepoint(rel_mpos) == True:
                self.name_box.onInputText(event, rel_mpos)
                    
            

    def draw(self):
        if self.toggle_dropdown:
            self.main_screen.blit(self.dropdown, self.dropdown_pos)
        if self.toggle_input:
            self.main_screen.blit(self.input_area, self.input_pos)
            

    def update_matrix(self, newmatrix):
        self.physics_engine.matrix = newmatrix

    #fix clicking of the menu,
    #implement loading functionality
    #create the saving menu & functionality.