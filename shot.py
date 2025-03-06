import pygame

from circleshape import CircleShape
from constants import SHOT_MAX_DISTANCE, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.initial_position = pygame.Vector2(x, y)
        self.distance_traveled = 0

    def update(self, dt: float) -> None:
        # Store old position to calculate distance
        old_position = pygame.Vector2(self.position)
        
        # Move the shot
        self.position += self.velocity * dt
        
        # Calculate distance traveled
        self.distance_traveled += old_position.distance_to(self.position)
        
        # Check if shot has traveled too far
        if self.distance_traveled > SHOT_MAX_DISTANCE:
            self.kill()
            return
            
        # Handle screen wrapping
        super().update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            self.position,
            self.radius,
            2
        )
