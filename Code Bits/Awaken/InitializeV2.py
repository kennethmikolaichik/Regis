"""Initialize
Created by: Kenneth Mikolaichik
5.8.2023"""
import time
import math
import numpy as np
import pigpio
#from klampt import IKObjective,IKSolver
#from klampt.modle import ik

# - - Speed Modifier - - #
Speed = 0.005
# This is how fast the robot moves, Zero is fastest
# it is the number of seconds to wait per each 0.1 degrees of movement
# Between 0 and 0.05 is usually reasonable

############### INTRODUCTION #################

# The positional solver determines where each motor is in cartesian space
# The inverse kinematic solver will determine desired angles
# from current position. The desired angles are put into a matrix,
# the current position translates directly into another matrix of angles
# as the current angles of the leg motors reach the desired angles,
# the number is converted to signal and is sent to the matrix of leg motors.



#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - - - - -Servo Motor Definitions- - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#

# Initialize pigpio library as 'pi'
pi = pigpio.pi()
# Create default PWM frequency for all the servos, 50Hz
DEFAULT_FREQ = 50
# Create a list of the GPIO pins that the servos are connected to
servos = [4, 5, 6, 7, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27]
# Initialize the servos
for pin in servos:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)


#- - Define Servo Groups - -#
Coxa = [7, 12, 23, 16] #Shoulders
Femur = [6, 25, 4, 21] #Bicept
Tarsus = [5, 24, 27, 20] #Forearm
Leg1 = [7, 6, 5] #RH Fwd
Leg2 = [12, 25, 24] #RH Aft
Leg3 = [23, 4, 27] #LH Fwd
Leg4 = [16, 21, 20] #RH Aft
Pan = [22] #Angle in xy-plane (zero is fwd)
Tilt = [13] #Angle from xy-plane to z-axis (zero is horizontal)
Head = [22, 13] #(xy, z)

#- - Signal Correction Matrix - -#
# This matrix is necessary to correct for way the motors are mounted.
Correction_Array = np.array([[1, -1, -1],
                             [1, 1, 1],
                             [-1, 1, 1],
                             [-1, -1, -1]])
#- - Leg Servo Matrix - -#
# C1 F1 T1
# C2 F2 T2
# C3 F3 T3
# C4 F4 T4
Servo_Array = np.array([[7, 6, 5],
                        [12, 25, 24],
                        [23, 4, 27],
                        [16, 21, 20]])

#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - - - - - Positional Definitions- - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#

#- - Positional Data - -#
Bx = float()
By = float()
Bz = float()
Body_Frame = [Bx, By, Bz]
#Center of body

Hx = float()
Hy = float()
Hz = float()
Head_Frame = [Hx, Hy, Hz]
#Center of head

#Leg1
#- - - - - -
#Manipulator
Mx1 = float()
My1 = float()
Mz1 = float()
M1_Frame = [Mx1, My1, Mz1]
#- - - - - -
Cx1 = float()
Cy1 = float()
Cz1 = float()
C1_Frame = [Cx1, Cy1, Cz1]
Fx1 = float()
Fy1 = float()
Fz1 = float()
F1_Frame = [Fx1, Fy1, Fz1]
Tx1 = float()
Ty1 = float()
Tz1 = float()
T1_Frame = [Tx1, Ty1, Tz1]

#Leg2
#- - - - - -
#Manipulator
Mx2 = float()
My2 = float()
Mz2 = float()
M2_Frame = [Mx2, My2, Mz2]
#- - - - - -
Cx2 = float()
Cy2 = float()
Cz2 = float()
C2_Frame = [Cx2, Cy2, Cz2]
Fx2 = float()
Fy2 = float()
Fz2 = float()
F2_Frame = [Fx2, Fy2, Fz2]
Tx2 = float()
Ty2 = float()
Tz2 = float()
T2_Frame = [Tx2, Ty2, Tz2]

#Leg3
#- - - - - -
#Manipulator
Mx3 = float()
My3 = float()
Mz3 = float()
M3_Frame = [Mx3, My3, Mz3]
#- - - - - -
Cx3 = float()
Cy3 = float()
Cz3 = float()
C3_Frame = [Cx3, Cy3, Cz3]
Fx3 = float()
Fy3 = float()
Fz3 = float()
F3_Frame = [Fx3, Fy3, Fz3]
Tx3 = float()
Ty3 = float()
Tz3 = float()
T3_Frame = [Tx3, Ty3, Tz3]

