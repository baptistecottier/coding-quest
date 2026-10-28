# Coding Quest Puzzles

This repository contains my solutions for the [Coding Challenges archive](https://pbaumgarten.com/docs/codingchallenges/) puzzles.

<!-- scoreboard:start -->
## Scoreboard

| Event | Days | ★ | Time |
| :-- | :-- | --: | --: |
| [2024 Challenge](events/2024/README.md) | `     ` `    ` | 0/9 | – |
| [2023 Challenge](events/2023/README.md) | `█████` `█████` | 10/10 | 52 ms |
| [2022 Challenge](events/2022/README.md) | `████▓` `█████` | 10/10 | 1 min 03 s |
| [2022 Prequel](events/prequel/README.md) | `█████` | 5/5 | 6 ms |
| **Total** | `█` 24 `▓` 1 ` ` 9 | **25/34** | 1 min 03 s |

<sub>`█` solved in under 1 s &emsp; `▓` solved in under 5 min &emsp; ` ` not solved<br>2 result(s) measured on uncommitted code, marked † on the event pages<br>Python 3.13.14 · Apple M3 · 28 October 2026</sub>
<!-- scoreboard:end -->

## Benchmark

```bash
uv run benchmark.py                    # every event
uv run benchmark.py 2023 prequel       # some events
uv run benchmark.py 2022 --days 1-5    # some days
uv run benchmark.py --changed          # only what changed since its last run
uv run benchmark.py --render           # redraw from benchmarks.json
```

Each day runs on the personal input in its own process with a 5 minute timeout; the time
covers preprocessing and solving. Answers are checked against the ones Puzzle Submitter
recorded as correct, completed by the `user_answer` of the data JSON files. Results are
stored in `events/benchmarks.json`, from which `scoreboard.py` writes the scoreboard above
and one page per event.
