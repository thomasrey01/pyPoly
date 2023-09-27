import pymunk
from car import Car


class Level:

    point_spacing = 40

    ground_friction = 1

    # Static ground shapes
    ground_pieces: [pymunk.Poly] = []

    # Immovable joints to connect the bridge to
    static_joints = {}

    bridge_joints = [(90, 200), (210, 0)]

    car: Car

    def __init__(self, space: pymunk.Space, width, height):
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
        

        # def no_point_collide(arbiter, space, data):
        #     return False


        # self.collision_handler = space.add_collision_handler(1, 1)
        # self.collision_handler.begin = no_point_collide

        # Ball / car
        self.car = Car(space)

        for i in range(0, width, self.point_spacing):
            for j in range(0, height, self.point_spacing):
                point_b = pymunk.Body(body_type=pymunk.Body.STATIC)
                point_b.position = (i, j)
                point_s = pymunk.Circle(point_b, 2)
                point_s.color = (255, 0, 0, 100)
                point_s.sensor = True

                space.add(point_b, point_s)
                self.static_joints[point_b.position] = point_b

    def get_static_joint(self, pos):
        return self.static_joints[pos]
        

