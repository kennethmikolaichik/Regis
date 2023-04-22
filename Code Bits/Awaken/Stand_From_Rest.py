# -*- coding: utf-8 -*-
"""
Stand_From_Rest
Created on Thu Apr  6 22:49:41 2023

@author: kenne
"""
import pigpio
import time

# Initialize pigpio library
pi = pigpio.pi()

# Set the default PWM frequency for all the servos to 50Hz
DEFAULT_FREQ = 50

#- - Define Leg Parameters - -#
#Tarsus
T_max = 2450
T_min = 1150
#Femur
F_max = 1950
F_min = 600
#Coxa
C_min = 1200
C_max = 2200

#- - -Initialize All ServoMotors - - - -#
# Create a list of the GPIO pins that the servos are connected to
ALL_SERVOS = [4, 5, 6, 7, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27]
# Initialize the servos
for pin in ALL_SERVOS:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)
    
#- - Define Servo Sets - -#
Coxa = [7, 12, 23, 16]
Femur = [6, 25, 4, 21]
Tarsus = [5, 24, 27, 20]
Pan = [22]
Tilt = [13]
Leg1 = [7, 6, 5]
Leg2 = [12, 25, 24]
Leg3 = [23, 4, 27]
Leg4 = [16, 21, 20]

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
    for motor, pos in zip(Femur, positions):
        pi.set_servo_pulsewidth(motor, pos)

# Raise Tarsus
pi.set_servo_pulsewidth(5, T_max) #Leg1
pi.set_servo_pulsewidth(24, T_min) #Leg2
pi.set_servo_pulsewidth(27, T_min) #Leg3
pi.set_servo_pulsewidth(20, T_max) #Leg4
time.sleep(.3)

# Raise Femurs
pi.set_servo_pulsewidth(6, F_max) #Leg1
pi.set_servo_pulsewidth(25, F_min) #Leg2
pi.set_servo_pulsewidth(4, F_min) #Leg3
pi.set_servo_pulsewidth(21, F_max) #Leg4
time.sleep(.3)

# Spread Coxa
#move_coxa([(C_max/2) for motor in Coxa])
#time.sleep(.3)

# Lower Tarsus
#move_tarsus([T_min for motor in Tarsus])
#time.sleep(.3)

# Femur to middle
#move_femur([1500 for motor in Femur])

print("Stand From Rest - completed sucessfully")
quit()
