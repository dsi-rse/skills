# Clinic PR review: #<n> <PR title>

**Repository:** <url> · **Author:** @<login> · **Task:** #<issue> · **Reviewed:** <date> at `<head sha>`

## Verdict: <Ready to merge | Changes requested | Could not verify>

<One or two sentences: what the PR does and the main reason for the verdict.>

<If a follow-up review: "**From the last review:** 1 done · 2 done · 3 not addressed — <one line on what's left>". Mark "replied" where the student explained why not, and say whether the reason holds.>

## Key findings

Ranked, most important first; five or fewer. Each is evidence for the TA to check, not text for the student.

1. **<Short title>** (blocking) — <what is wrong and why it matters, in one sentence>. <What fixing it would look like.> Evidence: `<file>` or `<notebook>`, cell <n>; <what you ran or read>.
2. **<Short title>** (blocking) — <...>

**Optional suggestions** (at most three, one line each):

- <...>

**What's working:** <one or two specific things done well — worth the TA mentioning>

## Checklist

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Notebooks run in order on a fresh clone | pass | all 4 notebooks ran in Docker (`01_`–`04_`) |
| 2 | Functions in modules, not notebooks | fail | `03_features.ipynb` cells 2, 5 define `clean_dates`, `bin_ages` |
| 3 | Clear notebook names | pass | |
| 4 | Runs in Docker | pass | `docker build` ok; `pytest` ok in container |
| 5 | Documented, clear purpose | pass | |
| 6 | No dead code | fail | `utils/io.py:40-58` commented-out loader |
| 7 | Tested | fail | `utils/features.py:bin_ages` has no test |
| 8 | Deleted tests justified | n/a | no tests removed |
| 9 | Ruff changes justified | pass | no new ignores |
| 10 | AGENTS.md followed / changes flagged | pass | AGENTS.md unchanged |
| 11 | PR links its issue | pass | closes #12 |
| 12 | Solves the task | pass | 3/3 acceptance criteria met |
| 13 | Coherence |  pass | 3/3 | |
| 14 | Results reproducible | could not verify | data on Box; TA copy not provided |
| 15 | No train/test leakage | n/a | no modeling |

## Flags

<Only if any: deleted or weakened tests, new ignores, edits to AGENTS.md or CLAUDE.md, committed secrets or data, unrelated changes. One line each, with the file.>

## What I ran

- `<command>` → <outcome>
- `<command>` → <outcome>

## Could not verify

- <what, why, and what the TA would need to do to check it>

