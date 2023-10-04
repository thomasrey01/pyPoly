import pymunk
from pymunk import Vec2d
from materiallist import material_list


class Builder:
    materials = {"a": material_list["asphalt"], "b": material_list["wood"]}

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

    sequence: str

    def __init__(self, sequence: str = ""):
        self.sequence = sequence

    def get_letter(self, num: int):
        return chr(ord('a') + num)

    def get_number(self, char: str):
        return ord(char) - ord('a')

    def build_bridge(self, build_beam_func):
        self.sequence = self.sequence.lower()

        for i in range(0, len(self.sequence), 4):
            material = self.materials[self.sequence[i + 3]]
            p1 = Vec2d(self.get_number(self.sequence[i]),
                        self.get_number(self.sequence[i + 1]))

            p2 = p1 + self.relative_positions[self.sequence[i + 2]]

            build_beam_func(material, p1, p2)

    def add_segment(self, start_x, start_y, rel_pos_enc, material_enc):
        self.sequence = self.sequence + self.get_letter(start_x) + self.get_letter(start_y) + rel_pos_enc + material_enc

    def simple_bridge(self, start:Vec2d, length:int):

        self.sequence = ""

        # build road
        for i in range(start.x, start.x + length):
            self.add_segment(i, start.y, 'a', 'a')
        
        # build supports
        wood = 'b'

        self.add_segment(start.x, start.y, 'b', wood)

        for i in range(start.x + 1, start.x + length - 1):
            self.add_segment(i, start.y + 1, 'a', wood)
            self.add_segment(i, start.y, 'c', wood)
            self.add_segment(i, start.y, 'b', wood)
            self.add_segment(i, start.y + 1, 'h', wood)

        self.add_segment(start.x + length - 1, start.y, 'c', wood)
        self.add_segment(start.x + length - 1, start.y + 1, 'h', wood)




