#!/usr/bin/env python3

"""
Render the scoreboards from events/benchmarks.json (written by benchmark.py):
the global one, between the scoreboard markers of README.md, and one detailed
page per event (events/<event>/README.md). A result measured on code that
differs from the last commit is marked †, so the published scoreboard never
hides it.

    uv run scoreboard.py
"""

import datetime
import json
import re
import subprocess
from pathlib import Path
from typing import NotRequired, TypedDict

ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / "events"
RESULTS = EVENTS / "benchmarks.json"
README = ROOT / "README.md"
MARKERS = ("<!-- scoreboard:start -->", "<!-- scoreboard:end -->")
ARCHIVE = "https://pbaumgarten.com/course/6/topic"

FAST = 1  # seconds
NBSP = " "  # keeps strips on one line, and an unsolved day an empty box
SYMBOLS = {"fast": "█", "slow": "▓", "unsolved": NBSP}
STATES = ("fast", "slow", "unsolved")


class Edition(TypedDict):
    """An event of the calendar."""

    name: str
    title: str
    topic: int
    page: int
    intro: str
    days: list[str]


class Result(TypedDict):
    """Result of a day in benchmarks.json."""

    status: str
    answer: str
    time: float | None
    date: str
    error: NotRequired[str]
    code: NotRequired[str | None]


class Meta(TypedDict, total=False):
    """Where and when the benchmark ran."""

    timeout: float
    machine: str
    date: str
    python: str


class Results(TypedDict):
    """Content of benchmarks.json: results by event, then by day."""

    meta: Meta
    events: dict[str, dict[str, Result]]


class Summary(TypedDict):
    """Stars, state of every day and total solving time of an event."""

    stars: int
    max: int
    states: list[str]
    time: float


# Every event in order, with its archive pages (topic, page of day 1: the
# following days are the next pages), introduction and the title of each day.
CALENDAR: dict[str, Edition] = {
    "prequel": {
        "name": "Prequel",
        "title": "2022 Prequel",
        "topic": 45,
        "page": 296,
        "intro": "Earth has recently discovered faster than light travel and "
        "has begun exploring stars, meeting other intelligent civilisations "
        "along the way. You are a crew member on the Earth Ship Turing, "
        "en-route to the planet Ral'Malgor. Your quest is simple: enjoy your "
        "first trip in space!",
        "days": [
            "Snakes and ladders",
            "Wordle with friends",
            "Survey an asteroid belt",
            "Lost in transmission",
            "Message from afar",
        ],
    },
    "2022": {
        "name": "2022",
        "title": "2022 Challenge",
        "topic": 44,
        "page": 286,
        "intro": "It's the year 2222. Working as an apprentice on the Earth "
        "Ship Turing, you and the crew are taking a brief rest stop on the "
        "planet Ral'Malgor. Enjoying your free time before the journey back "
        "to Earth, you embark on a quest: Find the perfect souvenir in the "
        "local alien markets!",
        "days": [
            "Engine diagnostics",
            "Lottery tickets",
            "Tour the stars",
            "Obsessing over Connect 4",
            "Spot the forgery",
            "Debugging",
            "Check the heat shields",
            "Message from home",
            "Lost in an alien market!",
            "A special painting",
        ],
    },
    "2023": {
        "name": "2023",
        "title": "2023 Challenge",
        "topic": 46,
        "page": 301,
        "intro": "The year is 2223 and you are completing your apprenticeship "
        "on the Starship Turing. You have had fun exploring the stars and "
        "strange new worlds but your mission is over and you are now headed "
        "home to Earth. Will your technical expertise in computer science be "
        "needed to save the day, or will you be able to relax and enjoy the "
        "ride?",
        "days": [
            "Inventory check",
            "Navigation sensor",
            "Tic tac toe",
            "Mayday!",
            "Decoding pixels",
            "Avoid the asteroids",
            "Snakes on a spaceship",
            "Shopping expedition",
            "Index tree",
            "The route home",
        ],
    },
    "2024": {
        "name": "2024",
        "title": "2024 Challenge",
        "topic": 47,
        "page": 311,
        "intro": "",
        "days": [
            "Purchase tickets",
            "Broken firewall",
            "Hotel door code",
            "Closest star systems",
            "Busy moon rovers",
            "Time to play fair",
            "The purge",
            "Connecting cities",
            "Mining tunnels",
        ],
    },
}


# ===========================================================================
# Day states
# ===========================================================================


def days_in(event: str) -> int:
    """Number of days of an event."""
    return len(CALENDAR[event]["days"])


def star(result: Result | None) -> str:
    """'ok', 'unknown' (answer not known locally) or 'no'."""
    answer = result["answer"] if result else None
    return answer if answer in ("ok", "unknown") else "no"


