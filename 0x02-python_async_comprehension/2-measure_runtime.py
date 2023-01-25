#!/usr/bin/python3
'''
2. Run time for four parallel comprehensions
'''
import asyncio
import random
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''
    Import async_comprehension from the previous file and write a
    measure_runtime coroutine that will execute async_comprehension
    four times in parallel using asyncio.gather.

    measure_runtime should measure the total runtime and return it.

    Notice that the total runtime is roughly 10 seconds,
    explain it to yourself.
    '''
    t_0 = time.time()
    comp = [async_comprehension() for i in range(4)]
    await asyncio.gather(*comp)
    t_1 = time.time()
    return (t_1 - t_0)
    '''
    t0 = time.time()
    fcts = [async_comprehension() for i in range(4)]
    await asyncio.gather(*fcts)

    return time.time() - t0
    '''
