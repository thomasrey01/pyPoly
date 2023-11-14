import pymunk
from pymunk import Vec2d
from material_properties import *

from goal import Goal


class Car:
    mass = 1000
    radius = 10
    position = Vec2d(100 / 2, 200 + radius)
    speed = 10
    friction = 10
    max_force = 1e7

    def __init__(self, space, position=None):
        self.body = pymunk.Body(self.mass, self.radius)

        if position is not None:
            self.position = position
        self.body.position = self.position

        self.shape = pymunk.Circle(self.body, 10, (0, 0))
        self.shape.friction = self.friction
        self.shape.filter = pymunk.ShapeFilter(
            categories=collision_categories["car"], mask=collision_masks["car"]
        )
        space.add(self.body, self.shape)

        self.motor = pymunk.SimpleMotor(self.body, space.static_body, -self.speed)
        self.motor.max_force = self.max_force
        space.add(self.motor)

    def get_pos(self):
        return self.body.position

    def distance_to_goal(self, goal: Goal):
        return self.get_pos().get_distance(goal.position)

    def has_reached_goal(self, goal: Goal):
        for goal_piece in goal.shapes:
            # Collision detected
            if len(goal_piece.shapes_collide(self.shape).points) > 0:
                return True
        return False

    def is_out_of_bounds(self, xMax: float, yMax: float):
        pos = self.get_pos()
        return not (0 <= pos.x <= xMax and 0 <= pos.y <= yMax)
