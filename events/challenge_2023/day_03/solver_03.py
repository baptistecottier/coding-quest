"""
Type: Challenge
Year: 2023
Day: 03 - Tic tac toe
"""


def preprocessing(
    puzzle_input: str
) -> list[tuple[list[int], list[int]]]:
    """
    Parses the puzzle input into a list of tuples, each containing two lists
    of integers extracted from each line.
    """
    games: list[tuple[list[int], list[int]]] = []
    for game in puzzle_input.splitlines():
        places = list(map(int, game.split()))
        games.append((places[::2], places[1::2]))
    return games


def solver(
    games: list[tuple[list[int], list[int]]]
) -> int:
    """
    Calculates the product of the number of games won by 'O', games won by 'X',
    and draws from a list of tic-tac-toe games.
    """
    wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]]

    win_o = win_x = draw = 0
    for game_x, game_o in games:
        if any(all(w in game_x[:3] for w in win) for win in wins):
            win_x += 1
        elif any(all(w in game_o[:3] for w in win) for win in wins):
            win_o += 1
        elif any(all(w in game_x[:4] for w in win) for win in wins):
            win_x += 1
        elif any(all(w in game_o[:4] for w in win) for win in wins):
            win_o += 1
        elif any(all(w in game_x for w in win) for win in wins):
            win_x += 1
        else:
            draw += 1

    return win_o * win_x * draw
