from gene import Gene
from simulation import Simulation

from pymunk import Vec2d
import random


# Genetic algorithm using tournament selection
class GeneticAlgorithm:
    num_per_generation: int  # Should be even
    num_generations: int
    num_start_segments: int
    gap_size: int  # Gap size in terms of grid units #TODO: refactor simulation to support this
    gap_height: int
    gap_start: int
    multithreading: bool

    anchors: [Vec2d] = []
    genes: [Gene] = []
    results = {}

    def __init__(
        self,
        num_per_generation=100,
        num_generations=100,
        num_start_segments=20,
        gap_length=9,
        gap_height=5,
        gap_start=3,
        multithreading=False,
    ):
        self.num_per_generation = num_per_generation
        self.num_generations = num_generations
        self.num_start_segments = num_start_segments
        self.gap_size = gap_length
        self.gap_height = gap_height
        self.gap_start = gap_start
        self.multithreading = multithreading

        if multithreading:
            import joblib  # TODO multithreading

        # Add left and right anchors
        for i in range(gap_height):
            self.anchors.append(Vec2d(gap_start, i))
            self.anchors.append(Vec2d(gap_start + gap_length, i))

        for i in range(self.num_per_generation):
            self.genes.append(Gene.random_gene(self.anchors, num_start_segments))

    def start(self):
        for generation in range(self.num_generations):
            self.run_generation(generation)

    def run_generation(self, generation: int):
        gen_results = {}

        # Run the simulations
        for gene in self.genes:
            bridge_string = gene.to_string()
            print(f"Bridge_string: {bridge_string}")

            simulation = Simulation(bridge_string= gene.to_string(), interactive=False)
            simulation.start()

            gen_results[gene] = simulation.score

        self.results[generation] = gen_results

        self.tournament_selection(gen_results)

    def tournament_selection(self, gen_results: dict):
        new_genes = []

        children_per_parent = 2

        for i in range(self.num_per_generation // children_per_parent):
            parent1 = self.tournament(gen_results)
            parent2 = self.tournament(gen_results)

            for c in range(children_per_parent):
                child = parent1.cross(parent2)
                child.mutate()
                new_genes.append(child)

        self.genes = new_genes

    def tournament(self, gen_results) -> Gene:
        candidate1, candidate2 = random.sample(list(gen_results.keys()), 2)
        if gen_results[candidate1] > gen_results[candidate2]:
            return candidate1
        return candidate2
