"""
Type: Challenge
Year: 2022
Day: 05 - Spot the forgery
"""

from hashlib import sha256
from typing import Iterator


def preprocessing(
    puzzle_input: str
) -> list[tuple[str, int, str]]:
    """
    Process raw input by splitting records into description, mined number,
    and hash components.
    """
    records: list[tuple[str, int, str]] = []
    for record in puzzle_input.splitlines():
        desc, mined_n, _, record_hash = record.split('|')
        records.append((desc, int(mined_n), record_hash))
    return records


def solver(
    records: list[tuple[str, int, str]]
) -> Iterator[str]:
    """
    Computes a final hash by verifying and processing a chain of
    blockchain-like records.
    """
    final_hash = '0' * 64
    for d, n, h in records:
        if sha256(f"{d}|{n}|{final_hash}".encode('utf-8')).hexdigest() != h:
            k = 0
            while True:
                h = sha256(f"{d}|{k}|{final_hash}".encode('utf-8')).hexdigest()
                if h.startswith("000000"):
                    final_hash = h
                    break
                k += 1
        else:
            final_hash = sha256(
                f"{d}|{n}|{final_hash}".encode('utf-8')
            ).hexdigest()
    yield final_hash
