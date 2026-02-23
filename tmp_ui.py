from functools import partial
import pygame as pg
from pygame import Surface, Rect
from pygame.constants import BUTTON_LEFT as BUTTON_LEFT
from pygame_gui.elements import UIImage
from scripts import ui_shim
from scripts.utils import load_image, sheet_to_sprites
from pygame.math import Vector2
import sys
from scripts.utils import sheet_to_sprite
from scripts.custom_sprites import tilingscale, ninepatchscale
from scripts.ui_shim import UIPanel


# --- setup base elements ---
pg.init()
pg.display.set_caption("Quick Start")
resolution = (636, 333)
display: Surface = pg.display.set_mode(resolution, pg.RESIZABLE)
background = pg.Surface(resolution)
background.fill(pg.Color("springgreen3"))
manager = ui_shim.UIManager(resolution, theme_path="theme/theme.json")
manager.get_theme().load_theme("theme/buttons_generated.json")
ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))
clock = pg.time.Clock()
# --------------------------

# ---///////////////////////////
# ---- expermental code here ---------
# ---///////////////////////////

nine_slice_func = partial(ninepatchscale, patch_margain=3, scale_func=tilingscale)
portrait_panel_rect: Rect = Rect(0, 0, 170, 146)
context_panel_rect: Rect = Rect(0, 0, 400, 99)
ui_components_sheet = load_image("art/ui_components.png")
ui_background_sprite = sheet_to_sprite(ui_components_sheet, Rect(0, 0, 60, 62))

portrait_panel = UIPanel(
    pg.Rect(
        0,
        -portrait_panel_rect[3],
        portrait_panel_rect[2],
        portrait_panel_rect[3],
    ),
    anchors={
        "left": "left",
        "right": "left",
        "top": "bottom",
        "bottom": "bottom",
    },
    object_id="#portrait_background",
)

parent_panel = UIPanel(
    pg.Rect(
        portrait_panel_rect[2],
        -(context_panel_rect[3]),
        context_panel_rect[2],
        context_panel_rect[3],
    ),
    anchors={
        "left": "left",
        "right": "right",
        "top": "bottom",
        "bottom": "bottom",
    },
    scale_func=nine_slice_func,
    object_id="#panel_background",
)

child_panel = UIPanel(
    pg.Rect(
        0,
        0,
        80,
        80,
    ),
    anchors={
        "left": "left",
        "right": "right",
        "top": "top",
        "bottom": "bottom",
    },
    container=parent_panel.get_container(),
)

grandchild_panel = UIPanel(
    pg.Rect(
        0,
        0,
        100,
        100,
    ),
    anchors={
        "left": "left",
        "right": "right",
        "top": "top",
        "bottom": "bottom",
    },
    container=child_panel.get_container(),
)


UIImage(
    context_panel_rect,
    ui_background_sprite,
    anchors={
        "left": "left",
        "right": "right",
        "top": "top",
        "bottom": "bottom",
    },
    scale_func=nine_slice_func,
    container=child_panel.get_container(),
    # container=parent_panel.get_container(),
)

# core loop
while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        processed = manager.process_events(event)

        if event.type == pg.VIDEORESIZE:
            manager.set_window_resolution(event.size)

    manager.update(time_delta)

    display.blit(background, (0, 0))
    manager.draw_ui(display)

    pg.display.update()
    print(grandchild_panel.relative_rect)
    parent_panel.get_container().clear()
