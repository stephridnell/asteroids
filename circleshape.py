import pygame

from shape import Shape


class CircleShape(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def check_collision(self, other):
        if isinstance(other, CircleShape):
            distance = self.position.distance_to(other.position)
            return distance < self.radius + other.radius
        return False
