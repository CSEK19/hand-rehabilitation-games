import multiprocessing
from multiprocessing import Process, Value, Array
import time
from home_screen import game
import pygame


def HGRHandler():
    while True:
        time.sleep(1)

if __name__ == "__main__":    
    p1 = multiprocessing.Process(target=HGRHandler)

    p1.start()

    screen = pygame.display.set_mode((1280, 720))
    game(screen)
    
    p1.join()
