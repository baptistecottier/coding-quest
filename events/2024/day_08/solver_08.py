"""
Type: Challenge
Year: 2024
Day: 08 - Connecting cities
"""

from functools import lru_cache


def preprocessing(puzzle_input: str):
    """
    Distance to cover and the set of available lengths.
    """
    lines = puzzle_input.splitlines()
    distance = int(lines[0])
    options = frozenset(map(int, lines[1].split(',')))
    return distance, options


def solver(distance: int, options: frozenset[int]):
    """
    Number of ways to cover the distance with the available lengths.
    """
    return count_options(distance, options)


@lru_cache
def count_options(distance: int, options: frozenset[int]):
    """
    Number of ordered sequences of options adding up exactly to distance.
    """
    if distance == 0:
        return 1
    if distance < 0:
        return 0
    return sum(count_options(distance - opt, options) for opt in options)
