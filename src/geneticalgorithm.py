from gene import Gene
from simulation import Simulation

from pymunk import Vec2d
import settings
import random
import joblib


# Genetic algorithm using tournament selection
class GeneticAlgorithm:
    num_per_generation: int  # Should be even
    num_generations: int
    num_start_segments: int
    gap_length: int  # Gap size in terms of grid units 
    gap_height: int
    gap_start: int
    multithreading: bool
    end_time: float
    display_best: bool
    filename: str

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
        display_best=True,
        filename = None
    ):
        self.num_per_generation = num_per_generation
        self.num_generations = num_generations
        self.num_start_segments = num_start_segments
        self.gap_length = gap_length
        self.gap_height = gap_height
        self.gap_start = gap_start
        self.multithreading = multithreading
        self.end_time = end_time
        self.display_best = display_best
        self.filename = filename

        self.genes = []
        self.best_gene = None
        self.results = {}

        self.anchors = []
        # Add left and right anchors
        for i in range(gap_height - 2, gap_height):
            self.anchors.append(Vec2d(gap_start, i))
            self.anchors.append(Vec2d(gap_start + gap_length, i))

        start_point = Vec2d(self.gap_start, self.gap_height)
        end_point = start_point + Vec2d(self.gap_length, 0)
        Gene.set_anchors(self.anchors)
        Gene.generate_fixed(start_point, end_point)

        for i in range(self.num_per_generation):
            self.genes.append(Gene.random_gene(num_start_segments))      

    def start(self):
        with open("genes_results.txt", 'a') as file:
            file.write(f"mutate chance: {settings.mutate_chance}\n")
            file.write(f"build cost: {settings.build_cost}\n")
            file.write(f"structural integrity: {settings.structural_integrity}\n")
            file.write(f"car distance: {settings.car_distance}\n")
            file.write(f"max force: {settings.max_force}\n")
            file.write('--------------------------------\n')
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

        start_point = Vec2d(self.gap_start, self.gap_height)
        end_point = start_point + Vec2d(self.gap_length, 0)

        def run_simulation(
            gene,
            end_time,
            gap_start=self.gap_start,
            gap_length=self.gap_length,
            gap_height=self.gap_height,
        ):
            Gene.set_anchors(self.anchors)
            Gene.generate_fixed(start_point, end_point)

            simulation = Simulation(
                bridge_string=gene.to_string(),
                interactive=False,
                drawing=False,
                end_time=end_time,
                gap_start=gap_start,
                gap_length=gap_length,
                gap_height=gap_height,
            )
            simulation.start()
            return simulation.score

        # Run the simulations
        if self.multithreading:
            scores = joblib.Parallel(n_jobs=1)(
                joblib.delayed(run_simulation)(
                    gene, self.end_time
                )
                for gene in self.genes
            )
            for gene, score in zip(self.genes, scores):
                gen_results[gene] = score

        else:
            for gene in self.genes:
                gen_results[gene] = self.run_simulation(gene)

        sorted_gen = sorted(gen_results.items(), key=lambda x: x[1])

        print(
            f"Generation {generation} max: {max(gen_results.values())} with gene: {sorted_gen[-1][0].to_string()}"
        )

        with open("genes_results.txt", 'a') as file:
            file.write(f"Generation {generation} max: {max(gen_results.values())} with gene: {sorted_gen[-1][0].to_string()}\n")


        if self.display_best:
            best_sim = Simulation(sorted_gen[-1][0].to_string(True), fps=0, interactive=False, drawing=True)
            best_sim.start()
                
        if self.filename is not None:
            self.save_genes(self.filename)

        self.tournament_selection(sorted_gen)

    def tournament_selection(self, sorted_gen: tuple):
        new_genes = []
        new_genes.append(sorted_gen[-1][0])
        children_per_parent = 2

        for i in range(self.num_per_generation // children_per_parent):
            parent1 = sorted_gen[-1]
            parent2 = sorted_gen[-2]

            for c in range(children_per_parent):
                child = parent1[0].cross(parent2[0])
                child.mutate()
                new_genes.append(child)

        self.genes = new_genes

    def load_genes(self, filename):
        with open(filename, 'rb') as file:
            self.genes = joblib.load(file)

    def save_genes(self, filename):
        with open(filename, 'wb') as file:
            joblib.dump(self.genes, file)