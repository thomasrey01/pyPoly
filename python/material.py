class Material:
    name: str
    strength: float
    max_length: float
    collision_type: int
    thickness: float
    density: float
    friction: float
    color: (float, float, float, float)

    def __init__(self, name, strength, max_length, thickness, density, friction, color):
        self.name = name
        self.strength = strength
        self.max_length = max_length
        self.thickness = thickness
        self.density = density
        self.friction = friction
        self.color = color

    def check_length(self, length):
        return length < self.max_length
