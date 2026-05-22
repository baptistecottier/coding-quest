"""
Type: Challenge
Year: 2022
Day: 08 - Message from home
"""


def preprocessing(
    puzzle_input: str
) -> list[str]:
    """
    Splits the puzzle input into lines and returns them as a tuple of strings.
    """
    return puzzle_input.splitlines()


def solver(
    ciphertext: str,
    secret_key: str
) -> str:
    """
    Decrypts a ciphertext using Vigenere substitution cipher based on a secret
    key.
    """
    alphabet = ("abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "0123456789"
                ".,;:?! '()")
    plain = ''
    size = len(secret_key)
    for i, c in enumerate(ciphertext):
        k = secret_key[i % size]
        plain += alphabet[alphabet.index(c) - alphabet.index(k) - 1]
    return plain
