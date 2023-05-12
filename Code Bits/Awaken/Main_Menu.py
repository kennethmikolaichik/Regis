"""Main_Menu
Created by: Kenneth Mikolaichik
5.10.2023"""
import time
import numpy as np
import subprocess


def Matrix_Update():
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
        '''
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
        '''
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
    
    
    
while True:
    Main_Pgm_Answer = int(0)
    while Main_Pgm_Answer == 0:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("                    MAIN PROGRAM --- LONG LIVE REGIS!                    ")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("\nSelect from the following:\n")
        print("  • Servo Angle Input")
        print("  • Desired Position Prompt")
        print("  • Get Current Positions")
        Main_Pgm_Answer = int(input("Enter 1,2,3...\n"))
    
    
    
    while Main_Pgm_Answer == 1:
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
        Answer = input("Enter 'q' to quit\nIs this Correct? Y/N\nenter Y or N\n")            
        if Answer == "q":
            Main_Pgm_Answer = 0
            break
        elif Answer == "y" or "Y":
            import Matrix_Update
            Main_Pgm_Answer = 0
        elif Answer == "n" or "N":
            print(" ")

    
    
    while Main_Pgm_Answer == 2:
        print("\nUNDER CONSTRUCTION! -SORRY-5.10.2023\n")
        time.sleep(1)
        Main_Pgm_Answer = 0
            
        '''
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - - - - - - -Desired Position Prompt- - - - - - -#
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - Desired Position Prompt - -#
        Dx = float()
        Dy = float()
        Dz = float()
        Desired_Position = [Dx, Dy, Dz]
        
        print("Enter desired position as: x y z in meters")
        print("Looking down from above, +x is to the right, +y is forward")
        print("Enter x coordinate...", end="\r")
        Dx = input()
        print("Enter y coordinate...", end="\r")
        Dy = input()
        print("Enter z coordinate, for default enter 'h'...", end="\r")
        Dz = input()
        if Dz == 'h':
            Dz = 0.09
        '''
        
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        #- - - - - - -Inverse Kinematic Solver - - - - - - -#
        #- - - - - - - - - - - - - - - - - - - - - - - - - -#
        '''
        ???
        ??? Need to get inverse kinematic solver for here!!!!!
        ???
        ???
        ???
        ???
        ???
        ???
        ???
        '''
        break
        
    while Main_Pgm_Answer == 3:
        subprocess.run(["python", "Get_Positions.py"])
        Main_Pgm_Answer = 0
        break
        
    while Main_Pgm_Answer >= 4:
        print("\nPlease Make a Valid Selection\n")
        time.sleep(1)
        Main_Pgm_Answer = 0
        break
        
        