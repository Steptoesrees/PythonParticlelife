import pygame
from input_box import InputBox

class matrixView():
    def __init__(self, screen, xloc, yloc, height, width, Physics):
        self.screen = screen

        self.matrix_view = pygame.Surface((width,height))

        self.xloc = xloc
        self.yloc = yloc
        self.width = width
        self.height = height

        
        self.colours = [(255,0,0),(0,255,0),(0,0,255)]
        self.physics_engine = Physics
        self.font = pygame.font.SysFont('segoeui', 12)

        self.cell_ratio = 3.5
        self.cell_size = min(self.width // self.cell_ratio, self.height // self.cell_ratio)
        self.header_thickness = self.cell_size//self.cell_ratio
        self.cells = self.create_cells()
        

    def draw(self):
        self.matrix_view.fill((40,40,40))
        

        padding = 5
        
        #top headers
        for i in range(3):
            pygame.draw.rect(self.matrix_view, self.colours[i], (self.header_thickness + padding*(i+1) + i * self.cell_size, 0, self.cell_size, self.header_thickness))
        
        #side headers
        for i in range(3):
            pygame.draw.rect(self.matrix_view, self.colours[i], (0, self.header_thickness + padding*(i+1) + i * self.cell_size, self.header_thickness, self.cell_size))
        
        
        for row in range(3):
            for col in range(3):
                val = self.physics_engine.matrix[row][col]
                
                if val > 0:
                    intensity = int(val * 255)
                    self.cells[row][col].colour_inactive = (0, intensity, 0)
                    self.cells[row][col].colour_active = (80,intensity,80)
                elif val < 0:
                    intensity = int(-val * 255)
                    self.cells[row][col].colour_inactive = (intensity, 0, 0)
                    self.cells[row][col].colour_active = (intensity, 80, 80)
                    
                else:
                    self.cells[row][col].colour_inactive = (0, 0, 0)

                if (self.cells[row][col].colour == self.cells[row][col].colour_inactive 
                and self.cells[row][col] != self.physics_engine.matrix[row][col]):
                    
                    self.cells[row][col].text = str(round(val,2))



        self.draw_cells()
        self.screen.blit(self.matrix_view, (self.xloc, self.yloc))

    def create_cells(self):
        self.cells = []
        
        padding = 5

        for row in range(3):
            row_cells = []
            for col in range(3):
                cell = InputBox((self.header_thickness + padding*(col+1) + col * self.cell_size, self.header_thickness + padding*(row+1) + row * self.cell_size), (self.cell_size, self.cell_size), str(self.physics_engine.matrix[row][col]))
                row_cells.append(cell)
            self.cells.append(row_cells)
        return self.cells

    def draw_cells(self):
        for row in self.cells:
            for cell in row:
                cell.draw(self.matrix_view)

    def input_event(self, event, mpos):
        for row in range(3):
            for col in range(3):
                if self.cells[row][col].colour == self.cells[row][col].colour_inactive:
                    self.cells[row][col].text = ''
                
                if self.cells[row][col].onInput(event, (mpos[0],mpos[1]-20)) and len(self.cells[row][col].text) > 0:
                    val = pygame.math.clamp(float(self.cells[row][col].text),-1.0,1.0)
                    self.physics_engine.matrix[row][col] = val