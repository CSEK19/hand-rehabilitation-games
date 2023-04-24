import pygame
from utils.constants import *

def paused(screen):
    pause = True
    selection = 0
    option_list(selection, screen)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selection = (selection + 1) % 2
                    option_list(selection, screen)
                elif event.key == pygame.K_UP:
                    selection = (selection - 1) % 2
                    option_list(selection, screen)
                elif event.key == pygame.K_RETURN:
                    return selection

def replay_or_return(selection, screen):
    popup_width, popup_height = 600, 160
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
    font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    options = ['Replay', 'Home']
    texts = [font_popup_text.render(text, True, DEFAULT_COLOR) if i != selection else font_popup_text.render(text, True,
                                                                                                             FONT_COLOR)
             for (i, text) in enumerate(options)]
    textRects = [text.get_rect() for text in texts]

    textRects[0].centerx = popup_surface.get_rect().centerx
    textRects[0].top = 0
    textRects[1].centerx = popup_surface.get_rect().centerx
    textRects[1].top = 40
    [popup_surface.blit(text, textRect) for text, textRect in zip(texts, textRects)]

    popup_rect = popup_surface.get_rect()
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    screen.blit(popup_surface, popup_rect)
    pygame.display.update()

def option_list(selection, screen):
    popup_width, popup_height = 600, 160
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 255))  # set alpha to 0
    font_popup = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    text_surface = font_popup.render("Game Paused", True, (255, 99, 71))
    text_rect = text_surface.get_rect()
    text_rect.centerx = popup_surface.get_rect().centerx
    text_rect.top = 20
    popup_surface.blit(text_surface, text_rect)

    options = ['Continue', 'Home']
    texts = [font_popup_text.render(text, True, DEFAULT_COLOR) if i != selection else font_popup_text.render(text, True,
                                                                                                             FONT_COLOR)
             for (i, text) in enumerate(options)]
    textRects = [text.get_rect() for text in texts]

    textRects[0].centerx = popup_surface.get_rect().centerx
    textRects[0].top = 80
    textRects[1].centerx = popup_surface.get_rect().centerx
    textRects[1].top = 120
    [popup_surface.blit(text, textRect) for text, textRect in zip(texts, textRects)]

    popup_rect = popup_surface.get_rect()
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    screen.blit(popup_surface, popup_rect)
    pygame.display.update()
