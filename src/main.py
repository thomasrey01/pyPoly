from simulation import Simulation
from genetic import BridgeGenetic
from sys import argv, exit
import sys
from geneticalgorithm import GeneticAlgorithm

def print_usage():
    print("Usage: python main.py {interactive, genetic}")
    print("python main.py -h for help")


def main():
    if len(argv) >= 2:
        # Genetic version for automatically testing genes
        # # Genetic still buggy for now
        if argv[1] == "genetic":
            #genetic = BridgeGenetic()
            gen_alg = GeneticAlgorithm(multithreading=True)
            gen_alg.start()

        # Interactive version for manually building bridge
        elif argv[1] == "interactive":
            #sim = Simulation(BridgeGenetic.new_gene(), interactive=True)
            sim = Simulation("", interactive=True)
            sim.start()

        elif argv[1] == "gene":
            if len(argv) < 3:
                print_usage()
            else:
                beams = argv[2]
                start_bridge = BridgeGenetic.new_gene()
                sim = Simulation(start_bridge + beams, interactive=True)
                sim.start()
        # Some extra arguments would be nice like parsing a custom string
        # or give it some initial string to start searching from
        elif argv[1] == "-h" or argv[1] == "--help":
            print_usage()
    else:
        print_usage()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Got keyboard interrupt")
        exit(0)
