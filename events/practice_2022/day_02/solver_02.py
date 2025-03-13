"""Coding Quest - Practice 2022 - Day 02 - Wordle with friends"""


def preprocessing(puzzle_input: str) -> tuple[list, set, dict, dict]:
    """
    Process the puzzle input to extract information about guesses and results.

    Args:
        puzzle_input (str): Raw puzzle input containing guess attempts and results, 
        followed by candidate words.

    Returns:
        tuple: A tuple containing:
            - words (list): Candidate words to be evaluated
            - absent (set): Letters that are not in the target word
            - correct_pos (dict): Dictionary mapping positions to letters that are 
              correct in those positions
            - wrong_pos (dict): Dictionary mapping letters to positions where they 
              are known to be incorrect
    """
    lines = puzzle_input.splitlines()
    guesses = [guess.split() for guess in lines[:3]]
    absent = set()
    correct_pos = {}
    wrong_pos = {}
    for attempt, result in guesses:
        for i, (l, r) in enumerate(zip(attempt, result)):
            if r == 'B':
                absent.add(l)
            elif r == 'G':
                correct_pos[i] = l
            else:
                wrong_pos[l] = i
    words = lines[3:]
    return words, absent, correct_pos, wrong_pos


def solver(words: list[str], absent: set[str], correct_pos: dict, wrong_pos: dict):
    """
    Find a word matching Wordle constraints.
    
    Args:
        words (list): List of candidate words
        absent (str): Letters not in the word
        correct_pos (dict): Map of index to letter for correct positions
        wrong_pos (dict): Map of letter to index for letters in word but wrong position
        
    Returns:
        str: First word matching all constraints
    """
    for word in words:
        if any(c in absent for c in word):
            continue
        if any(word[i] != l for i, l in correct_pos.items()):
            continue
        if any(l not in word or word[i] == l for l, i in wrong_pos.items()):
            continue
        return word
