import pygame


class Button():
    def __init__(self,colour, xloc, yloc, width, height,surface, use, value=None, 
                 text=''):
        #constructor method.
        self.colour = colour 
        self.button_rect = pygame.Rect(xloc,yloc,width,height) 
        self.surface = surface 
        self.function = use
        self.value = value
        
        self.font=pygame.font.SysFont('segoeui',15)
        self.text = text



    def draw(self, BR=0, text_pos=(None,None)):
        #draws the button
        pygame.draw.rect(self.surface,self.colour,(self.button_rect), border_radius=BR) 

        if self.text != '': #allows a custom text pos to be set
            text = self.font.render(self.text, True, (255,255,255))
            if text_pos != (None,None):
                text_x = self.button_rect.x + text_pos[0]
                text_y = self.button_rect.y + text_pos[1]
            else: #draws text on top of rect
                text_x = self.button_rect.x + (self.button_rect.width/2 - text.get_width()/2)
                text_y = self.button_rect.y + (self.button_rect.height/2 - text.get_height()/2)
            self.surface.blit(text, (text_x, text_y)) #draws button to screen


    def click(self, pos, value=None):
        if value != None: #allows a value to be passed through the click call instead of from the attribute
            self.value = value
        mousepos = pos
        if self.button_rect.collidepoint(mousepos) and self.function != None and self.value != None:
            self.function(self.value) # if clicked with a value, call function passing value as a parameter
        elif self.button_rect.collidepoint(mousepos) and self.function != None:
            self.function() #if clicked without a value, call function without passing a value
        else: 
            return False #if not clicked return false
        

    