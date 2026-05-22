"""
Type: Challenge
Year: 2023
Day: 06 - Solver 06
"""


def preprocessing(
    puzzle_input: str
) -> list[tuple[float, float, float, float]]:
    """
    Parse puzzle input into list of rectangle tuples (x, y, width, height).
    """
    asteroids: list[tuple[float, float, float, float]] = []
    for line in puzzle_input.splitlines():
        asteroid = tuple(map(float, line.split()))
        if len(asteroid) != 4:
            raise ValueError("Incorrect input format!")
        asteroids.append(asteroid)
    return asteroids


def solver(
        asteroids: list[tuple[float, float, float, float]]
) -> str:
    """
    Find the empty position in the region not covered by any asteroid
    trajectory.
    """
    region_size = 8 if len(asteroids) < 20 else 100
    space: set[tuple[int, int]] = {
        (x, y)
        for x in range(region_size)
        for y in range(region_size)}
    for ax, ay, sx, sy in asteroids:
        positions = {
            (int(ax + t * sx), int(ay + t * sy))
            for t in range(3600, 3660)}
        space.difference_update(positions)
    if len(space) != 1:
        raise ValueError(
            "Expected exactly one empty position, found: " + str(space)
        )
    return ':'.join(map(str, space.pop()))
