# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame

pygame.init()
death_count = 0
state = 'play3'
# Global Constants

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("sprites/DinoWallpaper.png")
pygame.display.set_icon(Ico)

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

FONT_COLOR=(56,83,153)

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

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
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

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


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

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


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
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, death_count, state
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 580
    points = 0
    font = pygame.font.SysFont('', 50)
    obstacles = []
    death_count = 0
    pause = False

    def score():
        global points, game_speed
        points += 0.1
        if int(points) % 5 == 0 and int(points) != 0:
            game_speed += 0.02
        current_time = datetime.datetime.now().hour
        text = font.render("Score: " + str(int(points)), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (150, 50)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                state = 'home'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                run = False
                state = 'home'

        SCREEN.fill((255, 255, 255))

        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        obstacles_idx_list = [0]
        if points > 50:
            obstacles_idx_list = [0, 1, 1]
        if points >120:
            obstacles_idx_list = [0, 1, 1, 2, 2]

        ob = random.choice(obstacles_idx_list)
        if len(obstacles) == 0:
            if ob == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif ob == 1:
                obstacles.append(Bird(BIRD))
            elif ob == 2:
                obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                run = False
                state = 'home'
                # game3(death_count)
        
        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def game3():
    global points, death_count, state
    global FONT_COLOR
    run = True
    exit = 0
    while run:
        if state == 'play3':
            main()
        else:
            current_time = datetime.datetime.now().hour
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("freesansbold.ttf", 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, FONT_COLOR)
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, FONT_COLOR)
                score = font.render("Your Score: " + str(round(points)), True, FONT_COLOR)
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        exit = 1
                    else:
                        state = 'play3'
        if exit == 1:
            break
    
    return 'home'


if __name__ == "__main__":
    game3()
