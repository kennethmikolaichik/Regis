import os
from time import sleep
count = 0
while count < 1000000:
    print('test string')
    
    
    
    current_array = list(map(int, os.environ["CURRENT_ARRAY"].split(',')))

    print("Received current_array:", current_array)
    
    
    
    sleep(.25)
    os.system('clear')
    count +=1


