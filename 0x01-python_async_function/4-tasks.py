#!/usr/bin/env python3
'''4. Tasks'''
import asyncio
import random
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''
    Import wait_random from the previous python file that you’ve
    written and write an async routine called wait_n that takes in
    2 int arguments (in this order): n and max_delay. You will spawn
    wait_random n times with the specified max_delay.
    wait_n should return the list of all the delays (float values).
    The list of the delays should be in ascending order without using sort()
    because of concurrency.
    '''
    result = [task_wait_random(max_delay) for i in range(n)]
    lists = []
    for i in asyncio.as_completed(result):
        li = await i
        lists.append(li)
    # await asyncio.sleep(max_delay)
    #x = random.sample(lists, len(lists))
    return lists
