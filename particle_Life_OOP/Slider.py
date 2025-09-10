import pygame
from Button import Button

class Sliders:
    def __init__(self, whole_pos, whole_width=100, neg=False):
        self.whole_width = whole_width
        self.whole_height = 40
        self.whole_pos = whole_pos
        self.whole = pygame.Surface((self.whole_width, self.whole_height))

        self.slider_width = self.whole_width*0.70
        self.slider_height = self.whole_height*0.1
        self.slider_pos = [self.whole_width*0.05, self.whole_height/2 - self.slider_height/2]
        self.slider = pygame.Rect(self.slider_pos[0],self.slider_pos[1],self.slider_width,self.slider_height)
        
        self.slider_button_length = self.whole_height*0.2
        self.slider_button_height = self.whole_height*0.6
        if not neg:
            self.slider_button_pos = [self.slider.x - self.slider_button_length/2, self.whole_height/2 - self.slider_button_height/2]
        else:
            self.slider_button_pos = [self.slider.x - self.slider_button_length/2 + self.slider_width/2, self.whole_height/2 - self.slider_button_height/2]
        self.slider_button_og_pos = self.slider_button_pos.copy()
        self.slider_button = Button((200,200,200), self.slider_button_pos[0], self.slider_button_pos[1], self.slider_button_length, self.slider_button_height, self.whole, None,None)

        
        self.input_length = self.whole_width*0.15
        self.input_height = self.whole_height*0.6
        self.input_pos = [self.whole_width*0.80, self.whole_height/2 - self.input_height/2]
        self.input_area = pygame.Rect(self.input_pos[0], self.input_pos[1],self.input_length,self.input_height)

        self.dragging = False
        
    def draw(self, screen):
        pygame.draw.rect(self.whole, (100,100,100), (self.slider))
        self.slider_button.draw()
        pygame.draw.rect(self.whole, (255,255,255), (self.input_area))
        screen.blit(self.whole, (self.whole_pos[0], self.whole_pos[1]))

    def input(self):
        pass

    def button_click(self):
        pass