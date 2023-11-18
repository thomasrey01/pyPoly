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
from materialproperties import material_list
from fitness import Fitness
from fitnessrenderer import FitnessRenderer


class Simulation:
    w:int
    h = 600
    point_spacing = 40

    fps: float
    sim_dt: float
    end_time: float
    interactive: bool
    gap_length:int
    gap_height:int
    gap_start:int

    running: bool
    drawing: bool
    first_time: bool
    beam_list: [Beam]
    selected_point_body: None
    sim_running: bool
    beam_dict: dict
    pivot_joints: [PivotJoint]
    object_list = []
    fitness: Fitness
    fitnessRenderer: FitnessRenderer

    def __init__(
        self,
        bridge_string="",
        fps=60,
        sim_dt=0.5 / 100,
        interactive=True,
        genetic_callback=None,
        end_time = 0,
        gap_length=8,
        gap_height=5,
        gap_start=3,
        drawing=False
    ):
        self.fps = fps
        self.sim_dt = sim_dt
        self.interactive = interactive
        self.bridge_string = bridge_string
        self.genetic_callback = genetic_callback
        self.end_time = end_time
        self.tick = 0
        self.score = 0
        self.gap_length = gap_length
        self.gap_height = gap_height
        self.gap_start = gap_start
        self.drawing = drawing

        self.w = self.point_spacing * (gap_length + 2 * gap_start)

        self.running = False
        self.first_time = True
        self.selected_point_body = None
        self.sim_running = False
        self.beam_list = []
        self.beam_dict = {}
        self.pivot_joints = []
        self.fitness = Fitness()

        self.make_space()

    def make_space(self):
        self.space = pymunk.Space()
        ### Init pymunk and create space

        self.space.gravity = (0.0, -981.0)

        self.b0 = self.space.static_body

        # Init level
        self.level = Level(self.space, self.w, self.h, self.gap_length, self.gap_height, self.gap_start, self.point_spacing)

        # Build simple bridge for testing 

        builder = Builder(self.bridge_string)
        if self.bridge_string == "":
            builder.simple_bridge(Vec2d(self.gap_start, self.gap_height), self.gap_length + 1)

        builder.build_bridge(self.add_beam)

        # Init fitness
        self.fitness.start_fitness(self.beam_list)

        if self.interactive:
            self.drawing = True

        if self.drawing:
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

    def start(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.loop()

    def add_beam(self, beam: Beam, multiply_spacing=True):
        if multiply_spacing:
            beam.start *= self.level.point_spacing
            beam.end *= self.level.point_spacing

        beam.createBody(self.space, self.object_list)
        self.add_beam_to_dict(beam, beam.start, beam.end)
        self.beam_list.append(beam)

    def add_beam_to_grid(self, material, grid_p1, grid_p2, multiply_spacing=True):
        if grid_p1 != grid_p2:
            if multiply_spacing:
                beam = Beam(
                    material,
                    grid_p1 * self.level.point_spacing,
                    grid_p2 * self.level.point_spacing,
                )
            else:
                beam = Beam(material, grid_p1, grid_p2)

            self.add_beam(beam, False)

    def select_point(self, mouse_pos):
        pos = (mouse_pos[0], self.h - mouse_pos[1])
        spacing = self.point_spacing
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
            self.add_beam_to_grid(
                material_list["wood"], self.selected_point_body, joint_point, False
            )
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
            if point[0] <= self.gap_start * self.level.point_spacing and point[1] <= self.gap_height * self.level.point_spacing:
                for beam in beam_list:
                    self.pivot_joints.append(
                        PivotJoint(
                            self.space,
                            beam.body,
                            self.level.ground_pieces[0].body,
                            point,
                        )
                    )
            if point[0] >= (self.gap_start + self.gap_length) * self.level.point_spacing and point[1] <= self.gap_height * self.level.point_spacing:
                for beam in beam_list:
                    self.pivot_joints.append(
                        PivotJoint(
                            self.space,
                            beam.body,
                            self.level.ground_pieces[1].body,
                            point,
                        )
                    )

            # Then to beams themselves
            for i in range(len(beam_list) - 1):
                for j in range(i + 1, len(beam_list)):
                    beam1, beam2 = beam_list[i], beam_list[j]
                    self.pivot_joints.append(
                        PivotJoint(self.space, beam1.body, beam2.body, point)
                    )

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
                self.reset()

            # Left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Sim has not run yet, allow building
                if self.first_time:
                    self.select_point(pygame.mouse.get_pos())

    # Method for calling from genetic tester

    def loop(self):
        num_broken = self.break_joints()

        if self.interactive:
            self.handle_events()

        if self.sim_running:
            self.space.step(self.sim_dt)

            # Update fitness function
            self.score = self.fitness.dynamic_fitness(
                self.sim_dt, self.level.car, self.level.goal, num_broken
            )
                
        if self.drawing:
            self.draw()
            self.clock.tick(self.fps)
            pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

        done, success = self.level.check_level_complete()
        self.tick += 1

        if self.end_time > 0 and self.tick * self.sim_dt > self.end_time:
            done = True

        if done:
            self.end_run()

    def end_run(self):
        self.running = False
        self.score = self.fitness.totalFitness

    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.Color("white"))

        # Draw space
        self.space.debug_draw(self.draw_options)

        # Draw fitness value
        self.fitnessRenderer.draw(self.screen)

        # All done, lets flip the display
        pygame.display.flip()

    def break_joints(self):
        num_broken = 0
        for joint in self.pivot_joints:
            if joint.should_break(self.sim_dt):
                num_broken += 1
                self.space.remove(joint.joint)
                self.pivot_joints.remove(joint)
        return num_broken
    
    def reset(self):
        for joint in self.pivot_joints:
            self.space.remove(joint.joint)
        self.pivot_joints = []
        for obj in self.object_list:
            self.space.remove(obj)
        self.object_list = []
        self.beam_list = []
        self.beam_dict = {}

        self.sim_running = False
        self.first_time = True

        self.level.reset_level()
