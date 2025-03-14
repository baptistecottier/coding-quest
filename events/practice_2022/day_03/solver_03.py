"""Coding Quest - Practice 2022 - Day 03 - Survey an asteroid belt"""


from collections import deque
from itertools import product


def preprocessing(puzzle_input):
    """
    Parse puzzle input into a list of lists of integers, where each integer is converted from a
    space-separated string.
    """
    return [[int(item) for item in line.split()] for line in puzzle_input.splitlines()]


def solver(grid):
    """
    Calculate the average density of comets in the grid.

    This function iterates through each cell in the grid, identifies comets (non-zero values),
    and computes the total density of all comets. The average density is then calculated by
    dividing the total density by the number of comets.

    Args:
        grid (list): A 2D list representing the grid with comet densities.

    Returns:
        int: The average density of comets (total density divided by number of comets).
    """
    n_comets = 0
    density = 0
    size = len(grid)
    seen = set()
    for x, y in product(range(size), repeat = 2):
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if grid[y][x] != 0:
            n_comets += 1
            density += compute_asteroid_density(x, y, grid, seen)
    return density // n_comets


def compute_asteroid_density(x, y, grid, seen):
    """
    Compute the total density of an asteroid cluster starting from a given position.

    This function calculates the density by exploring the grid using BFS (Breadth-First Search),
    adding up the density values of all connected non-zero cells.

    Args:
        x (int): The x-coordinate (column) of the starting position.
        y (int): The y-coordinate (row) of the starting position.
        grid (List[List[int]]): A 2D grid representing the asteroid field.
        seen (set): A set of coordinates that have already been visited.

    Returns:
        int: The total density of the connected asteroid cluster.
    """
    density = grid[y][x]
    size = len(grid)
    queue = deque()
    for dx, dy in [(x + 1, y), (x, y + 1)]:
        if 0 <= dx < size and 0 <= dy < size:
            queue.append((dx, dy))
            seen.add((dx, dy))
    while queue:
        tx, ty = queue.popleft()
        if grid[ty][tx] != 0:
            density += grid[ty][tx]
            for dx, dy in [(tx - 1, ty), (tx + 1, ty), (tx, ty - 1), (tx, ty + 1)]:
                if (dx, dy) not in seen and 0 <= dx < size and 0 <= dy < size:
                    queue.append((dx, dy))
                    seen.add((dx, dy))
    return density
