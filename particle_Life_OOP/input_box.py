import pygame
class InputBox():
    TextOffsetX = 5
    TextOffsety = 2.5
    def __init__(self, pos, size, text):
        posx = pos[0]
        posy = pos[1]
        width = size[0]
        height = size[1]
        self.rect = pygame.Rect(posx, posy, height, width)

        self.colour_inactive = (100, 100, 100)
        self.colour_active = (200, 200, 200)
        self.colour = self.colour_inactive

        self.text = text
        self.font = pygame.font.SysFont('segoeui', 15)

    def onInput(self, event, mousepos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos):
                self.colour = self.colour_active

            else:
                self.colour = self.colour_inactive

        if event.type == pygame.TEXTINPUT and self.colour == self.colour_active:
            if event.text.isdigit() or (event.text == '.' and '.' not in self.text) or (event.text == '-' and len(self.text) == 0):
                self.text += event.text
                
        
        if event.type == pygame.KEYDOWN and self.colour == self.colour_active:
            if event.key == pygame.K_BACKSPACE and self.colour == self.colour_active:
                self.text = self.text[:-1]
                

            if event.key == pygame.K_RETURN and self.colour == self.colour_active:
                self.colour = self.colour_inactive
                return True

    def onInputText(self, event, mousepos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos):
                self.colour = self.colour_active
                self.text = ""

            else:
                self.colour = self.colour_inactive

        if event.type == pygame.TEXTINPUT and self.colour == self.colour_active:
            self.text+= event.text

        

    def draw(self, screen):
        if len(self.text) > 7:
            self.text = self.text[:7]
        if self.colour != self.colour_active:
            self.colour = self.colour_inactive
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=3)
        text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + self.TextOffsetX, self.rect.y + self.TextOffsety))
        