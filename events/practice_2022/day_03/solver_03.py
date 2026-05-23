"""
Type: Practice
Year: 2022
Day: 03 - Survey an asteroid belt
"""

from collections import deque
from itertools import product


def preprocessing(
    puzzle_input: str
) -> list[list[int]]:
    """
    Parse puzzle input into a list of lists of integers, where each integer is
    converted from a space-separated string.
    """
    return [
        [int(item) for item in line.split()]
        for line in puzzle_input.splitlines()]


def solver(grid: list[list[int]]) -> int:
    """
    Calculates and yields the average density of comets in the given grid.
    """
    n_comets = 0
    density = 0
    size = len(grid)
    seen: set[tuple[int, int]] = set()
    for x, y in product(range(size), repeat=2):
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if grid[y][x] != 0:
            n_comets += 1
            density += compute_asteroid_density(x, y, grid, seen)
    return density // n_comets


def compute_asteroid_density(
    x: int,
    y: int,
    grid: list[list[int]],
    seen: set[tuple[int, int]]
) -> int:
    """
    Calculates the total density of connected non-zero asteroids starting from
    (x, y) in the grid, marking visited cells in 'seen'.
    """
    density = grid[y][x]
    size = len(grid)
    queue: deque[tuple[int, int]] = deque()
    for dx, dy in [(x + 1, y), (x, y + 1)]:
        if 0 <= dx < size and 0 <= dy < size:
            queue.append((dx, dy))
            seen.add((dx, dy))
    while queue:
        tx, ty = queue.popleft()
        if grid[ty][tx] != 0:
            density += grid[ty][tx]
            for dx, dy in [
                    (tx - 1, ty), (tx + 1, ty),
                    (tx, ty - 1), (tx, ty + 1)]:
                if (dx, dy) not in seen and 0 <= dx < size and 0 <= dy < size:
                    queue.append((dx, dy))
                    seen.add((dx, dy))
    return density
