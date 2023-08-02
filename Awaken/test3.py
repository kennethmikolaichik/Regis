import pygame
import time

# Camera configuration
MOVE_SPEED = 1

# Initialize Pygame
pygame.init()

# Main game loop
running = True
while running:
    Leg_Select = int(input("Enter 1 for Leg1, 2 for Leg2, etc..."))

    print("Use R and F to move Tibia, E and D to move Femur, and W and S to move Coxa")
    while True:  # Loop for continuous control until user exits

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                # Move camera based on arrow keys
                if event.key == pygame.K_r:
                    if Leg_Select == 1:
                        Tda1 += MOVE_SPEED
                    elif Leg_Select == 2:
                        Tda2 += MOVE_SPEED
                    elif Leg_Select == 3:
                        Tda3 += MOVE_SPEED
                    elif Leg_Select == 4:
                        Tda4 += MOVE_SPEED
                elif event.key == pygame.K_f:
                    if Leg_Select == 1:
                        Tda1 -= MOVE_SPEED
                    elif Leg_Select == 2:
                        Tda2 -= MOVE_SPEED
                    elif Leg_Select == 3:
                        Tda3 -= MOVE_SPEED
                    elif Leg_Select == 4:
                        Tda4 -= MOVE_SPEED
                elif event.key == pygame.K_e:
                    if Leg_Select == 1:
                        Fda1 += MOVE_SPEED
                    elif Leg_Select == 2:
                        Fda2 += MOVE_SPEED
                    elif Leg_Select == 3:
                        Fda3 += MOVE_SPEED
                    elif Leg_Select == 4:
                        Fda4 += MOVE_SPEED
                elif event.key == pygame.K_d:
                    if Leg_Select == 1:
                        Fda1 -= MOVE_SPEED
                    elif Leg_Select == 2:
                        Fda2 -= MOVE_SPEED
                    elif Leg_Select == 3:
                        Fda3 -= MOVE_SPEED
                    elif Leg_Select == 4:
                        Fda4 -= MOVE_SPEED
                elif event.key == pygame.K_w:
                    if Leg_Select == 1:
                        Cda1 += MOVE_SPEED
                    elif Leg_Select == 2:
                        Cda2 += MOVE_SPEED
                    elif Leg_Select == 3:
                        Cda3 += MOVE_SPEED
                    elif Leg_Select == 4:
                        Cda4 += MOVE_SPEED
                elif event.key == pygame.K_s:
                    if Leg_Select == 1:
                        Cda1 -= MOVE_SPEED
                    elif Leg_Select == 2:
                        Cda2 -= MOVE_SPEED
                    elif Leg_Select == 3:
                        Cda3 -= MOVE_SPEED
                    elif Leg_Select == 4:
                        Cda4 -= MOVE_SPEED

        # Add a small delay to control the speed of camera movement
        time.sleep(0.02)

    # Quit the program
    pygame.quit()
