"""
Type: Challenge
Year: 2022
Day: 04 - Obsessong over Connect 4
"""


def preprocessing(
    puzzle_input: str
) -> list[list[int]]:
    """
    Parse the input string into a list of games, where each game is a list of
    integers.
    """
    games: list[list[int]] = []
    for game in puzzle_input.splitlines():
        games.append([int(n) for n in game])
    return games


def solver(
    games: list[list[int]]
) -> int:
    """
    Solve a Connect Four game for three players, calculating the product of
    each player's wins.
    """
    wins = [0, 0, 0]
    for game in games:
        player = 0
        board = {c + 1: 0 for c in range(7)}
        tokens: list[set[tuple[int, int]]] = [set(), set(), set()]
        while game:
            col = game.pop(0)
            token = board[col]
            board[col] += 1
            tokens[player].add((col, token))
            if is_winner(tokens[player], col, token):
                wins[player] += 1
                break
            player = (player + 1) % 3
    return wins[0] * wins[1] * wins[2]


def is_winner(
    tokens: set[tuple[int, int]],
    x: int,
    y: int
) -> bool:
    """
    Check if a player has won by having 4 tokens in a row (vertically,
    horizontally, or diagonally).
    """
    return any((
        all((x, y - i) in tokens for i in range(4)),
        any(
            any((
                all((x - k + i, y) in tokens for i in range(4)),
                all((x - k + i, y - k + i) in tokens for i in range(4)),
                all((x - k + i, y + k - i) in tokens for i in range(4)),
            )) for k in range(4)
        )
    ))
