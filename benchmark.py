#!/usr/bin/env python3

"""
Benchmark every solution against the known answers, store the results in
events/benchmarks.json and regenerate the scoreboards.

Each day runs in its own process with a timeout (5 minutes by default). The
measured time covers preprocessing and solving, not interpreter start-up or
imports. Inputs are the ones cached by the Puzzle Submitter extension and
expected answers the ones it recorded as correct. A day with no known answer
cannot be verified.

Examples:
    uv run benchmark.py                    # every event
    uv run benchmark.py 2023 prequel       # some events
    uv run benchmark.py 2022 --days 1-5    # some days
    uv run benchmark.py --changed          # only what changed
    uv run benchmark.py --render           # redraw only
"""

import argparse
import datetime
import hashlib
import importlib.util
import inspect
import json
import os
import platform
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from collections.abc import Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
from typing import TypedDict, cast
from urllib.parse import unquote, urlparse

from scoreboard import CALENDAR, Result, Results, render

ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / "events"
RESULTS = EVENTS / "benchmarks.json"
INPUT_STORE = ROOT / ".puzzle-submitter" / "codingquest.json"
EXTENSION = "baptistecottier.puzzle-submitter"

# Inputs cached by Puzzle Submitter, by event, day and part.
type Inputs = dict[str, dict[str, dict[str, str]]]
# Expected answers recorded by Puzzle Submitter, by (event, day).
type Answers = dict[tuple[str, int], str]
# A solution to run: event, day, path, code fingerprint and expected answer.
type Task = tuple[str, int, Path, str | None, str | None]


class RunResult(TypedDict):
    """What a solution produced when run."""

    answer: str | None
    time: float | None
    timeout: bool
    error: str | None


# ===========================================================================
# Calendar
# ===========================================================================


def days_in(event: str) -> int:
    """Number of days of an event: 5 for the prequel, 9 or 10 otherwise."""
    return len(CALENDAR[event]["days"])


def solution_path(event: str, day: int) -> Path:
    """Path of the solution file of a day."""
    return EVENTS / event / f"day_{day:02}" / f"solver_{day:02}.py"


def has_solution(event: str, day: int) -> bool:
    """Whether a day has a solution (a file without a solver has none)."""
    path = solution_path(event, day)
    return path.is_file() and bool(
        re.search(r"^def solver\(", path.read_text(encoding="utf-8"), re.M)
    )


# ===========================================================================
# Inputs and expected answers
# ===========================================================================


