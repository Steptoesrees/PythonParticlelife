import pygame
class InputBox():
    #constants
    TextOffsetX = 5
    TextOffsety = 2.5
    def __init__(self, pos, size, text):
        #constructor function
        posx = pos[0]
        posy = pos[1]
        width = size[0]
        height = size[1]
        self.rect = pygame.Rect(posx, posy, height, width) # creates rect for input

        self.colour_inactive = (100, 100, 100) #sets active and inactive colour, colour is set to inactive
        self.colour_active = (200, 200, 200)
        self.colour = self.colour_inactive

        #text
        self.text = text
        self.font = pygame.font.SysFont('segoeui', 15)



    def onInput(self, event, mousepos): #allows user to enter a number
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos):
                self.colour = self.colour_active#sets the colour to active when the box is clicked on

            else:
                self.colour = self.colour_inactive #sets the colour to inactive when clicked off

        if event.type == pygame.TEXTINPUT and self.colour == self.colour_active:
            #when the box is active, allows the user to enter a number
            if event.text.isdigit() or (event.text == '.' and '.' not in self.text) or (event.text == '-' and len(self.text) == 0):
                self.text += event.text # adds the text added by the user to the text string
                
        
        if event.type == pygame.KEYDOWN and self.colour == self.colour_active:
            # when backspace is clicked, remove one from the text string
            if event.key == pygame.K_BACKSPACE and self.colour == self.colour_active:
                self.text = self.text[:-1]
                

            if event.key == pygame.K_RETURN and self.colour == self.colour_active:
                # when enter is pressed, return true
                self.colour = self.colour_inactive
                return True

    def onInputText(self, event, mousepos): #for entering any character
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos): #when clicking on the button, set it to active and clear the text
                self.colour = self.colour_active
                self.text = ""

            else:
                self.colour = self.colour_inactive

        if event.type == pygame.TEXTINPUT and self.colour == self.colour_active: 
            self.text+= event.text #when the user types, add the character to the text string

        

    def draw(self, screen): # draws the input box
        if len(self.text) > 7:
            self.text = self.text[:7] #limits length to 7 chars

        if self.colour != self.colour_active:
            self.colour = self.colour_inactive #updates the colours

        #draws the rect to screen then the text on top of it
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=3)
        text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + self.TextOffsetX, self.rect.y + self.TextOffsety))
        