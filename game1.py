import pygame, os
import random
import math
pygame.init()
pygame.font.init()
pygame.font.get_init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
font = pygame.font.SysFont('', 70)


# hard_colorLst = ['red', 'blue', 'green', 'white', 'black']
# hard_colorLst_code = [rgb(230, 57, 70), rgb(17, 138, 178), rgb(6, 214, 160), rgb(255,255,255),rgb(64, 61, 57), rgb(218,112,214), rgb(255,127,80)]
# hard_shapeLst = ['circle', 'square', 'triangle', 'oval', 'star', 'diamond']

border_color = (0,0,0)
border_width = 2

easy_colorLst = ['red', 'blue', 'green']
easy_colorLst_code = [(230, 57, 70), (17, 138, 178), (6, 214, 160)]
easy_shapeLst = ['circle', 'square', 'triangle']


medium_colorLst = ['red', 'blue', 'green', 'white', 'black']
medium_colorLst_code = [(230, 57, 70), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57)]
medium_shapeLst = ['circle', 'square', 'triangle', 'oval']

hard_colorLst = ['red', 'blue', 'green', 'white', 'black', 'purple', 'orange']
hard_colorLst_code = [(230, 57, 70), (17, 138, 178), (6, 214, 160), (255, 255, 255), (64, 61, 57), (218, 112, 214), (255, 127, 80)]
hard_shapeLst = ['circle', 'square', 'triangle', 'oval', 'star', 'diamond']


state = 'play'


screen = pygame.display.set_mode((screenWidth, screenHeight))
bg_image = pygame.image.load(os.path.join("sprites", "bg.png"))
bg_image_resized = pygame.transform.scale(bg_image, (screenWidth, screenHeight))


