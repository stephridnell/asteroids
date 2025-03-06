from typing import Type

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Shape(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_position()

    def wrap_position(self) -> None:
        # Wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def check_collision(self, other: Type['Shape']) -> bool:
        pass