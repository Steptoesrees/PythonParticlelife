from input_box import InputBox
from Button import Button
import json
import pygame

class save:
    def __init__(self, screen):
        with open("particle_Life_OOP\SavedMatrix.json", "r") as file:
            matrixes = json.load(file)
            self.MatrixNames =  matrixes.get("names", [])
            self.MatrixMatrix =  matrixes.get("matrixes", [])

        main_screen = screen
        self.dropdown = pygame.Surface(0,0)

    def save_input(self):
        pass
        
       
# click Button
# update dropdown <- will call toggle dropdown in the function
# draw dropdown
# event handler
# on click:
#  if mpos outside dropdown toggle dropdown off
#  run button.click for all buttons

    def update_dropdown(self):
        mpos = pygame.mouse.get_pos()
        padding = 5
        button_height = 20
        button_width = 80
        width = button_width + padding*2
        height = padding*2 + button_height*len(self.MatrixNames)

        self.dropdown = pygame.Surface((width,height))

        buttons = []
        for i in range (len(self.MatrixNames)-1):
            buttons.append(Button((155,155,155), mpos[0], mpos[1], button_width, button_height, self.dropdown, 
                                  self.load_matrix, self.MatrixMatrix[i], text = self.MatrixNames[i]))