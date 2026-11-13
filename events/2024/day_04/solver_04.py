"""
Type: Challenge
Year: 2024
Day: 04 - Closest star systems
"""

import re
from itertools import combinations


def preprocessing(puzzle_input: str):
    """
    X, Y and Z coordinates of each star system, skipping its name and
    distance.
    """
    pattern = r'.+\s{2}-?\d+\.\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)'
    return [
        (float(x), float(y), float(z))
        for x, y, z in re.findall(pattern, puzzle_input)]


def solver(star_systems: list[tuple[float, float, float]]):
    """
    Distance between the two closest star systems, to 3 decimal places.
    """
    return round(
        min(
            sum((tb - ta) ** 2 for ta, tb in zip(ssa, ssb)) ** .5
            for ssa, ssb in combinations(star_systems, 2)), 3)
