class Material:
    strength: float
    max_length: float
    collisionGroup: int
    thickness: float
    density: float
    friction: float
    color: (float, float, float, float)

    def __init__(self, strength, max_length, collisionGroup, thickness, density, friction, color):
        self.strength = strength
        self.max_length = max_length
        self.collisionGroup = collisionGroup
        self.thickness = thickness
        self.density = density
        self.friction = friction
        self.color = color

    def check_length(self, length):
        return length < self.max_length
