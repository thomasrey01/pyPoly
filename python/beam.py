from material import Material
import pymunk
from pymunk import Vec2d


class Beam:
    material: Material
    start: Vec2d
    end: Vec2d

    body = None

    def __init__(self, material, start, end):
        self.material = material

        self.start = start
        self.end = end
        self.sortPoints()

    def sortPoints(self):
        if self.end.x < self.start.x or (
            self.end.x == self.start.x and self.end.y < self.start.y
        ):
            self.start, self.end = self.end, self.start

    def createBody(self, space):
        length = self.start.get_distance(self.end)

        if not self.material.check_length(length):
            print("Warning: Beam is too long. It will not be added")
            return

        volume = self.material.thickness * length
        mass = self.material.density * volume

        diff = self.end - self.start
        normalized = diff.normalized()
        rotated = normalized.rotated_degrees(90)

        middle = self.start + diff / 2

        points = [
            -diff / 2 + rotated * self.material.thickness / 2,
            diff / 2 + rotated * self.material.thickness / 2,
            diff / 2 - rotated * self.material.thickness / 2,
            -diff / 2 - rotated * self.material.thickness / 2,
        ]

        body = pymunk.Body(mass, pymunk.moment_for_poly(mass, points))
        body.position = middle
        shape = pymunk.Poly(body, points)
        shape.friction = self.material.friction
        shape.color = self.material.color
        space.add(body, shape)
        self.body = body