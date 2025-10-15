import pygame

class Camera:
    def __init__(self, cam_x, cam_y, cam_size):
        #constructor function
        self.cam_size = cam_size
        self.cam = pygame.Surface((self.cam_size,self.cam_size))
        self.cam_x = cam_x
        self.cam_y = cam_y

        self.velocityV = False #boolean toggles set to false
        self.dragging = False



    def drawParticles(self, screen, physics):
        #clears the sim area
        self.cam.fill((0,0,0))

        #loops through all the particles
        for i in range(len(physics.particles)):
            physics.particles[i].drawParticle(self.cam, self.cam_size) #draws particles
            if self.velocityV:
                physics.particles[i].drawVelocityVector(self.cam, self.cam_size) #draws velocity vector if toggled on

        screen.blit(self.cam, (self.cam_x,self.cam_y))#draws the surface to the screen.
        
#relcoords = 1
#pos1 = mpos/camsize
#pos2 = (pos1*scale)*camsize
#scam = scam - (pos2-pos1)
    def zoomIn(self, zoom_amount, mpos):
        scale = 50 * abs(zoom_amount) #increase speed of zoom
        relmouse = [mpos[0]-self.cam_x, mpos[1]-self.cam_y] #relative mouse position
        self.cam_size += scale #increases the size of the sim area, this is the zooming
        self.cam_size = round(self.cam_size, 1) #improves performance, likely due to multipling the force and velocity of particles byt the cam size

        if self.cam_size > 40:# <- arbritrary, when the size gets small and you zoom in, the sim area can be moved very far away and lost.

            #calculates a new position of the sim area to keep the mouse on the same spot of the sim area
            self.cam_x = self.cam_x - (((relmouse[0]/self.cam_size)*scale)-(relmouse[0]/self.cam_size))
            self.cam_y = self.cam_y - (((relmouse[1]/self.cam_size)*scale)-(relmouse[1]/self.cam_size))
        
        self.cam = pygame.Surface((self.cam_size,self.cam_size)) #recreates the surface
    
    def zoomOut(self, zoom_amount, mpos):
        scale = 50 * abs(zoom_amount) #increase speed of zoom
        relmouse = [mpos[0]-self.cam_x, mpos[1]-self.cam_y] #relative mouse position
        self.cam_size -= 50 * abs(zoom_amount)#increases the size of the sim area, this is the zooming
        self.cam_size = round(self.cam_size, 1)#improves performance, likely due to multipling the force and velocity of particles byt the cam size
        if self.cam_size <= 0:
            self.cam_size = 1

        #calculates a new position of the sim area to keep the mouse on the same spot of the sim area
        self.cam_x = self.cam_x + (((relmouse[0]/self.cam_size)*scale)-(relmouse[0]/self.cam_size))
        self.cam_y = self.cam_y + (((relmouse[1]/self.cam_size)*scale)-(relmouse[1]/self.cam_size))
        self.cam = pygame.Surface((self.cam_size,self.cam_size))

    def pan(self, dx, dy):
        #moves the sim area by the same amount the mouse moves
        if self.dragging:
            self.cam_x += dx
            self.cam_y += dy
        
