import pygame, os
import random

pygame.init()
pygame.font.init()
pygame.font.get_init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
font = pygame.font.SysFont('', 50)

state = 'play2'

screen = pygame.display.set_mode((screenWidth, screenHeight))
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (screenWidth, screenHeight))

screen = pygame.display.set_mode((screenWidth, screenHeight))

# easy
moving_range_easy = [440, 640, 840]
objects_easy = [1]
speed_easy = 2

# easy
objects_med = [0, 1]

# hard
moving_range_hard = [240, 440, 640, 840, 1040]
speed_hard = 3


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
    speed = speed_easy
    moving_range = moving_range_easy
    objects_list = objects_easy

    class egg:
        is_egg = 1
        x_center, y_center = random.choice(moving_range_easy), 50

    class basket(pygame.sprite.Sprite):
        state = 'egg'
        x_center, y_center = screenWidth // 2, screenHeight
        rotate_stack = 0

        def change_state(self, state):
            if self.state == state:
                return
            self.rotate_stack = 36
            self.state = state
            MyGame.current_angle = 0 if (MyGame.current_angle // 180) % 2 == 0 else 180
            MyGame.r = 5
            # MyGame.batsketImg = pygame.transform.rotate(MyGame.batsketImg, 180)

        def rotate_animation(self):
            # if self.rotate_stack==0:
            #     return
            # self.rotate_stack -=1
            MyGame.batsketImg = pygame.transform.rotate(MyGame.bucketImg, MyGame.current_angle)

    def if_in_basket(self):
        cond1 = self.egg.y_center >= self.basket.y_center - 200
        cond2 = self.basket.x_center - 100 <= self.egg.x_center and self.egg.x_center <= self.basket.x_center + 100
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
    global state
    screen.fill(((255, 255, 255)))
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
        state = 'over2'

    MyGame.current_angle += MyGame.r
    if MyGame.current_angle % 180 == 0:
        MyGame.r = 0
    MyGame.basket.rotate_animation(MyGame.basket)


def over2():
    screen.fill(((255, 255, 255)))
    text1 = font.render(f'Your Score: {MyGame.score}', True, (56, 83, 153))
    textRect1 = text1.get_rect()
    textRect1.center = (screenWidth // 2, screenHeight // 3)
    screen.blit(text1, textRect1)


def game2():
    global state
    exit = 0

    while True:

        if state == 'play2':
            play2()
        if state == 'over2':
            over2()

        if MyGame.score >= 8:
            MyGame.objects_list = objects_med
        if MyGame.score >= 16:
            MyGame.speed = speed_hard
            MyGame.moving_range = moving_range_hard

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = 'play2'
                    MyGame.moving_range = moving_range_easy
                    MyGame.speed = speed_easy
                    MyGame.objects_list = objects_easy
                    MyGame.score = 0
                    MyGame.egg.x_center, MyGame.egg.y_center = random.choice(MyGame.moving_range), 50
                if event.key == pygame.K_b:
                    exit = 1
                if state == 'play2':
                    if event.key == pygame.K_z:
                        MyGame.basket.change_state(MyGame.basket, state='egg')
                    if event.key == pygame.K_x:
                        MyGame.basket.change_state(MyGame.basket, state='milk')
                    if event.key == pygame.K_LEFT:
                        if MyGame.basket.x_center > min(MyGame.moving_range):
                            MyGame.basket.x_center -= 200
                    if event.key == pygame.K_RIGHT:
                        if MyGame.basket.x_center < max(MyGame.moving_range):
                            MyGame.basket.x_center += 200

            if event.type == pygame.QUIT:
                exit = 1
                # pygame.quit()
                # sys.exit()
        if exit == 1:
            break
        pygame.display.flip()
        clock.tick(60)
    return 'home'


if __name__ == "__main__":
    game2()