class MyGame: 

    def __init__(self):
        self.score = 0
        self.num_answer = 3
        self.shapeWidth = 175
        self.colorLst = easy_colorLst
        self.colorLst_code = easy_colorLst_code
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
        elif(num_answer == 4):
            self.colorLst_code = medium_colorLst_code
            self.colorLst = medium_colorLst
            self.shapeLst = medium_shapeLst
        elif(num_answer == 5):
            self.colorLst_code = hard_colorLst_code
            self.colorLst = hard_colorLst
            self.shapeLst = hard_shapeLst

        self.random_answers()



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
    gapWidth = shapeWidth // 2 
    totalWidth = shapeWidth * num_answer + gapWidth * (num_answer - 1)
    left = ((screenWidth - totalWidth) // 2) + (shapeWidth + gapWidth) * index
    if my_game.num_answer == 4:
        left -= 0
    elif my_game.num_answer == 5:
        left -= 0


    top = screenHeight * 2 // 3
    ltrb = [left, top, left + shapeWidth, top + shapeWidth]

    if shape == 'oval':
        pygame.draw.ellipse(screen, color, pygame.Rect(ltrb[0]+50, ltrb[1], shapeWidth-100, shapeWidth))
        pygame.draw.ellipse(screen, border_color, pygame.Rect(ltrb[0]+50, ltrb[1], shapeWidth-100, shapeWidth), border_width)



    if shape == 'square':
        pygame.draw.rect(screen, color, pygame.Rect(ltrb[0], ltrb[1], shapeWidth, shapeWidth))
        pygame.draw.rect(screen, border_color, pygame.Rect(ltrb[0], ltrb[1], shapeWidth, shapeWidth), border_width)

    
    if shape == 'triangle':
        triangle_points = [[(ltrb[0]+ltrb[2])//2, ltrb[1]], [ltrb[0], ltrb[3]], [ltrb[2], ltrb[3]]]
        pygame.draw.polygon(screen, color, triangle_points)
        pygame.draw.polygon(screen, border_color, triangle_points, border_width)


        # pygame.draw.polygon(screen, color, [[(ltrb[0]+ltrb[2])//2, ltrb[1]], [ltrb[0], ltrb[3]], [ltrb[2], ltrb[3]]])
    
    if shape == 'circle':
        circle_points = [(ltrb[0]+ltrb[2])//2, (ltrb[1]+ltrb[3])//2]
        pygame.draw.circle(screen, color, circle_points, shapeWidth//2)
        pygame.draw.circle(screen, border_color, [(ltrb[0]+ltrb[2])//2, (ltrb[1]+ltrb[3])//2], shapeWidth//2, border_width) 


        # pygame.draw.circle(screen, color, [(ltrb[0]+ltrb[2])//2, (ltrb[1]+ltrb[3])//2], shapeWidth//2)

    if shape == 'star':
        left, top, right, bottom = ltrb
        width = right - left
        height = bottom - top
        centre_coord = (left + width//2, top + height//2)
        radius = min(width, height) // 2
        star_points = []
        for i in range(10):
            angle = i * 2 * math.pi / 10
            if i % 2 == 0:
                x = centre_coord[0] + radius * math.cos(angle - math.pi/2)
                y = centre_coord[1] + radius * math.sin(angle - math.pi/2)
            else:
                x = centre_coord[0] + radius/2 * math.cos(angle - math.pi/2)
                y = centre_coord[1] + radius/2 * math.sin(angle - math.pi/2)
            star_points.append((int(x), int(y)))
        star_points.reverse()
        pygame.draw.polygon(screen, color, star_points)
        pygame.draw.polygon(screen, border_color, star_points, border_width)





    if shape == 'diamond':
        diamond_points = [(ltrb[0] + shapeWidth//2, ltrb[1]),  # top point
                        (ltrb[0] + shapeWidth, ltrb[1] + shapeWidth//2),  # right point
                        (ltrb[0] + shapeWidth//2, ltrb[1] + shapeWidth),  # bottom point
                        (ltrb[0], ltrb[1] + shapeWidth//2)]  # left point

        # Draw the filled diamond
        pygame.draw.polygon(screen, color, diamond_points)

        # Draw the diamond border
        pygame.draw.polygon(screen, border_color, diamond_points, border_width)



def draw_selection(color, index, num_answer, my_game):
    shapeWidth = my_game.shapeWidth
    gapWidth = shapeWidth // 2 
    totalWidth = shapeWidth * num_answer + gapWidth * (num_answer - 1)
    left = ((screenWidth - totalWidth) // 2) + (shapeWidth + gapWidth) * index
    if my_game.num_answer == 4:
        left += 0
    elif my_game.num_answer == 5:
        left += 0
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
    screen_text(f'Score: {my_game.score}', (50,50,50), (100, 50))
    screen_text(f'Choose the {color_map[my_game.answer[0]]} {my_game.answer[1]}', (50,50,50), (screenWidth//2, screenHeight//3))
    if my_game.num_answer == 3:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 3, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 3, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 3, my_game)
        draw_selection((56,83,153), my_game.selection, num_answer=3, my_game=my_game)
    elif my_game.num_answer == 4:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 4, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 4, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 4, my_game)
        draw_shape_color(my_game.answerLst[3][0], my_game.answerLst[3][1], 3, 4, my_game)
        draw_selection((56,83,153), my_game.selection, num_answer=4, my_game=my_game)
    elif my_game.num_answer == 5:
        draw_shape_color(my_game.answerLst[0][0], my_game.answerLst[0][1], 0, 5, my_game)
        draw_shape_color(my_game.answerLst[1][0], my_game.answerLst[1][1], 1, 5, my_game)
        draw_shape_color(my_game.answerLst[2][0], my_game.answerLst[2][1], 2, 5, my_game)
        draw_shape_color(my_game.answerLst[3][0], my_game.answerLst[3][1], 3, 5, my_game)
        draw_shape_color(my_game.answerLst[4][0], my_game.answerLst[4][1], 4, 5, my_game)
        draw_selection((56,83,153), my_game.selection, num_answer=5, my_game=my_game)

def over(my_game):
    screen.fill(((255,255,255)))
    text1 = font.render(f'Your Score: {my_game.score}', True,(56,83,153))
    textRect1 = text1.get_rect()
    textRect1.center = (screenWidth//2, screenHeight//3)
    screen.blit(text1, textRect1)
    my_game.update(3)

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
                            if(my_game_1.score >= 1 and my_game_1.score < 2):
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