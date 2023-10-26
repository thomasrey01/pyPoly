from simulation import Simulation
from genetic import BridgeGenetic
# from builder import Builder
# from pymunk import Vec2d

def main():

    genetic = BridgeGenetic()

    sim = Simulation(bridge_string = genetic.new_gene(), interactive=True)
    sim.start()

    print(f"Fitness: {sim.fitness.totalFitness:.2f}")

    # builder = Builder()

    # builder.simple_bridge(Vec2d(3,3), 5)

    # print(builder.get_sequence())

if __name__ == "__main__":
    main()
