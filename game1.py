import pygame
import random
import math
import os

pygame.init()
pygame.font.init()
pygame.font.get_init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
font = pygame.font.SysFont('', 70)

# Color setting visualization
# hard_color_code_list = [rgb(230, 57, 70), rgb(17, 138, 178), rgb(6, 214, 160),
#                         rgb(255,255,255),rgb(64, 61, 57), rgb(218,112,214), rgb(255,127,80)]

# Setting for border shape
border_color = (0, 0, 0)
border_width = 2

# Setting level
easy_color_list = ['red', 'blue', 'green']
easy_color_code_list = [(230, 57, 70), (17, 138, 178), (6, 214, 160)]
easy_shape_list = ['circle', 'square', 'triangle']

medium_color_list = ['red', 'blue', 'green', 'white', 'black']
medium_color_code_list = [(230, 57, 70), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57)]
medium_shape_lst = ['circle', 'square', 'triangle', 'oval']

hard_color_list = ['red', 'blue', 'green', 'white', 'black', 'purple', 'orange']
hard_color_code_list = [(230, 57, 70), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57), (218, 112, 214),
                        (255, 127, 80)]
hard_shape_list = ['circle', 'square', 'triangle', 'oval', 'star', 'diamond']

state = 'play'

# Setting background
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


class MyGame:
    def __init__(self):
        self.answer_list = None
        self.correct_answer = None
        self.score = 0
        self.num_answer = 3
        self.shape_width = 175
        self.color_list = easy_color_list
        self.color_code_list = easy_color_code_list
        self.shape_list = easy_shape_list

        self.random_answers()
        self.selection = 0

    def update(self, num_answer):
        self.num_answer = num_answer
        if num_answer == 3:
            self.color_list = easy_color_list
            self.color_code_list = easy_color_code_list
            self.shape_list = easy_shape_list
        elif num_answer == 4:
            self.color_list = medium_color_list
            self.color_code_list = medium_color_code_list
            self.shape_list = medium_shape_lst
        elif num_answer == 5:
            self.color_list = hard_color_list
            self.color_code_list = hard_color_code_list
            self.shape_list = hard_shape_list

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

    if shape == 'oval':
        pygame.draw.ellipse(screen, color,
                            pygame.Rect(shape_rect[0] + 50, shape_rect[1], shape_width - 100, shape_width))
        pygame.draw.ellipse(screen, border_color,
                            pygame.Rect(shape_rect[0] + 50, shape_rect[1], shape_width - 100, shape_width),
                            border_width)

    if shape == 'square':
        pygame.draw.rect(screen, color, pygame.Rect(shape_rect[0], shape_rect[1], shape_width, shape_width))
        pygame.draw.rect(screen, border_color, pygame.Rect(shape_rect[0], shape_rect[1], shape_width, shape_width),
                         border_width)

    if shape == 'triangle':
        triangle_points = [[(shape_rect[0] + shape_rect[2]) // 2, shape_rect[1]], [shape_rect[0], shape_rect[3]],
                           [shape_rect[2], shape_rect[3]]]
        pygame.draw.polygon(screen, color, triangle_points)
        pygame.draw.polygon(screen, border_color, triangle_points, border_width)

    if shape == 'circle':
        circle_points = [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2]
        pygame.draw.circle(screen, color, circle_points, shape_width // 2)
        pygame.draw.circle(screen, border_color,
                           [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2],
                           shape_width // 2,
                           border_width)

    if shape == 'star':
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

    if shape == 'diamond':
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


def play(my_game):
    color_map = {my_game.color_code_list[i]: my_game.color_list[i] for i in range(len(my_game.color_code_list))}
    screen.blit(bg_image_resized, (0, 0))
    screen_text(f'Score: {my_game.score}', (50, 50, 50), (150, 50))
    screen_text(f'Choose the {color_map[my_game.correct_answer[0]]} {my_game.correct_answer[1]}', (50, 50, 50),
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


def over(my_game):
    screen.fill((255, 255, 255))
    screen_text(f'Your Score: {my_game.score}', (56, 83, 153), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    # Reset to level 3
    my_game.update(3) 
    my_game.random_answers()


def game1():
    global state
    is_running = True
    my_game_1 = MyGame()

    while True:
        if state == 'play':
            play(my_game_1)
        if state == 'over':
            over(my_game_1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = 'play'
                    my_game_1.score = 0
                if state == 'play':
                    if event.key == pygame.K_RETURN:
                        if my_game_1.selection == my_game_1.answer_list.index(my_game_1.correct_answer):
                            my_game_1.score += 1
                            if 8 <= my_game_1.score <= 15 and my_game_1.num_answer != 4:
                                my_game_1.update(4)
                            elif my_game_1.score > 15 and my_game_1.num_answer != 5:
                                my_game_1.update(5)
                            my_game_1.random_answers()
                        else:
                            state = 'over'
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        my_game_1.switch_selection(event.key)
                    if event.key == pygame.K_b:
                        is_running = False
            if event.type == pygame.QUIT:
                is_running = False
        if not is_running:
            break
        pygame.display.flip()
        clock.tick(60)
    return 'home'


if __name__ == "__main__":
    game1()
    