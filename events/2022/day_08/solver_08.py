"""
Type: Challenge
Year: 2022
Day: 08 - Message from home
"""

import re


def solver(
    ciphertext: str,
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
    secret_key = "Roads? Where We're Going, We Don't Need Roads."
    size = len(secret_key)
    for i, c in enumerate(ciphertext):
        k = secret_key[i % size]
        plain += alphabet[alphabet.index(c) - alphabet.index(k) - 1]
    answer = re.search(r'.+answer.+\'(.+)\'', plain)
    if answer is None:
        raise ValueError("Incorrect decryption, answer not found")
    return answer[1]
