import pygame
import pygame_gui

pygame.init()

# Display setup
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pygame GUI Window Example")

# GUI Manager setup
manager = pygame_gui.UIManager(WINDOW_SIZE)

# Create a UIWindow
ui_window = pygame_gui.elements.UIWindow(
    rect=pygame.Rect((200, 150), (400, 300)),
    manager=manager,
    window_display_title="My UI Window"
)

# Add a label inside the UIWindow
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 50), (300, 50)),
    text="Hello inside UIWindow!",
    manager=manager,
    container=ui_window
)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Process GUI events
        manager.process_events(event)

    # Update GUI state
    manager.update(time_delta)

    # Render
    screen.fill((40, 40, 40))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()