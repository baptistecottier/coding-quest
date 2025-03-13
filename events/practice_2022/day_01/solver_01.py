def preprocessing(puzzle_input: str) -> tuple[list[int], list[int]]:
    lines = [[int(item) for item in line.split()] for line in puzzle_input.splitlines()]
    grid_size = len(lines[0])
    grid_game = lines[:grid_size][::-1]
    board = []
    for i, l in enumerate(grid_game):
        if i % 2 == 0:
            board.extend(l)
        else:
            board.extend(l[::-1])

    rolls = lines[grid_size:]
    return board, rolls


def solver(board: list[int], rolls: list[int]):
    target = len(board) - 1
    player_one = 0
    player_two = 0
    turn = 0

    while True:
        move_one, move_two = rolls.pop(0)
        turn += 1
        player_one += move_one
        if player_one >= target:
            return turn
        while board[player_one] != 0:
            player_one += board[player_one]
            if player_one >= target:
                return turn

        player_two += move_two
        if player_two >= target:
            return 2 * turn
        while board[player_two] != 0:
            player_two += board[player_two]
            if player_two >= target:
                return 2 * turn

