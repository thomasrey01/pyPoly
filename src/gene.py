from __future__ import annotations # allows a class to reference itself
from beamgenome import BeamGenome
import random
from pymunk import Vec2d


class Gene:
    mutateChance = 0.05

    # Endpoints of bridge segments
    endpoints: set

    genomes: [BeamGenome]

    def random_gene(anchors, num_genomes):
        gene = Gene(anchors)

        for i in range(num_genomes):
            gene.add_segment(BeamGenome.randomSegment(gene.endpoints))
        
        return gene


    def from_string(gene_string: str, anchors=None):
        # char length of gene
        gl = 4
        assert len(gene_string) % gl == 0

        gene = Gene(anchors)

        for i in range(0, len(gene_string), gl):
            genotype = gene_string[i : i + gl]
            gene.add_segment(BeamGenome.from_string(genotype))

        return gene

    def __init__(self, anchors=None):
        self.genomes = []
        self.endpoints = set()
        if anchors:
            for anchor in anchors:
                self.endpoints.add(anchor)

    def add_segment(self, segment: BeamGenome):
        self.genomes.append(segment)

        for point in segment.get_endpoints():
            self.endpoints.add(point)

    def _mutationOccurs(self):
        return random.random() < self.mutateChance

    def _rebuild_endpoints(self):
        self.endpoints = set()
        for genome in self.genomes:
            endpoints = genome.get_endpoints()
            self.endpoints.add(endpoints[0])
            self.endpoints.add(endpoints[1])

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
        # shuffle both genes, take first half of both for new gene
        random.shuffle(self.genomes)
        random.shuffle(other.genomes)

        seq1 = random.sample(self.genomes, len(self.genomes) // 2)
        seq2 = random.sample(other.genomes, len(other.genomes) // 2)

        new_sequence = seq1 + seq2

        new_gene = Gene()
        for genome in new_sequence:
            new_gene.add_segment(genome)
        return new_gene

    def to_string(self):
        sequence = "".join([genome.to_string() for genome in self.genomes])
        return sequence
    
    def to_beams(self):
        return [genome.to_beam() for genome in self.genomes]
