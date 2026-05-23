# pylint: skip-file
# flake8: noqa
# type: ignore

"""Global solver for coding quest puzzles"""

import json
import os
import sys
import importlib.util
from inspect import signature
from pathlib import Path


def usage() -> None:
    print("Usage: python coding_quest.py [-c|-p] YEAR DAY")
    print("  -c       challenge")
    print("  -p       practice")
    print("  YEAR     4-digit year, e.g. 2022")
    print("  DAY      day number, e.g. 1 or 01")
    sys.exit(1)


def load_module(module_path: Path):
    if not module_path.exists():
        raise FileNotFoundError(f"Solver module not found: {module_path}")
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_input(value):
    if isinstance(value, str):
        return value
    return value


def solve(module, data):
    solver_func = module.solver
    try:
        n_args = len(signature(solver_func).parameters)
    except (ValueError, TypeError):
        n_args = 1

    if n_args > 1 and isinstance(data, (list, tuple)):
        result = solver_func(*data)
    else:
        result = solver_func(data)

    if hasattr(result, '__next__'):
        return list(result)
    if isinstance(result, (list, tuple)):
        return list(result)
    return [result]


def main() -> None:
    if len(sys.argv) != 4:
        usage()

    event_flag = sys.argv[1]
    if event_flag == '-c':
        event_type = 'challenge'
    elif event_flag == '-p':
        event_type = 'practice'
    else:
        usage()

    year = sys.argv[2]
    day = sys.argv[3].zfill(2)

    project_path = Path(os.path.abspath(os.getcwd()))
    json_path = project_path / 'events' / f"{event_type}_{year}" / f"day_{day}" / f"data_{day}.json"
    if not json_path.exists():
        print(f"JSON input file not found: {json_path}")
        sys.exit(1)

    data = json.loads(json_path.read_text(encoding='utf-8'))
    test_input = data.get('test_input')
    test_answer = str(data.get('test_answer'))
    user_input = data.get('user_input')

    if test_input is None:
        print(f"Missing test input in {json_path}")
        sys.exit(1)

    solver_module = load_module(project_path / 'events' / f"{event_type}_{year}" / f"day_{day}" / f"solver_{day}.py")

    if 'preprocessing' in dir(solver_module):
        pp = solver_module.preprocessing
    else:
        pp = lambda x: x

    test_data = prepare_input(pp(test_input))
    user_data = prepare_input(pp(user_input))

    computed_test = solve(solver_module, test_data)
    computed_user = solve(solver_module, user_data)
    has_failure = False

    if not computed_test:
        print('Solver produced no test output.')
        sys.exit(1)

    expected = test_answer
    actual = str(computed_test[0])

    if expected == actual:
        print('Test: ✅')
    else:
        print(f'Test: ❌ (result: {actual}, expect: {expected})')
        has_failure = True

    expected_user = str(data.get('user_answer'))
    if computed_user:
        user_result = str(computed_user[0]) if len(computed_user) == 1 else [str(x) for x in computed_user]
        if expected_user:
            if isinstance(user_result, list):
                user_match = all(str(x) == expected_user for x in user_result)
            else:
                user_match = user_result == expected_user
            if user_match:
                print('User: ✅')
            else:
                if isinstance(user_result, list):
                    print(f'User: ❌ (result: {user_result}, expect: {expected_user})')
                else:
                    print(f'User: ❌ (result: {user_result}, expect: {expected_user})')
                has_failure = True
        else:
            if isinstance(user_result, list):
                print('User answers:')
                for answer in user_result:
                    print('-', answer)
            else:
                print('User answer:', user_result)

    if has_failure:
        sys.exit(1)


if __name__ == '__main__':
    main()
