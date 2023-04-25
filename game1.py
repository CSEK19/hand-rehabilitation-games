import pygame
import random
import math
import os
from utils.constants import *
from utils.functions import replay_or_return, paused

# Color setting visualization
# hard_color_code_list = [rgb(230, 57, 70), rgb(17, 138, 178), rgb(6, 214, 160),
#                         rgb(255,255,255),rgb(64, 61, 57), rgb(218,112,214), rgb(255,127,80)]

# Setting for border shape
border_color = (0, 0, 0)
border_width = 2

# Setting for state
state_game_1 = 'play1'

# Setting background
screen = None
font = None
clock = None
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
enable_Vie_language = False

class MyGame:
    def __init__(self, enable_Vie_language):
        self.answer_list = None
        self.correct_answer = None
        self.score = 0
        self.num_answer = 3
        self.shape_width = 175
        self.color_code_list = EASY_COLOR_CODE_LIST
        if not enable_Vie_language:
            self.color_list = EASY_COLOR_LIST
            self.shape_list = EASY_SHAPE_LIST
        else:
            self.color_list = VIE_EASY_COLOR_LIST
            self.shape_list = VIE_EASY_SHAPE_LIST
        self.random_answers()
        self.selection = 0

    def update(self, num_answer):
        self.num_answer = num_answer
        if not enable_Vie_language:
            if num_answer == 3:
                self.color_list = EASY_COLOR_LIST
                self.color_code_list = EASY_COLOR_CODE_LIST
                self.shape_list = EASY_SHAPE_LIST
            elif num_answer == 4:
                self.color_list = MEDIUM_COLOR_LIST
                self.color_code_list = MEDIUM_COLOR_CODE_LIST
                self.shape_list = MEDIUM_SHAPE_LIST
            elif num_answer == 5:
                self.color_list = HARD_COLOR_LIST
                self.color_code_list = HARD_COLOR_CODE_LIST
                self.shape_list = HARD_SHAPE_LIST
        else:
            if num_answer == 3:
                self.color_list = VIE_EASY_COLOR_LIST
                self.color_code_list = EASY_COLOR_CODE_LIST
                self.shape_list = VIE_EASY_SHAPE_LIST
            elif num_answer == 4:
                self.color_list = VIE_MEDIUM_COLOR_LIST
                self.color_code_list = MEDIUM_COLOR_CODE_LIST
                self.shape_list = VIE_MEDIUM_SHAPE_LIST
            elif num_answer == 5:
                self.color_list = VIE_HARD_COLOR_LIST
                self.color_code_list = HARD_COLOR_CODE_LIST
                self.shape_list = VIE_HARD_SHAPE_LIST

    def random_answers(self):
        self.answer_list = [(random.choice(self.color_code_list), random.choice(self.shape_list)) for _ in
                            range(self.num_answer)]
        while len(set(self.answer_list)) < self.num_answer:
            self.answer_list = [(random.choice(self.color_code_list), random.choice(self.shape_list)) for _ in
                                range(self.num_answer)]
        self.correct_answer = random.choice(self.answer_list)

    def switch_selection(self, key):
        if key == pygame.K_RIGHT:
            self.selection = self.selection + 1 if self.selection < self.num_answer - 1 else 0
        if key == pygame.K_LEFT:
            self.selection = self.selection - 1 if self.selection > 0 else self.num_answer - 1


