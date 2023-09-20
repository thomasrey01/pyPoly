import pymunk
import pygame

class Level:

    def __init__(self, size: int):

        pygame.init()

        self.w, self.h = 1200, 600

        self.running = True
        self.size = size
        self.joints = []
        self.boxes = []
        self.space = pymunk.Space()
        self.screen = pygame.display.set_mode((self.w, self.h))
    
    def run(self):
        while self.running:
            self.loop()
    
    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
    
    def create_box(self, point=(200, 100), size=50):
        box = pymunk.Poly(self.space.static_body, [(point[0] - size, point[1] - size),
                                                   (point[0] - size, point[1] + size),
                                                   (point[0] + size, point[1] - size),
                                                   (point[0] + size, point[1] + size)])

        self.boxes.append(box)
        self.space.add(box)


demo = Level(0)
demo.create_box()
demo.run()
