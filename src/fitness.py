from beam import Beam
from car import Car
from goal import Goal
from joints import PivotJoint


class Fitness:
    # Weights for fitness function (higher is better)
    weights = {
        "build_cost": -0.01,  # Total cost of bridge
        "structural_integrity": -500,  # Penalty per broken joint
        "car_distance": -10,  # car distance
    }
    totalFitness = 0

    car_distance = None

    def start_fitness(self, beams: [Beam]):
        for beam in beams:
            self.totalFitness += beam.cost() * self.weights["build_cost"]

    def dynamic_fitness(self, dt: float, car: Car, goal: Goal, num_broken: int):
        self._update_car_distance(car, goal)
        self.totalFitness += num_broken * self.weights["structural_integrity"]
        return self.car_distance

    def _update_car_distance(self, car: Car, goal: Goal):
        new_car_distance = car.distance_to_goal(goal)

        if self.car_distance is None:
            diff = new_car_distance
        else:
            diff = new_car_distance - self.car_distance

        self.totalFitness += diff * self.weights["car_distance"]
        self.car_distance = new_car_distance
