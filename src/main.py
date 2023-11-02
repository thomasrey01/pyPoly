from simulation import Simulation
from genetic import BridgeGenetic
from sys import argv
# from builder import Builder
# from pymunk import Vec2d

def main():


    if (len(argv) == 2):

        # Genetic version for automatically testing genes
        # Genetic still buggy for now
        if argv[1] == "genetic":
            genetic = BridgeGenetic()
        # Interactive version for manually building bridge
        elif argv[1] == "interactive":
            sim = Simulation(bridge_string = BridgeGenetic.new_gene(), interactive=True)
            sim.start()
        
        # Some extra arguments would be nice like parsing a custom string
        # or give it some initial string to start searching from
        elif argv[1] == "-h" or argv[1] == "--help":
            pass
    else:
        print("Usage: python main.py {interactive, genetic}")
        print("python main.py -h for help")

    
    

    # print(f"Fitness: {sim.fitness.totalFitness:.2f}")

    # builder = Builder()

    # builder.simple_bridge(Vec2d(3,3), 5)

    # print(builder.get_sequence())

if __name__ == "__main__":
    main()
