# Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# В каждом решении нужно вывести время выполнения
# вычислений.

import multiprocessing
import time
from random import randint as ri

processes = [] 
start_time = time.time()

def create_array():    
    arr = [ri(1,100) for _ in range(1000000)]
    return arr

def sum_arr(arr):
    # arr = [ri(1,100) for _ in range(10)]
    res = 0
    for i in arr:
        res+=i
    return res

# array = create_array()

if __name__ == "__main__":
    process = multiprocessing.Process(target=sum_arr, args=[create_array()])
    processes.append(process)
    process.start()

    for process in processes:
        process.join() 
    print(sum_arr(create_array()))
    print(f"Sum counted in {time.time() - start_time:2f} seconds")
