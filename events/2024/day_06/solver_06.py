"""
Type: Challenge
Year: 2024
Day: 06 - Time to play fair
"""

import re


def preprocessing(puzzle_input: str):
    """
    Key and encrypted message, each given after a colon.
    """
    return re.findall(r'.+: (.*)', puzzle_input)


def solver(key: str, cipher: str):
    """
    Message decrypted with the Playfair table built from the key.
    """
    table = build_table(key)
    message = decipher(cipher, table)
    yield message


def build_table(key: str):
    """
    Playfair table as a 25-letter string read row by row: the letters of
    the key, then the rest of the alphabet without j, each only once.
    """
    table = ""
    for char in key + "abcdefghiklmnopqrstuvwxyz":
        if char not in table:
            table += char
    return table


def decipher(cipher: str, table: str):
    """
    Decrypt a Playfair message pair of letters by pair of letters, then put
    the spaces back where they were.
    """
    plain: list[str] = []
    spaces = [n for n in range(len(cipher)) if cipher[n] == ' ']
    cipher = cipher.replace(' ', '')
    for i in range(0, len(cipher), 2):
        idx1 = table.index(cipher[i])
        idx2 = table.index(cipher[i + 1])
        r1, c1 = idx1 // 5, idx1 % 5
        r2, c2 = idx2 // 5, idx2 % 5
        if r1 == r2:
            plain.append(table[5 * r1 + (c1 - 1) % 5])
            plain.append(table[5 * r1 + (c2 - 1) % 5])
        elif c1 == c2:
            plain.append(table[5 * ((r1 - 1) % 5) + c1])
            plain.append(table[5 * ((r2 - 1) % 5) + c2])
        else:
            plain.append(table[5 * r1 + c2])
            plain.append(table[5 * r2 + c1])
    for n in spaces:
        plain.insert(n, ' ')
    return ''.join(plain)
