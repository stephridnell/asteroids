import math
import random
from typing import Dict, List

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-30, 30)

        base_color = random.choice([
            (200, 200, 200),
            (160, 160, 160),
            (180, 160, 140),
        ])

        self.color = base_color
        self.dark_color = tuple(max(0, c - 40) for c in base_color)
        self.light_color = tuple(min(255, c + 40) for c in base_color)

        self.points = self._generate_points()
        self._generate_surface_details()

    def _generate_points(self) -> List[pygame.Vector2]:
        # create a more irregular asteroid by adding 8-12 points around the
        # circumference of the circle
        num_points = random.randint(8, 12)
        points: List[pygame.Vector2] = []

        for i in range(num_points):
            # calc angle for this point
            angle = (2 * math.pi * i) / num_points

            # add some randomness to the radius at each point
            radius_variation = random.uniform(0.8, 1.2)
            point = pygame.Vector2(
                math.cos(angle) * self.radius * radius_variation,
                math.sin(angle) * self.radius * radius_variation
            )

            points.append(point)

        return points

    def _generate_surface_details(self) -> None:
        self.craters: List[Dict[str, float]] = []

        # divide the asteroid into 8 sectors so we can distribute the craters
        # a bit more evenly
        num_sectors = 8
        sector_angles = [i * (2 * math.pi / num_sectors)
                         for i in range(num_sectors)]

        num_craters = random.randint(3, 5)
        used_sectors = set()

        for _ in range(num_craters):
            available_sectors = [i for i in range(
                num_sectors) if i not in used_sectors]
            if not available_sectors:
                break

            sector_idx = random.choice(available_sectors)
            used_sectors.add(sector_idx)

            # Calculate crater position within the sector
            sector_start = sector_angles[sector_idx]
            sector_end = sector_angles[(sector_idx + 1) % num_sectors]
            angle = random.uniform(sector_start, sector_end)

            # keep craters away from edges and center
            distance = random.uniform(self.radius * 0.3, self.radius * 0.7)
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance

            crater = {
                'pos': pygame.Vector2(x, y),
                'radius': random.uniform(self.radius * 0.1, self.radius * 0.2),
            }
            self.craters.append(crater)

    def draw(self, screen) -> None:
        rotated_points: List[pygame.Vector2] = []
        for point in self.points:
            # Rotate point
            rotated = point.rotate(math.degrees(self.rotation))
            # Translate to asteroid position
            translated = rotated + self.position
            rotated_points.append(translated)

        pygame.draw.polygon(screen, self.color, rotated_points)
        pygame.draw.polygon(screen, self.light_color, rotated_points, 2)

        for crater in self.craters:
            crater_pos = crater['pos'].rotate(
                math.degrees(self.rotation)) + self.position
            pygame.draw.circle(screen, self.dark_color,
                               crater_pos, crater['radius'])

    def update(self, dt) -> None:
        self.rotation += math.radians(self.rotation_speed * dt)
        super().update(dt)

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = random.uniform(20, 50)

        asteroid_1 = Asteroid(
            self.position.x,
            self.position.y,
            self.radius - ASTEROID_MIN_RADIUS
        )
        asteroid_2 = Asteroid(
            self.position.x,
            self.position.y,
            self.radius - ASTEROID_MIN_RADIUS
        )

        asteroid_1.velocity = self.velocity.rotate(angle) * 1.2
        asteroid_2.velocity = self.velocity.rotate(-angle) * 1.2
