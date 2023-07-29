def Engage():
    from Definitions import Current_Array
    import pigpio
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
    
    Desired_Angle_Array = Current_Array
    Matrix_Update.Matrix_Update()
    time.sleep(1.5)
    
    # All Tarsus Down
    Desired_Angle_Array = np.array ([[25, F_max, 0],
                                     [-25, F_max, 0],
                                     [25, F_max, 0],
                                     [-25, F_max, 0]])   
    Matrix_Update()
    Current_Array = Matrix_Update.Angle_Array 

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
    Current_Array = Matrix_Update.Matrix_Update.Angle_Array 
    '''
