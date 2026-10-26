"""
Type: Challenge
Year: 2023
Day: 05 - Decoding pixels
"""


def preprocessing(
    puzzle_input: str
) -> list[tuple[int, int, int, int]]:
    """
    Parse puzzle input into list of rectangle tuples (x, y, width, height).
    """
    rectangles: list[tuple[int, int, int, int]] = []
    for line in puzzle_input.splitlines():
        rectangle = tuple(map(int, line.split()))
        if len(rectangle) != 4:
            raise ValueError("Incprrect input format!")
        rectangles.append(rectangle)
    return rectangles


def solver(
        rectangles: list[tuple[int, int, int, int]]
) -> str:
    """
    Toggle pixels on a 10x50 screen based on rectangles.
    """
    screen: list[list[int]] = [[0 for _ in range(50)] for _ in range(10)]
    for start_x, start_y, width, height in rectangles:
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                screen[y][x] = 1 - screen[y][x]

    return '\n'.join(
        "".join('#' if n == 1 else ' ' for n in line)
        for line in screen)
