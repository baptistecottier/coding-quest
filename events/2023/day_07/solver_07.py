"""
Type: Challenge
Year: 2023
Day: 07 - Snakes on a spaceship
"""


def preprocessing(
    puzzle_input: str
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Parses the puzzle input to extract fruits coordinates and movement
    directions. Returns a tuple of fruits list and moves list.
    """
    lines = puzzle_input.splitlines()

    fruits: list[tuple[int, int]] = []
    for fruit in lines[1].split():
        coords = tuple(map(int, fruit.split(',')))
        if len(coords) != 2:
            raise ValueError("Incorrect input!")
        fruits.append(coords)

    moves_to_dir: dict[str, tuple[int, int]] = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, -1),
        'D': (0, 1),
    }
    moves: list[tuple[int, int]] = [moves_to_dir[m] for m in lines[3]]

    return (fruits, moves)


def solver(
    fruits: list[tuple[int, int]],
    moves: list[tuple[int, int]]
) -> int:
    """
    Simulates a snake game, moving the snake according to moves and collecting
    fruits. Returns the final score.
    """
    level: int = len(fruits)
    dim: int = level // 4 + 7
    visited = [(0, 0)]
    snake_length = 1
    fruit = fruits.pop(0)
    score: int = 0

    while moves:
        (x, y) = visited[-1]
        (dx, dy) = moves.pop(0)
        nx = x + dx
        ny = y + dy
        if (
                not ((0 <= nx < dim) and (0 <= ny < dim)) or
                (nx, ny) in visited[-snake_length:]):
            break

        visited.append((nx, ny))

        if (nx, ny) == fruit:
            score += 100
            fruit = fruits.pop(0)
            snake_length += 1
        score += 1
    return score
