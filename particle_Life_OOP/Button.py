import pygame


class Button():
    def __init__(self,colour, xloc, yloc, width, height,surface, text, use):
        self.colour = colour 
        self.button_rect = pygame.Rect(xloc,yloc,width,height) 
        self.surface = surface 
        self.function = use
        
        self.font=pygame.font.SysFont('segoeui',30)
        self.text = text



    def draw(self):
        pygame.draw.rect(self.surface,self.colour,(self.button_rect)) 

        if self.text != '':
            text = self.font.render(self.text, True, (255,255,255))
            text_x = self.button_rect.x + (self.button_rect.width/2 - text.get_width()/2)
            text_y = self.button_rect.y + (self.button_rect.height/2 - text.get_height()/2)
            self.surface.blit(text, (text_x, text_y))

    def click(self):
        mousepos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mousepos) and self.function != None:
            self.function()
        else:
            return False 
        

    