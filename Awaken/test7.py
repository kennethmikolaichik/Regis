import pygame
import time

# Initialize Pygame
pygame.init()

# Define the maximum and minimum motor angles and create variables to store the current motor angles and the angle step
MAX_ANGLE = 90
MIN_ANGLE = -90
current_angle1 = 0
current_angle2 = 0
current_angle3 = 0
angle_step = 1

# Set up the screen and display
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motor Angle Control")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Create boolean flags to track whether keys are pressed or not
r_key_pressed = False
f_key_pressed = False
e_key_pressed = False
d_key_pressed = False
w_key_pressed = False
s_key_pressed = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Continuous angle changes when keys are held down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r_key_pressed = True
            elif event.key == pygame.K_f:
                f_key_pressed = True
            elif event.key == pygame.K_e:
                e_key_pressed = True
            elif event.key == pygame.K_d:
                d_key_pressed = True
            elif event.key == pygame.K_w:
                w_key_pressed = True
            elif event.key == pygame.K_s:
                s_key_pressed = True

        # Stop changing angle when the keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                r_key_pressed = False
            elif event.key == pygame.K_f:
                f_key_pressed = False
            elif event.key == pygame.K_e:
                e_key_pressed = False
            elif event.key == pygame.K_d:
                d_key_pressed = False
            elif event.key == pygame.K_w:
                w_key_pressed = False
            elif event.key == pygame.K_s:
                s_key_pressed = False

    # Update the motor angles based on continuous key presses
    if r_key_pressed:
        current_angle1 += angle_step
        current_angle1 = min(current_angle1, MAX_ANGLE)  # Clamp angle to maximum value

    if f_key_pressed:
        current_angle1 -= angle_step
        current_angle1 = max(current_angle1, MIN_ANGLE)  # Clamp angle to minimum value

    if e_key_pressed:
        current_angle2 += angle_step
        current_angle2 = min(current_angle2, MAX_ANGLE)  # Clamp angle to maximum value

    if d_key_pressed:
        current_angle2 -= angle_step
        current_angle2 = max(current_angle2, MIN_ANGLE)  # Clamp angle to minimum value

    if w_key_pressed:
        current_angle3 += angle_step
        current_angle3 = min(current_angle3, MAX_ANGLE)  # Clamp angle to maximum value

    if s_key_pressed:
        current_angle3 -= angle_step
        current_angle3 = max(current_angle3, MIN_ANGLE)  # Clamp angle to minimum value

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the current motor angles on the screen
    font = pygame.font.Font(None, 36)
    angle_text1 = font.render(f"Motor 1 Angle: {current_angle1} degrees", True, (0, 0, 0))
    angle_text2 = font.render(f"Motor 2 Angle: {current_angle2} degrees", True, (0, 0, 0))
    angle_text3 = font.render(f"Motor 3 Angle: {current_angle3} degrees", True, (0, 0, 0))
    screen.blit(angle_text1, (20, 20))
    screen.blit(angle_text2, (20, 60))
    screen.blit(angle_text3, (20, 100))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit the program
pygame.quit()
