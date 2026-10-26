"""
Type: Practice
Year: 2022
Day: 05 - Message from afar
"""


def preprocessing(puzzle_input: str) -> list[str]:
    """Converts a hexadecimal string to a list of binary digits."""
    bit_length = 4 * len(puzzle_input)
    n = int(puzzle_input, 16)
    m = bin(n)[2:]
    return list(m.zfill(bit_length))


def solver(bin_message: list[str]) -> str:
    """
    Decodes a binary message using a custom variable-length encoding table and
    returns the decoded string.
    """
    table = {
        '0000': 'E', '0001': 'T', '0010': 'A', '0011': 'I', '0100': 'N',
        '0101': 'O', '0110': 'S', '0111': 'H', '10000': 'R', '10001': 'D',
        '10010': 'L', '10011': 'U', '10100': 'C', '10101': 'M', '10110': 'F',
        '10111': 'B', '1100000': 'F', '1100001': 'Y', '1100010': 'W',
        '1100011': 'G', '1100100': 'P', '1100101': 'B', '1100110': 'V',
        '1100111': 'K', '1101000': 'Q', '1101001': 'J', '1101010': 'X',
        '1101011': 'Z', '1110000': '0', '1110001': '1', '1110010': '2',
        '1110011': '3', '1110100': '4', '1110101': '5', '1110110': '6',
        '1110111': '7', '1111000': '8', '1111001': '9', '1111010': '_',
        '1111011': '.', '1111100': "'", '1111111': '*',
    }
    message = ""
    while True:
        key = ""
        while key not in table:
            key += bin_message.pop(0)
        if key == '1111111':
            break
        message += table[key]
    return message
