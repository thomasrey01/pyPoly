from beamgenome import BeamGenome
import random
from pymunk import Vec2d


class Gene:
    mutateChance = 0.1

    # Endpoints of bridge segments
    endpoints: set

    genomes: [BeamGenome]

    def from_string(gene_string: str):
        # char length of gene
        gl = 4
        assert len(gene_string) % gl == 0

        gene = Gene()

        for i in range(0, len(gene_string), gl):
            genotype = gene_string[i : i + gl]
            gene.add_segment(BeamGenome.from_string(genotype))

        return gene

    def __init__(self):
        self.genomes = []
        self.endpoints = set()

    def add_segment(self, segment: BeamGenome):
        self.genomes.append(segment)

        for point in segment.get_endpoints():
            self.endpoints.add(point)

    def _mutationOccurs(self):
        return random.random() < self.mutateChance

    def _rebuild_endpoints(self):
        self.endpoints = set()
        for genome in self.genomes:
            self.endpoints.add(genome.endpoints)

    def mutate(self):
        # Remove bridge segment
        if self._mutationOccurs():
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

        if self._mutationOccurs():
            segment = random.choice(self.genomes)
            segment.change_start(self.endpoints)
            self._rebuild_endpoints()

        if self._mutationOccurs():
            segment = random.choice(self.genomes)
            segment.change_end()

    def cross(self, other: Gene):
        pass

    def to_string(self):
        return "".join([genome.to_string() for genome in self.genomes])
