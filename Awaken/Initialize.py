
"""Initialize
Created by: Kenneth Mikolaichik
5.8.2023"""
import os
from playsound import playsound
import subprocess
import math
import numpy as np
import pigpio
import time
import pyttsx3
import pygame
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''Gyroscope stuff'''
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Pan_Update(Pan_Angle, Desired_Pan):
    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value 
    if Desired_Pan >= P_max:
        Desired_Pan = P_max
    if Desired_Pan <= P_min:
        Desired_Pan = P_min
    
    #if less than desired angle
    if Pan_Angle < Desired_Pan:
        Pan_Angle +=1 #increase angle towards desired angle
    #if greater than desired angle
    if Pan_Angle > Desired_Pan:
        Pan_Angle -=1 #dencrease angle towards desired angle   
    
    PWM_Signal = ((1000 * Pan_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(22, PWM_Signal)

    Pan_Update.Pan_Angle = Pan_Angle

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Tilt_Update(Tilt_Angle, Desired_Tilt):
    # Limiting Program: keeps motors from attempting to move past physical stops
    # Replaces improper value with limit value
    if Desired_Tilt >= Ti_max:
        Desired_Tilt = Ti_max
    if Desired_Tilt <= Ti_min:
        Desired_Tilt = Ti_min
    
    #if less than desired angle
    if Tilt_Angle < Desired_Tilt:
        Tilt_Angle +=1 #increase angle towards desired angle
    #if greater than desired angle
    if Tilt_Angle > Desired_Tilt:
        Tilt_Angle -=1 #dencrease angle towards desired angle   
    
    PWM_Signal = ((1000 * Tilt_Angle) / 90) + 1500
    pi.set_servo_pulsewidth(13, PWM_Signal)

    Tilt_Update.Tilt_Angle = Tilt_Angle

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Matrix_Update():
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    #- - - - - - - - Matrix Update Program - - - - - - -#
    #- - - - - - - - - - - - - - - - - - - - - - - - - -#
    
    # This program is the main way the robot moves. Matrix 'C' of small movements
    # is created approaching the value of matrix 'B' the desired motor position.
    # Matrix 'B' is checked to be within limits of the min and max values, it is corrected if needed.
    # These two matricies are then added together, the signal is transmitted to the motors.
    # The process repeats itself until the desired position is reached or the counter overflows.
    
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
    # Creates Matrix 'C' which adds or subtracts 0.1 so that elements of 'A' approach 'B'
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
        A = np.round(A, decimals=2, out=None)

        time.sleep(Speed) #Speed Controller
        #DEBUGGUING# print(A,"Current Angles\n\n",C, "adjustment Array\n\n", B,"Desired Angles\n\n", "completed =",np.allclose(A, B, rtol=0.001, atol=0.005))    
        
        # Tracks Loop and prints the time it takes to the screen
        #Move_Time = Speed*Counter     
        #print(Counter)
        #print(f"{Move_Time:.2f}s",end="\r")
        Counter +=1
        
        #Counter Runaway
        if Counter >= 1500:
            A = np.round(A, decimals=2, out=None)
            Matrix_Update.Angle_Array = A
            print("ERROR - Move_Time timeout")
            Counter = 0
            time.sleep(0.25)
            break

        #Comapres A to B within tolerance of 0.003
        #if equal then stop movement.         
        if np.allclose(A, B, rtol=0.003, atol=0.007) == True: 
            A = np.round(A, decimals=2, out=None)
            Matrix_Update.Angle_Array = A
            Counter = 0           
            break 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
def Solve_Inverse_Kinematic():
    print("IS THIS RIGHT??")
    # Need to get inverse kinematic solver for here!!!!!
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
os.system('clear')
print("")
print("******************************************************")
print("*   REGIS,  R-0.1:  Created by Kenneth Mikolaichik   *")
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
print("Speed setting:", Speed)

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
#Boot up Sound File
#playsound('/home/kennethmikolaichik/Regis/Sounds/holy-smokes-its-me-regis-im-a-sexy-little-monkey.mp3')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#- - Stand Up Sequence - -#
print("Please ensure Regis is laying flat and clear of obstacles, stand clear.", end="\r")
time.sleep(0.2)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear..", end="\r")
time.sleep(0.2)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear...", end="\r")
time.sleep(0.2)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear....", end="\r")
time.sleep(0.2)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear.....", end="\r")
time.sleep(0.2)
print("Please ensure Regis is laying flat and clear of obstacles, stand clear......", end="\r")
time.sleep(0.2)
print("\nPreparing to move!")
time.sleep(1.5)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# DEFAULT POSITION AT AWAKEN
#All shoulders square, Femurs Up, Tarsus Up
# Really need a way to move to this position slowly or remember last position!!!!!
Ca1 = float(25)
Ca2 = float(-25)
Ca3 = float(25)
Ca4 = float(-25)
Fa1 = float(F_min)
Fa2 = float(F_min)
Fa3 = float(F_min)
Fa4 = float(F_min)
Ta1 = float(T_min)
Ta2 = float(T_min)
Ta3 = float(T_min)
Ta4 = float(T_min) 
Current_Array = np.array([[Ca1, Fa1, Ta1],
                          [Ca2, Fa2, Ta2],
                          [Ca3, Fa3, Ta3],
                          [Ca4, Fa4, Ta4]])
# Head to center
Pan_Angle = 0
Tilt_Angle = 0
Desired_Pan = 0
Desired_Tilt = 0

Matrix_Update()
Current_Array = Matrix_Update.Angle_Array 

Pan_Update(Pan_Angle, Desired_Pan)
Pan_Angle = Pan_Update.Pan_Angle
Tilt_Update(Tilt_Angle, Desired_Tilt)
Tilt_Angle = Tilt_Update.Tilt_Angle

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
'''                               MAIN PROGRAM                              '''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
while True:
    Main_Pgm_Answer = int(0)
    while Main_Pgm_Answer == 0:
        os.system('clear')
        print("\n")
        print("   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("   $                    MAIN PROGRAM --- LONG LIVE REGIS!                  $")
        print("   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("\nSelect from the following:")
        print("  1) Sit Down")
        print("  2) Turn on Camera")     
        print("  3) Go to Maintenance Position")        
        print("  4) Move Robot / Servo Angle Input Mode")
        print("  5) Desired Position Prompt")
        print("  6) Get Current Servo Angles")
        print("  7) Get Current Joint Positions")
        print("  8) Get Current Leg Dimensions")
        print("  9) Wave Hello!")
        print(" 10) Stand Up")
        print(" 11) Stand Tall")
        print(" 12) Pan Left & Right")
        print(" 13) Control Camera Head")
        print(" 14) Turn on Camera with Object Detection")
        print(" 15) Get Gyro Data")
        print(" 16) Real Time Motor Control")
        print(" 17) Play a song")
        print(" 18) Get Vibration Sensor Data")
        print(" 19) Freak Out")
        
        Main_Pgm_Answer = int(input("Enter 1,2,3...\n"))
    #--------------------------------------------------------------------------
    #Sit
    while Main_Pgm_Answer == 1:
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
        os.system('clear')
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    #Turn on Camera
    while Main_Pgm_Answer == 2:
        subprocess.call(['lxterminal', '-e', 'python /home/kennethmikolaichik/Regis/Awaken/Camera/Picamera_with_OpenCV.py'])
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    #Default Position / Maintenence Mode
    while Main_Pgm_Answer == 3:
        #Legs
        Desired_Angle_Array = np.array ([[0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0]])   
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array

        #Head
        Pan_Angle = 0
        Tilt_Angle = 0
        Desired_Pan = 0
        Desired_Tilt = 0
        # Update Servo Signals
        Pan_Update(Pan_Angle, Desired_Pan)
        Pan_Angle = Pan_Update.Pan_Angle
        Tilt_Update(Tilt_Angle, Desired_Tilt)
        Tilt_Angle = Tilt_Update.Tilt_Angle

        os.system('clear')
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    #Servo Angle Input
    while Main_Pgm_Answer == 4:
        Answer = None
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - - - - - - - Desired Angle Prompt- - - - - - - -#
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        os.system('clear')
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
        os.system('clear')
        print("You have selected:\n\n",Desired_Angle_Array)
        
        Answer = input("\nEnter y/n or 'q' to quit\n\nIs this Correct?\n")            
        if Answer == "q":
            Main_Pgm_Answer = 0
            break
        elif Answer == "y":
            Matrix_Update()
            Current_Array = Matrix_Update.Angle_Array
            os.system('clear')
            print("\n\n Actual Servo Angles:\n",Matrix_Update.Angle_Array)
            Answer2 = input("\nAgain?\n 'y' or 'q' to quit\n")            
            if Answer2 == "q":
                Main_Pgm_Answer = 0
                break
            elif Answer == "y":
                continue

                continue
        elif Answer == "n":
            print(" ")
    #--------------------------------------------------------------------------
    #Desired Position Prompt
    while Main_Pgm_Answer == 5:
        os.system('clear')
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
        print("Enter x coordinate...\n", end="\r")
        Dx = input()
        print("Enter y coordinate...\n", end="\r")
        Dy = input()
        print("Enter z coordinate, for default enter 'h'...\n", end="\r")
        Dz = input()
        if Dz == 'h':
            Dz = 0.09
            
        #Calculates current position from current motor positions
        
        print("\nUNDER CONSTRUCTION! -SORRY-5.10.2023\n")
        print("requires inverse kinematic solver to be functional")
        dummy = input("press enter to continue")
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------  
    #Get Servo Angles 
    while Main_Pgm_Answer == 6: 
        os.system('clear')

        
        
        '''
        # Set the environment variable with Current_Array data
        os.environ['CURRENT_ARRAY'] = repr(Current_Array)

        #launches the file in another window but it closes immediately
        os.chdir('/home/kennethmikolaichik/Regis/Awaken')
        subprocess.call(['lxterminal', '-e', 'python',  'Display_Servo_Angles.py'])
        os.chdir('/')
        os.system('clear')
        Main_Pgm_Answer = 0
        break 
        '''
        def trunc(values, decs=0):
            return np.trunc(values*10**decs)/(10**decs)

        Current_Array = np.round(Current_Array, decimals=2, out=None)
        print("- Servo Angle Matrix -")
        print(Current_Array)
        
        '''
        for value in Current_Array:
            print("{:.2f}".format(value))     
        '''
        

        dummy = input("\npress enter to continue")
        os.system('clear')
        Main_Pgm_Answer = 0
        break 
        
     #--------------------------------------------------------------------------    
    #Get Current Frames / Positions
    while Main_Pgm_Answer == 7:
        deg2rad = (math.pi/180)
        
        #- - Positional Data - -#
        Body_Frame = [0, 0, 0]
        [Bx, By, Bz] = Body_Frame
        #Center of body

        #!!!!!!!!!!!!!issue here
        #Head_Frame = Body_Frame + [Head_Offset_x, Head_Offset_y, Head_Offset_z]
        #[Hx, Hy, Hz] = Head_Frame
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
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------    
    #Get Current Leg Dimensions
    while Main_Pgm_Answer == 8:
        
        # - - Dimensional Computations - - #  
        deg2rad = (math.pi/180)
        #Leg1
        Theta_1 = Current_Array[0,2] + 90
        Theta_1rad = deg2rad * Theta_1
        Reach_1 = math.sqrt(math.pow(Femur_Length, 2) + math.pow(Tarsus_Length, 2) - (2*Femur_Length*Tarsus_Length*math.cos(Theta_1rad)))
        
        #Leg2
        Theta_2 = Current_Array[1,2] + 90
        Theta_2rad = deg2rad * Theta_2
        Reach_2 = math.sqrt(math.pow(Femur_Length, 2) + math.pow(Tarsus_Length, 2) - (2*Femur_Length*Tarsus_Length*math.cos(Theta_2rad)))
        
        #Leg3
        Theta_3 = Current_Array[2,2] + 90
        Theta_3rad = deg2rad * Theta_3
        Reach_3 = math.sqrt(math.pow(Femur_Length, 2) + math.pow(Tarsus_Length, 2) - (2*Femur_Length*Tarsus_Length*math.cos(Theta_3rad)))

        #Leg4
        Theta_4 = Current_Array[3,2] + 90
        Theta_4rad = deg2rad * Theta_4
        Reach_4 = math.sqrt(math.pow(Femur_Length, 2) + math.pow(Tarsus_Length, 2) - (2*Femur_Length*Tarsus_Length*math.cos(Theta_4rad)))
        
        # - - Positional Computations - - #  
        os.system('clear')    
        print("Where reach is the Hypotenuse of the Femur and Tarsus,")
        print("the reach is computed with the law of cosines.")
        print(" ")
        print(f"Leg 1 reach: {Reach_1:.3f} meters")
        print("-------------------")
        print(f"Leg 2 reach: {Reach_2:.3f} meters")
        print("-------------------")
        print(f"Leg 3 reach: {Reach_3:.3f} meters")
        print("-------------------")
        print(f"Leg 4 reach: {Reach_4:.3f} meters")
        print(" ")

        dummy = input("press enter to continue")
        os.system('clear')
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    #Wave Hello
    while Main_Pgm_Answer == 9:
        os.system('clear')
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
        playsound('/home/kennethmikolaichik/Regis/Sounds/hello-hi-nice-to-see-you.mp3')
        os.system('clear')
        Main_Pgm_Answer = 0
        break     
    #--------------------------------------------------------------------------
    #Stand
    while Main_Pgm_Answer == 10:
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
        os.system('clear')
        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    #Stand Tall
    while Main_Pgm_Answer == 11:
        Desired_Angle_Array = np.array ([[25, F_min, 70],
                                         [-25, F_min, 70],
                                         [25, F_min, 70],
                                         [-25, F_min, 70]])         
        Matrix_Update()
        Current_Array = Matrix_Update.Angle_Array
        os.system('clear')
        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    #Pan L & R
    while Main_Pgm_Answer == 12:
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

        os.system('clear')
        Main_Pgm_Answer = 0
        break 
    #--------------------------------------------------------------------------
    #Control Camera Head
    while Main_Pgm_Answer == 13:
        Desired_Pan = Pan_Angle
        Desired_Tilt = Tilt_Angle

        # Camera Window configuration
        CAMERA_SPEED = 1
        WIDTH = 200
        HEIGHT = 150

        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Camera Control")

        # Camera position
        camera_x = Pan_Angle + 100
        camera_y = Tilt_Angle + 95

        # Flags to track key presses
        moving_left = False
        moving_right = False
        moving_up = False
        moving_down = False

        # Main game loop
        running = True
        while running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
 
                if event.type == pygame.KEYDOWN:
                    # Set the corresponding flag when a key is pressed down
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        moving_right = True
                    elif event.key == pygame.K_UP:
                        moving_up = True
                    elif event.key == pygame.K_DOWN:
                        moving_down = True

                if event.type == pygame.KEYUP:
                    # Reset the corresponding flag when a key is released
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        moving_right = False
                    elif event.key == pygame.K_UP:
                        moving_up = False
                    elif event.key == pygame.K_DOWN:
                        moving_down = False


            # Update camera position based on the flags
            if moving_left:
                camera_x -= CAMERA_SPEED
                Desired_Pan -=1
                
            if moving_right:
                camera_x += CAMERA_SPEED
                Desired_Pan +=1
            if moving_up:
                camera_y -= CAMERA_SPEED
                Desired_Tilt +=1
            if moving_down:
                camera_y += CAMERA_SPEED
                Desired_Tilt -=1
            
            # Limit camera position red dot and align with actual angles
            if camera_x >= 190:
                camera_x = 190
                Desired_Pan = 90
            if camera_x <= 10:
                camera_x = 10
                Desired_Pan = -90

            if camera_y >= 140:
                camera_y = 140
                Desired_Tilt = -45
            if camera_y <= 15:
                camera_y = 15
                Desired_Tilt = 80

            # Clear the screen
            screen.fill((0, 0, 0))
            # Draw camera position red dot
            pygame.draw.circle(screen, (255, 0, 0), (camera_x, camera_y), 10)
            # Update the screen
            pygame.display.flip()

            # Update Servo Signals
            Pan_Update(Pan_Angle, Desired_Pan)
            Pan_Angle = Pan_Update.Pan_Angle
            Tilt_Update(Tilt_Angle, Desired_Tilt)
            Tilt_Angle = Tilt_Update.Tilt_Angle

            os.system('clear')
            print("\nUse the Camera Control Window and your keyboards arrow keys")
            print("")
            print("Pan Angle:", Pan_Angle)
            print("Tilt Angle:", Tilt_Angle)
            
            #-------- Debugging
            #print("")
            #print("Camera x-axis:", camera_x)
            #print("Camera y-axis:", camera_y)

            # control the speed of camera movement
            time.sleep(Speed)

        # Quit the program
        pygame.quit()
        Main_Pgm_Answer = 0
        break     
    #--------------------------------------------------------------------------
    #Tensorflow Object Detectrion and Classification
    while Main_Pgm_Answer == 14:
        os.chdir('/home/kennethmikolaichik/Regis/examples/lite/examples/object_detection/raspberry_pi')
        subprocess.call(['lxterminal', '-e', 'python detect.py'])
        os.chdir('/')
        os.system('clear')
        Main_Pgm_Answer = 0
        break  
    #--------------------------------------------------------------------------
    #Print Gyroscope Data To Screen
    while Main_Pgm_Answer == 15:
        os.chdir('/home/kennethmikolaichik/Regis/Awaken')
        subprocess.Popen(['lxterminal', '-e', 'python', 'Get_Gyro_Data.py'])  # Use Popen to allow separate terminal
        os.chdir('/')
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    #Real Time Leg Control
    while Main_Pgm_Answer == 16:
        os.system('clear')
        # - - - - - - - - - - - 
        #Break Current Servo Angles Array into independent variables
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
        
        Pgm16 = int(input("\nselect Leg 1, 2, 3 or 4\n"))
        if Pgm16 == 1:
            current_angle1 = Ta1
            current_angle2 = Fa1
            current_angle3 = Ca1
        elif Pgm16 == 2:  
            current_angle1 = Ta2
            current_angle2 = Fa2
            current_angle3 = Ca2      
        elif Pgm16 == 3:
            current_angle1 = Ta3
            current_angle2 = Fa3
            current_angle3 = Ca3
        elif Pgm16 == 4:
            current_angle1 = Ta4
            current_angle2 = Fa4
            current_angle3 = Ca4

        os.system('clear')
        print("Close window to exit")

        # Initialize Pygame
        pygame.init()
        angle_step = 1
        # Set up the screen and display
        WIDTH, HEIGHT = 400, 200
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Motor Angle Control")
        # Set up the clock for controlling frame rate
        clock = pygame.time.Clock()
        # Create boolean flags to track whether keys are pressed or not
        r_key_pressed = False
        f_key_pressed = False
        e_key_pressed = False
        d_key_pressed = False
        a_key_pressed = False
        s_key_pressed = False

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Continuous angle changes when keys are held down
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        r_key_pressed = True
                    elif event.key == pygame.K_f:
                        f_key_pressed = True
                    elif event.key == pygame.K_e:
                        e_key_pressed = True
                    elif event.key == pygame.K_d:
                        d_key_pressed = True
                    elif event.key == pygame.K_a:
                        a_key_pressed = True
                    elif event.key == pygame.K_s:
                        s_key_pressed = True
                # Stop changing angle when the keys are released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        r_key_pressed = False
                    elif event.key == pygame.K_f:
                        f_key_pressed = False
                    elif event.key == pygame.K_e:
                        e_key_pressed = False
                    elif event.key == pygame.K_d:
                        d_key_pressed = False
                    elif event.key == pygame.K_a:
                        a_key_pressed = False
                    elif event.key == pygame.K_s:
                        s_key_pressed = False

            # Update the motor angles based on continuous key presses
            if r_key_pressed: #Tibia Up
                current_angle1 += angle_step
                current_angle1 = min(current_angle1, T_max)  # Clamp angle to maximum value
            if f_key_pressed: #Tibia Down
                current_angle1 -= angle_step
                current_angle1 = max(current_angle1, T_min)  # Clamp angle to minimum value
            if e_key_pressed: #Femur Down
                current_angle2 += angle_step
                current_angle2 = min(current_angle2, F_max)  # Clamp angle to minimum value
            if d_key_pressed: #Femur Up
                current_angle2 -= angle_step
                current_angle2 = max(current_angle2, F_min)  # Clamp angle to maximum value
            if a_key_pressed: #Coxa Aft
                current_angle3 += angle_step
                current_angle3 = min(current_angle3, C_max)  # Clamp angle to maximum value
            if s_key_pressed: #Coxa Fwd
                current_angle3 -= angle_step
                current_angle3 = max(current_angle3, C_min)  # Clamp angle to minimum value
            
            # Clear the screen
            screen.fill((255, 255, 255))
            # Display the current motor angles on the screen
            font = pygame.font.Font(None, 24)
            angle_text1 = font.render(f"Tarsus: {current_angle1:.2f} degrees", True, (0, 0, 0))
            angle_text2 = font.render(f"Femur: {current_angle2:.2f} degrees", True, (0, 0, 0))
            angle_text3 = font.render(f"Coxa: {current_angle3:.2f} degrees", True, (0, 0, 0))
            screen.blit(angle_text1, (20, 20))
            screen.blit(angle_text2, (20, 60))
            screen.blit(angle_text3, (20, 100))
            
            # Load Current Array with variable values
            if Pgm16 == 1:     
                Ta1 = current_angle1
                Fa1 = current_angle2
                Ca1 = current_angle3
            elif Pgm16 == 2:  
                Ta2 = current_angle1
                Fa2 = current_angle2
                Ca2 = current_angle3      
            elif Pgm16 == 3:
                Ta3 = current_angle1
                Fa3 = current_angle2
                Ca3 = current_angle3
            elif Pgm16 == 4:
                Ta4 = current_angle1
                Fa4 = current_angle2
                Ca4 = current_angle3
            Current_Array = np.array([[Ca1, Fa1, Ta1],
                                      [Ca2, Fa2, Ta2],
                                      [Ca3, Fa3, Ta3],
                                      [Ca4, Fa4, Ta4]])
   
            # - - - Update Servo Signal / Move Robot - - - #
            Current_Array = Current_Array*Correction_Array
            #Debugging
            #print("Corrected Array Values - ACTUAL MOTOR ANGLE")
            #print(Current_Array)
            for i in range(3): #scans rows from L/R, top to bottom
                Angle = Current_Array[0,i]
                PWM_Signal = ((1000 * Angle) / 90) + 1500
                Pin = Servo_Array[0,i]
                pi.set_servo_pulsewidth(Pin, PWM_Signal)
               
                Angle = Current_Array[1,i]
                PWM_Signal = ((1000 * Angle) / 90) + 1500
                Pin = Servo_Array[1,i]
                pi.set_servo_pulsewidth(Pin, PWM_Signal)
                Angle = Current_Array[2,i]
                PWM_Signal = ((1000 * Angle) / 90) + 1500
                Pin = Servo_Array[2,i]
                pi.set_servo_pulsewidth(Pin, PWM_Signal)
                Angle = Current_Array[3,i]
                PWM_Signal = ((1000 * Angle) / 90) + 1500
                Pin = Servo_Array[3,i]
                pi.set_servo_pulsewidth(Pin, PWM_Signal)
            Current_Array = Current_Array*Correction_Array
                
            # Update the screen
            pygame.display.flip()
            # Control the frame rate
            clock.tick(30)

        # Quit the program  
        pygame.quit()
        dummy = input("\npress enter to continue")
        os.system('clear')
        Pgm16 = 0
        Main_Pgm_Answer = 0
        break    
    #--------------------------------------------------------------------------
    #Play a Song
    while Main_Pgm_Answer == 17:
        os.chdir('/home/kennethmikolaichik/Regis/Awaken')
        subprocess.Popen(['lxterminal', '-e', 'python', 'Play_Classical_Music.py'])  # Use Popen to allow separate terminal
        os.chdir('/')
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    #Get Vibration Data
    while Main_Pgm_Answer == 18:
        os.chdir('/home/kennethmikolaichik/Regis/Awaken')
        subprocess.Popen(['lxterminal', '-e', 'python', 'VibTest.py'])  # Use Popen to allow separate terminal
        os.chdir('/')
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    #Freak Out
    while Main_Pgm_Answer == 19:
        import random
        print("Enter number of times to freak out:")
        Freak_Count = int(input())
        
        os.system('clear')          
        #here is where the freak out happens
        while Freak_Count > 0:      
            print("- Servo Angle Matrix -")
            print("Leg1:  C1 F1 T1 ")
            print(f"       {Cda1:.1f} {Fda1:.1f} {Tda1:.1f}")
            print("Leg2:  C2 F2 T2 ")
            print(f"       {Cda2:.1f} {Fda2:.1f} {Tda2:.1f}")
            print("Leg3:  C3 F3 T3 ")
            print(f"       {Cda3:.1f} {Fda3:.1f} {Tda3:.1f}")
            print("Leg4:  C4 F4 T4 ")
            print(f"       {Cda4:.1f} {Fda4:.1f} {Tda4:.1f}")
        
            #Leg freak out parameters
            Cda1 = float(random.randrange(-90,90))
            Fda1 = float(random.randrange(-90,90))
            Tda1 = float(random.randrange(-90,90))
            Cda2 = float(random.randrange(-90,90))
            Fda2 = float(random.randrange(-90,90))
            Tda2 = float(random.randrange(-90,90))
            Cda3 = float(random.randrange(-90,90))
            Fda3 = float(random.randrange(-90,90))
            Tda3 = float(random.randrange(-90,90))
            Cda4 = float(random.randrange(-90,90))
            Fda4 = float(random.randrange(-90,90))
            Tda4 = float(random.randrange(-90,90))
            Desired_Angle_Array = np.array([[Cda1, Fda1, Tda1],
                                            [Cda2, Fda2, Tda2],
                                            [Cda3, Fda3, Tda3],
                                            [Cda4, Fda4, Tda4]])
            Matrix_Update()

            time.sleep(0.1)
            Freak_Count -= 1
            os.system('clear')
        
        Current_Array = Matrix_Update.Angle_Array    
        os.system('clear')
        Main_Pgm_Answer = 0
        break
    #--------------------------------------------------------------------------
    while Main_Pgm_Answer >= 20: #Invalid Selection
        print("\nPlease Make a Valid Selection\n")
        dummy = input("press enter to continue")
        os.system('clear')
        Main_Pgm_Answer = 0
        break
        
        