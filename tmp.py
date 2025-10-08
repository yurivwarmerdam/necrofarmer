import pygame as pg
import pygame_gui
from scripts.utils import load_image, sheet_to_sprites
from pygame.math import Vector2

pg.init()

pg.display.set_caption("Quick Start")

resolution = (400, 300)

window_surface = pg.display.set_mode(resolution,pg.SCALED)

background = pg.Surface(resolution)
background.fill(pg.Color("#000000"))

manager = pygame_gui.UIManager(resolution)

ui_image = load_image("art/tst_ui.png")
button_sprites = sheet_to_sprites(load_image("art/thumbnails.png"), Vector2(46, 38))
outline_sprites = sheet_to_sprites(load_image("art/outlines.png"), Vector2(54, 46))


hello_button = pygame_gui.elements.UIButton(
    relative_rect=outline_sprites[(0, 0)].get_rect(), text="", manager=manager
)
# image_elem = pygame_gui.elements.UIImage(hello_button.get_abs_rect(), ui_image, manager)
hello_button.normal_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.hovered_images = [outline_sprites[(0, 0)], button_sprites[(0, 0)]]
hello_button.selected_images = [outline_sprites[(1, 0)], button_sprites[(0, 0)]]
hello_button.disabled_images = [outline_sprites[(2, 0)], button_sprites[(0, 0)]]

hello_button.set_position(Vector2(60,50))

hello_button.rebuild()

print(hello_button.drawable_shape)


clock = pg.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print(hello_button.normal_images)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pg.display.update()
