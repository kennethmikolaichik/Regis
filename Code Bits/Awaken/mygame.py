import pygame
import time

# Camera configuration
CAMERA_SPEED = 5
WIDTH = 400
HEIGHT = 400

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Camera Control")

# Camera position
camera_x = WIDTH // 2
camera_y = HEIGHT // 2

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Move camera based on arrow keys
            if event.key == pygame.K_LEFT:
                camera_x -= CAMERA_SPEED
            elif event.key == pygame.K_RIGHT:
                camera_x += CAMERA_SPEED
            elif event.key == pygame.K_UP:
                camera_y -= CAMERA_SPEED
            elif event.key == pygame.K_DOWN:
                camera_y += CAMERA_SPEED

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw camera position
    pygame.draw.circle(screen, (255, 0, 0), (camera_x, camera_y), 10)

    # Update the screen
    pygame.display.flip()

    # Add a small delay to control the speed of camera movement
    time.sleep(0.02)

# Quit the program
pygame.quit()
