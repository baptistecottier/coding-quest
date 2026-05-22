"""
Type: Challenge
Year: 2022
Day: 01 - Engine diagnostics
"""

from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> list[int]:
    """
    Converts a multiline string of integers into a list of integers.
    """
    return list(map(int, puzzle_input.splitlines()))


def solver(
    temperatures: list[int]
) -> Iterator[int]:
    """
    Count the number of one-minute periods where the 60-minute rolling average
    temperature is outside the safe range (1500-1600).
    """
    rolling_sum = sum(temperatures[:60])
    unsafe_temp = int(abs(rolling_sum - 93_000) > 3_000)
    for k in range(len(temperatures) - 60):
        rolling_sum = rolling_sum - temperatures[k] + temperatures[k + 60]
        unsafe_temp += int(abs(rolling_sum - 93_000) > 3_000)
    yield unsafe_temp
