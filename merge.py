import multiprocessing
from multiprocessing import Process, Value, Array
import time
from home_screen import game


def HGRHandler():
    while True:
        time.sleep(1)
        print(123)

if __name__ == "__main__":    
    p1 = multiprocessing.Process(target=HGRHandler)

    p1.start()
    game()
    p1.join()
