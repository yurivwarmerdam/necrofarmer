import pygame as pg
from pygame import Vector2
from pygame.sprite import Group
import sys
from scripts.tilemap import Tilemap
from math import floor

pg.init()

display = pg.display.set_mode((800, 400), pg.SCALED, pg.RESIZABLE)

clock = pg.time.Clock()


# debug_rect = pg.rect.Rect(0, 0, 50, 50)
# tst_surf = pg.surface.Surface((50, 50))
# tst_surf.fill("lightblue")
# pg.draw.rect(tst_surf, "yellow", debug_rect, 1)


# for i in range(5):
#     display.blit(tst_surf, (i * 10, i * 10))

render_layer=Group()

tilemap=Tilemap("art/tmx/tst_square_map.tmx",{"ground":render_layer})

pg.display.update()

print(render_layer)


# ---- ticking ----
while True:
    
    # --- event loop ---
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
            # TODO: Offsetting does not quite work. Let's keep iterating.
            tile=tilemap.world_to_map(mouse_pos)

            print(f"click: {mouse_pos} : {tile} : [{floor(tile.x)},{floor(tile.y)}]")
    
    # --- render loop ---
    display.fill("darkblue")
    render_layer.draw(display)
    pg.display.update()
    clock.tick(60)
