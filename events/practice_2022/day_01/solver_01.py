"""
Type: Practice
Year: 2022
Day: 01 - Snakes and ladders
"""


def preprocessing(
    puzzle_input: str
) -> tuple[list[int], list[int]]:
    """
    Parses the puzzle input into a flattened board list and a list of rolls
    for the game.
    """
    lines = [
        [int(item) for item in line.split()]
        for line in puzzle_input.splitlines()]
    grid_size = len(lines[0])
    grid_game = lines[:grid_size][::-1]
    board: list[int] = []
    for i, row in enumerate(grid_game):
        if i % 2 == 0:
            board.extend(row)
        else:
            board.extend(row[::-1])
    rolls: list[int] = []
    for a, b in lines[grid_size:]:
        rolls.append(a)
        rolls.append(b)
    return board, rolls


def solver(
    board: list[int],
    rolls: list[int]
) -> int:
    """
    Plays a game on a board, alternating between two players, until one exits
    the board, returning a score based on the winner and game duration.
    """
    positions = [0, 0]
    player = 0
    turn = 0.5

    while True:
        move = rolls.pop(0)
        turn += 0.5
        positions[player] = play(board, positions[player], move)
        if positions[player] == -1:
            break
        player = 1 - player
    return (1 + player) * int(turn)


def play(
    board: list[int],
    pos: int,
    move: int
) -> int:
    """
    Simulate a player's move on a board, adjusting position based on board
    values until landing on a zero space or exiting the board.
    """
    pos += move
    if pos >= len(board) - 1:
        return -1
    while board[pos] != 0:
        pos += board[pos]
        if pos >= len(board) - 1:
            return -1
    return pos
