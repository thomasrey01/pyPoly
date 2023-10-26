class BridgeGenetic:

    SEARCH_LENGTH = 12 # Trying 12 for now

    base_gene = "dfabefab"
    
    genes = {}

    def __init__(self):
        pass

    def start(self):
        pass

    def cross(self, gene1, gene2):
        pass

    def create_road(self): # Creating road gene
        gene = ""
        connected_points = []
        for i in range(11):
            gene += chr(ord('c') + i) + "faa"
            connected_points.append((chr(ord('c') + i), 'f'))
        return gene, connected_points

    def new_gene(self): # This method has to create a gene that starts at df and somehow ends at mg.
        gene, connected_points = self.create_road()
        # for i in range(self.SEARCH_LENGTH):
        print(f"Gene is: {gene}")
        print(f"Connected points are: {connected_points}")
        return gene



