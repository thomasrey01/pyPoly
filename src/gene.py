from __future__ import annotations  # allows a class to reference itself
from beamgenome import BeamGenome
import random
from pymunk import Vec2d


class Gene:
    anchors = None

    mutateChance = 0.01

    # Endpoints of bridge segments
    endpoints: set

    genomes: [BeamGenome]

    def set_anchors(anchors):
        Gene.anchors = anchors

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

    def __init__(self):
        self.genomes = []
        self.endpoints = set()
        for anchor in Gene.anchors:
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
        idx = 0
        while idx < len(self.genomes):
            if self._mutationOccurs():
                mutationType = random.choice(
                    ["remove", "add", "material", "start", "end"]
                )

                if mutationType == "remove" and len(self.genomes) > 1:
                    del self.genomes[idx]
                    self._rebuild_endpoints()
                    idx -= 1

                elif mutationType == "add":
                    self.add_segment(BeamGenome.randomSegment(self.endpoints))

                elif mutationType == "material":
                    self.genomes[idx].change_material()

                elif mutationType == "start":
                    self.genomes[idx].change_start(self.endpoints)
                    self._rebuild_endpoints()

                elif mutationType == "end":
                    self.genomes[idx].change_end()

                else:
                    raise KeyError("Unknown mutation type")

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

    def to_string(self):
        sequence = "".join([genome.to_string() for genome in self.genomes])
        return sequence

    def to_beams(self):
        return [genome.to_beam() for genome in self.genomes]
