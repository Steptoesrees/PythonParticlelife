import random
import pygame
import math
import ctypes
from physicsEngine import PhysicsEngine
from Camera import Camera
import Menu


running = True
pygame.init()
class main():
    def __init__(self):
        
        self.paused = False
        self.run()

    def run(self):
        running = True
        dragging = False
        

        screen_info = pygame.display.Info()
        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
        clock = pygame.time.Clock()
        
        P = PhysicsEngine()
        P.changeParticleCount(200)
        cam = Camera(0, 0,screen_info.current_h*3)
        print(P)
        menu = Menu.Menu(screen, screen_info.current_w, screen_info.current_h, P)
        taskbar = Menu.Taskbar(screen, screen_info.current_w, screen_info.current_h, menu, P)
        
        

        while running:
            
                    
            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_SPACE:
                        P.paused = not P.paused



                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.get_rel()
                        dragging = True
                        taskbar.click_buttons()     
                        menu.force_graph.click_buttons()                   

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                
                if event.type == pygame.MOUSEMOTION:
                    if dragging:
                        
                        rel = list(pygame.mouse.get_rel())
                        cam.pan(rel[0], rel[1])
                

                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        cam.zoomOut(event.y)
                        
                    if event.y > 0:
                            cam.zoomIn(event.y)

            P.interactions()

            cam.drawParticles(screen, P)

            menu.draw()
            
            taskbar.draw()
            
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()