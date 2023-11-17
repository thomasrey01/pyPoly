import pymunk
from pymunk import Vec2d

from car import Car
from goal import Goal
from collisions import *


class Level:
    ground_friction = 1

    # Static ground shapes
    ground_pieces: [pymunk.Poly]

    # Immovable joints to connect the bridge to
    static_joints: dict

    bridge_joints = [(90, 200), (210, 0)]

    point_spacing: int
    width: float
    height: float
    car: Car
    goal: Goal

    def __init__(self, space: pymunk.Space, width, height, gap_length, gap_height, gap_start, point_spacing):
        self.width = width
        self.height = height
        self.space = space
        self.point_spacing = point_spacing

        self.ground_pieces = []
        self.static_joints = {}

        # Calculate gap sizes in pixels
        gl_px = gap_length * self.point_spacing
        gh_px = gap_height * self.point_spacing
        gs_px = gap_start * self.point_spacing



        ground_points = [
            [(0, 0), (0, gh_px), (gs_px, gh_px), (gs_px, 0)],
            [
                (width, 0),
                (width, gh_px),
                (gs_px + gl_px, gh_px),
                (gs_px + gl_px, 0),
            ], 
        ]

        for ground in ground_points:
            ground_piece = pymunk.Poly(space.static_body, ground)
            ground_piece.friction = self.ground_friction
            ground_piece.filter = pymunk.ShapeFilter(
                categories=collision_categories["ground"],
                mask=collision_masks["ground"],
            )

            space.add(ground_piece)
            self.ground_pieces.append(ground_piece)

        # Ball / car
        self.car = Car(space, position=Vec2d(gs_px / 2, gh_px))

        # Goal
        goal_position = Vec2d(gs_px + gl_px + gs_px / 2, gh_px)
        self.goal = Goal(goal_position, space)

        return

        # joint points
        for i in range(0, width, self.point_spacing):
            for j in range(0, height, self.point_spacing):
                point_b = pymunk.Body(body_type=pymunk.Body.STATIC)
                point_b.position = (i, j)
                point_s = pymunk.Circle(point_b, 2)
                point_s.color = (255, 0, 0, 100)
                point_s.sensor = True

                space.add(point_b, point_s)
                self.static_joints[(i, j)] = (point_b, point_s)

    def get_static_joint(self, pos):
        return self.static_joints[pos]

    # Returns a bool tuple: if level has ended and if it ended successfully
    def check_level_complete(self) -> (bool, bool):
        if self.car.has_reached_goal(self.goal):
            return True, True
        elif self.car.is_out_of_bounds(self.width, self.height):
            return True, False
        return False, False

    def reset_level(self):
        self.car.reset_car()
