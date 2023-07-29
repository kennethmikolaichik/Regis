"""Main_Pgm
Created by: Kenneth Mikolaichik
7.26.2023"""
import os
import sys
import subprocess
import math
import numpy as np
import pigpio
import time
import pyttsx3
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import pygame
import Definitions
Current_Array = Definitions.Current_Array
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
print("")
print("******************************************************")
print("*   REGIS,  R-0.1:  Created by Kenneth Mikolaichik   *")
print("******************************************************")
print("")
sleep(2.5)
os.system('clear')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''


#subprocess.call(['python', 'Greeting.py']) #No good, waits to run
'''
#This works ok but there is a window that pops up over the main menu
os.chdir('/home/kennethmikolaichik/Regis/Awaken')
subprocess.call(['lxterminal', '-e', 'python Greeting.py'])
os.system('clear')
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
while True:
    Main_Pgm_Ans = int(0)
    while Main_Pgm_Ans == 0:
        print("\n")
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("|                    MAIN PROGRAM --- LONG LIVE REGIS!                  |")
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("\nSelect from the following:")
        print("  0) Engage Motors")
        print("  1) Wave Hello!")
        print("  2) Turn on Camera")     
        print("  3) Go to Maintenance Position")        
        print("  4) Move Robot / Servo Angle Input Mode")
        print("  5) Desired Position Prompt")
        print("  6) Get Current Servo Angles")
        print("  7) Get Current Frames / Positions")
        print("  8) Get Current Leg Dimensions")
        print("  9) Sit Down")
        print(" 10) Stand Up")
        print(" 11) Stand Tall")
        print(" 12) Pan Left & Right")
        print(" 13) Look Around")
        print(" 14) Turn on Camera with Object Detection")
        Main_Pgm_Ans = int(input("Enter 1,2,3...\n"))
        break

        '''
        if Main_Pgm_Ans.isdigit == False:
            os.system('clear')
            Main_Pgm_Ans == 0
            print("Invalid Input - try again")
            sleep(3)
            Main_Pgm_Ans == 0
            os.system('clear')
         '''

    while Main_Pgm_Ans == 0:
        import Engage_Motors
        Engage_Motors.Engage()
   
    while Main_Pgm_Ans == 1: #Wave Hello
        import Wave_Hello
        Wave_Hello.Wave_Hello()
        #subprocess.run(['python', 'Wave_Hello.py'])
    
    '''
    while Main_Pgm_Ans == 1: #Test
        import test1
        print("working up to here")
        test1.TEST()
        sleep(1)
        #print(variable)
    '''

