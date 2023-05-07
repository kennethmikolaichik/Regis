"""PWM_to_Angle
Created by: Kenneth Mikolaichik
5.6.2023"""
Signal = float(input("Enter PWM Signal value:"))
Angle = ((Signal-1500)/(1000))*90
print(Angle)