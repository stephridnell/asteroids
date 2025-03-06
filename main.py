import argparse

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from background import Background
from constants import FRAMES_PER_SECOND, SCREEN_HEIGHT, SCREEN_WIDTH
from gameover import draw_high_scores, draw_text, get_player_name
from player import Player
from score import Score
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

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    background = Background()
    score_manager = Score()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (updatable, drawable, shots)

    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_over and event.key == pygame.K_RETURN:
                    # Reset game
                    game_over = False
                    score_manager.reset_score()
                    for sprite in updatable:
                        sprite.kill()
                    AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        if not game_over:
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
                        # Add points based on asteroid size
                        points = int(asteroid.radius * 10)
                        score_manager.add_points(points)

                if player.check_collision(asteroid):
                    game_over = True
                    player_name = get_player_name(screen)
                    score_manager.update_high_scores(player_name)

            for sprite in drawable:
                sprite.draw(screen)

            draw_text(screen, f"Score: {score_manager.get_current_score()}", 24, 100, 20)

        else:
            screen.fill((0, 0, 0))
            draw_text(screen, "Game Over!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text(screen, f"Final Score: {score_manager.get_current_score()}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, "Press ENTER to play again", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            draw_high_scores(screen, score_manager)

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
