#!/usr/bin/env python3
"""Contains an aysnc function to calculate total execution time"""

import time
import asyncio


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    this function measures the total execution time of the imported
    wait_n function
    """
    start_time: float = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end_time: float = time.perf_counter()
    total_time = end_time - start_time
    return total_time / n
