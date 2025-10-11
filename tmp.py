import pygame as pg
import pygame_gui
from scripts.utils import load_image, sheet_to_sprites
from pygame.math import Vector2
import sys


class myPanel(pygame_gui.elements.UIPanel):
    def process_event(self, event: pg.Event) -> bool:
        return super().process_event(event)


pg.init()

pg.display.set_caption("Quick Start")

resolution = (400, 300)

display = pg.display.set_mode(resolution, pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("#000000"))

manager = pygame_gui.UIManager(resolution)

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))


hello_button = pygame_gui.elements.UIButton(
    relative_rect=outline_sprites[(0, 0)].get_rect(), text="", manager=manager
)
hello_button.normal_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.hovered_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.selected_images = [outline_sprites[(1, 0)], button_sprites[(0, 0)]]
hello_button.disabled_images = [outline_sprites[(2, 0)], button_sprites[(0, 0)]]

hello_button.set_position((60, 50))

hello_button.rebuild()

somethin_else = pygame_gui.elements.UIPanel(
    outline_sprites[0, 0].get_rect(), manager=manager
)
somethin_else.set_position((60, 100))

third = pygame_gui.elements.UIWindow(outline_sprites[0, 0].get_rect(),manager=manager, draggable=False)

third.set_position((60,150))

clock = pg.time.Clock()

print(pg.MOUSEBUTTONUP, pygame_gui.UI_BUTTON_PRESSED)

while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F8):
            pg.quit()
            sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print("image pressed")

        processed = manager.process_events(event)

        if event.type in [pg.MOUSEBUTTONUP, pygame_gui.UI_BUTTON_PRESSED,pg.MOUSEBUTTONDOWN]:
            print(processed, pg.event.event_name(event.type))

    manager.update(time_delta)

    display.blit(background, (0, 0))
    manager.draw_ui(display)

    pg.display.update()

# Ok, so mouse events get consumed. That's good.
# Now to figure out if that also happens when dealingw ith other ui elems.
# Start ehre: https://github.com/MyreMylar/pygame_gui_examples
# FOUND IT: https://github.com/MyreMylar/tower_defence
# Thought: Have my own UIPanel element that serves to:
#   - draw a picture
#   - consume clicks if the mouse pos overlaps
# Another thought: Maybe only draw a subset of the world the should actually be visile?
