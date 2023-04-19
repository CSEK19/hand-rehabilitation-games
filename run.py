import pygame, sys
import random
import os
from game1 import game1
from game2 import game2
from game3 import game3

pygame.init()
pygame.font.init()
pygame.font.get_init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
font = pygame.font.SysFont('', 60)
state = 'home'
screen = pygame.display.set_mode((screenWidth, screenHeight))
selection = 0

def game_list(selection):
    games = ['1. Shapes n Colors', '2. Eggs Catcher', '3. Dino Run']
    font2 = pygame.font.SysFont('', 40)
    texts = [font2.render(text, True,(56,83,153)) if i != selection else font2.render(text, True,(0,0,0)) for (i, text) in enumerate(games)]
    textRects = [text.get_rect() for text in texts]
    textRects[0].midleft = (screenWidth//3, 300)
    textRects[1].midleft = (screenWidth//3, 400)
    textRects[2].midleft = (screenWidth//3, 500)
    [screen.blit(text, textRect) for text, textRect in zip(texts, textRects)]

def home():
    global selection
    screen.fill(((255,255,255)))
    text1 = font.render('Video Games for Hand Rehabilitation', True,(56,83,153))
    textRect1 = text1.get_rect()
    textRect1.center = (screenWidth//2, screenHeight//4)
    screen.blit(text1, textRect1)
    game_list(selection)


def game(gesture):
    global selection, state
    while True:
        if state == 'home':
            home()
        if state == 'game1':
            state = game1()
        if state == 'game2':
            state = game2()
        if state == 'game3':
            state = game3()

        if gesture.value == 0:
            selection +=1
            if selection>2:
                selection = 0
        if gesture.value == 2:
            selection -= 1
            if selection<0:
                selection = 2
                
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        state = 'game1'
                    if event.key == pygame.K_2:
                        state = 'game2'
                    if event.key == pygame.K_3:
                        state = 'game3'
                    if event.key == pygame.K_DOWN:
                        selection +=1
                        if selection>2:
                            selection = 0
                    if event.key == pygame.K_UP:
                        selection -=1
                        if selection<0:
                            selection = 2
                    if event.key == pygame.K_RETURN:
                        state = f'game{selection+1}'
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(60)    

if __name__ == "__main__":
    while True:
        if state == 'home':
            home()
        if state == 'game1':
            state = game1()
        if state == 'game2':
            state = game2()
        if state == 'game3':
            state = game3()
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        state = 'game1'
                    if event.key == pygame.K_2:
                        state = 'game2'
                    if event.key == pygame.K_3:
                        state = 'game3'
                    if event.key == pygame.K_DOWN:
                        selection +=1
                        if selection>2:
                            selection = 0
                    if event.key == pygame.K_UP:
                        selection -=1
                        if selection<0:
                            selection = 2
                    if event.key == pygame.K_RETURN:
                        state = f'game{selection+1}'
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

        clock.tick(60)