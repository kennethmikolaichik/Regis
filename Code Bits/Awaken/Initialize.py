"""Initialize
Created by: Kenneth Mikolaichik
5.6.2023"""
import time
import numpy as np
import pigpio

# - - Behavior Modifiers - - #
Speed = 0.05
# This is how fast the robot moves, Zero is fastest
# it is the number of seconds to wait per each 0.1 degrees of movement
# Between 0 and 1 is usually reasonable

# - - Measurements / Dimensions - - #
# All data is in Meter/Second/Kilogram system
Body_Width = 0.09
Body_Height = 0.04
Body_Length = 0.105
Coxa_Length = 0.023
Femur_Length = 0.031
Tarsus_Length = 0.09

# Initialize pigpio library as 'pi'
pi = pigpio.pi()
# Set the default PWM frequency for all the servos to 50Hz
DEFAULT_FREQ = 50
# Create a list of the GPIO pins that the servos are connected to
servos = [4, 5, 6, 7, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27]
# Initialize the servos
for pin in servos:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)

# - - Angle to PWM Converter - - #
# Need some sort of feedback mechanism to get original position of motors.

# for leg 1 and leg 3 use 'Angle'.
# for legs 2 and 4 use 'Inverted_Angle' or just '-Angle'.
# As physical hardware, Legs 1 & 2 are mirror images of each other.
# Leg 1 is front and leg 2 is back.
# Leg 3 is front and 4 is back.
# Odd front, even back, 1 is fwd RH.
Angle = float()
PWM_Signal = ((1000 * Angle) / 90) + 1500

#- - Define Servo Sets - -#
Coxa = [7, 12, 23, 16]
Femur = [6, 25, 4, 21]
Tarsus = [5, 24, 27, 20]
Leg1 = [7, 6, 5]
Leg2 = [12, 25, 24]
Leg3 = [23, 4, 27]
Leg4 = [16, 21, 20]
Pan = [22]
Tilt = [13]
Head = [22, 13]

#- - Signal Correction Matrix - -#
Correction_Array = np.array([[1],
                             [-1],
                             [1],
                             [-1]])

#- - Leg Matrix - -#
# C1 F1 T1
# C2 F2 T2
# C3 F3 T3
# C4 F4 T4
# The inverse kinematic solver will determine desired angles
# of the leg motors in order to reach the desired position
# Angle data will be sent through the angle to PWM converter
# Then the PWM signal will be applied to the Leg Array
Servo_Array = np.array([[Leg1],
                        [Leg2],
                        [Leg3],
                        [Leg4]])

#- - Positional Data - -#
Bx = float()
By = float()
Bz = float()
Body_Frame = [Bx, By, Bz]

Hx = float()
Hy = float()
Hz = float()
Head_Frame = [Hx, Hy, Hz]

#Leg1
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

#- - Current Leg Servo Angle Matrix - -#
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

#- - Desired Angle Matrix - -#
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

#- - Positional Solver - -#
Position = Body_Frame = [0, 0, 0]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
#TEST DATA - DELETE!!!!
Tda1 = 40
Tda2 = 40
Tda3 = 40
Tda4 = 40
Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                [Cda2, Fda2, Tda2],
                                [Cda3, Fda3, Tda3],
                                [Cda4, Fda4, Tda4]])

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - Speed Controller & Matrix Update Program - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Combes through columns of 'A' from top to bottom and adds or subtracts 0.1,
# until Column 'A' = Column 'B' and matrix 'A' == 'B'
# Where i is the number of Rows of 'A'
# Correction_Array corrects for mirrored Leg hardware
A = Angle_Array * Correction_Array
B = Desired_Angle_Array * Correction_Array
MIN = Min_Angle_Array * Correction_Array
MAX = Max_Angle_Array * Correction_Array

for i in range(3): #scans rows from top to bottom

#Element [0,i] - - - - - - - - - - - - - - - - - - - - -  
    #For row 1, while less than desired angle
    while A[0,i] < B[0,i]:
        if A[0,i] > MAX[0,i]:
            break
        else:
            A[0,i] +=0.1 #increase angle towards desired angle
            # - Update servo signal - #
            Angle = A[0,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[0,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)
    #For row 1, while greater than desired angle
    while A[0,i] > B[0,i]:
        if A[0,i] >= MIN[0,i]:
            break
        else:
            A[0,i] -=0.1 #dencrease angle towards desired angle
            # - Update servo signal - #
            Angle = A[0,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[0,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)

#Element [1,i] - - - - - - - - - - - - - - - - - - - - -  
    #For row 2, while less than desired angle
    while A[1,i] < B[1,i]:
        if A[1,i] >= MAX[1,i]:
            break
        else:
            A[1,i] +=0.1 #increase angle towards desired angle
            # - Update servo signal - #
            Angle = A[1,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[1,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)
     #For row 2, while greater than desired angle        
    while A[1,i] > B[1,i]:
        if A[1,i] >= MIN[1,i]:
            break
        else:
            A[1,i] -=0.1 #dencrease angle towards desired angle
            # - Update servo signal - #
            Angle = A[1,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[1,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)

#Element [2,i] - - - - - - - - - - - - - - - - - - - - -          
    #For row 3, while less than desired angle            
    while A[2,i] < B[2,i]:
        if A[2,i] >= MAX[2,i]:
            break
        else:
            A[2,i] +=0.1 #increase angle towards desired angle
            # - Update servo signal - #
            Angle = A[2,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[2,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)
    #For row 3, while greater than desired angle            
    while A[2,i] > B[2,i]:
        if A[2,i] >= MIN[2,i]:
            break
        else:
            A[2,i] -=0.1 #dencrease angle towards desired angle
            # - Update servo signal - #
            Angle = A[2,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[2,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)

#Element [3,i] - - - - - - - - - - - - - - - - - - - - -        
    #For row 4, while less than desired angle     
    while A[3,i] < B[3,i]:
        if A[3,i] >= MAX[3,i]:
            break
        else:
            A[3,i] +=0.1 #increase angle towards desired angle
            # - Update servo signal - #
            Angle = A[3,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[3,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)
    #For row 4, while greater than desired angle 
    while A[3,i] > B[3,i]:
        if A[3,i] >= MIN[3,i]:
            break
        else:
            A[3,i] -=0.1 #dencrease angle towards desired angle
            # - Update servo signal - #
            Angle = A[3,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[3,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            time.sleep(Speed)

        
print(B,"   ",Servo_Array)

































