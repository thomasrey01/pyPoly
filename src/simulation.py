"""
Remake of the pyramid demo from the box2d testbed.
"""
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

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

    fps: float
    sim_dt: float

    running = False
    drawing: bool
    interactive: bool
    first_time = True
    beam_list = []
    selected_point_body = None
    sim_running = False
    beam_dict = {}
    pivots = []
    fitness = Fitness()
    fitnessRenderer: FitnessRenderer
    


    def __init__(self, bridge_string="", fps=60, sim_dt=0.5 / 100, interactive=True, genetic_callback=None):
        self.fps = fps
        self.sim_dt = sim_dt
        self.interactive = interactive
        self.bridge_string = bridge_string
        self.genetic_callback = genetic_callback
        self.tick = 0
        self.score = 0
        
        self.make_space()

    def make_space(self):

        self.space = pymunk.Space()
        ### Init pymunk and create space
        
        self.space.gravity = (0.0, -981.0)

        self.b0 = self.space.static_body

        # Init level
        self.level = Level(self.space, self.w, self.h)

        # Build simple bridge for testing

        builder = Builder()
        if self.bridge_string == "":
            builder.simple_bridge(Vec2d(2, 5), 11)
        else:
            builder.sequence = self.bridge_string
        builder.build_bridge(self.add_beam_to_grid, self.bridge_string)

        # Init fitness
        self.fitness.static_fitness(self.beam_list)

        if self.interactive:
            self.drawing = True
            pygame.init()

            self.screen = pygame.display.set_mode((self.w, self.h))
            self.clock = pygame.time.Clock()

            # draw options for drawing
            pymunk.pygame_util.positive_y_is_up = True
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

            # init fitness renderer
            self.fitnessRenderer = FitnessRenderer(self.fitness)

        if not self.interactive:
            self.add_anchors()
            self.first_time = False
            self.sim_running = True
            self.drawing = False

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

    def start(self):
        self.running = True
        self.run()

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                print(self.tick)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.first_time:
                    self.add_anchors()
                    self.first_time = not self.first_time
                self.sim_running = not self.sim_running
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.drawing = not self.drawing
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                continue
            # Left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.select_point(pygame.mouse.get_pos())

    # Method for calling from genetic tester

    def loop(self):
        if self.interactive:
            self.handle_events()

        if self.sim_running:
            self.space.step(self.sim_dt)

            # Update fitness function
            self.score = self.fitness.dynamic_fitness(self.sim_dt, self.level.car, self.level.goal)
        if self.drawing:
            self.draw()

        if self.interactive:
            # Tick clock and update fps in title
            self.clock.tick(self.fps)
            pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

        done, success = self.level.check_level_complete()
        self.tick += 1
        if self.tick > 100000:
            if self.genetic_callback:
                self.score = self.fitness.dynamic_fitness(self.sim_dt, self.level.car, self.level.goal)
                self.genetic_callback()
            

        if done:
            if self.genetic_callback:
                self.genetic_callback()
            self.running = False


    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.Color("white"))

        # Draw space
        self.space.debug_draw(self.draw_options)

        # Draw fitness value
        self.fitnessRenderer.draw(self.screen)

        # All done, lets flip the display
        pygame.display.flip()