def draw_shape_color(color, shape, index, num_answer, shape_width):
    gap_width = shape_width // 2
    total_width = shape_width * num_answer + gap_width * (num_answer - 1)
    left = ((SCREEN_WIDTH - total_width) // 2) + (shape_width + gap_width) * index
    top = SCREEN_HEIGHT * 2 // 3
    shape_rect = [left, top, left + shape_width, top + shape_width]

    if shape == 'oval' or shape == 'bầu dục':
        pygame.draw.ellipse(screen, color,
                            pygame.Rect(shape_rect[0] + 50, shape_rect[1], shape_width - 100, shape_width))
        pygame.draw.ellipse(screen, border_color,
                            pygame.Rect(shape_rect[0] + 50, shape_rect[1], shape_width - 100, shape_width),
                            border_width)

    if shape == 'square' or shape == 'vuông':
        pygame.draw.rect(screen, color, pygame.Rect(shape_rect[0], shape_rect[1], shape_width, shape_width))
        pygame.draw.rect(screen, border_color, pygame.Rect(shape_rect[0], shape_rect[1], shape_width, shape_width),
                         border_width)

    if shape == 'triangle' or shape == 'tam giác':
        triangle_points = [[(shape_rect[0] + shape_rect[2]) // 2, shape_rect[1]], [shape_rect[0], shape_rect[3]],
                           [shape_rect[2], shape_rect[3]]]
        pygame.draw.polygon(screen, color, triangle_points)
        pygame.draw.polygon(screen, border_color, triangle_points, border_width)

    if shape == 'circle' or shape == 'tròn':
        circle_points = [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2]
        pygame.draw.circle(screen, color, circle_points, shape_width // 2)
        pygame.draw.circle(screen, border_color,
                           [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2],
                           shape_width // 2,
                           border_width)

    if shape == 'star' or shape == 'ngôi sao':
        left, top, right, bottom = shape_rect
        width = right - left
        height = bottom - top
        centre_coord = (left + width // 2, top + height // 2)
        radius = min(width, height) * 0.5
        star_points = []
        for i in range(10):
            angle = i * 2 * math.pi / 10
            if i % 2 == 0:
                x = centre_coord[0] + radius * math.cos(angle - math.pi / 2)
                y = centre_coord[1] + radius * math.sin(angle - math.pi / 2)
            else:
                x = centre_coord[0] + radius / 2 * math.cos(angle - math.pi / 2)
                y = centre_coord[1] + radius / 2 * math.sin(angle - math.pi / 2)
            star_points.append((int(x), int(y)))
        star_points.reverse()
        pygame.draw.polygon(screen, color, star_points)
        pygame.draw.polygon(screen, border_color, star_points, border_width)

    if shape == 'diamond'or shape == 'kim cương' :
        diamond_points = [(shape_rect[0] + shape_width // 2, shape_rect[1]),  # top point
                          (shape_rect[0] + shape_width, shape_rect[1] + shape_width // 2),  # right point
                          (shape_rect[0] + shape_width // 2, shape_rect[1] + shape_width),  # bottom point
                          (shape_rect[0], shape_rect[1] + shape_width // 2)]  # left point

        # Draw the filled diamond
        pygame.draw.polygon(screen, color, diamond_points)
        # Draw the diamond border
        pygame.draw.polygon(screen, border_color, diamond_points, border_width)


def draw_selection(color, index, num_answer, shape_width):
    gap_width = shape_width // 2
    total_width = shape_width * num_answer + gap_width * (num_answer - 1)
    left = ((SCREEN_WIDTH - total_width) // 2) + (shape_width + gap_width) * index
    top = SCREEN_HEIGHT * 2 // 3
    shape_rect = [left, top, left + shape_width, top + shape_width]

    pygame.draw.rect(screen, color,
                     pygame.Rect(shape_rect[0] - 20, shape_rect[1] - 20, shape_width + 40, shape_width + 40), 5)


def screen_text(text, color, center):
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = center
    screen.blit(text_render, text_rect)
    return text_rect


def play(my_game):
    global title_rect
    color_map = {my_game.color_code_list[i]: my_game.color_list[i] for i in range(len(my_game.color_code_list))}
    screen.blit(bg_image_resized, (0, 0))
    if not enable_Vie_language:
        screen_text(f'Score: {my_game.score}', (50, 50, 50), (150, 50))
        screen_text(f'Choose the {color_map[my_game.correct_answer[0]]} {my_game.correct_answer[1]}',
                                (50, 50, 50),
                                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    else:
        screen_text(f'Điểm: {my_game.score}', (50, 50, 50), (150, 50))
        screen_text(f'Chọn hình {my_game.correct_answer[1]} màu {color_map[my_game.correct_answer[0]]}',
                                (50, 50, 50),
                                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    shape_width = my_game.shape_width
    selection = my_game.selection
    if my_game.num_answer == 3:
        draw_shape_color(my_game.answer_list[0][0], my_game.answer_list[0][1], 0, 3, shape_width)
        draw_shape_color(my_game.answer_list[1][0], my_game.answer_list[1][1], 1, 3, shape_width)
        draw_shape_color(my_game.answer_list[2][0], my_game.answer_list[2][1], 2, 3, shape_width)
        draw_selection((56, 83, 153), selection, 3, shape_width)
    elif my_game.num_answer == 4:
        draw_shape_color(my_game.answer_list[0][0], my_game.answer_list[0][1], 0, 4, shape_width)
        draw_shape_color(my_game.answer_list[1][0], my_game.answer_list[1][1], 1, 4, shape_width)
        draw_shape_color(my_game.answer_list[2][0], my_game.answer_list[2][1], 2, 4, shape_width)
        draw_shape_color(my_game.answer_list[3][0], my_game.answer_list[3][1], 3, 4, shape_width)
        draw_selection((56, 83, 153), selection, 4, shape_width)
    elif my_game.num_answer == 5:
        draw_shape_color(my_game.answer_list[0][0], my_game.answer_list[0][1], 0, 5, shape_width)
        draw_shape_color(my_game.answer_list[1][0], my_game.answer_list[1][1], 1, 5, shape_width)
        draw_shape_color(my_game.answer_list[2][0], my_game.answer_list[2][1], 2, 5, shape_width)
        draw_shape_color(my_game.answer_list[3][0], my_game.answer_list[3][1], 3, 5, shape_width)
        draw_shape_color(my_game.answer_list[4][0], my_game.answer_list[4][1], 4, 5, shape_width)
        draw_selection((56, 83, 153), selection, 5, shape_width)


def need_help():
    popup_width, popup_height = 800, 300
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 255))  # set alpha to 0
    font_popup = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    if not enable_Vie_language:
        help_text = 'How to Play'
        desc_text = "Select the right shape following the description"
        option0_text = "To change selection - move palm left or right"
        option1_text = "To select - make a fist"
        option2_text = "Make a fist to close this window"
    else:
        help_text = 'Cách chơi'
        desc_text = "Chọn hình đúng theo mô tả"
        option0_text = "Để thay đổi lựa chọn - lắc tay trái/phải"
        option1_text = "Để chọn - nắm chặt bàn tay"
        option2_text = "Nắm chặt bàn tay để đóng cửa sổ này"

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def over1(score):
    screen.fill(WHITE_COLOR)
    if not enable_Vie_language:
        text = font.render("Game Over", True, (255, 99, 71))
        text1 = font.render(f'Your Score: {score}', True, (56, 83, 153))
    else:
        text = font.render("Trò chơi kết thúc", True, (255, 99, 71))
        text1 = font.render(f'Điểm của bạn: {score}', True, (56, 83, 153))
    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    screen.blit(text, textRect)
    screen.blit(text1, textRect1)


def game1(home_screen, home_font, home_clock, language):
    global state_game_1, screen, font, clock, enable_Vie_language
    screen = home_screen
    font = home_font
    clock = home_clock
    exit = False
    is_first_time = True
    selection = 0
    enable_Vie_language = language
    my_game_1 = MyGame(enable_Vie_language)


    while True:
        if state_game_1 == 'play1':
            play(my_game_1)
        if state_game_1 == 'over':
            over1(my_game_1.score)
            replay_or_return(selection, screen, enable_Vie_language)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selection = (selection + 1) % 2
                        replay_or_return(selection, screen, enable_Vie_language)
                    elif event.key == pygame.K_UP:
                        selection = (selection - 1) % 2
                        replay_or_return(selection, screen, enable_Vie_language)
                    elif event.key == pygame.K_RETURN:
                        if selection == 0:
                            state_game_1 = 'play1'
                            my_game_1.score = 0
                            my_game_1.update(3)
                            my_game_1.random_answers()
                        else:
                            exit = 1

        if (is_first_time):
            need_help()
            is_first_time = False
        


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused(screen, enable_Vie_language) == 1:
                        exit = True
                if state_game_1 == 'play1':
                    if event.key == pygame.K_RETURN:
                        if my_game_1.selection == my_game_1.answer_list.index(my_game_1.correct_answer):
                            my_game_1.score += 1
                            if 8 <= my_game_1.score <= 15 and my_game_1.num_answer != 4:
                                my_game_1.update(4)
                            elif my_game_1.score >= 16 and my_game_1.num_answer != 5:
                                my_game_1.update(5)
                            my_game_1.random_answers()
                        else:
                            state_game_1 = 'over'
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        my_game_1.switch_selection(event.key)
                    elif event.key == pygame.K_b:
                        exit = True
                    elif event.key == pygame.K_h:
                        need_help()
                        play(my_game_1)
            if event.type == pygame.QUIT:
                exit = True
        if exit:
            state_game_1 = 'play1'
            my_game_1.score = 0
            break

        pygame.display.flip()
        clock.tick(60)

    return 'home'


if __name__ == "__main__":
    game1()
