"""
Type: Challenge
Year: 2023
Day: 01 - Inventory check
"""

from collections import defaultdict
from math import prod
from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> dict[str, int]:
    """
    Parses the puzzle input and returns a dictionary mapping each item to its
    total count.
    """
    items: dict[str, int] = defaultdict(int)
    for line in puzzle_input.splitlines():
        _, n, item = line.split(' ')
        items[item] += int(n)
    return items


def solver(
    items: dict[str, int]
) -> Iterator[int]:
    """
    Yields the product of each item's quantity modulo 100 from the input
    dictionary.
    """
    yield prod(qty % 100 for qty in items.values())
