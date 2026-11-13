"""
Type: Challenge
Year: 2024
Day: 09 - Mining tunnels
"""

from collections import deque


def preprocessing(puzzle_input: str):
    """
    Open cells of each floor, elevator cells, and the coordinates of the
    bottom-right cell of the maps.
    """
    floors: dict[int, set[tuple[int, int]]] = {}
    elevators: set[tuple[int, int]] = set()
    x = y = 0
    for floor, note in enumerate(puzzle_input.split("\n\n")):
        clear: set[tuple[int, int]] = set()
        for y, line in enumerate(note.splitlines()):
            for x, c in enumerate(line):
                if c != '#':
                    clear.add((x, y))
                if c == '$':
                    elevators.add((x, y))
        floors[floor] = clear
    return floors, elevators, x, y


def solver(floors: dict[int, set[tuple[int, int]]],
           elevators: set[tuple[int, int]], w: int, h: int):
    """
    Fewest steps from (0, 1) to (w, h - 1) on the first floor, an elevator
    taking to the other floor at no cost.
    """
    visited: set[tuple[int, tuple[int, int]]] = set()
    neighbours = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    queue: deque[tuple[int, int, tuple[int, int]]] = deque([(0, 0, (0, 1))])
    while queue:
        d, f, (x, y) = queue.popleft()
        if (x, y) == (w, h - 1) and f == 0:
            return d
        for dx, dy in neighbours:
            nx = x + dx
            ny = y + dy
            if (f, (nx, ny)) in visited or (nx, ny) not in floors[f]:
                continue
            queue.append((d + 1, f, (nx, ny)))
            visited.add((f, (nx, ny)))
        if (x, y) in elevators and (1 - f, (x, y)) not in visited:
            queue.append((d, 1 - f, (x, y)))
            visited.add((1 - f, (x, y)))
    raise ValueError("No path to the exit")
