"""Initialize
Created by: Kenneth Mikolaichik
5.7.2023"""
import time
import numpy as np

V = np.array([[0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0]])

A = np.array([[1.0, 1.0, 1.0],
              [1.0, 1.0, 1.0],
              [1.0, 1.0, 1.0],
              [1.0, 1.0, 1.0]])

B = np.array([[2, -2, -2],
              [2, 2, -2],
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

E = np.array([[1.0, -2.0, -3.0],
              [4.0, 5.0, -6.0],
              [7.0, 8.0, 9.0],
              [10.0, 11.0, 12.0]])

D = B+E

# Combes through columns of 'A' and adds 1 until Column 'A' = Column 'E'
# Where i is the number of Rows of 'A'
#A = Initial Array
#B = Target Array
'''
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
'''
'''
while np.array_equal(A, E) == False:
    for i in range(3):
        if A[0,i] < E[0,i]:
            V[0,i] +=.1
        if A[1,i] < E[1,i]:
            V[1,i] +=.1
        if A[2,i] < E[2,i]:
            V[2,i] +=.1
        if A[3,i] < E[3,i]:
            V[3,i] +=.1

    A = A+V

    V = np.array([[0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0]])
    print(A)
    time.sleep(0.3)
    if np.array_equal(A, E) == True:
        break
print(A)        
print(np.array_equal(A, E))
'''

while np.allclose(A, E, rtol=0.1, atol=0.1) == False:
    for i in range(3):
        if A[0,i] < E[0,i]:
            V[0,i] +=.1
        if A[0,i] > E[0,i]:
            V[0,i] -=.1    
        if A[1,i] < E[1,i]:
            V[1,i] +=.1
        if A[1,i] > E[1,i]:
            V[1,i] -=.1 
        if A[2,i] < E[2,i]:
            V[2,i] +=.1
        if A[2,i] > E[2,i]:
            V[2,i] -=.1 
        if A[3,i] < E[3,i]:
            V[3,i] +=.1
        if A[3,i] > E[3,i]:
            V[3,i] -=.1 
    A = A+V

    V = np.array([[0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0]])
    print(A, np.allclose(A, E, rtol=0.1, atol=0.1))
    time.sleep(0.1)
    if np.allclose(A, E, rtol=0.1, atol=0.1) == True:
        break
print(A)        
print(np.allclose(A, E, rtol=0.1, atol=0.1))











