from typing import List, Union

import pygame

from circleshape import CircleShape
from constants import DEBUG_MODE
from shape import Shape


class TriangleShape(Shape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y)
        self.radius = radius
        self.rotation = 0

    def get_triangle_points(self) -> List[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        # Draw the triangle
        pygame.draw.polygon(screen, (255, 255, 255), self.get_triangle_points(), 2)

        if DEBUG_MODE:
            # Draw circular hitbox in red
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius, 1)

            # Draw triangular hitbox in green
            pygame.draw.polygon(screen, (0, 255, 0), self.get_triangle_points(), 1)

            # Draw triangle points in blue
            for point in self.get_triangle_points():
                pygame.draw.circle(screen, (0, 0, 255), point, 2)

    def check_collision(self, other):
        if isinstance(other, CircleShape):
            # For circular objects, check if any point of the triangle is within the circle
            for point in self.get_triangle_points():
                if point.distance_to(other.position) < other.radius:
                    return True
            return False
        return False
