"""Initialize
Created by: Kenneth Mikolaichik
5.8.2023"""
import os
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
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Pan_Update():

    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value
    '''
    if Desired_Pan >= P_max
        Desired_Pan = P_max
    if Desired_Pan <= P_min
        Desired_Pan = P_min
    '''
    #if less than desired angle
    if Pan_Angle < Desired_Pan:
        Pan_Angle +=0.1 #increase angle towards desired angle
    #if greater than desired angle
    if Pan_Angle > Desired_Pan:
        Pan_Angle -=0.1 #dencrease angle towards desired angle   
    
    PWM_Signal = ((1000 * Pan_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(Pan, PWM_Signal)

    time.sleep(Speed) #Speed Controller

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Tilt_Update():

    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value
    '''
    if Desired_Pan >= P_max
        Desired_Pan = P_max
    if Desired_Pan <= P_min
        Desired_Pan = P_min
    '''
    #if less than desired angle
    if Tilt_Angle < Desired_Tilt:
        Tilt_Angle +=0.1 #increase angle towards desired angle
    #if greater than desired angle
    if Tilt_Angle > Desired_Tilt:
        Tilt_Angle -=0.1 #dencrease angle towards desired angle   
    
    PWM_Signal = ((1000 * Tilt_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(Pan, PWM_Signal)

    time.sleep(Speed) #Speed Controller


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Matrix_Update():
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - - Matrix Update Program - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    Matrix_Update.Angle_Array = Current_Array
    # Ca1 = Coxa, Current Angle, Leg one
    A = Matrix_Update.Angle_Array
    B = Desired_Angle_Array
    MIN = Min_Angle_Array
    MAX = Max_Angle_Array

    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value
    for i in range(3):
        if B[0,i] >= MAX[0,i]:
            B[0,i] = MAX[0,i]
        if B[0,i] <= MIN[0,i]:
            B[0,i] = MIN[0,i]
        if B[1,i] >= MAX[1,i]:
            B[1,i] = MAX[1,i]
        if B[1,i] <= MIN[1,i]:
            B[1,i] = MIN[1,i]
        if B[2,i] >= MAX[2,i]:
            B[2,i] = MAX[2,i]
        if B[2,i] <= MIN[2,i]:
            B[2,i] = MIN[2,i]
        if B[3,i] >= MAX[3,i]:
            B[3,i] = MAX[3,i]
        if B[3,i] <= MIN[3,i]:
            B[3,i] = MIN[3,i]

    # Combes through columns of 'A' from top to bottom, determines if difference,
    # Creates Matrix 'C' which adds or subtracts 0.1 until matrix 'A' == 'B'
    # Where i is the number of Rows of 'A', Runs left to right.
    # Each pass creates Matrix 'C' which has an element value of either 0 or +/-0.1
    # The adjustment matrix 'C' is then added to 'A', the current angles.
    # This information is then converted to PWM signal and sent to servo motor
    # The program will then halt according to the value of variable 'Speed'
    # The process repeats until 'A' == 'B', within tolerance.
    Counter = 1
    Move_Time = 0 
    while np.allclose(A, B, rtol=0.002, atol=0.005) == False: 
        
        #Create/Reset Adjustment Array of zeros
        C = np.array([[float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)],
                      [float(0.0), float(0.0), float(0.0)]])
        
        for i in range(3): #scans rows from top to bottom
        
        #Element [0,i] - - - - - - - - - - - - - - - - - - - - -  
            #For row 1, if less than desired angle
            if A[0,i] < B[0,i]:
                C[0,i] +=0.1 #increase angle towards desired angle
            #For row 1, if greater than desired angle
            if A[0,i] > B[0,i]:
                C[0,i] -=0.1 #dencrease angle towards desired angle   

                
        #Element [1,i] - - - - - - - - - - - - - - - - - - - - -  
            #For row 2, if less than desired angle
            if A[1,i] < B[1,i]:
                C[1,i] +=0.1 #increase angle towards desired angle        
             #For row 2, if greater than desired angle        
            if A[1,i] > B[1,i]:
                C[1,i] -=0.1 #dencrease angle towards desired angle   

                
        #Element [2,i] - - - - - - - - - - - - - - - - - - - - -          
            #For row 3, if less than desired angle            
            if A[2,i] < B[2,i]:
                C[2,i] +=0.1 #increase angle towards desired angle    
            #For row 3, if greater than desired angle            
            if A[2,i] > B[2,i]:
                C[2,i] -=0.1 #dencrease angle towards desired angle   

                
        #Element [3,i] - - - - - - - - - - - - - - - - - - - - -        
            #For row 4, if less than desired angle     
            if A[3,i] < B[3,i]:
                C[3,i] +=0.1 #increase angle towards desired angle   
            #For row 4, if greater than desired angle 
            if A[3,i] > B[3,i]:
                C[3,i] -=0.1 #dencrease angle towards desired angle    
                
        A = A+C #Adjust each element of angle Matrix 'A' by +/-0.1 of Matric 'C'
        A = A*Correction_Array #Correct for mirrored hardware setup
        
        # - - - Update Servo Signal / Move Robot - - - #
        for i in range(3): #scans rows from L/R, top to bottom
            Angle = A[0,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[0,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[1,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[1,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[2,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[2,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Angle = A[3,i]
            PWM_Signal = ((1000 * Angle) / 90) + 1500
            Pin = Servo_Array[3,i]
            pi.set_servo_pulsewidth(Pin, PWM_Signal)
        
        A = A*Correction_Array #Remove correction

        time.sleep(Speed) #Speed Controller
        #DEBUGGUING# print(A,"Current Angles\n\n",C, "adjustment Array\n\n", B,"Desired Angles\n\n", "completed =",np.allclose(A, B, rtol=0.001, atol=0.005))    
        
        # prints the time it takes to the screen
        Move_Time = Speed*Counter     
        print(f"{Move_Time:.2f}s",end="\r")
        Counter +=1
        
        #Counter Runaway
        if Counter >= 1500:
            Matrix_Update.Angle_Array = A
            print("ERROR - Move_Time timeout")
            Counter = 0
            time.sleep(1)
            break

        #Comapres A to B within tolerance of 0.001
        #if equal then stop movement.         
        if np.allclose(A, B, rtol=0.002, atol=0.005) == True: 
            Matrix_Update.Angle_Array = A
            Counter = 0           
            break 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
def Solve_Inverse_Kinematic():
    print("IS THIS RIGHT??")
    # Need to get inverse kinematic solver for here!!!!!
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
print("")
print("******************************************************")
print("* REGIS,    R-0.1:  Created by Kenneth Mikolaichik   *")
print("******************************************************")
print("")
os.system('sudo pigpiod')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#- - Define Min/Max Leg Servo Parameters - -#
# min is closed-curled under and squeezed together.
# max is extended out-legs held high and full fwd/aft.
#Coxa
C_min = -27
C_max = 63
#Femur
F_min = -49.5
F_max = 90
#Tarsus
T_min = -31.5
T_max = 85.5
#Pan
P_min = -90
P_max = 90
#Tilt
Ti_min = -45
Ti_max = 80

# - - Text to Speech Engine - - #
engine = pyttsx3.init()
engine.setProperty('rate', 110)

# - - Speed Modifier - - #
Speed = 0.000
# This is how fast the robot moves, Zero is fastest
# it is the number of seconds to wait per each 0.1 degrees of movement
# Between 0 and 0.05 is usually reasonable

# - - Measurements / Dimensions - - #
# All data is in Meter/Second/Kilogram system
# Measurements are taken from centers of axis of rotation
Body_Width = 0.09
Body_Height = 0.04
Body_Length = 0.105
Coxa_Length = 0.023
Femur_Length = 0.031
Tarsus_Length = 0.09
Head_Offset_x = 0.025 #GET REAL VALUES HERE
Head_Offset_y = 0.025 #GET REAL VALUES HERE 
Head_Offset_z = 0.025 #GET REAL VALUES HERE 


h = Height = 0.0
Body_Frame = [0, 0, h] #This should be taken from a GPS module or something

#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - - - - - - - Definitions - - - - - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#

#- - Define Servo Groups - -#
Coxa = [7, 12, 23, 16] #Shoulders
Femur = [6, 25, 4, 21] #Bicept
Tarsus = [5, 24, 27, 20] #Forearm
Leg1 = [7, 6, 5] #RH Fwd
Leg2 = [12, 25, 24] #RH Aft
Leg3 = [23, 4, 27] #LH Fwd
Leg4 = [16, 21, 20] #RH Aft
Pan = [22] #Angle in xy-plane (zero is fwd)
Tilt = [13] #Angle from xy-plane to z-axis (zero is horizontal)
Head_Servos = [22, 13] #(xy, z)

#- - Signal Correction Matrix - -#
# This matrix is necessary to correct for way the motors are mounted.
Correction_Array = np.array([[1, -1, 1],
                             [1, 1, -1],
                             [-1, 1, -1],
                             [-1, -1, 1]])
#- - Leg Servo Matrix - -#
# ([[C1 F1 T1],
#   [C2 F2 T2],
#   [C3 F3 T3],
#   [C4 F4 T4]])
Servo_Array = np.array([[7, 6, 5],
                        [12, 25, 24],
                        [23, 4, 27],
                        [16, 21, 20]])

Max_Angle_Array = np.array([[C_max, F_max, T_max],
                            [C_max, F_max, T_max],
                            [C_max, F_max, T_max],
                            [C_max, F_max, T_max]])

Min_Angle_Array = np.array([[C_min, F_min, T_min],
                            [C_min, F_min, T_min],
                            [C_min, F_min, T_min],
                            [C_min, F_min, T_min]])

#- - Leg Servo Desired Angle Matrix - -#
Cda1 = float()
Cda2 = float()
Cda3 = float()
Cda4 = float()
Fda1 = float()
Fda2 = float()
Fda3 = float()
Fda4 = float()
Tda1 = float()
Tda2 = float()
Tda3 = float()
Tda4 = float()
# Cda1 = Coxa, Desired Angle, Leg one
Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                [Cda2, Fda2, Tda2],
                                [Cda3, Fda3, Tda3],
                                [Cda4, Fda4, Tda4]])

Pan_Angle = 0
Tilt_Angle = 0
Desired_Pan = 0
Desired_Tilt = 0
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#- - Bring Servo Motors Online - -#
pi = pigpio.pi()
# Create default PWM frequency for all the servos, 50Hz
DEFAULT_FREQ = 50
# Create a list of the GPIO pins that the servos are connected to
servos = [4, 5, 6, 7, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27]
# Initialize the servos
for pin in servos:
    pi.set_mode(pin, pigpio.OUTPUT)    
    pi.set_PWM_frequency(pin, DEFAULT_FREQ)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''
#- - Stand Up Sequence - -#
print("Please ensure Regis is laying flat and clear of obstacles, stand clear.", end="\r")
time.sleep(0.4)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear..", end="\r")
time.sleep(0.4)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear...", end="\r")
time.sleep(0.4)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear....", end="\r")
time.sleep(0.4)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear.....", end="\r")
time.sleep(0.4)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear......", end="\r")
time.sleep(0.4)
print("\nPreparing to move!")
time.sleep(1.5)
'''
# DEFAULT POSITION AT AWAKEN
#All shoulders square, Femurs Up, Tarsus Up
# Really need a way to move to this position slowly!!!!!
Ca1 = float(25)
Ca2 = float(-25)
Ca3 = float(25)
Ca4 = float(-25)
Fa1 = float(F_max)
Fa2 = float(F_max)
Fa3 = float(F_max)
Fa4 = float(F_max)
Ta1 = float(T_max)
Ta2 = float(T_max)
Ta3 = float(T_max)
Ta4 = float(T_max) 
Current_Array = np.array([[Ca1, Fa1, Ta1],
                          [Ca2, Fa2, Ta2],
                          [Ca3, Fa3, Ta3],
                          [Ca4, Fa4, Ta4]])

Desired_Angle_Array = Current_Array
Matrix_Update()
time.sleep(1.5)
'''
# All Tarsus Down
Desired_Angle_Array = np.array ([[25, F_max, 0],
                                 [-25, F_max, 0],
                                 [25, F_max, 0],
                                 [-25, F_max, 0]])   
Matrix_Update()
Current_Array = Matrix_Update.Angle_Array 
'''
#Stand
Desired_Angle_Array = np.array ([[25, 5, -20],
                                 [-25, 5, -20],
                                 [25, 5, -20],
                                 [-25, 5, -20]])   
Matrix_Update()
Current_Array = Matrix_Update.Angle_Array 

Desired_Angle_Array = np.array ([[25, 5, 0],
                                 [-25, 5, 0],
                                 [25, 5, 0],
                                 [-25, 5, 0]])   
Matrix_Update()
Current_Array = Matrix_Update.Angle_Array 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
'''                               MAIN PROGRAM                              '''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
while True:
    Main_Pgm_Answer = int(0)
    while Main_Pgm_Answer == 0:
        print("\n\n")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$                    MAIN PROGRAM --- LONG LIVE REGIS!                  $")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("\nSelect from the following:")
        print("  1) Wave Hello!")
        print("  2) Turn on Camera")     
        print("  3) Go to Default Position (all leg servos zero)")        
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
        
        Main_Pgm_Answer = int(input("Enter 1,2,3...\n"))
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 1: #Wave Hello 
        print("\nHello!\n")
        Final_Array = Current_Array
        Ca1 = Current_Array[0,0]
        Ca2 = Current_Array[1,0]
        Ca3 = Current_Array[2,0]
        Ca4 = Current_Array[3,0]
        Fa1 = Current_Array[0,1]
        Fa2 = Current_Array[1,1]
        Fa3 = Current_Array[2,1]
        Fa4 = Current_Array[3,1]
        Ta1 = Current_Array[0,2]
        Ta2 = Current_Array[1,2]
        Ta3 = Current_Array[2,2]
        Ta4 = Current_Array[3,2]
        Desired_Angle_Array = np.array ([[Ca1, F_max, T_max],
                                        [Ca2, Fa2, Ta2],
                                        [Ca3, Fa3, Ta3],
                                        [Ca4, Fa4, Ta4]])  
        Matrix_Update()
        #---------
        Speed = 0.0001
        #---------
        Ca1 = Current_Array[0,0]
        Ca2 = Current_Array[1,0]
        Ca3 = Current_Array[2,0]
        Ca4 = Current_Array[3,0]
        Fa1 = Current_Array[0,1]
        Fa2 = Current_Array[1,1]
        Fa3 = Current_Array[2,1]
        Fa4 = Current_Array[3,1]
        Ta1 = Current_Array[0,2]
        Ta2 = Current_Array[1,2]
        Ta3 = Current_Array[2,2]
        Ta4 = Current_Array[3,2]
        Current_Array = Matrix_Update.Angle_Array
        Desired_Angle_Array = np.array ([[C_max, F_max, T_max],
                                         [Ca2, Fa2, Ta2],
                                         [Ca3, Fa3, Ta3],
                                         [Ca4, Fa4, Ta4]]) 
        Matrix_Update()
        #---------
        Ca1 = Current_Array[0,0]
        Ca2 = Current_Array[1,0]
        Ca3 = Current_Array[2,0]
        Ca4 = Current_Array[3,0]
        Fa1 = Current_Array[0,1]
        Fa2 = Current_Array[1,1]
        Fa3 = Current_Array[2,1]
        Fa4 = Current_Array[3,1]
        Ta1 = Current_Array[0,2]
        Ta2 = Current_Array[1,2]
        Ta3 = Current_Array[2,2]
        Ta4 = Current_Array[3,2]
        Current_Array = Matrix_Update.Angle_Array
        Desired_Angle_Array = np.array ([[-10, F_max, T_max],
                                         [Ca2, Fa2, Ta2],
                                         [Ca3, Fa3, Ta3],
                                         [Ca4, Fa4, Ta4]]) 
        Matrix_Update()
        #---------
        Ca1 = Current_Array[0,0]
        Ca2 = Current_Array[1,0]
        Ca3 = Current_Array[2,0]
        Ca4 = Current_Array[3,0]
        Fa1 = Current_Array[0,1]
        Fa2 = Current_Array[1,1]
        Fa3 = Current_Array[2,1]
        Fa4 = Current_Array[3,1]
        Ta1 = Current_Array[0,2]
        Ta2 = Current_Array[1,2]
        Ta3 = Current_Array[2,2]
        Ta4 = Current_Array[3,2]
        Current_Array = Matrix_Update.Angle_Array
        Desired_Angle_Array = np.array ([[C_max, F_max, T_max],
                                         [Ca2, Fa2, Ta2],
                                         [Ca3, Fa3, Ta3],
                                         [Ca4, Fa4, Ta4]]) 
        Matrix_Update()
        #---------
        Ca1 = Current_Array[0,0]
        Ca2 = Current_Array[1,0]
        Ca3 = Current_Array[2,0]
        Ca4 = Current_Array[3,0]
        Fa1 = Current_Array[0,1]
        Fa2 = Current_Array[1,1]
        Fa3 = Current_Array[2,1]
        Fa4 = Current_Array[3,1]
        Ta1 = Current_Array[0,2]
        Ta2 = Current_Array[1,2]
        Ta3 = Current_Array[2,2]
        Ta4 = Current_Array[3,2]
        Current_Array = Matrix_Update.Angle_Array
        Desired_Angle_Array = np.array ([[0, F_max, T_max],
                                        [Ca2, Fa2, Ta2],
                                        [Ca3, Fa3, Ta3],
                                        [Ca4, Fa4, Ta4]]) 
        Matrix_Update()
        #---------
        Current_Array = Matrix_Update.Angle_Array
        Desired_Angle_Array = Final_Array
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array 
        #---------
        engine.say("Hello, greetings and salutations")
        engine.runAndWait()
        engine.say("I am Regis")
        engine.runAndWait()
        dummy = input("\npress enter to continue")
        Main_Pgm_Answer = 0
        break    
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 2: #Turn on Camera
        subprocess.call(['lxterminal', '-e', 'python /home/kennethmikolaichik/Camera/Picamera_with_OpenCV.py'])
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 3: #Default Position
        Desired_Angle_Array = np.array ([[0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0]])   
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 4: #Servo Angle Input
        Answer = None
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - - - - - - - Desired Angle Prompt- - - - - - - -#
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        print("Enter desired Angles from L to R, Top to Bottom:\n")
        print("- Servo Angle Matrix -")
        print("Leg1:  C1 F1 T1 ")
        print("Leg2:  C2 F2 T2 ")
        print("Leg3:  C3 F3 T3 ")
        print("Leg4:  C4 F4 T4 ")
        Cda1 = float(input("C1:"))
        Fda1 = float(input("F1:"))
        Tda1 = float(input("T1:"))
        Cda2 = float(input("C2:"))
        Fda2 = float(input("F2:"))
        Tda2 = float(input("T2:"))
        Cda3 = float(input("C3:"))
        Fda3 = float(input("F3:"))
        Tda3 = float(input("T3:"))
        Cda4 = float(input("C4:"))
        Fda4 = float(input("F4:"))
        Tda4 = float(input("T4:"))
        Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                        [Cda2, Fda2, Tda2],
                                        [Cda3, Fda3, Tda3],
                                        [Cda4, Fda4, Tda4]])
        print("You have selected:\n",Desired_Angle_Array)
        
        Answer = input("Enter y/n or 'q' to quit\nIs this Correct?\n")            
        if Answer == "q":
            Main_Pgm_Answer = 0
            break
        elif Answer == "y":
            Matrix_Update()
            Current_Array = Matrix_Update.Angle_Array
            print("\n\n Servo Angles:\n",Matrix_Update.Angle_Array)
            Answer2 = input("Again?\n 'y' or 'q' to quit\n")            
            if Answer2 == "q":
                Main_Pgm_Answer = 0
                break
            elif Answer == "y":
                continue

                continue
        elif Answer == "n":
            print(" ")
    while Main_Pgm_Answer == 5: #Desired Position Prompt
        
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - - - - - - -Desired Position Prompt- - - - - - -#
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - Desired Position Prompt - -#
        Dx = float()
        Dy = float()
        Dz = float()
        Desired_Position = [Dx, Dy, Dz]
        
        print("Enter desired position from current position as: x y z in meters")
        print("Looking down from above, +x is to the right, +y is forward")
        print("Enter x coordinate...", end="\r")
        Dx = input()
        print("Enter y coordinate...", end="\r")
        Dy = input()
        print("Enter z coordinate, for default enter 'h'...", end="\r")
        Dz = input()
        if Dz == 'h':
            Dz = 0.09
            
        #Calculates current position from current motor positions
        
        print("\nUNDER CONSTRUCTION! -SORRY-5.10.2023\n")
        dummy = input("press enter to continue")
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------  
    while Main_Pgm_Answer == 6: #Get Servo Angles       
        print(Current_Array)
        dummy = input("press enter to continue")
        Main_Pgm_Answer = 0
        break    
     #--------------------------------------------------------------------------    
    while Main_Pgm_Answer == 7: #Get Current Frames / Positions
        deg2rad = (math.pi/180)
        
        #- - Positional Data - -#

        Body_Frame = [0, 0, 0]
        [Bx, By, Bz] = Body_Frame
        #Center of body


        Head_Frame = Body_Frame + [Head_Offset_x, Head_Offset_y, Head_Offset_z]
        [Hx, Hy, Hz] = Head_Frame
        #Center of head

        #Leg 1 - Fwd RH. Quadrant I (+x,+y, z)
        C1_Angle = Current_Array[0,0]
        C1_Offset_x = Coxa_Length * math.cos(Current_Array[0,0])
        C1_Offset_y = Coxa_Length * math.cos(Current_Array[0,0])
        
        C1_Frame = Body_Frame + [C1_Offset_x, C1_Offset_y, 0]
        [Cx1, Cy1, Cz1] = C1_Frame
        #- - - - - -
        F1_Angle = Current_Array[0,1]
        F1_Frame = C1_Frame + [Femur_Length * math.cos(F1_Angle), 0, Femur_Length * math.sin(F1_Angle)]
        [Fx1, Fy1, Fz1] = F1_Frame
        #- - - - - -
        
        T1_Frame = [Tx1, Ty1, Tz1]
        #- - - - - -
        #Manipulator





        M1_Frame = [Mx1, My1, Mz1]
        #Leg2
        #- - - - - -
        #Manipulator
        M2_Frame = [Mx2, My2, Mz2]
        #- - - - - -
        C2_Frame = [Cx2, Cy2, Cz2]
        F2_Frame = [Fx2, Fy2, Fz2]
        T2_Frame = [Tx2, Ty2, Tz2]

        #Leg3
        #- - - - - -
        #Manipulator
        M3_Frame = [Mx3, My3, Mz3]
        #- - - - - -
        C3_Frame = [Cx3, Cy3, Cz3]
        F3_Frame = [Fx3, Fy3, Fz3]
        T3_Frame = [Tx3, Ty3, Tz3]

        #Leg4
        #- - - - - -
        #Manipulator
        M4_Frame = [Mx4, My4, Mz4]
        #- - - - - -
        C4_Frame = [Cx4, Cy4, Cz4]
        F1_Frame = [Fx4, Fy4, Fz4]
        T4_Frame = [Tx4, Ty4, Tz4]
          
        print("Positional Data:")
        print("Body_Frame =", Body_Frame)
        print("Head_Frame =", Head_Frame)
        print("Leg1:")
        print("Coxa 1 =", C1_Frame)
        print("Femur 1 =", F1_Frame)
        print("Tarsus 1 =", T1_Frame)
        print("Leg2:")
        print("Coxa 2 =", C2_Frame)
        print("Femur 2 =", F2_Frame)
        print("Tarsus 2 =", T2_Frame)
        print("Leg3:")
        print("Coxa 3 =", C3_Frame)
        print("Femur 3 =", F3_Frame)
        print("Tarsus 3 =", T3_Frame)
        print("Leg4:")
        print("Coxa 4 =", C4_Frame)
        print("Femur 4 =", F4_Frame)
        print("Tarsus 4 =", T4_Frame)


    
    
    
        print("\nUNDER CONSTRUCTION! -SORRY-5.10.2023\n")
        dummy = input("press enter to continue")
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------    
    while Main_Pgm_Answer == 8: #Get Current Leg Dimensions
        # - - Dimensional Computations - - #    

        deg2rad = (math.pi/180)
        #Leg1

        F1lr = Femur_Length * (math.cos(deg2rad*Current_Array[0,1]))#Leg1 Femur [i,1]
        F1lh = Femur_Length * (math.sin(deg2rad*Current_Array[0,1]))#Leg1 Femur [i,1]
        Theta_1 = deg2rad*Current_Array[0,1] + deg2rad*Current_Array[0,2]
        T1lr = Tarsus_Length * math.sin(Theta_1)
        T1lh = Tarsus_Length * math.cos(Theta_1)
        Reach_1r = F1lr + T1lr
        Reach_1h = F1lh + T1lh

        #Leg2
        F2lr = Femur_Length * math.cos(deg2rad*Current_Array[1,1])
        F2lh = Femur_Length * math.sin(deg2rad*Current_Array[1,1])
        Theta_2 = deg2rad*Current_Array[1,1] + deg2rad*Current_Array[1,2]
        T2lr = Tarsus_Length * math.sin(Theta_2)
        T2lh = Tarsus_Length * math.cos(Theta_2)
        Reach_2r = F2lr + T2lr
        Reach_2h = F2lh + T2lh

        #Leg3
        F3lr = Femur_Length * math.cos(deg2rad*Current_Array[2,1]) #Leg 1 Femur [i,1]
        F3lh = Femur_Length * math.sin(deg2rad*Current_Array[2,1]) #Leg 1 Femur [i,1]
        Theta_3 = deg2rad*Current_Array[2,1] + deg2rad*Current_Array[2,2]
        T3lr = Tarsus_Length * math.sin(Theta_3)
        T3lh = Tarsus_Length * math.cos(Theta_3)
        Reach_3r = F3lr + T3lr
        Reach_3h = F3lh + T3lh

        #Leg4
        F4lr = Femur_Length * math.cos(deg2rad*Current_Array[3,1]) #Leg 1 Femur [i,1]
        F4lh = Femur_Length * math.sin(deg2rad*Current_Array[3,1]) #Leg 1 Femur [i,1]
        Theta_4 = deg2rad*Current_Array[3,1] + deg2rad*Current_Array[3,2]
        T4lr = Tarsus_Length * math.sin(Theta_4)
        T4lh = Tarsus_Length * math.cos(Theta_4)
        Reach_4r = F4lr + T4lr
        Reach_4h = F4lh + T4lh
         
        # - - Positional Computations - - #      
        print("Where reach is the Hypotenuse of the Femur and Tarsus,")
        print("and z is the position above or below initial xy-plane.")
        print(f"Leg 1 reach: {Reach_1r:.3f}")
        print(f"Leg 1 z: {Reach_1h:.3f}")
        print(f"Leg 2 reach: {Reach_2r:.3f}")
        print(f"Leg 2 z: {Reach_2h:.3f}")
        print(f"Leg 3 reach: {Reach_3r:.3f}")
        print(f"Leg 3 z: {Reach_3h:.3f}")
        print(f"Leg 4 reach: {Reach_4r:.3f}")
        print(f"Leg 4 z: {Reach_4h:.3f}")
        print("\n")
        #---------
        dummy = input("press enter to continue")
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 9:
        #Sit
        Desired_Angle_Array = np.array ([[25, 80, -40],
                                         [-25, 80, -40],
                                         [25, 80, -40],
                                         [-25, 80, -40]])  
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array 

        Desired_Angle_Array = np.array ([[15, 80, -40],
                                        [-15, 80, -40],
                                        [15, 80, -40],
                                        [-15, 80, -40]]) 
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 10:
        #Stand

        speed = 0
        # Legs up
        Desired_Angle_Array = np.array ([[25, F_max, T_min],
                                         [-25, F_max, T_min],
                                         [25, F_max, T_min],
                                         [-25, F_max, T_min]])         
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array 
        
        # All Tarsus Down    
        Desired_Angle_Array = np.array ([[25, F_max, 0],
                                         [-25, F_max, 0],
                                         [25, F_max, 0],
                                         [-25, F_max, 0]])   
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array 
        
        # Stand
        Desired_Angle_Array = np.array ([[25, 5, -20],
                                         [-25, 5, -20],
                                         [25, 5, -20],
                                         [-25, 5, -20]])   
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array 

        Desired_Angle_Array = np.array ([[25, 20, 5],
                                         [-25, 20, 5],
                                         [25, 20, 5],
                                         [-25, 20, 5]])   
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array
        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 11:    
        speed = 0
        #Stand Tall
        Desired_Angle_Array = np.array ([[25, F_min, 70],
                                         [-25, F_min, 70],
                                         [25, F_min, 70],
                                         [-25, F_min, 70]])         
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array

        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 12:
        #Pan L & R
        #- -DEFINE PARAMETERS- -#
        position = 1500
        pi = pigpio.pi()
        #- - -MOTOR SETUP- - - -#
        pi.set_mode(22, pigpio.OUTPUT)
        pi.set_PWM_frequency(22, 50)
        pi.set_servo_pulsewidth(22, position) #sets pan to center(1500)
        pi.set_servo_pulsewidth(13, position) #sets pan to center(1500)
        #- - - - - - - - - - - -#
        while position <= 2250:    
            position = position -10
            degree = ((position-1500)/(1000))*90
            pi.set_servo_pulsewidth(22, position)
            print(f"ServoSignal:{position}, Degree:{degree:.1f}° ", end="\r")
            time.sleep(.1)
            if position <= 750:
                break
        while position >= 750:
            position = position +10
            degree = ((position-1500)/(1000))*90
            pi.set_servo_pulsewidth(22, position)
            print(f"ServoSignal:{position}, Degree:{degree:.1f}° ", end="\r")
            time.sleep(.1)
            if position >= 2250:
                break
        while position <= 2250:    
            position = position -10
            degree = ((position-1500)/(1000))*90
            pi.set_servo_pulsewidth(22, position)
            print(f"ServoSignal:{position}, Degree:{degree:.1f}° ", end="\r")
            time.sleep(.1)
            if position <= 1500:
                break
        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer == 13:
        # Camera configuration
        CAMERA_SPEED = 5
        WIDTH = 400
        HEIGHT = 400

        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Camera Control")

        # Camera position
        camera_x = WIDTH // 2
        camera_y = HEIGHT // 2

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Move camera based on arrow keys
                    if event.key == pygame.K_LEFT:
                        camera_x -= CAMERA_SPEED
                        Desired_Pan -=1
                        
                    elif event.key == pygame.K_RIGHT:
                        camera_x += CAMERA_SPEED
                        Desired_Pan +=1

                    elif event.key == pygame.K_UP:
                        camera_y -= CAMERA_SPEED
                        Desired_Tilt -=1

                    elif event.key == pygame.K_DOWN:
                        camera_y += CAMERA_SPEED
                        Desired_Tilt +=1

            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw camera position
            pygame.draw.circle(screen, (255, 0, 0), (camera_x, camera_y), 10)

            # Update the screen
            pygame.display.flip()
            
            # Update Servo Signal
            Pan_Update()
            Tilt_Update()

        # Quit the program
        pygame.quit()
        Main_Pgm_Answer = 0
        break     
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer >= 14: #Invalid Selection
        print("\nPlease Make a Valid Selection\n")
        dummy = input("press enter to continue")
        Main_Pgm_Answer = 0
        break
        
        