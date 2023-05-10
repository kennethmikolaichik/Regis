"""Get_Positions
Created by: Kenneth Mikolaichik
5.10.2023"""

import math
import numpy as np
from Initialize import Body_Width
from Initialize import Body_Height
from Initialize import Body_Length
from Initialize import Coxa_Length
from Initialize import Femur_Length
from Initialize import Tarsus_Length
from Matrix_Update import Angle_Array
#- - - - - - - - - Positional Solver - - - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#
# The entirety of these calculations are based off of the body frame as inputs
# and the dimensions of the physical robot that are shown below.

# - - Dimensional Computations - - #    

deg2rad = (math.pi/180)
#Leg1

F1lr = Femur_Length * (math.cos(deg2rad*Angle_Array[0,1]))#Leg1 Femur [i,1]
F1lh = Femur_Length * (math.sin(deg2rad*Angle_Array[0,1]))#Leg1 Femur [i,1]
Theta_1 = deg2rad*Angle_Array[0,1] + deg2rad*Angle_Array[0,2]
T1lr = Tarsus_Length * math.sin(Theta_1)
T1lh = Tarsus_Length * math.cos(Theta_1)
Reach_1r = F1lr + T1lr
Reach_1h = F1lh + T1lh

#Leg2
F2lr = Femur_Length * np.cos(deg2rad*Angle_Array[1,1])
F2lh = Femur_Length * np.sin(deg2rad*Angle_Array[1,1])
Theta_2 = deg2rad*Angle_Array[1,1] + deg2rad*Angle_Array[1,2]
T2lr = Tarsus_Length * np.sin(Theta_2)
T2lh = Tarsus_Length * np.cos(Theta_2)
Reach_2r = F2lr + T2lr
Reach_2h = F2lh + T2lh

#Leg3
F3lr = Femur_Length * np.cos(deg2rad*Angle_Array[2,1]) #Leg 1 Femur [i,1]
F3lh = Femur_Length * np.sin(deg2rad*Angle_Array[2,1]) #Leg 1 Femur [i,1]
Theta_3 = deg2rad*Angle_Array[2,1] + deg2rad*Angle_Array[2,2]
T3lr = Tarsus_Length * np.sin(Theta_3)
T3lh = Tarsus_Length * np.cos(Theta_3)
Reach_3r = F3lr + T3lr
Reach_3h = F3lh + T3lh

#Leg4
F4lr = Femur_Length * np.cos(deg2rad*Angle_Array[3,1]) #Leg 1 Femur [i,1]
F4lh = Femur_Length * np.sin(deg2rad*Angle_Array[3,1]) #Leg 1 Femur [i,1]
Theta_4 = deg2rad*Angle_Array[3,1] + deg2rad*Angle_Array[3,2]
T4lr = Tarsus_Length * np.sin(Theta_4)
T4lh = Tarsus_Length * np.cos(Theta_4)
Reach_4r = F4lr + T4lr
Reach_4h = F4lh + T4lh
 
# - - Positional Computations - - #      
 
print(f"Leg 1 reach: {Reach_1r:.3f}")
print(f"Leg 1 z: {Reach_1h:.3f}")

print(f"Leg 2 reach: {Reach_2r:.3f}")
print(f"Leg 2 z: {Reach_2h:.3f}")

print(f"Leg 3 reach: {Reach_3r:.3f}")
print(f"Leg 3 z: {Reach_3h:.3f}")

print(f"Leg 4 reach: {Reach_4r:.3f}")
print(f"Leg 4 z: {Reach_4h:.3f}")

print("\n")
'''
###############LAST WORKING 5.9.2023

#- - - - - - - - - - - - - - - - - - - - - - - - - -#
#- - - - - - - - Positional Definitions- - - - - - -#
#- - - - - - - - - - - - - - - - - - - - - - - - - -#

#- - Positional Data - -#
Bx = float()
By = float()
Bz = float()
Body_Frame = [Bx, By, Bz]
#Center of body

Hx = float()
Hy = float()
Hz = float()
Head_Frame = [Hx, Hy, Hz]
#Center of head

#Leg1
#- - - - - -
#Manipulator
Mx1 = float()
My1 = float()
Mz1 = float()
M1_Frame = [Mx1, My1, Mz1]
#- - - - - -
Cx1 = float()
Cy1 = float()
Cz1 = float()
C1_Frame = [Cx1, Cy1, Cz1]
Fx1 = float()
Fy1 = float()
Fz1 = float()
F1_Frame = [Fx1, Fy1, Fz1]
Tx1 = float()
Ty1 = float()
Tz1 = float()
T1_Frame = [Tx1, Ty1, Tz1]

#Leg2
#- - - - - -
#Manipulator
Mx2 = float()
My2 = float()
Mz2 = float()
M2_Frame = [Mx2, My2, Mz2]
#- - - - - -
Cx2 = float()
Cy2 = float()
Cz2 = float()
C2_Frame = [Cx2, Cy2, Cz2]
Fx2 = float()
Fy2 = float()
Fz2 = float()
F2_Frame = [Fx2, Fy2, Fz2]
Tx2 = float()
Ty2 = float()
Tz2 = float()
T2_Frame = [Tx2, Ty2, Tz2]

#Leg3
#- - - - - -
#Manipulator
Mx3 = float()
My3 = float()
Mz3 = float()
M3_Frame = [Mx3, My3, Mz3]
#- - - - - -
Cx3 = float()
Cy3 = float()
Cz3 = float()
C3_Frame = [Cx3, Cy3, Cz3]
Fx3 = float()
Fy3 = float()
Fz3 = float()
F3_Frame = [Fx3, Fy3, Fz3]
Tx3 = float()
Ty3 = float()
Tz3 = float()
T3_Frame = [Tx3, Ty3, Tz3]

#Leg4
#- - - - - -
#Manipulator
Mx4 = float()
My4 = float()
Mz4 = float()
M4_Frame = [Mx4, My4, Mz4]
#- - - - - -
Cx4 = float()
Cy4 = float()
Cz4 = float()
C4_Frame = [Cx4, Cy4, Cz4]
Fx4 = float()
Fy4 = float()
Fz4 = float()
F1_Frame = [Fx4, Fy4, Fz4]
Tx4 = float()
Ty4 = float()
Tz4 = float()
T4_Frame = [Tx4, Ty4, Tz4]
  
print("\nHave a nice day\n\n")
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
'''






