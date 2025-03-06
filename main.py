import pygame

from constants import *
from player import Player


def main():
    pygame.init()  # Initialize pygame
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    
    # Game loop setup
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

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
        
        # Clear screen
        screen.fill((0, 0, 0))

        # Draw game objects here
        player.draw(screen)

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()