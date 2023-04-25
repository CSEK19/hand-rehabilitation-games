import pygame
import sys
from game1 import game1
from game2 import game2
from game3 import game3
from utils.constants import *

pygame.mixer.init(44100, -16, 2, 2048)

pygame.init()
pygame.font.init()
pygame.font.get_init()

clock = pygame.time.Clock()
font = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
font_setting = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

pygame.display.set_caption("Video Games for Hand Rehabilitation")
music = pygame.mixer.Sound('music/music.mp3')
music.set_volume(0.5)

state = 'home'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
selection = 0
enable_setting = False
enable_music = False
enable_Vie_language = True
setting_selection = 0
is_playing_music = False


def game_list(selection):
    games = ['1. Shapes and Colors', '2. Eggs and Milk', '3. Dino Run'] 
    texts = [font.render(text, True, (64, 61, 57)) if i != selection else font.render(text, True, FONT_COLOR) for
             (i, text) in enumerate(games)]
    textRects = [text.get_rect() for text in texts]
    textRects[0].midleft = (SCREEN_WIDTH // 3, 300)
    textRects[1].midleft = (SCREEN_WIDTH // 3, 400)
    textRects[2].midleft = (SCREEN_WIDTH // 3, 500)
    [screen.blit(text, textRect) for text, textRect in zip(texts, textRects)]


def setting_list(selection):
    if enable_Vie_language:
        music_text = 'Âm nhạc: Bật' if enable_music else 'Âm nhạc: Tắt'
        language_text = 'Ngôn ngữ: Tiếng Anh' if not enable_Vie_language else 'Ngôn ngữ: Tiếng Việt'
        save_text = 'Lưu'
    else:
        music_text = 'Music: Enabled' if enable_music else 'Music: Disabled'
        language_text = 'Language: English' if not enable_Vie_language else 'Language: Vietnamese'
        save_text = 'Save'
    games = [music_text, language_text, save_text]
    texts = [
        font_setting.render(text, True, (64, 61, 57)) if i != selection else font_setting.render(text, True, FONT_COLOR)
        for
        (i, text) in enumerate(games)]
    textRects = [text.get_rect() for text in texts]
    textRects[0].midleft = (SCREEN_WIDTH // 3, 300)
    textRects[0].centerx = SCREEN_WIDTH // 2
    textRects[1].midleft = (SCREEN_WIDTH // 3, 350)
    textRects[1].centerx = SCREEN_WIDTH // 2
    textRects[2].midleft = (SCREEN_WIDTH // 3, 400)
    textRects[2].centerx = SCREEN_WIDTH // 2

    [screen.blit(text, textRect) for text, textRect in zip(texts, textRects)]


def home():
    global selection, enable_setting, enable_music, enable_Vie_language, setting_selection
    screen.fill(WHITE_COLOR)
    if not enable_Vie_language:
        text1 = font.render('Video Games for Hand Rehabilitation', True, FONT_COLOR)
        text2 = font_setting.render('Settings', True, (64, 61, 57))

    else:
        text1 = font.render('Trò chơi tập luyện và phục hồi khả năng sử dụng tay', True, FONT_COLOR)
        text2 = font_setting.render('Cài đặt', True, (64, 61, 57))

    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    screen.blit(text1, textRect1)

    textRect2 = text2.get_rect()
    textRect2.center = (SCREEN_WIDTH - 100, 50)
    screen.blit(text2, textRect2)

    if enable_setting:
        screen.fill(WHITE_COLOR)
        if not enable_Vie_language:
            text2 = font_setting.render('Settings', True, FONT_COLOR)
            text3 = font.render('Settings', True, (255, 99, 71))

        else:
            text2 = font_setting.render('Cài đặt', True, FONT_COLOR)
            text3 = font.render('Cài đặt', True, (255, 99, 71))

        textRect2.center = (SCREEN_WIDTH - 100, 50)
        screen.blit(text2, textRect2)

        popup_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 25)
        pygame.draw.rect(screen, WHITE_COLOR, popup_rect)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 1)

        textRect3 = text3.get_rect()
        textRect3.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        screen.blit(text3, textRect3)
        setting_list(setting_selection)

    else:
        game_list(selection)


def game():
    global state, selection, enable_setting, setting_selection, enable_music, enable_Vie_language, is_playing_music

    while True:
        if enable_music:
            if not is_playing_music:
                music.play(loops=-1)
            is_playing_music = True
        else:
            music.stop()
            is_playing_music = False
        if state == 'home':
            home()
        if state == 'game1':
            state = game1(screen, font, clock, enable_Vie_language)
        if state == 'game2':
            state = game2(screen, font, clock)
        if state == 'game3':
            state = game3(screen, font, clock)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not enable_setting:
                    if event.key == pygame.K_1:
                        state = 'game1'
                    if event.key == pygame.K_2:
                        state = 'game2'
                    if event.key == pygame.K_3:
                        state = 'game3'
                    if event.key == pygame.K_RETURN:
                        state = f'game{selection + 1}'
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % 3
                    if event.key == pygame.K_p:
                        enable_setting = not enable_setting
                else:
                    if event.key == pygame.K_RETURN:
                        if setting_selection == 0:
                            enable_music = not enable_music
                        elif setting_selection == 1:
                            enable_Vie_language = not enable_Vie_language
                        elif setting_selection == 2:
                            enable_setting = False
                    if event.key == pygame.K_UP:
                        setting_selection = (setting_selection - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        setting_selection = (setting_selection + 1) % 3

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    game()
