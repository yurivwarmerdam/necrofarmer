import asyncio
import pygame as pg

clock = pg.time.Clock()



async def sleeper(time:int):
    print("starting sleep")
    asyncio.sleep(time/1000)
    print("finished sleep")


def main():
    # time = clock.get_time()
    # ticks = pg.time.get_ticks()
    # while True:
    #     time = clock.get_time()
    #     ticks = pg.time.get_ticks()
    #     print(time, ticks)
    #     clock.tick(60)
    task=asyncio.create_task(sleeper(1))
    print(task.done())

    task


if __name__ == "__main__":
    main()
