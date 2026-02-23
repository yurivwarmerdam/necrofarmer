import pygame as pg
from pygame import Surface
from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
import sys


pg.init()

resolution = (636, 333)

display: Surface = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("springgreen3"))


a_rect = pg.Rect(0, 0, 50, 50)
a_surf = pg.Surface((50, 50), pg.SRCALPHA)
pg.draw.circle(a_surf, pg.Color("red"), (25, 25), 25)

clock = pg.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            point = pg.mouse.get_pos()
            coll = a_surf.get_rect().collidepoint(point)
            print(f"collide? {coll}")
            if coll:
                corrected = (
                    point[0] - a_surf.get_rect().x,
                    point[1] - a_surf.get_rect().y,
                )

                value = a_surf.get_at(corrected)
                print(value)
                if value != pg.Color(0, 0, 0, 0):
                    print("which is true")

    display.blit(background, (0, 0))
    display.blit(
        a_surf,
    )

    pg.display.update()

# Ok, so mouse events get consumed. That's good.
# Now to figure out if that also happens when dealingw ith other ui elems.
# Start ehre: https://github.com/MyreMylar/pygame_gui_examples
# FOUND IT: https://github.com/MyreMylar/tower_defence
# Thought: Have my own UIPanel element that serves to:
#   - draw a picture
#   - consume clicks if the mouse pos overlaps
# Another thought: Maybe only draw a subset of the world the should actually be visile?
