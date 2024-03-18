#!/usr/bin/env python3
"""Contains a function that returns list of delays"""

import asyncio
import random
from typing import List, Callable


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    an async function that returns the list of delays in an ascending
    order
    """
    total_delays: List[float] = await asyncio.gather(
        *(wait_random(max_delay) for h in range(n))
        )
    return sorted(total_delays)
