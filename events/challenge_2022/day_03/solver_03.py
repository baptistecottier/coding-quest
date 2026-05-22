"""
Type: Challenge
Year: 2022
Day: 03 - Tour the stars
"""

from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> list[list[int]]:
    """
    Converts puzzle input into a list of integer coordinates.
    """
    coordinates = [
        list(map(int, line.split()))
        for line in puzzle_input.splitlines()
        ]
    return coordinates


def solver(
    coordinates: list[list[int]]
) -> Iterator[int]:
    """
    Calculates total Euclidean distance traveled through 3D coordinates.
    """
    distance = 0
    x, y, z = 0, 0, 0
    while coordinates:
        tx, ty, tz = coordinates.pop(0)
        delta = int(((tx - x) ** 2 + (ty - y) ** 2 + (tz - z) ** 2) ** .5)
        distance += delta
        x, y, z = tx, ty, tz
    yield distance
