import multiprocessing
from multiprocessing import Process, Value, Array
import time
import random
from game import game


def HGRHandler(gesture):
    while True:
        time.sleep(1)
        gesture.value = random.randint(0,2)
        print(gesture.value)

def a(gesture):
    while True:
        print(gesture.value)

if __name__ == "__main__":
    gesture = Value('d', 0)
    
    p1 = multiprocessing.Process(target=HGRHandler, args= (gesture,))
    p2 = multiprocessing.Process(target=game, args=(gesture,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
