"""Leg1_UP"""

import pigpio
import time

pi = pigpio.pi()

pi.set_mode(7, pigpio.OUTPUT)
pi.set_mode(6, pigpio.OUTPUT)
pi.set_mode(8, pigpio.OUTPUT)

pi.set_PWM_frequency(7, 50)
pi.set_PWM_frequency(6, 50)
pi.set_PWM_frequency(8, 50)

pi.set_servo_pulsewidth(7, 1450)
pi.set_servo_pulsewidth(6, 500)
pi.set_servo_pulsewidth(5, 2450)

print("completed sucessfully")
quit()

