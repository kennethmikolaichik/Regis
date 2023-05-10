"""Main_Menu
Created by: Kenneth Mikolaichik
5.10.2023"""
import time
import numpy as np
import subprocess

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
            subprocess.run(["python", "Matrix_Update.py"])
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
        
        