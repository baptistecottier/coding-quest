"""
Type: Challenge
Year: 2023
Day: 02 - Navigation sensor
"""


def preprocessing(
    puzzle_input: str
) -> set[int]:
    """
    Converts a multiline string of integers into a set of integers.
    """
    records: set[int] = set()
    for line in puzzle_input.splitlines():
        records.add(int(line))
    return records


def solver(
    records: set[int]
) -> int:
    """
    returns the rounded average of modified records with even parity from the
    input set.
    """
    expected_record = 0
    good_parity = 0
    for record in records:
        bits = bin(record)[2:]
        bits = (16 - len(bits)) * '0' + bits
        if sum(b == '1' for b in bits) % 2 == 0:
            good_parity += 1
            expected_record += int('0' + bits[1:], 2)
    return round(expected_record / good_parity)
