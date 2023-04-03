"""Full_Pan"""
#- - - -LIBRARIES- - - -#
import pigpio
import time
#- -DEFINE PARAMETERS- -#
position = 1500
pi = pigpio.pi()
#- - -MOTOR SETUP- - - -#
pi.set_mode(22, pigpio.OUTPUT)
pi.set_PWM_frequency(22, 50)
pi.set_servo_pulsewidth(22, position) #sets pan to center(1500)
#- - - - - - - - - - - -#
while position <= 2250:    
    position = position -10
    degree = ((position-1500)/(1000))*90
    print(f"ServoSignal:{position}, Degree:{degree:.1f}°", end="\r")
    time.sleep(.1)
    if position <= 750:
        break
while position >= 750:
    position = position +10
    degree = ((position-1500)/(1000))*90
    print(f"ServoSignal:{position}, Degree:{degree:.1f}°", end="\r")
    time.sleep(.1)
    if position >= 2250:
        break
while position <= 2250:    
    position = position -10
    degree = ((position-1500)/(1000))*90
    print(f"ServoSignal:{position}, Degree:{degree:.1f}°", end="\r")
    time.sleep(.1)
    if position <= 1500:
        break
print("Completed Sucessfully")
quit()