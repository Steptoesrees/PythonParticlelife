import pygame
from Button import Button

class Sliders:
    def __init__(self, menu, whole_pos, whole_width=100, neg=False, max_val=1, slider_val=0, Name=''):

        self.max_val = max_val
        self.slider_value = slider_val
        self.neg = neg
        self.menu = menu

        #create the surface to draw on
        self.whole_width = whole_width
        self.whole_height = 40
        self.whole_pos = whole_pos
        self.whole = pygame.Surface((self.whole_width, self.whole_height))

        #create the bar for the slider to slide accross
        self.slider_width = self.whole_width*0.70
        self.slider_height = self.whole_height*0.1
        self.slider_pos = [self.whole_width*0.05, self.whole_height/2 - self.slider_height/2]
        self.slider = pygame.Rect(self.slider_pos[0],self.slider_pos[1],self.slider_width,self.slider_height)
        
        #create the button that slides across the slider bar thing
        self.slider_button_length = self.whole_height*0.4
        self.slider_button_height = self.whole_height*0.6
        if not neg:
            self.slider_button_pos = [self.slider.x - self.slider_button_length/2, self.whole_height/2 - self.slider_button_height/2]
            self.slider_button_og_pos = self.slider_button_pos.copy()
            self.slider_button_pos[0] = self.slider_value*(self.slider_width/self.max_val) + self.slider_button_og_pos[0]
        else:
            self.slider_button_pos = [self.slider.x - self.slider_button_length/2 + self.slider_width/2, self.whole_height/2 - self.slider_button_height/2]
            self.slider_button_og_pos = self.slider_button_pos.copy()
            self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_length/2
        
        self.slider_button = Button((200,200,200), self.slider_button_pos[0], self.slider_button_pos[1], self.slider_button_length, self.slider_button_height, self.whole, self.move, None)

        
        #create the input box to show the value of the slider (the value can also be modified by typing in here)
        self.input_length = self.whole_width*0.15
        self.input_height = self.whole_height*0.6
        self.input_pos = [self.whole_width*0.80, self.whole_height/2 - self.input_height/2]
        self.input_area = Button((90,90,90), self.input_pos[0], self.input_pos[1],self.input_length,self.input_height, self.whole, None, None)

        #create font for input box and lable
        self.label_font=pygame.font.SysFont('segoeui',12)
        self.label = self.label_font.render(Name, True, (255,255,255))

        

    def draw(self, screen):
        self.whole.fill((50,50,50))
        self.whole.blit(self.label, (5,1))
        pygame.draw.rect(self.whole, (100,100,100), (self.slider))
        self.slider_button.draw()
        self.input_area.draw()
        self.input_text()
        screen.blit(self.whole, (self.whole_pos[0], self.whole_pos[1]))

    def updateslider(self):
        if self.menu.sliderdrag:
            pass
        else:
            if not self.neg:
                self.slider_button_pos[0] = self.slider_value * (self.slider_width / self.max_val) + self.slider_button_og_pos[0]
            else:
                self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_length/2
            self.slider_button.button_rect.x = self.slider_button_pos[0]

    def move(self, dx):
        
        if self.menu.sliderdrag == True:
            self.slider_button_pos[0] += dx
            if self.slider_button_pos[0] < self.slider.x: #clamp position of slider
                self.slider_button_pos[0] = self.slider.x
            if self.slider_button_pos[0] > self.slider.x + self.slider_width:
                self.slider_button_pos[0] = self.slider.x + self.slider_width
            

            if not self.neg:#clamp value of slider when its only positive
                slider_value = self.slider_button_pos[0] - self.slider_pos[0]
                slider_value = round(slider_value / (((self.slider_button_og_pos[0]-self.slider_pos[0]) + self.slider_width)/self.max_val),2)


            else:#clamp value when it can be negative 
                slider_value = (self.slider_button_pos[0]-self.slider_pos[0])-self.slider_width/2
                slider_value = round(slider_value / 
                                     ((((self.slider_button_og_pos[0]-self.slider_pos[0])-self.slider_width/2) + 
                                       self.slider_width)/self.max_val/2),2)

            
            if slider_value >= self.max_val:
                slider_value = self.max_val
            if slider_value <= -self.max_val:
                slider_value = -self.max_val
            self.slider_value = slider_value
        
        self.slider_button.button_rect.x = self.slider_button_pos[0]
            

    def button_click(self, mousepos, dx):
        mousepos = (mousepos[0]-self.whole_pos[0]  , mousepos[1]- self.whole_pos[1])
        self.slider_button.click(mousepos, value=dx)

    def input_text(self):
        text = str(self.slider_value)
        if len(text) > 5:
            text = text[:5]
        
        text = self.label_font.render(text, True, (255,255,255))
        self.whole.blit(text, (self.input_pos[0]+5, self.input_pos[1]+(self.input_height/2 - text.get_height()/2)))
        self.input_area.draw(text_pos=(5,self.input_height/2 - text.get_height()/2))