from dataclasses import dataclass

@dataclass # Removes the need of specifying constructor
class Material:
    name: str
    strength: float
    max_length: float
    collision_type: int
    thickness: float
    density: float
    friction: float
    color: (float, float, float, float)
    cost: float

    def check_length(self, length):
        return length < self.max_length