def state(result: Result | None) -> str:
    """One of 'fast', 'slow' or 'unsolved'."""
    if result is None or result["status"] != "solved":
        return "unsolved"
    if result["time"] is None:
        return "unsolved"
    return "fast" if result["time"] < FAST else "slow"


def format_time(seconds: float) -> str:
    """Human-readable duration: < 1 ms, 12 ms, 3.2 s, 1 min 05 s."""
    if seconds < 0.001:
        return "< 1 ms"
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 60:
        return f"{seconds:.1f} s"
    minutes, seconds = divmod(round(seconds), 60)
    return f"{minutes} min {seconds:02} s" if seconds else f"{minutes} min"


def summary(event: str, days: dict[str, Result]) -> Summary:
    """Stars, state of every day and total solving time of an event."""
    results = [days.get(str(day)) for day in range(1, days_in(event) + 1)]
    states = [state(result) for result in results]
    return {
        "stars": sum(star(result) == "ok" for result in results),
        "max": days_in(event),
        "states": states,
        "time": sum(
            result["time"]
            for result, s in zip(results, states)
            if s != "unsolved"
            and result is not None
            and result["time"] is not None
        ),
    }


def events() -> list[str]:
    """Every event, the latest first."""
    return list(reversed(CALENDAR))


# ===========================================================================
# Uncommitted code
# ===========================================================================


def committed_blobs() -> dict[str, str] | None:
    """Git object id of every file of the last commit, by path."""
    try:
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    entries = (entry.split("\t", 1) for entry in listing.split("\0") if entry)
    return {path: meta.split()[2] for meta, path in entries}


def uncommitted(results: Results) -> set[tuple[str, str]]:
    """(event, day) of the results measured on uncommitted code."""
    blobs = committed_blobs()
    if blobs is None:
        return set()
    flagged: set[tuple[str, str]] = set()
    for event in events():
        for day, entry in results["events"].get(event, {}).items():
            path = f"events/{event}/day_{int(day):02}/solver_{int(day):02}.py"
            if entry.get("code") != blobs.get(path):
                flagged.add((event, day))
    return flagged


# ===========================================================================
# Pages
# ===========================================================================


def symbol(day_state: str) -> str:
    """Symbol of a day state, always in the code font, so that it looks the
    same as in the strips: block characters differ a lot between fonts."""
    return f"`{SYMBOLS[day_state]}`"


def strip(states: list[str]) -> str:
    """One symbol per day, as one code span per block of five days."""
    symbols = "".join(SYMBOLS[s] for s in states)
    return NBSP.join(
        f"`{symbols[i:i + 5]}`" for i in range(0, len(symbols), 5)
    )


def labels(timeout: float) -> dict[str, str]:
    """Meaning of each day state."""
    return {
        "fast": f"solved in under {FAST} s",
        "slow": f"solved in under {format_time(timeout)}",
        "unsolved": "not solved",
    }


def legend(timeout: float) -> str:
    """Meaning of the day symbols, on one line."""
    return " &emsp; ".join(
        f"{symbol(s)} {label}" for s, label in labels(timeout).items()
    )


def environment(meta: Meta) -> str:
    """Where and when the benchmark ran."""
    parts: list[str] = []
    if python := meta.get("python"):
        parts.append(f"Python {python}")
    if machine := meta.get("machine"):
        parts.append(machine)
    if date := meta.get("date"):
        day = datetime.date.fromisoformat(date)
        parts.append(day.strftime("%-d %B %Y"))
    return " · ".join(parts)


def homepage(results: Results, flagged: set[tuple[str, str]]) -> str:
    """Global scoreboard: one row per event."""
    lines = [
        "| Event | Days | ★ | Time |",
        "| :-- | :-- | --: | --: |",
    ]
    total: Summary = {"stars": 0, "max": 0, "states": [], "time": 0}
    for event in events():
        s = summary(event, results["events"].get(event, {}))
        time = format_time(s["time"]) if s["time"] else "–"
        lines.append(
            f"| [{CALENDAR[event]['title']}](events/{event}/README.md) "
            f"| {strip(s['states'])} | {s['stars']}/{s['max']} | {time} |"
        )
        total["stars"] += s["stars"]
        total["max"] += s["max"]
        total["states"] += s["states"]
        total["time"] += s["time"]
    counts = " ".join(
        f"{symbol(s)} {total['states'].count(s)}" for s in STATES
    )
    lines.append(
        f"| **Total** | {counts} | **{total['stars']}/{total['max']}** "
        f"| {format_time(total['time']) if total['time'] else '–'} |"
    )

    timeout = results["meta"].get("timeout", 300)
    notes = [legend(timeout)]
    if flagged:
        notes.append(
            f"{len(flagged)} result(s) measured on uncommitted code, "
            "marked † on the event pages"
        )
    notes.append(environment(results["meta"]))
    return "\n".join(
        [
            "## Scoreboard",
            "",
            *lines,
            "",
            f"<sub>{'<br>'.join(notes)}</sub>",
        ]
    )


