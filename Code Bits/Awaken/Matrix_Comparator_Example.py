# -*- coding: utf-8 -*-
"""
Created on Sun May  7 00:42:12 2023

@author: kenne
"""
import numpy as np

A = np.array([[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]])

B = np.array([[2, 2, 2],
              [2, 2, 2],
              [2, 2, 2],
              [2, 2, 2]])

C = np.array([[3, 3, 3],
              [3, 3, 3],
              [3, 3, 3],
              [3, 3, 3]])

I = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1],
              [0, 0, 0]])

E = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])

D = B+E

# Combes through columns of 'A' and adds 1 until Column 'A' = Column 'E'
# Where i is the number of Rows of 'A'
#A = Initial Array
#B = Target Array

for i in range(3):
    while A[0,i] < B[0,i]:
        A[0,i] +=1
    while A[0,i] > B[0,i]:
        A[0,i] -=1
    while A[1,i] < B[1,i]:
        A[1,i] +=1
    while A[1,i] > B[1,i]:
        A[1,i] -=1
    while A[2,i] < B[2,i]:
        A[2,i] +=1
    while A[2,i] > B[2,i]:
        A[2,i] -=1
    while A[3,i] < B[3,i]:
        A[3,i] +=1
    while A[3,i] > B[3,i]:
        A[3,i] -=1
print(A)














