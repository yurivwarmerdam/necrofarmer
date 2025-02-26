from threading import Thread
from time import sleep


def sleeper():
    print("starting sleep")
    sleep(2)
    print("ending sleep")


if __name__ == "__main__":
    print("starting main loop")
    t1=Thread(target=sleeper)
    t1.start()
    print("ending main loop")