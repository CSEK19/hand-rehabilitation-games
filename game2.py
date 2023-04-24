import pygame
import os
import random
from utils.constants import *
from utils.functions import replay_or_return, paused

state_game_2 = 'play2'

screen = None
font = None
clock = None
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# easy
moving_range_easy = [440, 640, 840]
objects_easy = [1]
speed_easy = 2

# easy
objects_med = [0, 1]

# hard
moving_range_hard = [240, 440, 640, 840, 1040]
speed_hard = 2


class MyGame:
    batsketImg = pygame.image.load('sprites/basket_milk.png')
    batsketImg = pygame.transform.scale(batsketImg, (180, 400))
    bucketImg = pygame.image.load('sprites/basket_milk.png')
    bucketImg = pygame.transform.scale(bucketImg, (180, 400))
    eggImg = pygame.image.load('sprites/egg.png')
    eggImg = pygame.transform.scale(eggImg, (100, 100))
    milkImg = pygame.image.load('sprites/milk-bottle.png')
    milkImg = pygame.transform.scale(milkImg, (100, 100))
    current_angle = 0
    r = 0
    score = 0
    speed = 8
    moving_range = moving_range_easy
    objects_list = objects_easy

    class egg:
        is_egg = 1
        x_center, y_center = random.choice(moving_range_easy), 50

    class basket(pygame.sprite.Sprite):
        state = 'egg'
        x_center, y_center = SCREEN_WIDTH // 2, SCREEN_HEIGHT
        rotate_stack = 0

        def change_state(self, state):
            if self.state == state:
                return
            self.rotate_stack = 36
            self.state = state
            MyGame.current_angle = 0 if (MyGame.current_angle // 180) % 2 == 0 else 180
            MyGame.r = 10
            # MyGame.batsketImg = pygame.transform.rotate(MyGame.batsketImg, 180)

        def rotate_animation(self):
            # if self.rotate_stack==0:
            #     return
            # self.rotate_stack -=1
            MyGame.batsketImg = pygame.transform.rotate(MyGame.bucketImg, MyGame.current_angle)

    def if_in_basket(self):
        cond1 = self.egg.y_center >= self.basket.y_center - 200
        cond2 = self.basket.x_center - 100 <= self.egg.x_center <= self.basket.x_center + 100
        cond3 = self.egg.is_egg == (self.basket.state == 'egg')
        return cond1 and cond2 and cond3

    def move_basket(self, key_pressed_is):
        org = self.basket.x_center
        if key_pressed_is[pygame.K_LEFT]:
            self.basket.x_center -= 10
        elif key_pressed_is[pygame.K_RIGHT]:
            self.basket.x_center += 10
        if self.basket.x_center > 1180 or self.basket.x_center < 100:
            self.basket.x_center = org


def screen_text(text, color, center):
    text1 = font.render(text, True, color)
    textRect1 = text1.get_rect()
    textRect1.center = center
    screen.blit(text1, textRect1)


def play2():
    global state_game_2
    screen.blit(bg_image_resized, (0, 0))
    if MyGame.egg.is_egg:
        screen.blit(MyGame.eggImg, MyGame.eggImg.get_rect(center=(MyGame.egg.x_center, MyGame.egg.y_center)))
    else:
        screen.blit(MyGame.milkImg, MyGame.milkImg.get_rect(center=(MyGame.egg.x_center, MyGame.egg.y_center)))
    screen.blit(MyGame.batsketImg, MyGame.batsketImg.get_rect(center=(MyGame.basket.x_center, MyGame.basket.y_center)))
    screen_text(f'Score: {MyGame.score}', (56, 83, 153), (150, 50))

    # key_pressed_is = pygame.key.get_pressed()
    # MyGame.move_basket(MyGame, key_pressed_is)

    MyGame.egg.y_center += MyGame.speed
    if MyGame.if_in_basket(MyGame):
        MyGame.egg.x_center, MyGame.egg.y_center = random.choice(MyGame.moving_range), 50
        MyGame.egg.is_egg = random.choice(MyGame.objects_list)
        MyGame.score += 1
    elif MyGame.egg.y_center >= 900:
        state_game_2 = 'over2'

    MyGame.current_angle += MyGame.r
    if MyGame.current_angle % 180 == 0:
        MyGame.r = 0
    MyGame.basket.rotate_animation(MyGame.basket)


def need_help():
    global screen
    pause = True

    popup_width, popup_height = 1000, 300
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 255))  # set alpha to 0
    font_popup = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    text_surface = font_popup.render("How to Play", True, (255, 99, 71))
    text_rect = text_surface.get_rect()
    text_rect.centerx = popup_surface.get_rect().centerx
    text_rect.top = 20
    popup_surface.blit(text_surface, text_rect)

    desc_text = "Collect eggs with basket, collect milk with large bottle"
    desc_surface = font_popup_text.render(desc_text, True, FONT_COLOR)
    desc_rect = desc_surface.get_rect()
    desc_rect.centerx = popup_surface.get_rect().centerx
    desc_rect.top = 75
    popup_surface.blit(desc_surface, desc_rect)

    option0_text = "To move container - move palm left or right"
    option0_surface = font_popup_text.render(option0_text, True, DEFAULT_COLOR)
    option0_rect = option0_surface.get_rect()
    option0_rect.centerx = popup_surface.get_rect().centerx
    option0_rect.top = 125
    popup_surface.blit(option0_surface, option0_rect)

    option1_text = "To convert between bottle and basket - rotate palm"
    option1_surface = font_popup_text.render(option1_text, True, DEFAULT_COLOR)
    option1_rect = option1_surface.get_rect()
    option1_rect.centerx = popup_surface.get_rect().centerx
    option1_rect.top = 175
    popup_surface.blit(option1_surface, option1_rect)

    option2_text = "Make a fist to close this window"
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


