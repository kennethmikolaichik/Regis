"""Leg1_Tarsus_Test.py"""


import pigpio
import time

pi = pigpio.pi()
# Set the default PWM frequency for all the servos to 50Hz
DEFAULT_FREQ = 50
T=5
C=7
F=6
servos = [C, F, T]
for pin in servos:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)
    
#Tarsus
LGT_max = 2450
LGT_min = 1150
#Femur
LGF_max = 2050
LGF_min = 500
#Coxa
LGC_min = 1200 #do not know value
LGC_max = 2200 #do not know value

#- - - - - - - - - - - -#
C_position = 1500
F_position = 1500
T_position = 1500
while T_position <= LGT_max:    
    T_position = T_position -10
    degree = ((T_position-1500)/(1000))*90
    pi.set_servo_pulsewidth(T, T_position)
    print(f"Coxa ServoSignal:{T_position}, Degree:{degree:.1f}° ", end="\r")
    time.sleep(.1)
    if T_position <= LGT_min:
        break
while T_position >= LGT_min:
    T_position = T_position +10
    degree = ((T_position-1500)/(1000))*90
    pi.set_servo_pulsewidth(T, T_position)
    print(f"Coxa ServoSignal:{T_position}, Degree:{degree:.1f}° ", end="\r")
    time.sleep(.1)
    if T_position >= LGT_max:
        break    
    
    
    
    
print("Leg1_Tarsus_Test - completed sucessfully")
quit()

