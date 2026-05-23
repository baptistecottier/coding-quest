"""
Type: Challenge
Year: 2023
Day: 08 - Shopping expedition
"""


def preprocessing(
        puzzle_input: str
) -> list[list[int]]:
    """
    Parse puzzle input into a 2D list of integers.
    """
    return [list(map(int, line.split())) for line in puzzle_input.splitlines()]


def solver(
        distances: list[list[int]]
) -> int:
    """
    Solve traveling salesman problem using dynamic programming with bitmask.
    """
    n = len(distances)
    bound = 2 * sum(distances[0])
    full_mask = (1 << n) - 1
    shortest_dp: list[list[int]] = [
        [bound for _ in range(n)]
        for _ in range(1 << n)]
    shortest_dp[1][0] = 0

    for visited in range(1, 1 << n):
        for shop in range(n):
            if (not (visited >> shop & 1) or
                    shortest_dp[visited][shop] == bound):
                continue
            for next_shop in range(n):
                if visited >> next_shop & 1:
                    continue
                new_mask = visited | (1 << next_shop)
                distance = (shortest_dp[visited][shop] +
                            distances[shop][next_shop])
                if distance < shortest_dp[new_mask][next_shop]:
                    shortest_dp[new_mask][next_shop] = distance

    shortest = min(shortest_dp[full_mask][i] + distances[i][0]
                   for i in range(1, n))
    return shortest + 2
