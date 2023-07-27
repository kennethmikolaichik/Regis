"""Main_Menu
Created by: Kenneth Mikolaichik
7.26.2023"""
from time import sleep
import os, sys, subprocess
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
print("")
print("******************************************************")
print("*   REGIS,  R-0.1:  Created by Kenneth Mikolaichik   *")
print("******************************************************")
print("")
os.system('sudo pigpiod')
sleep(2.5)
os.system('clear')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
while True:
    Main_Pgm_Ans = int(0)
    while Main_Pgm_Ans == 0:
        print("\n")
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("|                    MAIN PROGRAM --- LONG LIVE REGIS!                  |")
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("\nSelect from the following:")
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