def load_inputs() -> Inputs:
    """Inputs from the store shared with Puzzle Submitter, if any."""
    try:
        with open(INPUT_STORE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def puzzle_input(inputs: Inputs, event: str, day: int) -> str | None:
    """Input of a day, as cached by Puzzle Submitter."""
    text = inputs.get(event, {}).get(str(day), {}).get("1")
    return text.rstrip("\n") if text else None


def _workspace_storages() -> list[Path]:
    """VS Code's per-workspace storage folders (stable and Insiders)."""
    bases = [
        Path.home() / "Library/Application Support",
        Path.home() / ".config",
        Path(os.environ.get("APPDATA", Path.home())),
    ]
    return [
        base / app / "User/workspaceStorage"
        for base in bases
        for app in ("Code", "Code - Insiders")
    ]


def load_answers() -> Answers:
    """
    Answers recorded as correct by Puzzle Submitter for this repository, as
    {(event, day): answer}. They live in the extension's workspace state,
    inside the VS Code workspace storage of this repository. A day recorded
    as solved without its answer (true) cannot be used.
    """
    answers: Answers = {}
    for storage in _workspace_storages():
        for workspace in storage.glob("*/workspace.json"):
            try:
                folder: str = json.loads(
                    workspace.read_text(encoding="utf-8")
                ).get("folder", "")
            except (OSError, json.JSONDecodeError):
                continue
            if unquote(urlparse(folder).path).rstrip("/") != str(ROOT):
                continue
            database = workspace.with_name("state.vscdb").as_uri() + "?mode=ro"
            try:
                with closing(
                    sqlite3.connect(database, uri=True)
                ) as connection:
                    row = connection.execute(
                        "SELECT value FROM ItemTable WHERE key = ?",
                        (EXTENSION,),
                    ).fetchone()
            except sqlite3.Error:
                continue
            state: dict[str, object] = json.loads(row[0]) if row else {}
            for key, recorded in state.items():
                match = re.fullmatch(
                    r"puzzleSubmitter\.progress\.codingquest\.(\w+)\.(\d+)",
                    key,
                )
                if not match or not isinstance(recorded, dict):
                    continue
                answer = cast(dict[str, object], recorded).get("1")
                if isinstance(answer, str):
                    answers[(match[1], int(match[2]))] = answer
    return answers


def expected_answer(answers: Answers, event: str, day: int) -> str | None:
    """Known answer of a day, as recorded by Puzzle Submitter."""
    answer = answers.get((event, day))
    return normalise(answer) if answer else None


def fingerprint(path: Path) -> str | None:
    """Git object id of a file as in the working tree, None if missing."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ===========================================================================
# Running a solution
# ===========================================================================


def normalise(answer: object) -> str:
    """
    String form of an answer, as it would be submitted. Trailing spaces and
    surrounding blank lines are dropped, so that a drawn answer
    compares by its pixels.
    """
    if isinstance(answer, float) and answer.is_integer():
        answer = int(answer)
    text = "\n".join(line.rstrip() for line in str(answer).splitlines())
    text = text.strip("\n")
    return text if "\n" in text else text.strip()


def child(path: str) -> None:
    """
    Run one solution on the input read from stdin, the way coding_quest.py
    does: preprocessing(input), then solver() on its result. The answer is
    written to stdout as a JSON line. Everything the solution prints is
    discarded.
    """
    out = os.fdopen(os.dup(1), "w", encoding="utf-8")
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)

    def emit(**message: object) -> None:
        out.write(json.dumps(message) + "\n")
        out.flush()

    data = sys.stdin.read()
    sys.path.insert(0, str(ROOT))
    try:
        spec = importlib.util.spec_from_file_location(
            "benchmarked_solution", path
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        start = time.perf_counter()
        args = (
            module.preprocessing(data)
            if hasattr(module, "preprocessing")
            else data
        )
        try:
            arity = len(inspect.signature(module.solver).parameters)
        except (TypeError, ValueError):
            arity = 1
        result: object
        if arity > 1 and isinstance(args, (list, tuple)):
            result = module.solver(*args)
        else:
            result = module.solver(args)
        if hasattr(result, "__next__"):
            result = list(cast(Iterator[object], result))
        if isinstance(result, (list, tuple)):
            items = cast(Sequence[object], result)
            result = items[0] if len(items) == 1 else items
        emit(answer=normalise(result), done=time.perf_counter() - start)
    except BaseException as exc:  # pylint: disable=broad-except
        emit(error=f"{type(exc).__name__}: {str(exc)[:200]}")
    out.close()
    os._exit(
        0
    )  # do not wait for threads or processes left behind by the solution


def run(path: Path, data: str, timeout: float) -> RunResult:
    """Run one solution in its own process and collect its answer."""
    command = [sys.executable, __file__, "--child", str(path)]
    with subprocess.Popen(
        command,
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        start_new_session=True,
    ) as process:
        try:
            output, _ = process.communicate(data, timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            output, _ = process.communicate()
            timed_out = True
        _kill_group(process.pid)

    answer: str | None = None
    total: float | None = None
    error: str | None = None
    for line in output.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        answer = message.get("answer", answer)
        total = message.get("done", total)
        error = message.get("error", error)
    if (
        total is not None
    ):  # answered in time, only a leftover process was still running
        timed_out = False
    if not timed_out and total is None and error is None:
        error = f"exited with code {process.returncode}"
    return {
        "answer": answer,
        "time": total,
        "timeout": timed_out,
        "error": error,
    }


def _kill_group(pgid: int) -> None:
    """Kill whatever a solution left behind in its process group."""
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


# ===========================================================================
# Benchmark
# ===========================================================================


def grade(run_result: RunResult, expected: str | None) -> Result:
    """Compare a run with the expected answer, keep what the board needs."""
    given = run_result["answer"]
    if given is None:
        answer = "missing"
    elif expected is None:
        answer = "unknown"
    else:
        answer = "ok" if given == expected else "wrong"
    if run_result["timeout"]:
        status = "timeout"
    elif answer == "ok":
        status = "solved"
    elif run_result["error"]:
        status = "error"
    else:
        status = "wrong"
    result: Result = {
        "status": status,
        "answer": answer,
        "time": round(run_result["time"], 4)
        if run_result["time"] is not None
        else None,
        "date": datetime.date.today().isoformat(),
    }
    if run_result["error"]:
        result["error"] = run_result["error"]
    return result


def load_results() -> Results:
    """Previous results, so that a partial run only updates what it ran."""
    if RESULTS.is_file():
        with open(RESULTS, encoding="utf-8") as f:
            return json.load(f)
    return {"meta": {}, "events": {}}


def save_results(results: Results) -> None:
    """Write the results, in calendar order, one line per day."""
    events: list[str] = []
    for event in CALENDAR:
        days = results["events"].get(event)
        if not days:
            continue
        lines = [
            f'    "{day}": {json.dumps(entry, ensure_ascii=False)}'
            for day, entry in sorted(days.items(), key=lambda d: int(d[0]))
        ]
        events.append(f'    "{event}": {{\n' + ",\n".join(lines) + "\n    }")
    with open(RESULTS, "w", encoding="utf-8") as f:
        f.write(
            '{\n  "meta": '
            + json.dumps(results["meta"], ensure_ascii=False)
            + ',\n  "events": {\n'
            + ",\n".join(events)
            + "\n  }\n}\n"
        )


def describe(result: Result) -> str:
    """One-line summary of a result for the console."""
    star = {"ok": "★", "unknown": "?"}.get(result["answer"], "☆")
    if result["status"] == "timeout":
        return f"{star} timeout"
    if result["time"] is None:
        return f"{star} {result.get('error', result['status'])}"
    return f"{star} {result['time']:.3f}s {result['status']}"


def machine() -> str:
    """Short description of the machine running the benchmark."""
    try:
        return subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return platform.processor() or platform.machine()


def outdated(
    result: Result | None, code: str | None, expected: str | None
) -> bool:
    """
    Whether a result needs a new run: never measured, measured on other code,
    or with an answer that could not be verified then but can be now.
    """
    if result is None or result.get("code") != code:
        return True
    return result["answer"] == "unknown" and expected is not None


def collect_tasks(
    results: Results,
    answers: Answers,
    targets: list[str],
    days: list[int] | None,
    changed: bool,
) -> list[Task]:
    """
    The (event, day, path, code, expected) of every solution to run, dropping
    from results the days whose solution no longer exists.
    """
    tasks: list[Task] = []
    for event in targets or CALENDAR:
        for day in days or range(1, days_in(event) + 1):
            if day > days_in(event):
                continue
            entries = results["events"].setdefault(event, {})
            if not has_solution(event, day):
                entries.pop(str(day), None)
                continue
            path = solution_path(event, day)
            code = fingerprint(path)
            expected = expected_answer(answers, event, day)
            if changed and not outdated(entries.get(str(day)), code, expected):
                continue
            tasks.append((event, day, path, code, expected))
    return tasks


def benchmark(
    targets: list[str],
    days: list[int] | None,
    timeout: float,
    jobs: int,
    changed: bool = False,
) -> None:
    """
    Run the selected solutions and merge their results into benchmarks.json.
    With changed, only the outdated results are run again.
    """
    results = load_results()
    inputs = load_inputs()
    answers = load_answers()
    if not answers:
        print(
            "No answer recorded by Puzzle Submitter: "
            "no solution can be verified."
        )
    lock = threading.Lock()

    tasks = collect_tasks(results, answers, targets, days, changed)
    if not tasks:
        print("Every result is up to date.")
        save_results(results)
        return

    print(
        f"Benchmarking {len(tasks)} solution(s), "
        f"timeout {timeout:g}s, {jobs} job(s)",
        flush=True,
    )

    def task(item: Task) -> None:
        event, day, path, code, expected = item
        data = puzzle_input(inputs, event, day)
        if data is None:
            run_result: RunResult = {
                "answer": None,
                "time": None,
                "timeout": False,
                "error": "no input",
            }
        else:
            run_result = run(path, data, timeout)
        with lock:
            result = grade(run_result, expected)
            result["code"] = code
            results["events"][event][str(day)] = result
            save_results(results)
            print(f"  {event:>7} day {day:>2} {describe(result)}", flush=True)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(task, tasks))

    results["meta"] = {
        "timeout": timeout,
        "machine": machine(),
        "date": datetime.date.today().isoformat(),
        "python": platform.python_version(),
    }
    save_results(results)


def parse_target(text: str) -> str:
    """An event of the calendar: 'prequel' or a year such as '2023'."""
    if text.lower() in CALENDAR:
        return text.lower()
    raise argparse.ArgumentTypeError(
        f"{text!r} is not an event ({', '.join(CALENDAR)})"
    )


def parse_days(text: str) -> list[int]:
    """Parse '1-5', '1,3,5' or '1-3,7' into a sorted list of days."""
    days: set[int] = set()
    for chunk in text.split(","):
        start, _, end = chunk.strip().partition("-")
        days.update(range(int(start), int(end or start) + 1))
    return sorted(days)


def main() -> None:
    """Entry point."""
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        child(sys.argv[2])

    parser = argparse.ArgumentParser(
        description="Benchmark Coding Quest solutions"
    )
    parser.add_argument(
        "targets",
        type=parse_target,
        nargs="*",
        help=f"events to run, among {', '.join(CALENDAR)} (default: all)",
    )
    parser.add_argument(
        "--days",
        type=parse_days,
        help='days to run, e.g. "1-5" or "1,3"',
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300,
        help="timeout per day in seconds (default: 300)",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="solutions run in parallel (default: 1, the most accurate)",
    )
    parser.add_argument(
        "--changed",
        action="store_true",
        help="only run solutions whose code changed since their last run, "
        "new ones, and ones that can now be verified",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="only regenerate the scoreboards from the stored results",
    )
    args = parser.parse_args()

    if not args.render:
        benchmark(
            args.targets, args.days, args.timeout, args.jobs, args.changed
        )
    render()


if __name__ == "__main__":
    main()
