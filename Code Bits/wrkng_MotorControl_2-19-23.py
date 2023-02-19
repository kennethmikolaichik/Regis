import pigpio
import time

#initialize pigpio library and connect to the local Pi
pi = pigpio.pi()

pi.set_mode(7, pigpio.OUTPUT)

pi.set_servo_pulsewidth(7, 1550)
pi.set_PWM_frequency(7, 50)
time.sleep(1)





pi.stop()