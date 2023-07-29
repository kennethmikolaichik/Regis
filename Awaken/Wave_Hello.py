"""Wave_Hello
Created by: Kenneth Mikolaichik
7.28.2023"""
from Matrix_Update import *
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def Wave_Hello():
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
    os.system('clear')
    Main_Pgm_Ans = 0
    return Main_Pgm_Ans