def stars_cell(day_star: str) -> str:
    """★ earned, ☆ not earned, ? answer unknown locally (cannot be checked)."""
    return {"ok": "★", "no": "☆", "unknown": "?"}[day_star]


def time_cell(result: Result, timeout: float) -> str:
    """Solving time, or why there is none."""
    if result["status"] == "timeout":
        return f"> {format_time(timeout)}"
    if result["time"] is None:
        return "error"
    return format_time(result["time"])


def navigation(event: str) -> str:
    """Links to the previous event, the scoreboard and the next event."""
    order = list(CALENDAR)
    index = order.index(event)
    links: list[str] = []
    if index > 0:
        previous = order[index - 1]
        links.append(
            f"[← {CALENDAR[previous]['name']}](../{previous}/README.md)"
        )
    links.append("[Scoreboard](../../README.md#scoreboard)")
    if index + 1 < len(order):
        following = order[index + 1]
        links.append(
            f"[{CALENDAR[following]['name']} →](../{following}/README.md)"
        )
    return " · ".join(links)


def summary_table(s: Summary, timeout: float) -> list[str]:
    """Stars, number of days in each state and solving time."""
    lines = [f"| Stars | {s['stars']}/{s['max']} |", "| :-- | --: |"]
    lines += [
        f"| {symbol(key)} {label} | {s['states'].count(key)} |"
        for key, label in labels(timeout).items()
    ]
    time = format_time(s["time"]) if s["time"] else "–"
    return lines + [f"| Time of solved days | {time} |"]


def puzzle_url(event: str, day: int) -> str:
    """Page of a day in the Coding Quest archive."""
    edition = CALENDAR[event]
    return f"{ARCHIVE}/{edition['topic']}/doc/{edition['page'] + day - 1}"


def day_table(
    event: str,
    days: dict[str, Result],
    s: Summary,
    timeout: float,
    flagged: set[tuple[str, str]],
) -> list[str]:
    """One row per day: title, symbol, star and time."""
    lines = [
        "| Day | Puzzle | Solution | Time |",
        "| --: | :-- | :-- | --: |",
    ]
    for day, puzzle in enumerate(CALENDAR[event]["days"], 1):
        entry = days.get(str(day))
        cells = [str(day), f"[{puzzle}]({puzzle_url(event, day)})"]
        day_symbol = symbol(s["states"][day - 1])
        day_star = stars_cell(star(entry))
        if entry is None:  # no solution: nothing to link or time
            cells += [f"{day_symbol} {day_star}", ""]
        else:
            flag = (event, str(day)) in flagged
            cells += [
                f"{day_symbol} [{day_star}](day_{day:02}/solver_{day:02}.py)",
                time_cell(entry, timeout) + (" †" if flag else ""),
            ]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def event_page(
    results: Results, event: str, flagged: set[tuple[str, str]]
) -> str:
    """Detailed page of an event: summary, then one row per day."""
    days = results["events"].get(event, {})
    s = summary(event, days)
    timeout = results["meta"].get("timeout", 300)

    notes = [legend(timeout)]
    if any(star(entry) == "unknown" for entry in days.values()):
        notes.append("? no answer known locally, so it cannot be verified")
    if any(key[0] == event for key in flagged):
        notes.append("† measured on code that differs from the last commit")
    notes.append(environment(results["meta"]))

    intro = CALENDAR[event]["intro"]
    return "\n".join(
        [
            f"# Coding Quest {CALENDAR[event]['title']}",
            "",
            *([f"_{intro}_", ""] if intro else []),
            navigation(event),
            "",
            *summary_table(s, timeout),
            "",
            *day_table(event, days, s, timeout, flagged),
            "",
            f"<sub>{'<br>'.join(notes)}</sub>",
            "",
        ]
    )


# ===========================================================================
# Output
# ===========================================================================


def render() -> None:
    """Write the global scoreboard and every event page."""
    with open(RESULTS, encoding="utf-8") as f:
        results: Results = json.load(f)
    flagged = uncommitted(results)

    text = README.read_text(encoding="utf-8")
    start, end = MARKERS
    block = f"{start}\n{homepage(results, flagged)}\n{end}"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"README.md has no {start} … {end} block to fill")
    README.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")

    pages = events()
    for event in pages:
        page = EVENTS / event / "README.md"
        page.write_text(event_page(results, event, flagged), encoding="utf-8")
    print(f"Scoreboards written: README.md and {len(pages)} event page(s)")


if __name__ == "__main__":
    render()
