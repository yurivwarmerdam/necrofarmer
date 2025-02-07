import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Display Text Example")

# Set up the font
font = pygame.font.Font(None, 74)  # None uses the default font, 74 is the font size

# Create text surface
text = font.render("Hello, Pygame!", True, (255, 255, 255))  # White color

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (black in this case)
    screen.fill((0, 0, 0))

    # Display the text
    screen.blit(text, (200, 250))  # (200, 250) is the position

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()