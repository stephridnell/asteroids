import random

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from star import Star


class Background:
    def __init__(self):
        self.stars = []
        self.num_stars = 300
        self._generate_stars()
        self._create_nebula()

    def _create_nebula(self) -> None:
        self.nebula_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            # fade from dark blue to black
            blue = int(50 * (1 - y / SCREEN_HEIGHT))
            colour = (0, 0, blue)
            pygame.draw.line(self.nebula_surface, colour,
                             (0, y), (SCREEN_WIDTH, y))

    def _generate_stars(self) -> None:
        for _ in range(self.num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)

            # create different types of stars with predetermined distribution
            star_type = random.random()
            if star_type < 0.6:  # 60% small
                size = random.randint(1, 2)
            elif star_type < 0.85:  # 25% medium
                size = random.randint(2, 3)
            elif star_type < 0.95:  # 10% large
                size = random.randint(3, 4)
            else:  # 5% very large
                size = random.randint(4, 5)

            self.stars.append(Star(x, y, size))

    def update(self, dt) -> None:
        for star in self.stars:
            star.update(dt)

    def draw(self, screen) -> None:
        screen.blit(self.nebula_surface, (0, 0))
        for star in self.stars:
            star.draw(screen)
