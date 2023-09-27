"""
Remake of the pyramid demo from the box2d testbed.
"""

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from level import Level


class Simulation:
    w = 600
    h = 600

    def __init__(self):
        self.running = True
        self.drawing = True
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -981.0)

        # Init level
        self.level = Level(self.space, self.w, self.h)

        # temporary bridge
        bridge_points = [(-210, 0), (-210, 5), (210, 5), (210, 0)]

        bridge_b = pymunk.Body(100, pymunk.moment_for_poly(100, bridge_points))
        bridge_b.position = Vec2d(self.w / 2, 200)
        bridge_s = pymunk.Poly(bridge_b, bridge_points)

        bridge_s.friction = 1
        self.space.add(bridge_b, bridge_s)

        """
        ### pyramid
        x = Vec2d(-270, 7.5) + (300, 250)
        y = Vec2d(0, 0)
        deltaX = Vec2d(0.5625, 1.1) * 20
        deltaY = Vec2d(1.125, 0.0) * 20

        for i in range(25):
            y = Vec2d(*x)
            for j in range(i, 25):
                size = 10
                points = [(-size, -size), (-size, size), (size, size), (size, -size)]
                mass = 1.0
                moment = pymunk.moment_for_poly(mass, points, (0, 0))
                body = pymunk.Body(mass, moment)
                body.position = y
                shape = pymunk.Poly(body, points)
                shape.friction = 1
                self.space.add(body, shape)

                y += deltaY

            x += deltaX
        """

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

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.drawing = not self.drawing
            # Left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.add_body(pygame.mouse.get_pos())

        fps = 30.0
        dt = 1.0 / 100
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
