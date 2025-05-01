from pygame.time import get_ticks, Clock


clock = Clock()

while True:
    print(f"ticking!{get_ticks()}")
    clock.tick(60)
