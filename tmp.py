import pygame
import pygame_gui
from scripts.utils import load_image

pygame.init()

pygame.display.set_caption("Quick Start")
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((800, 600))

ui_image = load_image("art/tst_ui.png")

hello_button = pygame_gui.elements.UIButton(
    relative_rect=ui_image.get_rect(), text="Say Hello", manager=manager
)
# image_elem = pygame_gui.elements.UIImage(hello_button.get_abs_rect(), ui_image, manager)
hello_button.normal_images = [ui_image]
hello_button.hovered_images = [ui_image]
hello_button.selected_images = [ui_image]
hello_button.disabled_images = [ui_image]
hello_button.rebuild()

print(hello_button.drawable_shape)


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print(hello_button.normal_images)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
