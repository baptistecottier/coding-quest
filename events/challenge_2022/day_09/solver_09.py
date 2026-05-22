"""
Type: Challenge
Year: 2022
Day: 09 - Lost in alien market
"""

from collections import deque
from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> tuple[set[tuple[int, int]], tuple[int, int], tuple[int, int]]:
    """
    Parses the puzzle input to extract wall positions and maze start/end
    points.
    """
    walls: set[tuple[int, int]] = set()
    lines = puzzle_input.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
    return (
        walls,
        (lines[0].index(' '), 0),
        (lines[-1].index(' '), len(lines) - 1)
    )


def solver(
    walls: set[tuple[int, int]],
    start: tuple[int, int],
    end: tuple[int, int]
) -> Iterator[int]:
    """
    Finds the shortest path length from start to end in a grid with obstacles.
    """
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            yield len(path)
            return

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if ((x + dx, y + dy) not in walls and 0 <= y + dy
                    and (x + dx, y + dy) not in seen):
                queue.append(path + [(x + dx, y + dy)])
                seen.add((x + dx, y + dy))
