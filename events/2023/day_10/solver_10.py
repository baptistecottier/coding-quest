"""
Type: Challenge
Year: 2023
Day: 10 - The route home
"""

import heapq
from collections import defaultdict
from math import inf


def preprocessing(
    puzzle_input: str
) -> dict[str, set[tuple[str, int]]]:
    """
    Parse each line 'A => B:d C:d' into the destinations reachable from A
    with their travel times.
    """
    travels: dict[str, set[tuple[str, int]]] = {}
    for line in puzzle_input.splitlines():
        depart, _, *destinations = line.split()
        travels[depart] = set()
        for destination in destinations:
            name, time = destination.split(':')
            travels[depart].add((name, int(time)))
    return travels


def solver(
    travels: dict[str, set[tuple[str, int]]]
) -> int:
    """
    Shortest travel time from TYC to EAR with Dijkstra, counting a 600 delay
    at every stop but the last one.
    """
    start, end, delay = 'TYC', 'EAR', 600
    queue = [(0, start)]
    best: dict[str, float] = defaultdict(lambda: inf)
    best[start] = 0
    while queue:
        time, position = heapq.heappop(queue)
        if position == end:
            return time - delay
        if best[position] < time:
            continue
        for destination, duration in travels.get(position, set()):
            arrival = time + duration + delay
            if arrival < best[destination]:
                best[destination] = arrival
                heapq.heappush(queue, (arrival, destination))
    raise ValueError(f"No route from {start} to {end}")
