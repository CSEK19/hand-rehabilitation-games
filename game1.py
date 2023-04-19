import pygame, os
import random
import math
pygame.init()
pygame.font.init()
pygame.font.get_init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
font = pygame.font.SysFont('', 50)

# colorLst = ['red', 'blue', 'green', 'yellow', 'black']
# colorLst_code = [rgb(239, 71, 111), rgb(17, 138, 178), rgb(6, 214, 160), rgb(255, 209, 102),rgb(64, 61, 57)]
# shapeLst = ['rectangle', 'triangle', 'circle', 'oval']


# easy_colorLst = ['red', 'blue', 'green']
# easy_colorLst_code = [rgb(239, 71, 111), rgb(17, 138, 178), rgb(6, 214, 160)]
# easy_shapeLst = ['circle', 'square', 'triangle']

# medium_colorLst = ['red', 'blue', 'green', 'white', 'black']
# medium_colorLst_code = [rgb(239, 71, 111), rgb(17, 138, 178), rgb(6, 214, 160), rgb(255,255,255),rgb(64, 61, 57)]
# medium_shapeLst = ['circle', 'square', 'triangle', 'oval']


# hard_colorLst = ['red', 'blue', 'green', 'white', 'black']
# hard_colorLst_code = [rgb(239, 71, 111), rgb(17, 138, 178), rgb(6, 214, 160), rgb(255,255,255),rgb(64, 61, 57), rgb(218,112,214), rgb(255,127,80)]
# hard_shapeLst = ['circle', 'square', 'triangle', 'oval', 'star', 'diamond']


easy_colorLst = ['red', 'blue', 'green']
easy_colorLst_code = [(239, 71, 111), (17, 138, 178), (6, 214, 160)]
easy_shapeLst = ['circle', 'square', 'triangle']

medium_colorLst = ['red', 'blue', 'green', 'white', 'black']
medium_colorLst_code = [(239, 71, 111), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57)]
medium_shapeLst = ['circle', 'square', 'triangle', 'oval']

hard_colorLst = ['red', 'blue', 'green', 'white', 'black']
hard_colorLst_code = [(239, 71, 111), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57), (218, 112, 214), (255, 127, 80)]
hard_shapeLst = ['circle', 'square', 'triangle', 'oval', 'star', 'diamond']


state = 'play'


screen = pygame.display.set_mode((screenWidth, screenHeight))
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (screenWidth, screenHeight))


class MyGame: 

    def __init__(self):
        self.score = 0
        self.num_answer = 3
        self.shapeWidth = 150
        self.colorLst_code = easy_colorLst_code
        self.colorLst = easy_colorLst
        self.shapeLst = easy_shapeLst
        
        self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        while len(set(self.answerLst))<self.num_answer:
            self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        
        self.answer = random.choice(self.answerLst)
        self.selection = 0

    def update(self, num_answer):
        self.num_answer = num_answer
        if(num_answer == 3):
            self.colorLst_code = easy_colorLst_code
            self.colorLst = easy_colorLst
            self.shapeLst = easy_shapeLst
        if(num_answer == 4):
            self.colorLst_code = medium_colorLst_code
            self.colorLst = medium_colorLst
            self.shapeLst = medium_shapeLst
        elif(num_answer == 5):
            self.colorLst_code = hard_colorLst_code
            self.colorLst = hard_colorLst
            self.shapeLst = hard_shapeLst

        
        self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        while len(set(self.answerLst))<self.num_answer:
            self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        
        self.answer = random.choice(self.answerLst)
        self.selection = 0



    def random_answers(self):
        self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        while len(set(self.answerLst))<self.num_answer:
            self.answerLst = [(random.choice(self.colorLst_code), random.choice(self.shapeLst)) for _ in range(self.num_answer)]
        self.answer = random.choice(self.answerLst)

    
    def switch_selection(self, key):
        if key == pygame.K_RIGHT:
            self.selection = self.selection+1 if self.selection<self.num_answer-1 else 0
        if key == pygame.K_LEFT:
            self.selection = self.selection-1 if self.selection>0 else self.num_answer-1


