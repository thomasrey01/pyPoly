from gene import Gene
from simulation import Simulation

from pymunk import Vec2d
import random
import joblib


# Genetic algorithm using tournament selection
class GeneticAlgorithm:
    num_per_generation: int  # Should be even
    num_generations: int
    num_start_segments: int
    gap_size: int  # Gap size in terms of grid units #TODO: refactor simulation to support this
    gap_height: int
    gap_start: int
    multithreading: bool
    end_time: float

    anchors: [Vec2d]
    genes: [Gene]
    results: dict

    def __init__(
        self,
        num_per_generation=100,
        num_generations=1000,
        num_start_segments=20,
        gap_length=9,
        gap_height=5,
        gap_start=3,
        multithreading=False,
        end_time=20,
    ):
        self.num_per_generation = num_per_generation
        self.num_generations = num_generations
        self.num_start_segments = num_start_segments
        self.gap_size = gap_length
        self.gap_height = gap_height
        self.gap_start = gap_start
        self.multithreading = multithreading
        self.end_time = end_time

        self.genes = []
        self.results = {}

        self.anchors = []
        # Add left and right anchors
        for i in range(gap_height):
            self.anchors.append(Vec2d(gap_start, i))
            self.anchors.append(Vec2d(gap_start + gap_length, i))

        Gene.set_anchors(self.anchors)

        for i in range(self.num_per_generation):
            self.genes.append(Gene.random_gene(num_start_segments))

    def start(self):
        for generation in range(self.num_generations):
            self.run_generation(generation)

    def run_simulation(self, gene):
        simulation = Simulation(
            bridge_string=gene.to_string(), interactive=False, end_time=self.end_time
        )
        simulation.start()
        return simulation.score

    def run_generation(self, generation: int):
        gen_results = {}

        def run_simulation(gene, end_time):
            Gene.set_anchors(self.anchors)

            simulation = Simulation(
                bridge_string=gene.to_string(),
                interactive=False,
                end_time=end_time,
            )
            simulation.start()
            return simulation.score

        # Run the simulations
        if self.multithreading:
            scores = joblib.Parallel(n_jobs=-1)(
                joblib.delayed(run_simulation)(gene, self.end_time)
                for gene in self.genes
            )
            for gene, score in zip(self.genes, scores):
                gen_results[gene] = score

        else:
            for gene in self.genes:
                gen_results[gene] = self.run_simulation(gene)

        print(f"Generation {generation} max: {max(gen_results.values())}")

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
