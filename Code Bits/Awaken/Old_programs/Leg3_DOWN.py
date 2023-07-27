""""Leg3_DOWN"""

import pigpio
import time

pi = pigpio.pi()

pi.set_mode(27, pigpio.OUTPUT)
pi.set_mode(4, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

pi.set_PWM_frequency(27, 50)
pi.set_PWM_frequency(4, 50)
pi.set_PWM_frequency(23, 50)

pi.set_servo_pulsewidth(27, 2000)
pi.set_servo_pulsewidth(4, 950)
pi.set_servo_pulsewidth(23, 1450)

print("completed sucessfully")
quit()


