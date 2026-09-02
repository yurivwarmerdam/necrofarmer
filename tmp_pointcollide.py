import sys
import pygame as pg
from pygame.sprite import Sprite, Group


class MySprite(Sprite):
    def __init__(self, rect: pg.Rect, *groups) -> None:
        super().__init__(*groups)

        self.image = pg.Surface([rect[2], rect[3]], flags=pg.SRCALPHA)
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect = rect

        center = (rect[2] // 2, rect[3] // 2)
        radius = min(rect[2], rect[3]) / 2
        pg.draw.circle(self.image, (0, 0, 0, 0), center, radius)


class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((400, 300))
        self.clock = pg.time.Clock()
        self.group = Group()
        self.sprite = MySprite(pg.Rect(20, 20, 60, 60), self.group)
        self.indicator = pg.Surface([10, 10])
        self.indicator.fill("red")

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill((200, 200, 200))
            self.group.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    Main().run()
