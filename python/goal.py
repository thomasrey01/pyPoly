import pymunk
from pymunk import Vec2d

class Goal:
    #Position of bottom left corner
    position: Vec2d
    width: float = 10
    height: float = 200
    flag_size: float = 10

    shapes: [pymunk.Shape] = []

    def __init__(self, position, space):
        self.position = position

        points = [
            Vec2d(0, 0),
            Vec2d(self.height, 0),
            Vec2d(self.height, self.width - self.flag_size),
            Vec2d(0, self.width - self.flag_size)
        ]

        pole = pymunk.Poly(space.static_body, points)
        pole.color = (0,0,0,255)
        space.add(pole)

        self.shapes.append(pole)



    


