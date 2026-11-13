"""
Type: Challenge
Year: 2024
Day: 05 - Busy moon rovers
"""

import re


def preprocessing(puzzle_input: str):
    """
    Distance table between the named locations, and each rover journey as
    the indices of the locations it goes through.
    """
    table, paths = puzzle_input.split('\n\n')
    lines = table.split('\n', maxsplit=1)
    names = re.findall(r'(\w+)', lines[0])
    distances = [list(map(int, re.findall(r'(\s\d+)', line)))
                 for line in lines[1].splitlines()]
    journeys = [list(map(names.index, re.findall(r'(\w+)', line)[3:]))
                for line in paths.splitlines()]
    return distances, journeys


def solver(distances: list[list[int]], journeys: list[list[int]]):
    """
    Total distance travelled by the rovers along all their journeys.
    """
    yield sum(
        sum(distances[j[i]][j[i + 1]] for i in range(len(j) - 1))
        for j in journeys
    )
