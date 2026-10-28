"""
Type: Challenge
Year: 2023
Day: 05 - Decoding pixels
"""

from itertools import groupby

# Every glyph met in the example and the puzzle input, followed by the
# characters they show, in the same order.
GLYPHS: str = """
######                ##  ####  ####
#                    # #     #  #  #
#       ####   ####    #     #  #  #
######  #  ##  #       #    #   #  #
#       #  ##  #       #    #   #  #
#       #  ##  #       #   #    #  #
######  #  ##  ####    #   #    ####
"""
CHARACTERS = "Enc170"


def split_glyphs(drawing: list[str]) -> list[tuple[str, ...]]:
    """
    Split a drawing into its glyphs: the runs of columns with a lit pixel,
    each cut down to the rows between its top and bottom lit pixels.
    """
    width = max(map(len, drawing))
    rows = [row.ljust(width) for row in drawing]
    glyphs: list[tuple[str, ...]] = []
    for lit, run in groupby(range(width),
                            lambda x: any(row[x] == '#' for row in rows)):
        if lit:
            columns = list(run)
            lines = [row[columns[0]:columns[-1] + 1] for row in rows]
            used = [y for y, line in enumerate(lines) if '#' in line]
            glyphs.append(tuple(lines[used[0]:used[-1] + 1]))
    return glyphs


def read(drawing: list[str]) -> str:
    """
    Text displayed by a drawing, read glyph by glyph.
    """
    font = dict(zip(split_glyphs(GLYPHS.splitlines()), CHARACTERS,
                    strict=True))
    text = ""
    for glyph in split_glyphs(drawing):
        if glyph not in font:
            raise ValueError("Unknown glyph:\n" + "\n".join(glyph))
        text += font[glyph]
    return text


def preprocessing(
    puzzle_input: str
) -> list[tuple[int, int, int, int]]:
    """
    Parse puzzle input into list of rectangle tuples (x, y, width, height).
    """
    rectangles: list[tuple[int, int, int, int]] = []
    for line in puzzle_input.splitlines():
        rectangle = tuple(map(int, line.split()))
        if len(rectangle) != 4:
            raise ValueError("Incorrect input format!")
        rectangles.append(rectangle)
    return rectangles


def solver(
        rectangles: list[tuple[int, int, int, int]]
) -> str:
    """
    Toggle pixels on a 10x50 screen based on rectangles, then read the
    passcode they display.
    """
    screen: list[list[int]] = [[0 for _ in range(50)] for _ in range(10)]
    for start_x, start_y, width, height in rectangles:
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                screen[y][x] = 1 - screen[y][x]

    drawing = ["".join('#' if n == 1 else ' ' for n in line)
               for line in screen]
    return read(drawing)
