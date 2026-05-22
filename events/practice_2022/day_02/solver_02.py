"""
Type: Practice
Year: 2022
Day: 02 - Wordle with friends
"""

from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> tuple[list[str], set[str], dict[int, str], dict[str, int]]:
    """
    Process the puzzle input to extract information about guesses and results.
    """
    lines = puzzle_input.splitlines()
    guesses = [guess.split() for guess in lines[:3]]
    absent: set[str] = set()
    correct_pos: dict[int, str] = {}
    wrong_pos: dict[str, int] = {}
    for attempt, result in guesses:
        for i, (c, r) in enumerate(zip(attempt, result)):
            if r == 'B':
                absent.add(c)
            elif r == 'G':
                correct_pos[i] = c
            else:
                wrong_pos[c] = i
    words = lines[3:]
    return words, absent, correct_pos, wrong_pos


def solver(
    words: list[str],
    absent: set[str],
    correct_pos: dict[int, str],
    wrong_pos: dict[str, int]
) -> Iterator[str]:
    """
    Find a word matching Wordle constraints.
    """
    word = ""
    for word in words:
        if any(c in absent for c in word):
            continue
        if any(word[i] != c for i, c in correct_pos.items()):
            continue
        if any(c not in word or word[i] == c for c, i in wrong_pos.items()):
            continue
        break
    yield word
