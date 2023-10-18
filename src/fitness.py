import pymunk
import math

from beam import Beam
from car import Car 
from goal import Goal


class Fitness:
    # Weights for fitness function (higher is better)
    weights = {
        "build_cost": -0.1, # Total cost of 
        "instability": -0.1, # movement per time step
        "car_distance": -1 # min car distance 
        # TODO: structural integrity (breaking stuff)

    }
    totalFitness = 0

    min_car_distance = math.inf

    def static_fitness(self, beams: [Beam]):
        for beam in beams:
            self.totalFitness += beam.cost() * self.weights["build_cost"]

    def dynamic_fitness(self, dt: float, car: Car, goal: Goal):

        # TODO stability of bridge

        self._update_car_distance(car, goal)

    def _update_car_distance(self, car: Car, goal: Goal):
        new_car_distance = goal.get_distance(car)

        if(new_car_distance < self.min_car_distance):
            if math.isinf(self.min_car_distance):
                diff = new_car_distance
            else: 
                diff = new_car_distance - self.min_car_distance

            self.totalFitness += diff * self.weights["car_distance"]
            self.min_car_distance = new_car_distance












