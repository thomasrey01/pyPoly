import pymunk
from pymunk import Vec2d
from beam import Beam

class PivotJoint:
    def __init__(self, space, body1: pymunk.Body, body2: pymunk.Body, point):

        beam1_point = point - body1.position
        beam2_point = point - body2.position

        joint1 = pymunk.constraints.PinJoint(body1, body2, beam1_point, beam2_point)
        space.add(joint1)