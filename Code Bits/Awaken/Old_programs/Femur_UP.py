"""Created by: Kenneth Mikolaichik
4.23.2023"""

import pigpio
import time
import numpy as np

# - - Behavior Modifiers - - #
Speed = 0.05
# This is how fast the robot moves, Zero is fastest
# it is the number of seconds per degrees of movement
# Between 0 and 0.1 is usually reasonable

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
C_Angle = float()
F_Angle = float()
T_Angle = float()
S_Signal = float()
Inverted_Angle = -Angle
S_Signal = ((1000 * Angle) / 90) + 500
N_Signal = ((1000 * Inverted_Angle) / 90) + 500

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

#- - Leg Matrix - -#
# C1 F1 T1
# C2 F2 T2
# C3 F3 T3
# C4 F4 T4
# The inverse kinematic solver will determine angles
# of the leg motors in order to reach the desired position
# Angle data will be sent through the angle to PWM converter
# Then the PWM signal will be applied to the Leg Array
LegArray = np.array([[Leg1],
                     [Leg2],
                     [Leg3],
                     [Leg4]])

#- - Positional Data - -#
h = 0


Bx = float()
By = float()
Bz = h
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

#- - Define Leg Parameters - -#
#Coxa
C_min = -27
C_max = 63
#Femur
F_min = -49.5
F_max = 90
#Tarsus
T_min = -31.5
T_max = 85.5

#- - Positional Solver - -#
Position = Body_Frame

Dx = float()
Dy = float()
Dz = float()
Desired_Position = [Dx, Dy, Dz]


#- - Define Classes - -#
# Move the servos to a new position
def move_leg1(positions):
    for motor, pos in zip(Leg1, positions):
        pi.set_servo_pulsewidth(motor, pos)
        
def move_leg2(positions):
    for motor, pos in zip(Leg2, positions):
        pi.set_servo_pulsewidth(motor, pos)        

def move_leg3(positions):
    for motor, pos in zip(Leg3, positions):
        pi.set_servo_pulsewidth(motor, pos)

def move_leg4(positions):
    for motor, pos in zip(Leg4, positions):
        pi.set_servo_pulsewidth(motor, pos)
                                                                
def move_coxa(positions):
    for motor, pos in zip(Coxa, positions):
        pi.set_servo_pulsewidth(motor, pos)

def move_tarsus(positions):
    for motor, pos in zip(Tarsus, positions):
        pi.set_servo_pulsewidth(motor, pos)

def move_femur(positions):
    S_Signal = ((1000 * Angle) / 90) + 1500
    pi.set_servo_pulsewidth(6, S_Signal) #Leg1
    pi.set_servo_pulsewidth(25, N_Signal) #Leg2
    pi.set_servo_pulsewidth(4, S_Signal) #Leg3
    pi.set_servo_pulsewidth(21, N_Signal) #Leg4                            
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Femurs Up
while F_Angle <= F_max:
    
    F_Angle = F_Angle + 0.5
    Inverted_Angle = -1 * F_Angle
    S_Signal = ((1000 * F_Angle) / 90) + 1500
    N_Signal = ((1000 * Inverted_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(6, N_Signal) #Leg1
    pi.set_servo_pulsewidth(25, S_Signal) #Leg2
    pi.set_servo_pulsewidth(4, S_Signal) #Leg3
    pi.set_servo_pulsewidth(21, N_Signal) #Leg4
    print(f"ServoSignal:{S_Signal:.1f}, Angle:{F_Angle:.1f}° ", end="\r")
    time.sleep(Speed)
    if F_Angle >= F_max:
        break

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Testing position to desired position
while Position < Desired_Position:
    
    F_Angle = F_Angle + 0.5
    Inverted_Angle = -1 * F_Angle
    S_Signal = ((1000 * F_Angle) / 90) + 1500
    N_Signal = ((1000 * Inverted_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(6, N_Signal) #Leg1
    pi.set_servo_pulsewidth(25, S_Signal) #Leg2
    pi.set_servo_pulsewidth(4, S_Signal) #Leg3
    pi.set_servo_pulsewidth(21, N_Signal) #Leg4
    print(f"ServoSignal:{S_Signal:.1f}, Angle:{F_Angle:.1f}° ", end="\r")
    time.sleep(Speed)
    if F_Angle >= F_max:
        break
    