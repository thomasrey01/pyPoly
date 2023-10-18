import pymunk
from pymunk import Vec2d


class Goal:
    # Position of bottom left corner
    position: Vec2d
    pole_width: float = 5
    height: float = 50
    flag_size: float = 20

    shapes: [pymunk.Shape] = []

    def __init__(self, position, space):
        self.position = position

        points = [
            Vec2d(0, 0),
            Vec2d(0, self.height),
            Vec2d(self.pole_width, self.height),
            Vec2d(self.pole_width, 0),
        ]

        pole = pymunk.Poly(space.static_body, [p + position for p in points])
        pole.color = (0, 0, 0, 255)
        space.add(pole)

        self.shapes.append(pole)

        flag_points = [
            Vec2d(self.pole_width + 1, self.height - self.flag_size),
            Vec2d(self.pole_width + 1, self.height),
            Vec2d(self.pole_width + self.flag_size, self.height - self.flag_size / 2),
        ]

        flag = pymunk.Poly(space.static_body, [p + position for p in flag_points])
        flag.color = (255, 0, 0, 255)
        space.add(flag)
        self.shapes.append(flag)

        for shape in self.shapes:
            shape.sensor = True

    def reached_goal(self, shape: pymunk.Shape):
        for goal_piece in self.shapes:
            if len(goal_piece.shapes_collide(shape).points) > 0:
                print(goal_piece.shapes_collide(shape))
                return True
        return False