#Leg4
#- - - - - -
#Manipulator
Mx4 = float()
My4 = float()
Mz4 = float()
M4_Frame = [Mx4, My4, Mz4]
#- - - - - -
Cx4 = float()
Cy4 = float()
Cz4 = float()
C4_Frame = [Cx4, Cy4, Cz4]
Fx4 = float()
Fy4 = float()
Fz4 = float()
F1_Frame = [Fx4, Fy4, Fz4]
Tx4 = float()
Ty4 = float()
Tz4 = float()
T4_Frame = [Tx4, Ty4, Tz4]

#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - Angle Matricies and Motor Bounds- - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#

#- - Leg Servo Current Angle Matrix - -#
Ca1 = float()
Ca2 = float()
Ca3 = float()
Ca4 = float()
Fa1 = float()
Fa2 = float()
Fa3 = float()
Fa4 = float()
Ta1 = float()
Ta2 = float()
Ta3 = float()
Ta4 = float()
# Ca1 = Coxa, Current Angle, Leg one
Angle_Array = np.array([[Ca1, Fa1, Ta1],
                        [Ca2, Fa2, Ta2],
                        [Ca3, Fa3, Ta3],
                        [Ca4, Fa4, Ta4]])

#- - Define Min/Max Leg Servo Parameters - -#
#Coxa
C_min = -27
C_max = 63
#Femur
F_min = -49.5
F_max = 90
#Tarsus
T_min = -31.5
T_max = 85.5

Max_Angle_Array = np.array([[C_max, F_max, T_max],
                            [C_max, F_max, T_max],
                            [C_max, F_max, T_max],
                            [C_max, F_max, T_max]])

Min_Angle_Array = np.array([[C_min, F_min, T_min],
                            [C_min, F_min, T_min],
                            [C_min, F_min, T_min],
                            [C_min, F_min, T_min]])

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

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

