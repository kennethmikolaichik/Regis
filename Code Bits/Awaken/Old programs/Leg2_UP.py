"""Leg2_UP"""

import pigpio
import time

pi = pigpio.pi()

pi.set_mode(12, pigpio.OUTPUT)
pi.set_mode(25, pigpio.OUTPUT)
pi.set_mode(24, pigpio.OUTPUT)

pi.set_PWM_frequency(12, 50)
pi.set_PWM_frequency(25, 50)
pi.set_PWM_frequency(24, 50)

pi.set_servo_pulsewidth(12, 1450)
pi.set_servo_pulsewidth(25, 500)
pi.set_servo_pulsewidth(24, 2450)

print("completed sucessfully")
quit()


