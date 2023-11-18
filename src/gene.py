from __future__ import annotations  # allows a class to reference itself
from beamgenome import BeamGenome
import random
from pymunk import Vec2d


class Gene:
    fixed_segments = []

    anchors = []

    # Endpoints of bridge segments
    endpoints: set

    genomes: [BeamGenome]

    def set_anchors(anchors):
        Gene.anchors = anchors

    # Generate fixed asphalt segments
    def generate_fixed(start_point, end_point):
        Gene.fixed_segments = []
        for i in range(start_point.x, end_point.x):
            Gene.fixed_segments.append(BeamGenome(i, start_point.y, 'a', 'a'))

    def random_gene(num_genomes):
        gene = Gene()

        for i in range(num_genomes):
            gene.add_segment(BeamGenome.randomSegment(gene.endpoints))

        return gene

    def from_string(gene_string: str):
        # char length of gene
        gl = 4
        assert len(gene_string) % gl == 0

        gene = Gene()

        for i in range(0, len(gene_string), gl):
            genotype = gene_string[i : i + gl]
            gene.add_segment(BeamGenome.from_string(genotype))

        return gene

    def __init__(self, mutate_chance=0.05):
        self.genomes = []
        self.endpoints = set()
        self.mutate_chance = mutate_chance
        for anchor in Gene.anchors:
            self.endpoints.add(anchor)

    def add_segment(self, segment: BeamGenome):
        self.genomes.append(segment)

        for point in segment.get_endpoints():
            self.endpoints.add(point)

    def _mutationOccurs(self):
        return random.random() < self.mutate_chance

    def _rebuild_endpoints(self):
        self.endpoints = set()
        for genome in self.genomes:
            endpoints = genome.get_endpoints()
            self.endpoints.add(endpoints[0])
            self.endpoints.add(endpoints[1])

    def mutate(self):
        idx = 0
        while idx < len(self.genomes):
            if self._mutationOccurs():
                val = random.randint(0, 10)
                

                if val < 1 and len(self.genomes) > 1:
                    del self.genomes[idx]
                    self._rebuild_endpoints()
                    idx -= 1

                else:
                    self.add_segment(BeamGenome.randomSegment(self.endpoints))

        
            idx += 1
            """


            # Remove bridge segment
            if self._mutationOccurs() and len(self.genomes) > 1:
                idxRemoved = random.randint(0, len(self.genomes) - 1)
                del self.genomes[idxRemoved]
                self._rebuild_endpoints()

            # Add bridge segment
            if self._mutationOccurs():
                self.add_segment(BeamGenome.randomSegment(self.endpoints))

            # Change a segment's material
            if self._mutationOccurs():
                segment = random.choice(self.genomes)
                segment.change_material()

            # Change start point
            if self._mutationOccurs():
                segment = random.choice(self.genomes)
                segment.change_start(self.endpoints)
                self._rebuild_endpoints()

            # Change end point
            if self._mutationOccurs():
                segment = random.choice(self.genomes)
                segment.change_end()
            """

    def cross(self, other: Gene):
        # shuffle both genes, take first half of both for new gene
        random.shuffle(self.genomes)
        random.shuffle(other.genomes)

        seq1 = random.sample(self.genomes, max(len(self.genomes) // 2, 1))
        seq2 = random.sample(other.genomes, max(len(other.genomes) // 2, 1))

        new_sequence = seq1 + seq2
        assert len(new_sequence) > 1

        new_gene = Gene()
        for genome in new_sequence:
            new_gene.add_segment(genome)
        return new_gene

    def to_string(self, include_fixed=False):
        if(include_fixed):
            fixed_sequence = "".join([fixed_segment.to_string() for fixed_segment in Gene.fixed_segments])
        else:
            fixed_sequence = ""

        sequence = "".join([genome.to_string() for genome in self.genomes])
        return fixed_sequence + sequence

    def to_beams(self):
        fixed = [fixed.to_beam() for fixed in Gene.fixed_segments]

        variable = [genome.to_beam() for genome in self.genomes]

        return fixed + variable