def draw_shape_color(color, shape, index, num_answer, my_game):
    shapeWidth = my_game.shapeWidth
    gapWidth = shapeWidth // 2  # set gap width to half the shape width
    totalWidth = shapeWidth * num_answer + gapWidth * (num_answer - 1)
    left = (screenWidth - totalWidth) // 2 + (shapeWidth + gapWidth) * index
    top = screenHeight * 2 // 3
    ltrb = [left, top, left + shapeWidth, top + shapeWidth]
     


    if shape == 'oval':
        pygame.draw.ellipse(screen, color, pygame.Rect(ltrb[0]+50, ltrb[1], shapeWidth-100, shapeWidth))

    if shape == 'square':
        pygame.draw.rect(screen, color, pygame.Rect(ltrb[0], ltrb[1], shapeWidth, shapeWidth))
    
    if shape == 'triangle':
        pygame.draw.polygon(screen, color, [[(ltrb[0]+ltrb[2])//2, ltrb[1]], [ltrb[0], ltrb[3]], [ltrb[2], ltrb[3]]])
    
    if shape == 'circle':
        pygame.draw.circle(screen, color, [(ltrb[0]+ltrb[2])//2, (ltrb[1]+ltrb[3])//2], shapeWidth//2)

    if shape == 'star':
        left, top, right, bottom = ltrb

        center_x = (left + right) / 2
        center_y = (top + bottom) / 2
        width = right - left
        height = bottom - top
        heart_size = min(width, height) * 0.8

        # Calculate the coordinates of the top left and bottom right corners of the heart
        heart_tl_x = center_x - heart_size / 2
        heart_tl_y = center_y - heart_size / 2
        heart_br_x = center_x + heart_size / 2
        heart_br_y = center_y + heart_size / 2

        cp1_x = heart_tl_x + heart_size / 4
        cp1_y = heart_tl_y - heart_size / 4
        cp2_x = heart_br_x - heart_size / 4
        cp2_y = heart_tl_y - heart_size / 4
        cp3_x = heart_br_x + heart_size / 4
        cp3_y = heart_tl_y + heart_size / 4
        cp4_x = heart_tl_x - heart_size / 4
        cp4_y = heart_tl_y + heart_size / 4

        pygame.draw.lines(screen, color, False, [(cp1_x, cp1_y), (center_x, heart_tl_y), (cp2_x, cp2_y)], 5)
        pygame.draw.lines(screen, color, False, [(cp2_x, cp2_y), (heart_br_x, center_y), (cp3_x, cp3_y)], 5)
        pygame.draw.lines(screen, color, False, [(cp3_x, cp3_y), (center_x, heart_br_y), (cp4_x, cp4_y)], 5)
        pygame.draw.lines(screen, color, False, [(cp4_x, cp4_y), (heart_tl_x, center_y), (cp1_x, cp1_y)], 5)




    
    if shape == 'diamond':
        pygame.draw.polygon(screen, color, [[ltrb[0] + shapeWidth//2, ltrb[1]], [ltrb[0], ltrb[1] + shapeWidth//2], [ltrb[0] + shapeWidth//2, ltrb[1] + shapeWidth], [ltrb[0] + shapeWidth, ltrb[1] + shapeWidth//2]])


def draw_selection(color, index, num_answer, my_game):
    shapeWidth = my_game.shapeWidth
    totalWidth = shapeWidth * num_answer + (num_answer - 1) * shapeWidth // 2
    left = (screenWidth - totalWidth) // 2 + (shapeWidth * 3 // 2) * index
    top = screenHeight * 2 // 3
    ltrb = [left, top, left + shapeWidth, top + shapeWidth]

    pygame.draw.rect(screen, color, pygame.Rect(ltrb[0]-20, ltrb[1]-20, shapeWidth+40, shapeWidth+40),5)

def screen_text(text, color, center):
    text1 = font.render(text, True,color)
    textRect1 = text1.get_rect()
    textRect1.center = center
    screen.blit(text1, textRect1)

def play(my_game):
    color_map = {my_game.colorLst_code[i]: my_game.colorLst[i] for i in range(len(my_game.colorLst_code))}
    screen.blit(bg_image_resized, (0, 0))
    screen_text(f'SCORE: {my_game.score}', (56,83,153), (100, 50))
    screen_text(f'Choose the {color_map[my_game.answer[0]]} {my_game.answer[1]}', (56,83,153), (screenWidth//2, screenHeight//3))
    if my_game.score < 1:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 3, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 3, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 3, my_game)
        draw_selection((56,83,153), my_game.selection, num_answer=3, my_game=my_game)

    elif my_game.score > 1 and my_game.score < 2:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 3, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 3, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 3, my_game)
        draw_shape_color(my_game.answerLst[3][0], my_game.answerLst[3][1], 3, 4, my_game)
        draw_selection((56,83,153), my_game.selection, num_answer=4, my_game=my_game)
    else:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 3, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 3, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 3, my_game)
        draw_shape_color(my_game.answerLst[3][0], my_game.answerLst[3][1], 3, 5, my_game)
        draw_shape_color(my_game.answerLst[3][0], my_game.answerLst[3][1], 4, 5, my_game)

        draw_selection((56,83,153), my_game.selection, num_answer=5, my_game=my_game)

def over(my_game):
    screen.fill(((255,255,255)))
    text1 = font.render(f'Your Score: {my_game.score}', True,(56,83,153))
    textRect1 = text1.get_rect()
    textRect1.center = (screenWidth//2, screenHeight//3)
    screen.blit(text1, textRect1)
    my_game.update(0)

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
                        if my_game_1.selection == my_game_1.answerLst.index(my_game_1.answer):
                            my_game_1.score +=1
                            my_game_1.random_answers()
                            if(my_game_1.score >= 1):
                                my_game_1.update(4)
                            elif (my_game_1.score >= 2):
                                my_game_1.update(5)

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