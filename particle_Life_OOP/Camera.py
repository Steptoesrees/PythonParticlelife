import pygame

class Camera:
    def __init__(self, cam_x, cam_y, cam_size):
        self.cam_size = cam_size
        self.cam = pygame.Surface((self.cam_size,self.cam_size))
        self.cam_x = cam_x
        self.cam_y = cam_y
        self.dragging = False


    def drawParticles(self, screen, physics):
        self.cam.fill((0,0,0))
        for i in range(len(physics.particles)):
            physics.particles[i].drawParticle(self.cam, self.cam_size)
        screen.blit(self.cam, (self.cam_x,self.cam_y))
        
#relcoords = 1
#pos1 = mpos/camsize
#pos2 = (pos1*scale)*camsize
#scam = scam - (pos2-pos1)
    def zoomIn(self, zoom_amount, mpos):
        scale = 50 * abs(zoom_amount)
        relmouse = [mpos[0]-self.cam_x, mpos[1]-self.cam_y]
        self.cam_size += scale
        self.cam_size = round(self.cam_size, 1)
        if self.cam_size > 40:
            self.cam_x = self.cam_x - (((relmouse[0]/self.cam_size)*scale)-(relmouse[0]/self.cam_size))
            self.cam_y = self.cam_y - (((relmouse[1]/self.cam_size)*scale)-(relmouse[1]/self.cam_size))
        
        self.cam = pygame.Surface((self.cam_size,self.cam_size))
    
    def zoomOut(self, zoom_amount, mpos):
        scale = 50 * abs(zoom_amount)
        relmouse = [mpos[0]-self.cam_x, mpos[1]-self.cam_y]
        self.cam_size -= 50 * abs(zoom_amount)
        if self.cam_size <= 0:
            self.cam_size = 1
        if self.cam_size > 40:
            self.cam_x = self.cam_x + (((relmouse[0]/self.cam_size)*scale)-(relmouse[0]/self.cam_size))
            self.cam_y = self.cam_y + (((relmouse[1]/self.cam_size)*scale)-(relmouse[1]/self.cam_size))
        self.cam = pygame.Surface((self.cam_size,self.cam_size))

    def pan(self, dx, dy):
        if self.dragging:
            self.cam_x += dx
            self.cam_y += dy
        
