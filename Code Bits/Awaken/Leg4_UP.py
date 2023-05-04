"""Leg4_UP"""

import pigpio
import time

pi = pigpio.pi()

pi.set_mode(16, pigpio.OUTPUT)
pi.set_mode(21, pigpio.OUTPUT)
pi.set_mode(20, pigpio.OUTPUT)

pi.set_PWM_frequency(16, 50)
pi.set_PWM_frequency(21, 50)
pi.set_PWM_frequency(20, 50)

pi.set_servo_pulsewidth(16, 1450)
pi.set_servo_pulsewidth(21, 500)
pi.set_servo_pulsewidth(20, 2450)

print("completed sucessfully")
quit()


