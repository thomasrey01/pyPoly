import pymunk
from collisions import *

class Car:
    mass = 10
    radius = 10
    position = (100 / 2, 200 + radius)
    speed = 10
    friction = 1
    max_force = 100000

    def __init__(self, space, position=None):
        self.body = pymunk.Body(self.mass, self.radius)

        if position is not None:
            self.position = position
        self.body.position = self.position

        self.shape = pymunk.Circle(self.body, 10, (0, 0))
        self.shape.friction = self.friction
        self.shape.filter = pymunk.ShapeFilter(categories=collision_categories["car"], mask=collision_masks["car"])
        space.add(self.body, self.shape)

        self.motor = pymunk.SimpleMotor(self.body, space.static_body, -self.speed)
        self.motor.max_force = self.max_force
        space.add(self.motor)

    def get_pos(self):
        return self.body.position
