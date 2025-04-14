import asyncio




async def draw_loop():
    while True:
        await asyncio.sleep(1 / 60)  # ~16.67ms
        print("Draw frame")

async def update_loop():
    while True:
        await asyncio.sleep(1 / 60)
        print("Game update")

async def behavior_tree_loop():
    while True:
        await asyncio.sleep(0.25)  # Trigger every ~250ms
        print("Update behavior trees")


def main():
    pass


if __name__ == "__main__":
    main()