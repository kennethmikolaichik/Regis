import pygame
import time

# Initialize Pygame
pygame.init()

# Define the maximum and minimum motor angles and create variables to store the current motor angle and the angle step
MAX_ANGLE = 90
MIN_ANGLE = -90
current_angle = 0
angle_step = 1

# Set up the screen and display
WIDTH, HEIGHT = 200, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motor Angle Control")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Create boolean flags to track whether 'r' and 'f' keys are pressed or not
r_key_pressed = False
f_key_pressed = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Continuous angle changes when 'r' or 'f' keys are held down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r_key_pressed = True
            elif event.key == pygame.K_f:
                f_key_pressed = True

        # Stop changing angle when the 'r' or 'f' keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                r_key_pressed = False
            elif event.key == pygame.K_f:
                f_key_pressed = False

    # Update the motor angle based on continuous key presses
    if r_key_pressed:
        current_angle += angle_step
        current_angle = min(current_angle, MAX_ANGLE)  # Clamp angle to maximum value

    if f_key_pressed:
        current_angle -= angle_step
        current_angle = max(current_angle, MIN_ANGLE)  # Clamp angle to minimum value

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the current motor angle on the screen
    font = pygame.font.Font(None, 36)
    angle_text = font.render(f"Motor Angle: {current_angle} degrees", True, (0, 0, 0))
    screen.blit(angle_text, (20, 20))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit the program
pygame.quit()
