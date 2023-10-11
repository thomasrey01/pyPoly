import pymunk
from pymunk import Vec2d
from beam import Beam

class PivotJoint:
    def __init__(self, space, body1: Beam, body2: Beam, point):

        beam1_point = point - body1.body.position
        beam2_point = point - body2.body.position

        joint1 = pymunk.constraints.PinJoint(body1.body, body2.body, beam1_point, beam2_point)
        space.add(joint1)