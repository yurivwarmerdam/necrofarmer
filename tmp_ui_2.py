import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIImage

pygame.init()
WINDOW_SIZE = (800, 480)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

clock = pygame.time.Clock()
running = True

# Panel that spans full width and keeps doing so on resize
panel = UIPanel(
    relative_rect=pygame.Rect(0, 0, WINDOW_SIZE[0], 100),
    manager=manager,
    anchors={'left': 'left', 'right': 'right', 'top': 'top'}
)

# A simple placeholder image
img_surf = pygame.Surface((1, 1))
img_surf.fill((200, 100, 50))

# UIImage anchored left/right so it stretches with the panel
ui_image = UIImage(
    relative_rect=pygame.Rect(0, 10, WINDOW_SIZE[0]-20, 80),
    image_surface=img_surf,
    manager=manager,
    container=panel,
    anchors={'left': 'left', 'right': 'right'}
)

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            manager.set_window_resolution(event.size)
            pass

        manager.process_events(event)

    manager.update(dt)
    screen.fill((30, 30, 30))
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