def over2():
    screen.fill(WHITE_COLOR)
    text1 = font.render(f'Your Score: {MyGame.score}', True, (56, 83, 153))
    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50)
    text = font.render("Game Over", True, (255, 99, 71))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    screen.blit(text, textRect)
    screen.blit(text1, textRect1)


def game2(home_screen, home_font, home_clock):
    global state_game_2, screen, font, clock
    screen = home_screen
    font = home_font
    clock = home_clock
    exit = 0
    is_first_time = True
    selection = 0

    while True:
        if state_game_2 == 'play2':
            play2()
        if state_game_2 == 'over2':
            over2()
            replay_or_return(selection, screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selection = (selection + 1) % 2
                        replay_or_return(selection, screen)
                    elif event.key == pygame.K_UP:
                        selection = (selection - 1) % 2
                        replay_or_return(selection, screen)
                    elif event.key == pygame.K_RETURN:
                        if selection == 0:
                            state_game_2 = 'play2'
                            MyGame.score = 0
                            MyGame.egg.x_center, MyGame.egg.y_center = random.choice(moving_range_easy), 50

                        else:
                            exit = 1

        if 8 <= MyGame.score <= 15:
            MyGame.objects_list = objects_med
        elif MyGame.score >= 16:
            MyGame.speed = speed_hard
            MyGame.moving_range = moving_range_hard

        if is_first_time:
            need_help()
            is_first_time = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    exit = 1
                if state_game_2 == 'play2':
                    if event.key == pygame.K_z:
                        if MyGame.basket.state == 'milk':
                            MyGame.basket.change_state(MyGame.basket, state='egg')
                        else:
                            MyGame.basket.change_state(MyGame.basket, state='milk')
                    elif event.key == pygame.K_LEFT:
                        if MyGame.basket.x_center > min(MyGame.moving_range):
                            MyGame.basket.x_center -= 200
                    elif event.key == pygame.K_RIGHT:
                        if MyGame.basket.x_center < max(MyGame.moving_range):
                            MyGame.basket.x_center += 200
                    elif event.key == pygame.K_p:
                        if paused(screen) == 0:
                            continue
                        else:
                            exit = 1
                    elif event.key == pygame.K_h:
                        need_help()

            if event.type == pygame.QUIT:
                exit = 1
                # pygame.quit()
                # sys.exit()
        if exit == 1:
            state_game_2 = 'play2'
            MyGame.score = 0
            MyGame.egg.x_center, MyGame.egg.y_center = random.choice(moving_range_easy), 50
            break

        pygame.display.flip()
        clock.tick(60)

    return 'home'


if __name__ == "__main__":
    game2()
