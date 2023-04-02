""""Full_Pan"""

import pigpio
import time
#- - - - - - - - - - - -#
position = 1500
x = 0
#- - - - - - - - - - - -#
pi = pigpio.pi()

pi.set_mode(22, pigpio.OUTPUT)
pi.set_PWM_frequency(22, 50)

pi.set_servo_pulsewidth(22, position) #sets pan to center

while x < 100:
    while position < 2250:    
        position = position -10
        print(position)
        time.sleep(.1)
        x = x+1
        if position <= 750:
            break
    while position >= 750:
        position = position +10
        print(position)
        time.sleep(.1)
        x = x+1
        if position >= 2250:
            break
    break
print("completed Sucessfully")
quit()

