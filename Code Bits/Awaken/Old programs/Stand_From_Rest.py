"""
Created by: Kenneth Mikolaichik
4.23.2023"""
import pigpio
import time
import numpy as np
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Need some sort of feedback mechanism to get original position of motors.

#for leg 1 and leg 3 use 'Angle'.
#for legs 2 and 4 use 'Inverted_Angle' or just '-Angle'.
#As physical hardware, Legs 1 & 2 are mirror images of each other.
#Leg 1 is front and leg 2 is back.
#Leg 3 is front and 4 is back.
#Odd front, even back, 1 is fwd RH.
Angle = float()
C_Angle = float()
F_Angle = float()
T_Angle = float()
S_Signal = float()
Inverted_Angle = -Angle
S_Signal = ((1000 * Angle) / 90) + 500
N_Signal = ((1000 * Inverted_Angle) / 90) + 500
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -

#- - Define Servo Sets - -#
Coxa = [7, 12, 23, 16]
Femur = [6, 25, 4, 21]
FFemur = [6, 4]
RFemur = [25, 21]
Tarsus = [5, 24, 27, 20]

Leg1 = [7, 6, 5]
Leg2 = [12, 25, 24]
Leg3 = [23, 4, 27]
Leg4 = [16, 21, 20]

Pan = [22]
Tilt = [13]

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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    time.sleep(.05)
    if F_Angle >= F_max:
        break

#Tarsus Up
while T_Angle <= T_max:
    
    T_Angle = T_Angle + 0.5
    Inverted_Angle = -1 * T_Angle
    S_Signal = ((1000 * T_Angle) / 90) + 1500
    N_Signal = ((1000 * Inverted_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(5, N_Signal) #Leg1
    pi.set_servo_pulsewidth(24, S_Signal) #Leg2
    pi.set_servo_pulsewidth(27, S_Signal) #Leg3
    pi.set_servo_pulsewidth(20, N_Signal) #Leg4
    print(f"ServoSignal:{S_Signal:.1f}, Angle:{T_Angle:.1f}° ", end="\r")
    time.sleep(.05)
    if T_Angle >= T_max:
        break
    
#Femurs to Center
while F_Angle >= 0:
    
    F_Angle = F_Angle - 0.5
    Inverted_Angle = -1 * F_Angle
    S_Signal = ((1000 * F_Angle) / 90) + 1500
    N_Signal = ((1000 * Inverted_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(6, N_Signal) #Leg1
    pi.set_servo_pulsewidth(25, S_Signal) #Leg2
    pi.set_servo_pulsewidth(4, S_Signal) #Leg3
    pi.set_servo_pulsewidth(21, N_Signal) #Leg4
    print(f"ServoSignal:{S_Signal:.1f}, Angle:{F_Angle:.1f}° ", end="\r")
    time.sleep(.05)
    if F_Angle <= 0:
        break
    
    