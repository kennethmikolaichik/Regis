import pygame
import time

# Initialize Pygame
pygame.init()

# Define the initial motor angle and create a variable to store the current motor angle
MOTOR_ANGLE = 0
current_angle = 0

# Set up the screen and display
WIDTH, HEIGHT = 200, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motor Angle Control")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

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
                current_angle += 1
            elif event.key == pygame.K_f:
                current_angle -= 1

        # Stop changing angle when the 'r' or 'f' keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r or event.key == pygame.K_f:
                current_angle = 0

    # Update the motor angle based on continuous key presses
    MOTOR_ANGLE = current_angle

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the current motor angle on the screen
    font = pygame.font.Font(None, 36)
    angle_text = font.render(f"Motor Angle: {MOTOR_ANGLE} degrees", True, (0, 0, 0))
    screen.blit(angle_text, (20, 20))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit the program
pygame.quit()
