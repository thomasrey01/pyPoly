import pymunk
from car import Car


class Level:
    ground_friction = 1

    # Static ground shapes
    ground_pieces: [pymunk.Poly] = []

    # Immovable joints to connect the bridge to
    static_joints = []

    car: Car

    def __init__(self, space, width, height):
        ground_points = [
            [(0, 0), (0, 200), (100, 200), (100, 0)],
            [
                (width, 0),
                (width, 200),
                (width - 100, 200),
                (width - 100, 0),
            ],
        ]

        for ground in ground_points:
            ground_piece = pymunk.Poly(space.static_body, ground)
            ground_piece.friction = self.ground_friction
            space.add(ground_piece)
            self.ground_pieces.append(ground_piece)

        # Ball / car
        self.car = Car(space)
