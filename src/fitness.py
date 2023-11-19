from beam import Beam
from car import Car
from goal import Goal
import settings
from joints import PivotJoint


class Fitness:
    # Weights for fitness function (higher is better)
    weights = {
        "build_cost": -0.0001,  # Total cost of bridge
        "structural_integrity": -500,  # Penalty per broken joint
        "car_distance": -100,  # car distance
    }
    totalFitness: int
    car_distance: int

    def __init__(self) -> None:
        self.totalFitness = 0
        self.car_distance = None
        self.weights["build_cost"] = settings.build_cost
        self.weights["structural_integrity"] = settings.structural_integrity
        self.weights["car_distance"] = settings.car_distance

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
