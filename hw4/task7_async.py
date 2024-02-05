from random import randint as ri
import time
import asyncio

start_time = time.time()


async def create_array():    
    arr = [ri(1,100) for _ in range(1000000)]
    return arr

async def sum_arr():
    res = 0
    for i in await create_array():
        res+=i
    return res

if __name__=='__main__':
    asyncio.run(sum_arr())
    print(f"Sum counted in {time.time() - start_time:2f} seconds")
