# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import pygame
from utils.constants import *

death_count = 0
state_game_3 = 'play3'

screen = None
font = None
clock = None
enable_Vie_language = False

RUNNING = [
    pygame.image.load(os.path.join("sprites/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("sprites/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("sprites/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("sprites/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("sprites/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("sprites/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("sprites/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("sprites/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("sprites/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("sprites/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("sprites/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("sprites/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("sprites/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("sprites/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("sprites/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 510
    Y_POS_DUCK = 540
    JUMP_VEL = 8

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.duck_interval = 25
        self.duck_count = 0

    def update(self, key):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (key == pygame.K_UP) and not self.dino_jump and self.dino_rect.y == 510:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif (key == pygame.K_DOWN and not self.dino_jump) or self.duck_count > 0:
            self.duck_count += 1
            if self.duck_count == self.duck_interval:
                self.duck_count = 0
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not key and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 2
            self.jump_vel -= 0.4
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, my_screen):
        my_screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, my_screen):
        my_screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 525


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 500


class Bird(Obstacle):
    BIRD_HEIGHTS = [450, 490, 520]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, death_count, state_game_3, font
    run = True
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 580
    points = 0
    obstacles = []
    death_count = 0
    pause = False

    def score():
        global points, game_speed, font, enable_Vie_language
        points += 0.05
        if int(points) % 5 == 0 and int(points) != 0 and int(points) <= 100:
            points += 0.01
            game_speed += 0.02
        if not enable_Vie_language:
            text = font.render("Score: " + str(int(points)), True, FONT_COLOR)
        else:
            text = font.render("Điểm: " + str(int(points)), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (150, 50)
        screen.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def need_help():
        global screen, enable_Vie_language
        nonlocal pause
        pause = True

        popup_width, popup_height = 1000, 300
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
        font_popup = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
        font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

        if not enable_Vie_language:
            help_text = 'How to Play'
            desc_text = "Control the dinosaur to avoid obstacles as much as possible"
            option0_text = "To jump - move palm up"
            option1_text = "To duck - move palm down"
            option2_text = "Make a fist to continue"
        else:
            help_text = 'Cách chơi'
            desc_text = "Điều khiển chú khủng long để tránh các chướng ngại vật"
            option0_text = "Để nhảy - lắc cổ tay hướng lên"
            option1_text = "Để cúi - lắc cổ tay hướng xuống"
            option2_text = "Nắm chặt bàn tay để tiếp tục"

        text_surface = font_popup.render(help_text, True, (255, 99, 71))
        text_rect = text_surface.get_rect()
        text_rect.centerx = popup_surface.get_rect().centerx
        text_rect.top = 20
        popup_surface.blit(text_surface, text_rect)

        desc_surface = font_popup_text.render(desc_text, True, FONT_COLOR)
        desc_rect = desc_surface.get_rect()
        desc_rect.centerx = popup_surface.get_rect().centerx
        desc_rect.top = 75
        popup_surface.blit(desc_surface, desc_rect)

        option0_surface = font_popup_text.render(option0_text, True, DEFAULT_COLOR)
        option0_rect = option0_surface.get_rect()
        option0_rect.centerx = popup_surface.get_rect().centerx
        option0_rect.top = 125
        popup_surface.blit(option0_surface, option0_rect)

        option1_surface = font_popup_text.render(option1_text, True, DEFAULT_COLOR)
        option1_rect = option1_surface.get_rect()
        option1_rect.centerx = popup_surface.get_rect().centerx
        option1_rect.top = 175
        popup_surface.blit(option1_surface, option1_rect)

        option2_surface = font_popup_text.render(option2_text, True, FONT_COLOR)
        option2_rect = option2_surface.get_rect()
        option2_rect.centerx = popup_surface.get_rect().centerx
        option2_rect.top = 225
        popup_surface.blit(option2_surface, option2_rect)

        popup_rect = popup_surface.get_rect()
        popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        screen.blit(popup_surface, popup_rect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def option_list(selection):
        global screen, enable_Vie_language
        popup_width, popup_height = 600, 160
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
        font_popup = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
        font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

        if not enable_Vie_language:
            text_surface = font_popup.render("Game Paused", True, (255, 99, 71))
            options = ['Continue', 'Home']
        else:
            text_surface = font_popup.render("Trò chơi tạm dừng", True, (255, 99, 71))
            options = ['Tiếp tục', 'Quay lại màn hình chính']

        text_rect = text_surface.get_rect()
        text_rect.centerx = popup_surface.get_rect().centerx
        text_rect.top = 20
        popup_surface.blit(text_surface, text_rect)

        texts = [
            font_popup_text.render(text, True, DEFAULT_COLOR) if i != selection else font_popup_text.render(text, True,
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

    def paused():
        nonlocal pause
        pause = True
        selection = 0
        option_list(selection)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selection = (selection + 1) % 2
                        option_list(selection)
                    elif event.key == pygame.K_UP:
                        selection = (selection - 1) % 2
                        option_list(selection)
                    elif event.key == pygame.K_RETURN:
                        return selection

    is_first_time = True
    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                state_game_3 = 'home'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused() == 1:
                        run = False
                        state_game_3 = 'exit'
                    else:
                        run = True
                elif event.key == pygame.K_b:
                    run = False
                    state_game_3 = 'exit'
                elif event.key == pygame.K_h:
                    need_help()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    key = event.key

        screen.fill(WHITE_COLOR)

        # userInput = pygame.key.get_pressed()

        player.draw(screen)
        player.update(key)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 2) == 2:
                obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.collidepoint(obstacle.rect.center):
                pygame.time.delay(1000)
                death_count += 1
                run = False
                state_game_3 = 'home'

        background()
        cloud.draw(screen)
        cloud.update()
        score()
        clock.tick(30)
        if is_first_time:
            need_help()
            is_first_time = False

        pygame.display.update()


def replay_or_return(selection):
    global screen, enable_Vie_language
    popup_width, popup_height = 600, 160
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
    font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    if not enable_Vie_language:
        options = ['Replay', 'Home']
    else:
        options = ['Chơi lại', 'Quay về màn hình chính']
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
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 300)

    screen.blit(popup_surface, popup_rect)
    pygame.display.update()


def game3(home_screen, home_font, home_clock, lang):
    global points, death_count, state_game_3, screen, font, clock, enable_Vie_language
    screen = home_screen
    font = home_font
    clock = home_clock
    run = True
    exit = 0
    selection = 0
    enable_Vie_language = lang

    while run:
        if state_game_3 == 'play3':
            main()
        elif state_game_3 == 'exit':
            exit = 1
            state_game_3 = 'play3'
        else:
            screen.fill(WHITE_COLOR)
            if not enable_Vie_language:
                score = font.render("Your Score: " + str(round(points)), True, FONT_COLOR)
                text = font.render("Game Over", True, (255, 99, 71))
            else:
                score = font.render("Điểm của bạn: " + str(round(points)), True, FONT_COLOR)
                text = font.render("Trò chơi kết thúc", True, (255, 99, 71))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            screen.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, textRect)
            screen.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            replay_or_return(selection)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selection = (selection + 1) % 2
                        replay_or_return(selection)
                    elif event.key == pygame.K_UP:
                        selection = (selection - 1) % 2
                        replay_or_return(selection)
                    elif event.key == pygame.K_RETURN:
                        if selection == 0:
                            state_game_3 = 'play3'
                        else:
                            exit = 1
        if exit == 1:
            state_game_3 = 'play3'
            break

    return 'home'


if __name__ == "__main__":
    game3()
