"""Leg1_DOWN"""

import pigpio
import time

pi = pigpio.pi()

pi.set_mode(5, pigpio.OUTPUT)
pi.set_mode(6, pigpio.OUTPUT)
pi.set_mode(7, pigpio.OUTPUT)

pi.set_servo_pulsewidth(5, 1150)
pi.set_servo_pulsewidth(6, 2050)
pi.set_servo_pulsewidth(7, 1450)

print("Leg1_DOWN - completed sucessfully")
quit()
