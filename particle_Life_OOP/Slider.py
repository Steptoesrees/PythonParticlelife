import pygame
from Button import Button
from input_box import InputBox

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
        self.slider_button_width = self.whole_height*0.4
        self.slider_button_height = self.whole_height*0.6
        if not neg:
            self.slider_button_pos = [self.slider.x - self.slider_button_width/2, self.whole_height/2 - self.slider_button_height/2]
            self.slider_button_og_pos = self.slider_button_pos.copy()
            self.slider_button_pos[0] = self.slider_value*(self.slider_width/self.max_val) + self.slider_button_og_pos[0]
        else:
            self.slider_button_pos = [self.slider.x - self.slider_button_width/2 + self.slider_width/2, self.whole_height/2 - self.slider_button_height/2]
            self.slider_button_og_pos = self.slider_button_pos.copy()
            self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_width/2
        
        self.slider_button = Button((200,200,200), self.slider_button_pos[0], self.slider_button_pos[1], self.slider_button_width, self.slider_button_height, self.whole, self.move, None)

        
        #create the input box to show the value of the slider (the value can also be modified by typing in here)
        self.input_width = self.whole_width*0.15
        self.input_height = self.whole_height*0.6
        self.input_pos = [self.whole_width*0.80, self.whole_height/2 - self.input_height/2]
        self.input_box = InputBox(self.input_pos, (self.input_height, self.input_width), str(self.slider_value))

        #create font for input box and lable
        self.label_font=pygame.font.SysFont('segoeui',12)
        self.label = self.label_font.render(Name, True, (255,255,255))

        

    def draw(self, screen):
        self.whole.fill((50,50,50))
        self.whole.blit(self.label, (5,1))
        pygame.draw.rect(self.whole, (100,100,100), (self.slider))
        self.slider_button.draw()
        self.input_box.draw(self.whole)
        screen.blit(self.whole, (self.whole_pos[0], self.whole_pos[1]))

    def updateslider(self):
        

        if self.menu.sliderdrag:
            pass
        

        else:
            if not self.neg:
                self.slider_button_pos[0] = self.slider_value * (self.slider_width / self.max_val) + self.slider_button_og_pos[0]
            else:
                self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_width/2
            self.slider_button.button_rect.x = self.slider_button_pos[0]

    def move(self, dx):
        
        if self.menu.sliderdrag == True:
            self.slider_button_pos[0] += dx

            min_pos = self.slider.x - self.slider_button_width/2
            max_pos = self.slider.x + self.slider_width - self.slider_button_width/2
            if self.slider_button_pos[0] < min_pos: #clamp position of slider
                self.slider_button_pos[0] = min_pos
            if self.slider_button_pos[0] > max_pos:
                self.slider_button_pos[0] = max_pos
            
            

            if not self.neg:#find value when positive
                pos = (self.slider_button_pos[0] - (self.slider.x - self.slider_button_width / 2)) / self.slider_width
                slider_value = pos * self.max_val

            else:#find value when negative
                start_pos = self.slider.x + self.slider_width / 2 - self.slider_button_width / 2
                slider_value = (self.slider_button_pos[0]-self.slider_pos[0])-self.slider_width/2
                relative_pos = (self.slider_button_pos[0] - start_pos) / (self.slider_width / 2)
                slider_value = relative_pos * self.max_val

            
            if slider_value >= self.max_val:
                slider_value = self.max_val
            if slider_value <= -self.max_val:
                slider_value = -self.max_val
            self.slider_value = slider_value
            self.input_box.text = str(self.slider_value)
        
        self.slider_button.button_rect.x = self.slider_button_pos[0]
            

    def button_click(self, mousepos, dx):
        mousepos = (mousepos[0]-self.whole_pos[0]  , mousepos[1]- self.whole_pos[1])
        self.slider_button.click(mousepos, value=dx)

    def Input(self, event, mousepos):
        mousepos = (mousepos[0]-self.whole_pos[0]  , mousepos[1]- self.whole_pos[1])
        self.input_box.onInput(event, mousepos)

        if self.input_box.color == self.input_box.color_inactive:
            try:
                val = float(self.input_box.text)
                if val > self.max_val:
                    val = self.max_val
                if val < -self.max_val:
                    val = -self.max_val
                self.slider_value = val
            except ValueError:
                self.input_box.text = str(self.slider_value)
    
        
