# -*- coding: utf-8 -*-
"""Angle_to_PWM
Created on Fri Apr 21 14:46:54 2023

@author: Kenneth Mikolaichik
"""
#Uncomment for debugging
#import time

Angle = int()
S_Signal = float()
#for leg 1 and leg 3 use 'Angle'.
#for legs 2 and 4 use 'Inverted_Angle' or just '-Angle'.
#As physical hardware, Legs 1 & 2 are mirror images of each other.
#Leg 1 is front and leg 2 is back.
#Same goes for legs 3 and 4.
#Leg 3 is front and 4 is back.
#Odd front, even back, 1 is fwd RH.
Inverted_Angle = -Angle
S_Signal = ((1000 * Angle) / 90) + 500
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""Test code to debug angle to PWM Signal converter"""
#Angle = 0
#while True:
#    time.sleep(.5)
#    Angle = Angle -1
#    S_Signal = ((1000 * Angle) / 90) + 1500
#    print ("standard", S_Signal, Angle)
#    Inverted_Angle = -Angle
#    S_Signal = ((1000 * Inverted_Angle) / 90) + 1500
#    print ("inverted", S_Signal, Inverted_Angle)

