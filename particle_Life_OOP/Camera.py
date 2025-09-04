import pygame
from Particle import Particle
from physicsEngine import PhysicsEngine

class Camera:
    def __init__(self, cam_x, cam_y, cam_size):
        self.cam_size = cam_size
        self.cam = pygame.Surface((self.cam_size,self.cam_size))
        self.cam_x = cam_x
        self.cam_y = cam_y


    def drawParticles(self, screen, physics):
        self.cam.fill((0,0,0))
        for i in range(len(physics.particles)):
            physics.particles[i].drawParticle(self.cam, self.cam_size)
            screen.blit(self.cam, (self.cam_x,self.cam_y))
            

    def zoomIn(self, zoom_amount):
        self.cam_size += 50 * abs(zoom_amount)
        self.cam = pygame.Surface((self.cam_size,self.cam_size))
    
    def zoomOut(self, zoom_amount):
        self.cam_size -= 50 * abs(zoom_amount)
        if self.cam_size <= 0:
            self.cam_size = 1
        self.cam = pygame.Surface((self.cam_size,self.cam_size))

    def pan(self, dx, dy):
        self.cam_x += dx
        self.cam_y += dy
        
