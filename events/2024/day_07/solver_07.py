"""
Type: Challenge
Year: 2024
Day: 07 - The purge
"""


def preprocessing(puzzle_input: str):
    """
    Each folder as its lines: its id, then one line per file or subfolder.
    """
    return [f.splitlines() for f in puzzle_input.split('Folder: ') if f]


def solver(folders: list[list[str]]):
    """
    Total size of the files removed: the temporary and delete ones, and
    everything in a folder being removed.
    """
    to_delete: set[int] = set()
    removed = 0
    for folder in folders:
        f_id = int(folder[0])
        for file in folder[1:]:
            words = file.split()
            if (f_id in to_delete or "temporary" in words[1]
                    or "delete" in words[1]):
                if 'FOLDER' in file:
                    to_delete.add(int(words[-1][:-1]))
                else:
                    removed += int(words[-1])
    yield removed
