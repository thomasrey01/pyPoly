"""
Remake of the pyramid demo from the box2d testbed.
"""

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from level import Level
from material import Material
from beam import Beam

wood = Material(100, 999, None, 5, 1, 1, (164,116,73, 255))

class Simulation:
    w = 600
    h = 600

    def __init__(self):
        self.running = True
        self.drawing = True

        self.selected_point_body = None

        self.sim_running = False

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -981.0)

        # Init level
        self.level = Level(self.space, self.w, self.h)

        # Add temporary bridge for testing
        
        beam = Beam(wood, Vec2d(90, 210), Vec2d(self.w - 90, 210))
        beam.createBody(self.space)

        ### draw options for drawing
        pymunk.pygame_util.positive_y_is_up = True
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    def add_body(self, pos):
        size = 10
        points = [(-size, -size), (-size, size), (size, size), (size, -size)]
        mass = 1.0
        moment = pymunk.moment_for_poly(mass, points, (0, 0))
        body = pymunk.Body(mass, moment)

        pos = (pos[0], self.h - pos[1])

        body.position = pos
        shape = pymunk.Poly(body, points)
        shape.friction = 1
        self.space.add(body, shape)

    def run(self):
        while self.running:
            self.loop()
    
    def select_point(self, mouse_pos):
        pos = (mouse_pos[0], self.h - mouse_pos[1])
        spacing = self.level.point_spacing
        x, y = 0, 0
        if pos[0] % spacing > spacing // 2:
            x = pos[0] + (spacing - pos[0] % spacing)
        else:
            x = pos[0] - pos[0] % spacing

        if pos[1] % spacing > spacing // 2:
            y = pos[1] + (spacing - pos[1] % spacing)
        else:
            y = pos[1] - pos[1] % spacing
        
        joint_point = Vec2d(x, y)

        if self.selected_point_body == None:
            self.selected_point_body = joint_point
        else:
            beam = Beam(wood, self.selected_point_body, joint_point)
            beam.createBody(self.space)
            self.selected_point_body = None

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.sim_running = not self.sim_running
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.drawing = not self.drawing
            # Left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # self.add_body(pygame.mouse.get_pos())
                self.select_point(pygame.mouse.get_pos())

        fps = 30.0
        dt = 1.0 / 100
        if self.sim_running:
            self.space.step(dt)
        if self.drawing:
            self.draw()

        ### Tick clock and update fps in title
        self.clock.tick(fps)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

    def draw(self):
        ### Clear the screen
        self.screen.fill(pygame.Color("white"))

        ### Draw space
        self.space.debug_draw(self.draw_options)

        ### All done, lets flip the display
        pygame.display.flip()


def main():
    demo = Simulation()
    demo.run()


if __name__ == "__main__":
    main()
