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

        # initialise save area
        padding = 5
        button_height = 20
        button_width = 60
        input_width = 140
        area_width = input_width + button_width + padding*3
        area_height = button_height + padding*2
        self.matrix_data = ["name", self.physics_engine.matrix]
        print (self.matrix_data)
        self.save_area = pygame.Surface((area_width,area_height))
        self.input_box = InputBox((padding,padding), (input_width, button_height), "enter matrix name")
        self.confirm_button = Button((100,100,100), (padding*2)+input_width, padding, button_width, button_height, self.save_area, self.save_matrix, self.matrix_data)
        

    def save_input(self):
        self.toggle_input = not self.toggle_input
        self.toggle_dropdown = False
        mpos = pygame.mouse.get_pos()
        self.input_pos = mpos
        
       
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
        self.toggle_input = False
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
      
      
                    
            

    def draw(self):
        if self.toggle_dropdown:
            self.main_screen.blit(self.dropdown, self.dropdown_pos)
        if self.toggle_input:
            self.confirm_button.draw()
            self.input_box.draw(self.save_area)
            self.main_screen.blit(self.save_area, self.input_pos)
            

    def update_matrix(self, newmatrix):
        self.physics_engine.matrix = newmatrix



    def save_matrix(self, data):
        json_data = {"name": data[0], "matrix": data[1]}
        try:
            #from geeksforgeeks
            with open("SavedMatrix.json", "r+") as file:
                matrixes = json.load(file)
                matrixes.append(json_data)
                file.seek(0)
                json.dump(matrixes, file)
                
        except:
            #from geeksforgeeks
            with open("particle_Life_OOP//SavedMatrix.json", "r+") as file:
                matrixes = json.load(file)
                matrixes.append(json_data)
                file.seek(0)
                json.dump(matrixes, file)
                

    #fix clicking of the menu,
    #implement loading functionality
    #create the saving menu & functionality.


    #SAVE MATIX
    #initialise with a surface, input area and button.
    #event handling
    #   