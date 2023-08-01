'''

#- - Leg Servo Matrix - -#
# ([[C1 F1 T1],
#   [C2 F2 T2],
#   [C3 F3 T3],
#   [C4 F4 T4]])

Ca1 = float(25)
Ca2 = float(-25)
Ca3 = float(25)
Ca4 = float(-25)
Fa1 = float(F_max)
Fa2 = float(F_max)
Fa3 = float(F_max)
Fa4 = float(F_max)
Ta1 = float(T_max)
Ta2 = float(T_max)
Ta3 = float(T_max)
Ta4 = float(T_max) 
Current_Array = np.array([[Ca1, Fa1, Ta1],
                          [Ca2, Fa2, Ta2],
                          [Ca3, Fa3, Ta3],
                          [Ca4, Fa4, Ta4]])

#- - Leg Servo Desired Angle Matrix - -#
Cda1 = float()
Cda2 = float()
Cda3 = float()
Cda4 = float()
Fda1 = float()
Fda2 = float()
Fda3 = float()
Fda4 = float()
Tda1 = float()
Tda2 = float()
Tda3 = float()
Tda4 = float()
# Cda1 = Coxa, Desired Angle, Leg one
Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                [Cda2, Fda2, Tda2],
                                [Cda3, Fda3, Tda3],
                                [Cda4, Fda4, Tda4]])


'''


Main_Pgm_Answer = 15

while Main_Pgm_Answer == 15:

    import pygame
    import time

    # Camera configuration
    MOVE_SPEED = 1

    # Initialize Pygame
    pygame.init()

    # Main game loop
    running = True
    while running:
        Leg_Select = input("Enter 1 for Leg1, 2 for Leg2, etc...")

        print("Use R and F to move Tibia, E and D to move Femur, and W and S to move Coxa")
        while Leg_Select == 1:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Move Leg motors with the designated keys

                    #Tibia
                    if event.key == pygame.K_r:
                        Tda1 += MOVE_SPEED
                        print(Tda1)
                    elif event.key == pygame.K_f:
                        Tda1 -= MOVE_SPEED
                        print(Tda1)

                    #Femur
                    elif event.key == pygame.K_e:
                        Fda1 += MOVE_SPEED
                        print(Fda1)
                    elif event.key == pygame.K_d:
                        Fda1 -= MOVE_SPEED
                        print(Fda1)

                    #Coxa
                    elif event.key == pygame.K_w:
                        Cda1 += MOVE_SPEED
                        print(Cda1)
                    elif event.key == pygame.K_s:
                        Cda1 -= MOVE_SPEED
                        print(Cda1)
                # Add a small delay to control the speed of camera movement
                time.sleep(0.02)

        while Leg_Select == 2:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Move camera based on arrow keys

                    #Tibia
                    if event.key == pygame.K_r:
                        Tda2 += MOVE_SPEED1
                    elif event.key == pygame.K_f:
                        Tda2 -= MOVE_SPEED
                    
                    #Femur
                    elif event.key == pygame.K_e:
                        Fda2 += MOVE_SPEED
                    elif event.key == pygame.K_d:
                        Fda2 -= MOVE_SPEED
                    
                    #Coxa
                    elif event.key == pygame.K_w:
                        Cda2 += MOVE_SPEED
                    elif event.key == pygame.K_s:
                        Cda2 -= MOVE_SPEED
                # Add a small delay to control the speed of camera movement
                time.sleep(0.02)

        while Leg_Select == 3:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Move camera based on arrow keys

                    #Tibia
                    if event.key == pygame.K_r:
                        Tda3 += MOVE_SPEED1
                    elif event.key == pygame.K_f:
                        Tda3 -= MOVE_SPEED
                    
                    #Femur
                    elif event.key == pygame.K_e:
                        Fda3 += MOVE_SPEED
                    elif event.key == pygame.K_d:
                        Fda3 -= MOVE_SPEED
                    
                    #Coxa
                    elif event.key == pygame.K_w:
                        Cda3 += MOVE_SPEED
                    elif event.key == pygame.K_s:
                        Cda3 -= MOVE_SPEED

                # Add a small delay to control the speed of camera movement
                time.sleep(0.02)

        while Leg_Select == 4:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Move camera based on arrow keys

                    #Tibia
                    if event.key == pygame.K_r:
                        Tda4 += MOVE_SPEED1
                    elif event.key == pygame.K_f:
                        Tda4 -= MOVE_SPEED
                    
                    #Femur
                    elif event.key == pygame.K_e:
                        Fda4 += MOVE_SPEED
                    elif event.key == pygame.K_d:
                        Fda4 -= MOVE_SPEED
                    
                    #Coxa
                    elif event.key == pygame.K_w:
                        Cda4 += MOVE_SPEED
                    elif event.key == pygame.K_s:
                        Cda4 -= MOVE_SPEED


                # Add a small delay to control the speed of camera movement
                time.sleep(0.02)

        # Quit the program ???????
        pygame.quit()

    




