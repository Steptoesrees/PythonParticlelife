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

        self.color_inactive = (100, 100, 100)
        self.color_active = (200, 200, 200)
        self.color = self.color_inactive

        self.text = text
        self.font = pygame.font.SysFont('segoeui', 15)

    def onInput(self, event, mousepos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos):
                self.color = self.color_active

            else:
                self.color = self.color_inactive

        if event.type == pygame.TEXTINPUT and self.color == self.color_active:
            print("test")
            if event.text.isdigit() or (event.text == '.' and '.' not in self.text):
                self.text += event.text
                
        
        if event.type == pygame.KEYDOWN and self.color == self.color_active:
            if event.key == pygame.K_BACKSPACE and self.color == self.color_active:
                self.text = self.text[:-1]
                

            if event.key == pygame.K_RETURN and self.color == self.color_active:
                self.color = self.color_inactive
                

        

    def draw(self, screen):
        if len(self.text) > 7:
            self.text = self.text[:7]
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + self.TextOffsetX, self.rect.y + self.TextOffsety))
        