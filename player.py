import pygame

from constants import (PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN,
                       PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED)
from shot import Shot
from triangleshape import TriangleShape


class Player(TriangleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.timer = 0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

        super().update(dt)

    def shoot(self, dt):
        if self.timer > 0:
            return

        shot = Shot(self.position, self.rotation)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN

    def check_collision(self, other):
        # Get the triangle points
        triangle_points = self.get_triangle_points()

        # For circular objects (like asteroids), check if any point of the
        # triangle is within the circle
        if isinstance(other, TriangleShape):
            for point in triangle_points:
                if point.distance_to(other.position) < other.radius:
                    return True
            return False

        # For other shapes, use the parent class's circular collision
        return super().check_collision(other)
