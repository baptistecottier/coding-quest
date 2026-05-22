"""
Type: Challenge
Year: 2022
Day: 07 - Check the heat shields
"""

from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> tuple[int, list[list[tuple[int, int]]]]:
    """
    Preprocesses the puzzle input into a height and a list of intervals per
    row.
    """
    lines = puzzle_input.splitlines()
    if len(lines) < 10:
        w: int = 10
        h: int = 10
    elif len(lines) < 100:
        w = 100
        h = 100
    else:
        w, h = 20_000, 100_000

    intervals: list[list[tuple[int, int]]] = [[] for _ in range(w)]
    for line in lines:
        sx, sy, nx, ny = map(int, line.split())
        for x in range(sx, sx + nx):
            intervals[x].append((sy, sy + ny - 1))
    return (h, intervals)


def solver(
    h: int,
    occupied: list[list[tuple[int, int]]]
) -> Iterator[int]:
    """
    Calculates the total number of uncovered positions for each set of
    occupied intervals within a range of length h.
    """
    total = 0
    for intervals in occupied:
        uncovered = h
        intervals = sorted(intervals, key=lambda x: x[0])
        if intervals:
            s1, e1 = intervals.pop(0)
            while intervals:
                s2, e2 = intervals.pop(0)
                if s2 > e1:
                    uncovered -= (e1 - s1 + 1)
                    s1, e1 = s2, e2
                elif e1 < e2:
                    e1 = e2
            uncovered -= (e1 - s1 + 1)
        total += uncovered
    yield total
