from beam import Beam
import utils
from pymunk import Vec2d
from material_properties import material_list
import random


class BeamGenome:
    material_dict = {"a": material_list["asphalt"], "b": material_list["wood"]}

    """
    d   c   b
    e   .   a
    f   g   h
    """
    relative_positions = {
        "a": Vec2d(1, 0),
        "b": Vec2d(1, 1),
        "c": Vec2d(0, 1),
        "d": Vec2d(-1, 1),
        "e": Vec2d(-1, 0),
        "f": Vec2d(-1, -1),
        "g": Vec2d(0, -1),
        "h": Vec2d(1, -1),
    }

    x_start: int
    y_start: int
    end_pos: str
    material: str  # "a" or "b"

    # init from string (genotype)
    def from_string(genotype: str):
        x_start = utils.get_number(genotype[0])
        y_start = utils.get_number(genotype[1])
        end_pos = genotype[2]
        material = genotype[3]

        return BeamGenome(x_start, y_start, end_pos, material)

    # Create random segment that is connected to the bridge
    def randomSegment(points: set):
        p_start = random.choice(points)
        p_end = random.choice(BeamGenome.relative_positions)
        material = random.choice(BeamGenome.material_dict)
        return BeamGenome(p_start.x, p_start.y, p_end, material)

    # init from properties
    def __init__(self, x_start: int, y_start: int, end_pos: str, material: str):
        self.x_start = x_start
        self.y_start = y_start
        self.end_pos = end_pos
        self.material = material

    # Change the beam material. Because we have only 2 materials, they are simply swapped
    def change_material(self):
        if self.material == "a":
            self.material = "b"
        else:
            self.material = "a"

    # Change the starting x and y to random position
    def change_start(self, points: set):
        p_start = random.choice(points)
        self.x_start = p_start.x
        self.y_start = p_start.y

    # Change the end position randomly
    def change_end(self):
        self.end_pos = random.choice(self.relative_positions)

    # Get the endpoints as a Vec2d
    def get_endpoints(self):
        p1 = Vec2d(self.x_start, self.y_start)
        p2 = p1 + self.relative_positions[self.end_pos]
        return p1, p2

    # Return string
    def to_string(self):
        genotype = (
            utils.get_letter(self.x_start)
            + utils.get_letter(self.y_start)
            + self.end_pos
            + self.material
        )
        return genotype

    # Return Beam
    # NOTE: Returns beam with grid coordinates, it needs to be converted to pixel coordinates
    def to_beam(self):
        p1, p2 = self.get_endpoints()

        beam = Beam(self.material_dict[self.material], p1, p2)
        return beam
