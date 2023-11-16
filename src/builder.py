from pymunk import Vec2d
from material_properties import *
from gene import Gene
from beamgenome import BeamGenome


class Builder:
    gene: Gene

    def __init__(self, sequence: str = ""):
        sequence = sequence.lower()
        self.gene = Gene.from_string(sequence)

    def build_bridge(self, build_beam_func):
        beams = self.gene.to_beams()

        for beam in beams:
            build_beam_func(beam)

    def add_segment(self, start_x, start_y, rel_pos_enc, material_enc):
        beamGenome = BeamGenome(start_x, start_y, rel_pos_enc, material_enc)
        self.gene.add_segment(beamGenome)

    def simple_bridge(self, start: Vec2d, length: int):
        self.gene = Gene()

        asphalt = "a"

        # build road
        for i in range(start.x, start.x + length - 1):
            self.add_segment(i, start.y, "a", asphalt)

        # build supports
        wood = "b"

        for i in range(start.x, start.x + length - 1):
            # horizontal
            self.add_segment(i, start.y - 1, "a", wood)

            # cross beams
            self.add_segment(i, start.y - 1, "b", wood)
            self.add_segment(i, start.y, "h", wood)

            # vertical
            self.add_segment(i, start.y, "g", wood)
