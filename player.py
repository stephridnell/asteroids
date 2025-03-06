import os

import pygame

from constants import (PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN,
                       PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED)
from shot import Shot
from triangleshape import TriangleShape


class Player(TriangleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.timer = 0
        self.rotation = 180

        sprite_path = os.path.join('images', 'rocket.png')
        try:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # scale the sprite to match the player radius while maintaining aspect ratio
            original_width, original_height = self.sprite.get_size()
            aspect_ratio = original_height / original_width
            
            # Use width as the base for scaling
            target_width = int(PLAYER_RADIUS * 1.5)  # Slightly larger than radius
            target_height = int(target_width * aspect_ratio)
            
            self.sprite = pygame.transform.scale(self.sprite, (target_width, target_height))

        except (pygame.error, FileNotFoundError):
            print(f"Warning: Could not load rocket sprite from {sprite_path}")
            print("Falling back to default triangle shape")
            self.sprite = None

    def draw(self, screen):
        if self.sprite:
            rotated_sprite = pygame.transform.rotate(self.sprite, -self.rotation + 180)
            rect = rotated_sprite.get_rect(center=self.position)
            screen.blit(rotated_sprite, rect)
        else:
            # fallback triangle shape if sprite loading fails
            points = self.get_triangle_points()
            rotated_points = []
            for point in points:
                rotated = point.rotate(self.rotation)
                translated = rotated + self.position
                rotated_points.append(translated)
            
            pygame.draw.polygon(screen, (255, 255, 255), rotated_points)
            pygame.draw.polygon(screen, (200, 200, 200), rotated_points, 2)

    def get_triangle_points(self):
        points = [
            pygame.Vector2(0, self.radius),
            pygame.Vector2(-self.radius * 0.6, -self.radius * 0.6),
            pygame.Vector2(self.radius * 0.6, -self.radius * 0.6),
        ]
        return points

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
