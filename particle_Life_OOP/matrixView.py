import pygame
from input_box import InputBox
from Button import Button
from saveLoad import save as s

class matrixView():
    def __init__(self, screen, main_screen, xloc, yloc, height, width, Physics):
        self.screen = screen

        self.matrix_view = pygame.Surface((width,height))

        self.save = s(screen, main_screen, Physics)

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

        self.saveButton = Button((155,155,155), (self.header_thickness + 20 + self.cell_size*3),(self.header_thickness+5), 80,20, self.matrix_view, self.save.activate_input, text = "save Matrix")
        self.loadButton = Button((155,155,155), (self.header_thickness + 20 + self.cell_size*3),(self.header_thickness+30), 80,20, self.matrix_view, self.save.update_dropdown, text = "Load Matrix")
        self.removeButton = Button((155,155,155), (self.header_thickness + 20 + self.cell_size*3),(self.header_thickness+55), 80,20, self.matrix_view, self.save.update_rem_dropdown, text = "Del Matrix")
        

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

        #self.saveing and loading buttons
        



        self.draw_cells()
        self.saveButton.draw()
        self.loadButton.draw()
        self.removeButton.draw()

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
        mpos = (mpos[0] - self.xloc, mpos[1] - self.yloc)
        for row in range(3):
            for col in range(3):
                if self.cells[row][col].colour == self.cells[row][col].colour_inactive:
                    self.cells[row][col].text = ''
                
                if self.cells[row][col].onInput(event, mpos) and len(self.cells[row][col].text) > 0:
                    val = pygame.math.clamp(float(self.cells[row][col].text),-1.0,1.0)
                    self.physics_engine.matrix[row][col] = val

        self.save.event_handler(event,mpos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.save.toggle_input and not self.save.toggle_rem_dropdown:
                self.saveButton.click(mpos)
            if not self.save.toggle_dropdown and not self.save.toggle_rem_dropdown:
                self.loadButton.click(mpos)
            if not self.save.toggle_dropdown and not self.save.toggle_input:
                self.removeButton.click(mpos)
            

