from simulation import Simulation
import random


class BridgeGenetic:
    
    gene_scores = {}

    def __init__(self, search_length=25, seed=None):
        self.search_length = search_length

        self.seed = seed

        random.seed(self.seed)
        
        self.start()

    def start(self):

        num_iterations = random.randint(5, 10)
        simulation = Simulation(bridge_string=self.new_gene(), interactive=False)
        simulation.genetic_callback = self.sim_done
        other_simulation = Simulation(bridge_string=self.new_gene(), interactive=False)
        simulation.start()
        other_simulation.start()
        num_genes = 2

        # for _ in range(num_iterations):
        # for _ in range(num_genes):
            
        #     simulation.start()
        #     simulation.reset()

    def random_bridge(self):
        gene = self.new_gene()

        for _ in range(self.search_length):
            pass


        return gene

    def cross(self, gene1, gene2):
        pass

    

    def new_gene(self=None): # This method has to create a gene that starts at df and somehow ends at mg.

        # This method will get deleted after
        def create_road(): # Creating road gene
            gene = ""
            connected_points = []
            for i in range(11):
                gene += chr(ord('c') + i) + "faa"
                connected_points.append((chr(ord('c') + i), 'f'))
            return gene, connected_points

        gene, connected_points = create_road()
        print(f"Gene is: {gene}")
        print(f"Connected points are: {connected_points}")

        return gene
    
    def sim_done(self, score, gene):
        print(f"Final score is: {score}")
        self.gene_scores[gene] = score

