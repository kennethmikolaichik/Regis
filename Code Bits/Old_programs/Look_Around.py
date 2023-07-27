"""Look_Around"""
#- - - -LIBRARIES- - - -#
import pigpio
import time
#- -DEFINE PARAMETERS- -#
position = 1500
pi = pigpio.pi()
#- - -MOTOR SETUP- - - -#
# Set the default PWM frequency for all the servos to 50Hz
DEFAULT_FREQ = 50
Pan = [22]
Tilt = [13]

pi.set_mode(22, pigpio.OUTPUT)
pi.set_PWM_frequency(22, 50)
pi.set_servo_pulsewidth(22, position) #sets pan to center(1500)

pi.set_mode(13, pigpio.OUTPUT)
pi.set_PWM_frequency(13, 50)
pi.set_servo_pulsewidth(13, position) #sets pan to center(1500)

##Look Around##

while position <= 1750:    
    position = position -10
    degree = ((position-1500)/(1000))*90
    pi.set_servo_pulsewidth(22, position)
    pi.set_servo_pulsewidth(13, position)
    time.sleep(.05)
    if position <= 1250:
        break
while position >= 1250:
    position = position +10
    degree = ((position-1500)/(1000))*90
    pi.set_servo_pulsewidth(22, position)
    pi.set_servo_pulsewidth(13, position)
    time.sleep(.05)
    if position >= 1750:
        break
while position <= 1750:    
    position = position -10
    degree = ((position-1500)/(1000))*90
    pi.set_servo_pulsewidth(22, position)
    pi.set_servo_pulsewidth(13, position)
    time.sleep(.05)
    if position <= 1500:
        break
