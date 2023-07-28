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
