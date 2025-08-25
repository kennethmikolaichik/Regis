import RPi.GPIO as GPIO
import time
import os

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number to which the sensor is connected
sensor_pin = 26

# Set up the GPIO pin as input
GPIO.setup(sensor_pin, GPIO.IN)

count = 0
while count <= 990:
    try:
        print("Vibration sensor reading:")

        while True:
            # Read the sensor value
            sensor_value = GPIO.input(sensor_pin)

            # Print the sensor value
            if sensor_value:
                os.system('clear')
                print("Vibration detected!")
            else:
                os.system('clear')
                print("No vibration.")

            # Wait for a short period before reading again
            time.sleep(0.1)
            
            count +=1

    except KeyboardInterrupt:
        # Clean up GPIO on Ctrl+C
        GPIO.cleanup()


