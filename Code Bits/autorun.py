#!/usr/bin/python
import time
import os
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 110)

print("")
print("******************************************************")
print("* REGIS,    R-0.1:  Created by Kenneth Mikolaichik   *")
print("******************************************************")
print("")

time.sleep(0.5)
engine.say("Regis Online!")
engine.runAndWait()

time.sleep(0.5)
os.system('sudo pigpiod')
engine.say("Motors initialized.")
engine.runAndWait()

time.sleep(0.5)
os.system('sudo python3 /home/kennethmikolaichik/Camera/Picamera_with_OpenCV.py')
engine.say("Camera initialized.")
engine.runAndWait()

time.sleep(0.5)
os.system('sudo python3 /home/kennethmikolaichik/Camera/Picamera_Preview.py')

time.sleep(0.5)
engine.say("Awaiting input.")
engine.runAndWait()



