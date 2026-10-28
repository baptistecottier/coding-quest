"""
Type: Challenge
Year: 2024
Day: 01 - Purchase tickets
"""

import re
from collections import defaultdict


def preprocessing(
    puzzle_input: str
) -> dict[str, list[tuple[str, int]]]:
    """
    Group the charges 'Airline: Item cost' by airline.
    """
    costs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for name, item, cost in re.findall(r'(\S+): (\S+) (\d+)', puzzle_input):
        costs[name].append((item, int(cost)))
    return costs


def solver(
    costs: dict[str, list[tuple[str, int]]]
) -> int:
    """
    Cheapest ticket: the lowest total over airlines, discounts and rebates
    being taken off.
    """
    to_subtract = {"Discount", "Rebate"}
    return min(
        sum(-cost if item in to_subtract else cost for item, cost in items)
        for items in costs.values()
    )
