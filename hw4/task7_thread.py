import threading
import time
from random import randint as ri


threads = [] 
start_time = time.time()


def create_array():    
    arr = [ri(1,100) for _ in range(1000000)]
    return arr

def sum_arr(arr):
    res = 0
    for i in arr:
        res+=i
    return res

thread = threading.Thread(target=sum_arr, args=[create_array()])
threads.append(thread)
thread.start()

for thread in threads:
    thread.join()  
print(sum_arr(create_array()))
print(f"Sum counted in {time.time() - start_time:2f} seconds")
