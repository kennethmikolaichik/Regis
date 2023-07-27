"""4.1.2023"""
import pigpio
import time

# Initialize pigpio library and connect to the local Pi
pi = pigpio.pi()

# Set the default PWM frequency for all the servos to 50Hz
DEFAULT_FREQ = 50

# Create a list of the GPIO pins that the servos are connected to
servos = [4, 5, 6, 7, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27]

# Initialize the servos to their default position
for pin in servos:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)
    pi.set_servo_pulsewidth(pin, 1500)

# Move the servos to a new position
def move_servos(positions):
    for pin, pos in zip(servos, positions):
        pi.set_servo_pulsewidth(pin, pos)

# Example usage
# Move all servos to 0 degrees
#move_servos([850 for pin in servos])
#time.sleep(1)

print("Default Position - completed sucessfully")
quit()