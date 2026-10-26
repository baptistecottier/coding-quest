"""
Type: Challenge
Year: 2022
Day: 06 - Debugging
"""


class Register(dict[str, int]):
    """
    A dictionary-based register that initializes with named keys and provides
    safe item retrieval with fallback to integer conversion.
    """
    def __init__(self, *args: int):
        if len(args) == 1 and isinstance(args[0], dict):
            super().__init__(args[0])
        else:
            super().__init__(zip(
                'abcdefghixy'.upper(),
                args + (11 - len(args)) * (0,)))

    def get_source(self, item: str) -> int:
        """
        Returns the value associated with 'item' if present, otherwise returns
        'item' converted to an integer.
        """
        if item in self:
            return self[item]
        return int(item)


def preprocessing(
    puzzle_input: str
) -> list[tuple[str, list[str]]]:
    """
    Parses the puzzle input into a list of operations, each represented as a
    tuple of the operation
    and its arguments.
    """
    operations: list[tuple[str, list[str]]] = []
    for operation in puzzle_input.splitlines():
        op, *args = operation.split(' ')
        operations.append((op, args))
    return operations


def solver(
    operations: list[tuple[str, list[str]]]
) -> str:
    """
    Executes a sequence of register-based operations and yields the resulting
    output string.
    """
    reg = Register()
    index = 0
    ceq_cge = False
    output = ""
    while 0 <= index < len(operations):
        op, args = operations[index]
        match op:
            case 'ADD':
                reg[args[0]] += reg.get_source(args[1])
            case 'MOD':
                reg[args[0]] %= reg.get_source(args[1])
            case 'DIV':
                reg[args[0]] //= reg.get_source(args[1])
            case 'MOV':
                reg[args[0]] = reg.get_source(args[1])
            case 'JMP':
                index += reg.get_source(args[0]) - 1
            case 'JIF' if ceq_cge:
                index += reg.get_source(args[0]) - 1
            case 'CEQ':
                ceq_cge = (reg.get_source(args[0]) == reg.get_source(args[1]))
            case 'CGE':
                ceq_cge = (reg.get_source(args[0]) >= reg.get_source(args[1]))
            case 'OUT':
                output += str(reg.get_source(args[0]))
            case 'END':
                break
            case _:
                pass
        index += 1
    return output
