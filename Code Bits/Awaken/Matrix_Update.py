"""Matrix_Update
Created by: Kenneth Mikolaichik
5.10.2023"""

import time
import numpy as np
import pigpio
from Initialize import Speed
from Initialize import Angle_Array
from Initialize import Desired_Angle_Array
from Initialize import Min_Angle_Array
from Initialize import Max_Angle_Array
from Initialize import Correction_Array
from Initialize import Servo_Array
pi = pigpio.pi()
#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - - - - - Matrix Update Program - - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#


A = Angle_Array
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
# The program will then halt according to the value of 'Speed' (line 9)
# The process repeats until 'A' == 'B', within tolerance.
Counter = 1
Move_Time = 0 
while np.allclose(A, B, rtol=0.001, atol=0.001) == False: 
    
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
    
    # - - - Update servo signal - - - #
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
    #Debugging#    print(A,"Current Angles\n\n",C, "adjustment Array\n\n", B,"Desired Angles\n\n", "completed =",np.allclose(A, B, rtol=0.001, atol=0.001))    
    Move_Time = Speed*Counter     
    print(f"{Move_Time:.2f}s",end="\r")
    Counter +=1
    #Comapres A to B within tolerance of 0.001
    #if equal then stop movement. 
    if Counter >= 1500:
        print("ERROR - Move_Time timeout")
        time.sleep(1)
        break
    
    if np.allclose(A, B, rtol=0.001, atol=0.005) == True:
        #Set all Arrays Equal    
        Angle_Array = B
        A = Angle_Array
        print("\n Servo Angles:\n",Angle_Array)
        Counter = 0
        break