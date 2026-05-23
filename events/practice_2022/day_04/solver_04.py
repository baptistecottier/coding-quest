"""
Type: Practice
Year: 2022
Day: 04 - Lost in transmission
"""


def preprocessing(puzzle_input: str) -> list[list[int]]:
    """
    Converts hexadecimal strings from the puzzle input into a list of lists
    of integers.
    """
    received_bytes: list[list[int]] = []
    for line in puzzle_input.splitlines():
        received_bytes.append([int(item, 16) for item in line.split()])
    return received_bytes


def solver(received_bytes: list[list[int]]) -> int:
    """
    Identifies and yields a correction value for a single erroneous element in
    a 2D list of bytes based on row and column checksums, or yields 0 if no
    error is found.
    """
    for y, row in enumerate(received_bytes[:-1]):
        if sum(row[:-1]) % 256 != row[-1]:
            for x, col_cs in enumerate(received_bytes[-1]):
                col_sum = sum(
                    received_bytes[dy][x]
                    for dy in range(len(received_bytes) - 1))
                cs_verif = col_sum - col_cs
                cs_verif %= 256
                if cs_verif != 0:
                    correction = (
                        (received_bytes[y][x] - cs_verif)
                        * received_bytes[y][x]
                    )
                    return correction
    return 0
