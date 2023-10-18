import pygame

from fitness import Fitness


class FitnessRenderer:
    text_color = (0, 0, 0)
    background_color = (255, 255, 255)

    font: pygame.font.Font
    position: tuple
    fitness: Fitness

    def __init__(self, fitness: Fitness, position=(0, 0)):
        self.position = position
        self.fitness = fitness
        self.font = pygame.font.Font("freesansbold.ttf", 32)

    def draw(self, screen):
        text = self.font.render(
            f"F: {self.fitness.totalFitness:.2f}",
            True,
            self.text_color,
            self.background_color,
        )

        textRect = text.get_rect()
        textRect.topleft = self.position

        screen.blit(text, textRect)
