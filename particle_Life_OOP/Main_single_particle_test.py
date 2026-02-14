import pygame
import ctypes
from physicsEngine import PhysicsEngine
from Camera import Camera
from saveLoad import save as s

import Menu


# main class, everything starts here
class main():
    # constructor function
    def __init__(self):
        self.run()  # calls the run function

    def setup_single_particle_test(self, physics_engine):
        physics_engine.particles = []
        physics_engine.addParticle()

        particle = physics_engine.particles[0]
        particle.pos_x = 0.05
        particle.pos_y = 0.05
        particle.vel_x = -1.0
        particle.vel_y = -1.0

    def run(self):
        running = True

        # gets the computer's monitor size, sets window size to be the size of the monitor
        screen_info = pygame.display.Info()
        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))

        # initialises clock
        clock = pygame.time.Clock()

        # creates objects for the main componants of the project
        physics_engine = PhysicsEngine()
        self.setup_single_particle_test(physics_engine)
        cam = Camera(0, 0, screen_info.current_h * 2)
        menu = Menu.Menu(screen, screen_info.current_w, screen_info.current_h, physics_engine)
        taskbar = Menu.Taskbar(screen, screen_info.current_w, screen_info.current_h, menu, physics_engine, cam)

        # main game loop
        while running:

            mousepos = pygame.mouse.get_pos()

            # clear screen
            screen.fill((0, 0, 0))

            # event loop
            for event in pygame.event.get():

                menu.input_event(event)

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if physics_engine.paused:
                        if event.key == pygame.K_k:
                            physics_engine.interactions(bypass=True)

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_SPACE:
                        physics_engine.paused = not physics_engine.paused

                # calls functions that only happen on a mouse clck
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        pygame.mouse.get_rel()
                        if taskbar.mouse_in_taskbar(mousepos):
                            taskbar.click_buttons()
                        elif menu.mouse_in_menu(mousepos):
                            menu.force_graph.click_buttons(event)
                            menu.graph_matrix_button.click((mousepos[0], mousepos[1]))
                            menu.sliderdrag = True
                        else:
                            cam.dragging = True

                # toggles dragging toggles off on button release
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        cam.dragging = False
                        menu.sliderdrag = False

                # for moving the simulation area and the sliders
                if event.type == pygame.MOUSEMOTION:
                    rel = list(pygame.mouse.get_rel())
                    cam.pan(rel[0], rel[1])
                    menu.slide(mousepos, rel[0])

                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        cam.zoomOut(event.y, mousepos)

                    if event.y > 0:
                        cam.zoomIn(event.y, mousepos)

            # this function is where all the particle calculations happen
            physics_engine.interactions()

            cam.drawParticles(screen, physics_engine)

            menu.draw()

            taskbar.draw(clock)

            # updates display, sets clock speedteams
            pygame.display.update()
            clock.tick(31)


if __name__ == '__main__':
    # initialises pygame, key repeat, and font, then calls the main class
    pygame.init()
    pygame.key.set_repeat(500, 50)
    pygame.key.start_text_input()
    pygame.font.init()
    main()
