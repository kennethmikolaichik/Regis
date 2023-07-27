"""Angle_to_PWM
Created by: Kenneth Mikolaichik
5.6.2023"""
Angle = float(input("Enter Angle:"))
PWM_Signal = ((1000 * Angle) / 90) + 1500
print(PWM_Signal)