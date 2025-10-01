import pygame
import ctypes
from physicsEngine import PhysicsEngine
from Camera import Camera
from saveLoad import save as s

import Menu


running = True
pygame.init()
class main():
    def __init__(self):
        self.paused = False
        self.run()

    def run(self):
        running = True
        

        screen_info = pygame.display.Info()
        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
        clock = pygame.time.Clock()
        save = s(screen)
        
        physics_engine = PhysicsEngine()
        physics_engine.changeParticleCount(200)
        cam = Camera(0, 0,screen_info.current_h*2)
        menu = Menu.Menu(screen, screen_info.current_w, screen_info.current_h, physics_engine)
        taskbar = Menu.Taskbar(screen, screen_info.current_w, screen_info.current_h, menu, physics_engine)
        
        

        while running:
            
            mousepos = pygame.mouse.get_pos()
            screen.fill((0, 0, 0))

            for event in pygame.event.get():

                menu.input_event(event)

                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_SPACE:
                        physics_engine.paused = not physics_engine.paused



                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        pygame.mouse.get_rel()
                        if taskbar.mouse_in_taskbar(mousepos):
                            taskbar.click_buttons()   
                        elif menu.mouse_in_menu(mousepos):  
                            menu.force_graph.click_buttons()
                            menu.graph_matrix_button.click((mousepos[0],mousepos[1]))
                            menu.sliderdrag = True 
                        else:  
                            cam.dragging = True


                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        cam.dragging = False
                        menu.sliderdrag = False

                
                if event.type == pygame.MOUSEMOTION:
                    rel = list(pygame.mouse.get_rel())
                    cam.pan(rel[0], rel[1])
                    menu.slide(mousepos, rel[0])
                    
                
                

                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        cam.zoomOut(event.y)
                        
                    if event.y > 0:
                            cam.zoomIn(event.y)

            physics_engine.interactions()

            cam.drawParticles(screen, physics_engine)

            menu.draw()
            save.update_dropdown()
            save.draw()
            
            taskbar.draw(clock)
            
            pygame.display.update()
            clock.tick(31)


if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(500, 50)
    pygame.key.start_text_input()
    pygame.font.init()
    main()