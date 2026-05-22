"""
Type: Challenge
Year: 2022
Day: 02 - Lottery tickets
"""


def preprocessing(
    puzzle_input: str
) -> list[list[int]]:
    """
    Converts each line of the input into a list of integers, creating a list
    of tickets.
    """
    tickets: list[list[int]] = []
    for ticket in puzzle_input.splitlines():
        tickets.append(list(map(int, ticket.split())))
    return tickets


def solver(
    tickets: list[list[int]]
) -> int:
    """
    Calculate winnings based on matches between tickets and a fixed draw.
    """
    draw = {12, 48, 30, 95, 15, 55, 97}
    winnings = 0
    for ticket in tickets:
        score = len([num for num in ticket if num in draw]) - 3
        if score >= 0:
            winnings += 10 ** score
    return winnings
