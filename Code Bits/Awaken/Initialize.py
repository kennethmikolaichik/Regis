"""Initialize
Created by: Kenneth Mikolaichik
5.8.2023"""
import numpy as np
import pigpio

# - - Speed Modifier - - #
Speed = 0.005
# This is how fast the robot moves, Zero is fastest
# it is the number of seconds to wait per each 0.1 degrees of movement
# Between 0 and 0.05 is usually reasonable

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

