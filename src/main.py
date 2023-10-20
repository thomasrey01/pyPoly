from simulation import Simulation

def main():
    sim = Simulation(bridge_string = "", interactive=True)
    sim.start()

    print(f"Fitness: {sim.fitness.totalFitness:.2f}")

if __name__ == "__main__":
    main()
