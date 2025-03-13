"""Coding Quest - Practice 2022 - Day 01 - Snakes and ladders"""


def preprocessing(puzzle_input: str) -> tuple[list[int], list[int]]:
    """
    Preprocess the puzzle input to extract the game board and sequence of rolls.

    The input is expected to be a multi-line string where:
    - The first N lines represent an N×N grid for the game board
    - The remaining lines contain the sequence of dice rolls

    Args:
        puzzle_input: A string containing the puzzle input

    Returns:
        A tuple containing:
        - board: A flattened list representing the game board in a snake pattern
        - rolls: A list of dice roll sequences
    """
    lines = [[int(item) for item in line.split()] for line in puzzle_input.splitlines()]
    grid_size = len(lines[0])
    grid_game = lines[:grid_size][::-1]
    board = []
    for i, l in enumerate(grid_game):
        if i % 2 == 0:
            board.extend(l)
        else:
            board.extend(l[::-1])
    rolls = []
    for a, b in lines[grid_size:]:
        rolls.append(a)
        rolls.append(b)
    return board, rolls


def solver(board: list[int], rolls: list[int]):
    """
    Simulates a board game with two players taking turns rolling dice.
    
    Args:
        board: List representing the game board where non-zero values indicate special moves
        rolls: List of tuples (move_one, move_two) representing dice rolls for each player
    
    Returns:
        The number of turns taken to reach the target position (end of board)
        """
    target = len(board) - 1
    positions = [0, 0]
    player = 0
    turn = 0.5

    while True:
        move = rolls.pop(0)
        turn += 0.5
        positions[player] += move
        if positions[player] >= target:
            return (1 + player) * int(turn)
        while board[positions[player]] != 0:
            positions[player] += board[positions[player]]
            if positions[player] >= target:
                return (1 + player) * int(turn)

        player = 1 - player
