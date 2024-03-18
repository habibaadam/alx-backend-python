#!/usr/bin/env python3
"""function that returns an asyncio.task"""


import asyncio
import random


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Creates and returns a task"""
    task = asyncio.create_task(wait_random(max_delay))
    return task
