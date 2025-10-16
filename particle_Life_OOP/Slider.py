import pygame
from Button import Button
from input_box import InputBox

class Sliders:
    def __init__(self, menu, whole_pos, whole_width=100, neg=False, max_val=1, slider_val=0, Name=''):
        #constructor method

        
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
            self.slider_button_og_pos = self.slider_button_pos.copy() #finds the positon of the button at a value of 0

            #sets positon of slider based on value passed into the method
            self.slider_button_pos[0] = self.slider_value*(self.slider_width/self.max_val) + self.slider_button_og_pos[0]


        else:
            self.slider_button_pos = [self.slider.x - self.slider_button_width/2 + self.slider_width/2, self.whole_height/2 - self.slider_button_height/2]
            self.slider_button_og_pos = self.slider_button_pos.copy() #finds the positon of the button at a value of 0
            self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_width/2
        
        
        #sets positon of slider based on value passed into the method
        self.slider_button = Button((200,200,200), self.slider_button_pos[0], self.slider_button_pos[1], self.slider_button_width, self.slider_button_height, self.whole, self.move, None)



        
        #create the input box to show the value of the slider 
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
        pygame.draw.rect(self.whole, (100,100,100), (self.slider)) #draw the 'slider bar'
        self.slider_button.draw()
        self.input_box.draw(self.whole)
        screen.blit(self.whole, (self.whole_pos[0], self.whole_pos[1]))

    def updateslider(self):
        if self.menu.sliderdrag: # skip if the slider is being moved
            pass
        

        else:
            #update the position of the slider based on its value
            if not self.neg:
                self.slider_button_pos[0] = self.slider_value * (self.slider_width / self.max_val) + self.slider_button_og_pos[0]
            else:
                self.slider_button_pos[0] = self.slider.x + self.slider_width/2 + (self.slider_value/self.max_val)*(self.slider_width/2) - self.slider_button_width/2
            self.slider_button.button_rect.x = self.slider_button_pos[0]

    def move(self, dx):
        
        if self.menu.sliderdrag == True: #if left click is held down:
            self.slider_button_pos[0] += dx #moves the x pos of the button by the same amount the mouse moves.

            #find min and max post the button should be at
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
                relative_pos = (self.slider_button_pos[0] - start_pos) / (self.slider_width / 2)
                slider_value = relative_pos * self.max_val

            self.slider_value = slider_value
            self.input_box.text = str(self.slider_value) #update the text in the box to be the value
        
        self.slider_button.button_rect.x = self.slider_button_pos[0] # update the position of the slider
            

    def button_click(self, mousepos, dx): #finds relative mouse position and calls the slider buttons click function with the mouse movement as a parameter
        mousepos = (mousepos[0]-self.whole_pos[0]  , mousepos[1]- self.whole_pos[1])
        self.slider_button.click(mousepos, value=dx)

    def Input(self, event, mousepos):
        mousepos = (mousepos[0]-self.whole_pos[0]  , mousepos[1]- self.whole_pos[1]) #relative mouse position
        self.input_box.onInput(event, mousepos)  # calls the inputs box onInput function

        if self.input_box.colour == self.input_box.colour_inactive: #updates the value when clicked off
            if self.input_box.text != '': #checks the text is not empty
                val = float(self.input_box.text) #converts text to a value

                #clamps the value to not go beyond the bounds set by the sliders max value
                if val > self.max_val:
                    val = self.max_val
                if val < -self.max_val:
                    val = -self.max_val

                self.slider_value = val #updates the slider's value
                
    
        
