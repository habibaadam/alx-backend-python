#!/usr/bin/env python3
"""Contains a function that returns list of delays or coroutines"""

import asyncio
from typing import List, Callable


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    an async function that returns the list of delays in an ascending
    order, but with an imported function from 3-tasks.py
    """
    total_delays: List[float] = await asyncio.gather(
        *(task_wait_random(max_delay) for h in range(n))
    )
    return sorted(total_delays)
