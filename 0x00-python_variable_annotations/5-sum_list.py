#!/usr/bin/env python3
"""
Write a type-annotated function sum_list which takes list input_list of floats
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    returns the sum of the list of floats
    """
    return sum(input_list)
