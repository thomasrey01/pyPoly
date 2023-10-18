"""
Remake of the pyramid demo from the box2d testbed.
"""

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from joints import PivotJoint

from level import Level
from beam import Beam
from builder import Builder
from material_properties import material_list
from fitness import Fitness
from fitnessrenderer import FitnessRenderer


class Simulation:
    w = 600
    h = 600

    running = True
    drawing = True
    first_time = True
    beam_list = []
    selected_point_body = None
    sim_running = False
    beam_dict = {}
    pivots = []
    fitness = Fitness()
    fitnessRenderer: FitnessRenderer

    def __init__(self, bridge_string=None, speed=None):
        pygame.init()

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -981.0)

        self.b0 = self.space.static_body

        # Init level
        self.level = Level(self.space, self.w, self.h)

        ### draw options for drawing
        pymunk.pygame_util.positive_y_is_up = True
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        builder = Builder()
        builder.simple_bridge(Vec2d(2, 5), 11)
        builder.build_bridge(self.add_beam_to_grid)

        # Init fitness and fitness renderer
        self.fitnessRenderer = FitnessRenderer(self.fitness)
        self.fitness.static_fitness(self.beam_list)

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

    def add_beam_to_grid(self, material, grid_p1, grid_p2):
        beam = Beam(
            material,
            grid_p1 * self.level.point_spacing,
            grid_p2 * self.level.point_spacing,
        )
        beam.createBody(self.space)
        self.add_beam_to_dict(beam, beam.start, beam.end)
        self.beam_list.append(beam)

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
            beam = Beam(material_list["wood"], self.selected_point_body, joint_point)
            beam.createBody(self.space)

            self.add_beam_to_dict(beam, joint_point, self.selected_point_body)
            self.beam_list.append(beam)

            self.selected_point_body = None

    def add_beam_to_dict(self, beam, point1, point2):
        if point1 in self.beam_dict:
            self.beam_dict[point1].append(beam)
        else:
            self.beam_dict[point1] = [beam]

        if point2 in self.beam_dict:
            self.beam_dict[point2].append(beam)
        else:
            self.beam_dict[point2] = [beam]

    def add_anchors(self):
        for point in self.beam_dict:
            # Adding anchors to ground first

            beam_list = self.beam_dict[point]
            if point[0] <= 120 and point[1] <= 200:
                for beam in beam_list:
                    PivotJoint(
                        self.space, beam.body, self.level.ground_pieces[0].body, point
                    )
            if point[0] >= self.w - 120 and point[1] <= 200:
                for beam in beam_list:
                    PivotJoint(
                        self.space, beam.body, self.level.ground_pieces[1].body, point
                    )

            # Then to beams themselves
            for i in range(len(beam_list) - 1):
                for j in range(i + 1, len(beam_list)):
                    beam1, beam2 = beam_list[i], beam_list[j]
                    PivotJoint(self.space, beam1.body, beam2.body, point)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.first_time:
                    self.add_anchors()
                    self.first_time = not self.first_time
                self.sim_running = not self.sim_running
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.drawing = not self.drawing
            # Left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # self.add_body(pygame.mouse.get_pos())
                self.select_point(pygame.mouse.get_pos())

        fps = 60.0
        dt = 0.5 / 100
        if self.sim_running:
            self.space.step(dt)

            # Update fitness function
            self.fitness.dynamic_fitness(dt, self.level.car, self.level.goal)
        if self.drawing:
            self.draw()

        # Tick clock and update fps in title
        self.clock.tick(fps)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

        if self.level.check_level_complete():
            self.running = False
            print("SUCCES")  # TODO: handle level complete
            print(f"Fitness: {self.fitness.totalFitness:.2f}")

    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.Color("white"))

        # Draw space
        self.space.debug_draw(self.draw_options)

        # Draw fitness value
        self.fitnessRenderer.draw(self.screen)

        # All done, lets flip the display
        pygame.display.flip()


def main():
    demo = Simulation()
    demo.run()


if __name__ == "__main__":
    main()
