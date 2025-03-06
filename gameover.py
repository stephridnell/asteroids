
import sys

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from score import Score


def draw_text(
        screen: pygame.Surface,
        text: str,
        size: int,
        x: int,
        y: int,
        color: tuple[int, int, int] = (255, 255, 255)
) -> None:
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def draw_high_scores(screen: pygame.Surface, score_manager: Score) -> None:
    draw_text(screen, "High Scores", 36, SCREEN_WIDTH // 2, 50)
    y = 100
    for i, (name, score) in enumerate(score_manager.get_high_scores(), 1):
        text = f"{i}. {name}: {score}"
        draw_text(screen, text, 24, SCREEN_WIDTH // 2, y)
        y += 30


def get_player_name(screen: pygame.Surface) -> str:
    name = ""
    input_active = True
    while input_active:
        screen.fill((0, 0, 0))
        draw_text(screen, "Enter your name:", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(screen, name + "|", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode

    return name