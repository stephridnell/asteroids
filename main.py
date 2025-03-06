import argparse

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from background import Background
from constants import FRAMES_PER_SECOND, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Asteroids Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug visualization')
    args = parser.parse_args()

    # Set debug mode based on command line argument
    global DEBUG_MODE
    DEBUG_MODE = args.debug

    # Initialize pygame
    pygame.init()

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print(f"Debug mode: {'enabled' if DEBUG_MODE else 'disabled'}")

    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Initialize background
    background = Background()

    # Initialize sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Initialize asteroid field
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    AsteroidField()

    # Initialize player
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Initialize shot
    Shot.containers = (updatable, drawable, shots)

    # Game loop setup
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update game state
        dt = clock.tick(FRAMES_PER_SECOND) / 1000.0  # Convert to seconds

        background.update(dt)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw background
        background.draw(screen)

        for sprite in updatable:
            sprite.update(dt)

        # Check for collisions
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.check_collision(shot):
                    asteroid.split()
                    shot.kill()

            if asteroid.check_collision(player) and not DEBUG_MODE:
                print("Game over!")
                running = False

        for sprite in drawable:
            sprite.draw(screen)

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
