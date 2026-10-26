"""
Type: Challenge
Year: 2023
Day: 09 - Index Tree
"""

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    """
    Binary search tree node with value and left/right children.
    """
    value: int
    left: "Node | None" = None
    right: "Node | None" = None


def preprocessing(
    puzzle_input: str
) -> list[int]:
    """
    Parse hexadecimal values from puzzle input.
    """
    return list(map(lambda x: int(x, 16), puzzle_input.split()))


def solver(
    values: list[int]
) -> int:
    """
    Build a binary search tree and return the product of the max depth count
    and max depth.
    """
    root = Node(values.pop(0), None, None)
    depths: dict[int, int] = defaultdict(int)
    depths[1] = 1
    while values:
        value = values.pop(0)
        depth = 1
        node = root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = Node(value, None, None)
                    depths[depth + 1] += 1
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(value, None, None)
                    depths[depth + 1] += 1
                    break
                node = node.right
            depth += 1
    return max(depths.values()) * max(depths)
