"""
Type: Challenge
Year: 2022
Day: 10 - A special painting
"""

from pathlib import Path
from PIL import Image
from typing import Iterator


def preprocessing(
    image_path: Path
) -> str:
    """
    Load an image from the given path and return a string of parities
    (0 for even, 1 for odd) of the red channel of each pixel.
    """
    rgb_pixels = image_to_rgb_list(image_path)
    return ''.join([str(pixel[0] % 2) for pixel in rgb_pixels])


def solver(
    image_bytes: str
) -> Iterator[str]:
    """
    Decodes a message from a list of image bytes by interpreting each group of
    8 bits as an ASCII character, stopping at a null byte.
    """
    message = ""
    for i in range(0, len(image_bytes), 8):
        index = int(image_bytes[i: i + 8], 2)
        if index == 0:
            break
        message += chr(index)
    if len(message) >= 100:
        message = message.split(' ')[-1].replace('.', '')
    yield message


def image_to_rgb_list(
    image_path: Path
) -> list[tuple[int, int, int]]:
    """
    Load an image and return its pixels as a list of RGB tuples.
    """
    with Image.open(image_path) as image:
        rgb = image.convert('RGB')
        return [
            tuple(pxl) for pxl in rgb.getdata()]  # type: ignore[attr-defined]
