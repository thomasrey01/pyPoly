from simulation import Simulation

class BridgeGenetic:
    
    gene_scores = {}

    def __init__(self, search_length=12):
        self.search_length = search_length
        self.simulation = Simulation(bridge_string=self.new_gene(), interactive=False)
        self.simulation.genetic_callback = self.sim_done
        self.simulation.start()
        # self.simulation.auto_start()

    def start(self):
        pass

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
    
    def sim_done(self):
        score = self.simulation.score
        gene = self.simulation.bridge_string
        print(f"Final score is: {score}")
        self.gene_scores[gene] = score

