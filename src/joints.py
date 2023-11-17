import pymunk
from pymunk import Vec2d
from beam import Beam


class PivotJoint:
    joint: pymunk.PinJoint
    max_force: float

    def __init__(
        self, space, body1: pymunk.Body, body2: pymunk.Body, point, max_force=3e6
    ):
        self.max_force = max_force
        beam1_point = point - body1.position
        beam2_point = point - body2.position

        self.joint = pymunk.constraints.PinJoint(body1, body2, beam1_point, beam2_point)
        space.add(self.joint)

    def get_force(self, dt):
        return self.joint.impulse / dt

    def should_break(self, dt):
        return self.get_force(dt) > self.max_force