while True:
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - - Desired Angle Prompt- - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    while True:
        print("Enter desired Angles from L to R, Top to Bottom:\n")
        print("- Servo Angle Matrix -")
        print("Leg1:  C1 F1 T1 ")
        print("Leg2:  C2 F2 T2 ")
        print("Leg3:  C3 F3 T3 ")
        print("Leg4:  C4 F4 T4 ")
        Cda1 = float(input("C1:"))
        Fda1 = float(input("F1:"))
        Tda1 = float(input("T1:"))
        Cda2 = float(input("C2:"))
        Fda2 = float(input("F2:"))
        Tda2 = float(input("T2:"))
        Cda3 = float(input("C3:"))
        Fda3 = float(input("F3:"))
        Tda3 = float(input("T3:"))
        Cda4 = float(input("C4:"))
        Fda4 = float(input("F4:"))
        Tda4 = float(input("T4:"))
        Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                        [Cda2, Fda2, Tda2],
                                        [Cda3, Fda3, Tda3],
                                        [Cda4, Fda4, Tda4]])
        print("You have selected:\n",Desired_Angle_Array)
        Answer = input("Is this Correct? Y/N\n")
        if Answer == "y":
            break
        if Answer == "Y":
            break
        else:
            print("enter Y or N\n")
    
    '''
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - -Desired Position Prompt- - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - Desired Position Prompt - -#
    Dx = float()
    Dy = float()
    Dz = float()
    Desired_Position = [Dx, Dy, Dz]
    
    print("Enter desired position as: x y z in meters")
    print("Looking down from above, +x is to the right, +y is forward")
    print("Enter x coordinate...", end="\r")
    Dx = input()
    print("Enter y coordinate...", end="\r")
    Dy = input()
    print("Enter z coordinate, for default enter 'h'...", end="\r")
    Dz = input()
    if Dz == 'h':
        Dz = 0.09
    '''
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - -Inverse Kinematic Solver - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    '''
    ???
    ??? Need to get inverse kinematic solver for here!!!!!
    ???
    ???
    ???
    ???
    ???
    ???
    ???
    '''
    
    
    '''
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #TEST DATA - DELETE!!!!
    Cda1 = 10
    Cda2 = 30
    Cda3 = 30
    Cda4 = 10
    Fda1 = 8
    Fda2 = -8
    Fda3 = -8
    Fda4 = 8
    Tda1 = -40
    Tda2 = -40
    Tda3 = -40
    Tda4 = -40
    Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                    [Cda2, Fda2, Tda2],
                                    [Cda3, Fda3, Tda3],
                                    [Cda4, Fda4, Tda4]])
    
    '''
    
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - - Matrix Update Program - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    
    A = Angle_Array
    B = Desired_Angle_Array
    MIN = Min_Angle_Array
    MAX = Max_Angle_Array
    
    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value
    for i in range(3):
        if B[0,i] >= MAX[0,i]:
            B[0,i] = MAX[0,i]
        if B[0,i] <= MIN[0,i]:
            B[0,i] = MIN[0,i]
        if B[1,i] >= MAX[1,i]:
            B[1,i] = MAX[1,i]
        if B[1,i] <= MIN[1,i]:
            B[1,i] = MIN[1,i]
        if B[2,i] >= MAX[2,i]:
            B[2,i] = MAX[2,i]
        if B[2,i] <= MIN[2,i]:
            B[2,i] = MIN[2,i]
        if B[3,i] >= MAX[3,i]:
            B[3,i] = MAX[3,i]
        if B[3,i] <= MIN[3,i]:
            B[3,i] = MIN[3,i]
    
    # Combes through columns of 'A' from top to bottom, determines if difference,
    # Creates Matrix 'C' which adds or subtracts 0.1 until matrix 'A' == 'B'
    # Where i is the number of Rows of 'A', Runs left to right.
    # Each pass creates Matrix 'C' which has an element value of either 0 or +/-0.1
    # The adjustment matrix 'C' is then added to 'A', the current angles.
    # This information is then converted to PWM signal and sent to servo motor
    # The program will then halt according to the value of 'Speed' (line 9)
    # The process repeats until 'A' == 'B', within tolerance.
    Counter = 1
    Move_Time = 0 
    while np.allclose(A, B, rtol=0.001, atol=0.001) == False: 
        
        #Create/Reset Adjustment Array of zeros
        C = np.array([[float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)]])
        
        for i in range(3): #scans rows from top to bottom
        
        #Element [0,i] - - - - - - - - - - - - - - - - - - - - -  
            #For row 1, if less than desired angle
            if A[0,i] < B[0,i]:
                C[0,i] +=0.1 #increase angle towards desired angle
            #For row 1, if greater than desired angle
            if A[0,i] > B[0,i]:
                C[0,i] -=0.1 #dencrease angle towards desired angle   
    
                
        #Element [1,i] - - - - - - - - - - - - - - - - - - - - -  
            #For row 2, if less than desired angle
            if A[1,i] < B[1,i]:
                C[1,i] +=0.1 #increase angle towards desired angle        
             #For row 2, if greater than desired angle        
            if A[1,i] > B[1,i]:
                C[1,i] -=0.1 #dencrease angle towards desired angle   
    
                
        #Element [2,i] - - - - - - - - - - - - - - - - - - - - -          
            #For row 3, if less than desired angle            
            if A[2,i] < B[2,i]:
                C[2,i] +=0.1 #increase angle towards desired angle    
            #For row 3, if greater than desired angle            
            if A[2,i] > B[2,i]:
                C[2,i] -=0.1 #dencrease angle towards desired angle   
    
                
        #Element [3,i] - - - - - - - - - - - - - - - - - - - - -        
            #For row 4, if less than desired angle     
            if A[3,i] < B[3,i]:
                C[3,i] +=0.1 #increase angle towards desired angle   
            #For row 4, if greater than desired angle 
            if A[3,i] > B[3,i]:
                C[3,i] -=0.1 #dencrease angle towards desired angle    
                
        A = A+C #Adjust each element of angle Matrix 'A' by +/-0.1 of Matric 'C'
        A = A*Correction_Array #Correct for mirrored hardware setup
          
        # - - - Update servo signal - - - #
        for i in range(3): #scans rows from L/R, top to bottom
            Angle = A[0,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[0,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[1,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[1,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[2,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[2,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[3,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[3,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            
        A = A*Correction_Array #Remove correction
    
        time.sleep(Speed) #Speed Controller
        #Debugging#    print(A,"Current Angles\n\n",C, "adjustment Array\n\n", B,"Desired Angles\n\n", "completed =",np.allclose(A, B, rtol=0.001, atol=0.001))    
        Move_Time = Speed*Counter     
        print(f"{Move_Time:.2f}s",end="\r")
        Counter +=1
        #Comapres A to B within tolerance of 0.001
        #if equal then stop movement. 
        if Counter >= 1500:
            print("ERROR - Move_Time timeout")
            time.sleep(1)
            break
        
        if np.allclose(A, B, rtol=0.001, atol=0.005) == True:
            
            Counter = 0
            break
        
    Angle_Array = B
    A = Angle_Array
    print("\n Servo Angles:\n",Angle_Array)    
    
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - - - Positional Solver - - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    
    # The entirety of these calculations are based off of the body frame as inputs
    # and the dimensions of the physical robot that are shown below.
    
    # - - Measurements / Dimensions - - #
    # All data is in Meter/Second/Kilogram system
    # Measurements are taken from centers of axis of rotation
    Body_Width = 0.09
    Body_Height = 0.04
    Body_Length = 0.105
    Coxa_Length = 0.023
    Femur_Length = 0.031
    Tarsus_Length = 0.09
    
    h = Height = 0.0
    Body_Frame = [0, 0, h] #This should be taken from a GPS module or something

    # - - Dimensional Computations - - #    
    
    deg2rad = (math.pi/180)
    #Leg1
    
    F1lr = Femur_Length * (math.cos(deg2rad*Angle_Array[0,1]))#Leg1 Femur [i,1]
    F1lh = Femur_Length * (math.sin(deg2rad*Angle_Array[0,1]))#Leg1 Femur [i,1]
    Theta_1 = deg2rad*Angle_Array[0,1] + deg2rad*Angle_Array[0,2]
    T1lr = Tarsus_Length * math.sin(Theta_1)
    T1lh = Tarsus_Length * math.cos(Theta_1)
    Reach_1r = F1lr + T1lr
    Reach_1h = F1lh + T1lh
    
    #Leg2
    F2lr = Femur_Length * np.cos(deg2rad*Angle_Array[1,1])
    F2lh = Femur_Length * np.sin(deg2rad*Angle_Array[1,1])
    Theta_2 = deg2rad*Angle_Array[1,1] + deg2rad*Angle_Array[1,2]
    T2lr = Tarsus_Length * np.sin(Theta_2)
    T2lh = Tarsus_Length * np.cos(Theta_2)
    Reach_2r = F2lr + T2lr
    Reach_2h = F2lh + T2lh
    
    #Leg3
    F3lr = Femur_Length * np.cos(deg2rad*Angle_Array[2,1]) #Leg 1 Femur [i,1]
    F3lh = Femur_Length * np.sin(deg2rad*Angle_Array[2,1]) #Leg 1 Femur [i,1]
    Theta_3 = deg2rad*Angle_Array[2,1] + deg2rad*Angle_Array[2,2]
    T3lr = Tarsus_Length * np.sin(Theta_3)
    T3lh = Tarsus_Length * np.cos(Theta_3)
    Reach_3r = F3lr + T3lr
    Reach_3h = F3lh + T3lh
    
    #Leg4
    F4lr = Femur_Length * np.cos(deg2rad*Angle_Array[3,1]) #Leg 1 Femur [i,1]
    F4lh = Femur_Length * np.sin(deg2rad*Angle_Array[3,1]) #Leg 1 Femur [i,1]
    Theta_4 = deg2rad*Angle_Array[3,1] + deg2rad*Angle_Array[3,2]
    T4lr = Tarsus_Length * np.sin(Theta_4)
    T4lh = Tarsus_Length * np.cos(Theta_4)
    Reach_4r = F4lr + T4lr
    Reach_4h = F4lh + T4lh
 
    # - - Positional Computations - - #      
    
    print(f"Femur 1 reach: {F1lr:.3f}")
    print(f"Femur 1 z: {F1lh:.3f}")
    print(f"Leg1 Femur + Tarsus Angle: {Theta_1:.3f}radians")
    print(f"Tarsus 1 reach: {T1lr:.3f}")
    print(f"Tarsus 1 z: {T1lh:.3f}")
    print(f"Leg 1 reach: {Reach_1r:.3f}")
    print(f"Leg 1 z: {Reach_1h:.3f}")
    print("\n")
    time.sleep(3)
    ###############LAST WORKING 5.9.2023
    
    
    
    
    
    
    
    
    
    






















