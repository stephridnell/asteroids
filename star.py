import math
import random
from typing import Tuple

import pygame

from circleshape import CircleShape


class Star(CircleShape):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size)

        # store original radius for pulsing
        self.original_radius = size

        # brightness/colour props
        self.base_brightness = random.randint(200, 255)
        self.colour_variation = random.randint(-20, 20)

        # movment props
        self.speed = random.uniform(0.1, 0.3)
        self.movement_type = random.random()
        self.angle = random.uniform(0, 2 * math.pi)
        self.angle_speed = random.uniform(0.1, 0.3)

        # twinkle props
        self.twinkle_speed = random.uniform(1, 3)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.twinkle_amount = random.uniform(0.2, 0.4)

        # pulse props
        self.pulse_speed = random.uniform(0.5, 1.5)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.pulse_amount = random.uniform(0.1, 0.3)

        # set colour last cos it needs some of the props to set it
        self.colour = self._get_colour()

    def _get_colour(self) -> Tuple[int, int, int]:
        # calc twinkling brightness
        twinkle = math.sin(self.twinkle_phase) * self.twinkle_amount
        brightness = math.floor(self.base_brightness +
                                self.colour_variation + twinkle)

        # make sure brightness stays at 255 or lower
        brightness = min(255, max(0, brightness))

        # add colour tinting, pretty subtle
        tint = random.choice([(0, 0, 0),       # white
                              (100, 0, 0),     # red
                              (0, 100, 0),     # green
                              (0, 0, 100),     # blue
                              (100, 100, 0),   # yellow
                              ])

        return (
            min(255, max(0, brightness + tint[0])),
            min(255, max(0, brightness + tint[1])),
            min(255, max(0, brightness + tint[2]))
        )

    def update(self, dt: float) -> None:
        self.twinkle_phase += self.twinkle_speed * dt
        self.pulse_phase += self.pulse_speed * dt

        if self.movement_type < 0.6:  # 60% straight down
            self.position.y += self.speed * dt
        elif self.movement_type < 0.8:  # 20% diagonal
            self.position.y += self.speed * dt
            self.position.x += math.sin(self.angle) * self.speed * 0.5 * dt
            self.angle += self.angle_speed * dt
        else:  # 20% wave motion
            self.position.y += self.speed * dt
            self.position.x += math.sin(self.angle) * self.speed * 0.3 * dt
            self.angle += self.angle_speed * dt

        self.colour = self._get_colour()

        # update size with pulsing (using original radius as base)
        pulse_factor = 1 + math.sin(self.pulse_phase) * self.pulse_amount
        self.radius = self.original_radius * pulse_factor

        # werap around screen
        screen_height = pygame.display.get_surface().get_height()
        screen_width = pygame.display.get_surface().get_width()

        if self.position.y > screen_height:
            self.position.y = 0
            self.position.x = random.randint(0, screen_width)
            # reset some properties for variety
            self.twinkle_phase = random.uniform(0, 2 * math.pi)
            self.pulse_phase = random.uniform(0, 2 * math.pi)
            self.angle = random.uniform(0, 2 * math.pi)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
