class Material:
    strength: float
    max_length: float
    collisionGroup: int
    thickness: float
    density: float
    friction: float

    def __init__(self, strength, max_length, collisionGroup, thickness, density, friction):
        self.strength = strength
        self.max_length = max_length
        self.collisionGroup = collisionGroup
        self.thickness = thickness
        self.density = density
        self.friction = friction

    def check_length(self, length):
        return length < self.max_length
