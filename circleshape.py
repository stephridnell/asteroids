import pygame

from shape import Shape


class CircleShape(Shape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y)
        self.radius = radius

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def check_collision(self, other) -> bool:
        if isinstance(other, CircleShape):
            distance = self.position.distance_to(other.position)
            return distance < self.radius + other.radius
        return False
