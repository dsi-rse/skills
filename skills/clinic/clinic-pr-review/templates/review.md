# Clinic PR review: #<n> <PR title>

**Repository:** <url> · **Author:** @<login> · **Task:** #<issue> · **Reviewed:** <date> at `<head sha>`

## Verdict: <Ready to merge | Changes requested | Could not verify>

<One or two sentences: what the PR does and the main reason for the verdict.>

## For the TA

### Checklist

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
| 13 | Results reproducible | could not verify | data on Box; TA copy not provided |
| 14 | No train/test leakage | n/a | no modeling |

### Flags

<Only if any: deleted or weakened tests, new ignores, edits to AGENTS.md or CLAUDE.md, committed secrets or data, unrelated changes. One line each, with the file.>

### What I ran

- `<command>` → <outcome>
- `<command>` → <outcome>

### Could not verify

- <what, why, and what the TA would need to do to check it>

---

## Comment for the student

*(Paste-ready. Everything below the line.)*

---

<One-sentence summary of the PR and where it stands.>

**What's working:** <one or two specific things done well>

**Requested changes**

1. **<Short title>** — <what is wrong and why it matters, in one sentence>. <What to do, in one sentence.> (`<file>` or `<notebook>`, cell <n>)
2. **<Short title>** — <...>

**Suggestions (optional)**

- <one line each, at most three>

<If a follow-up review: open with "**From the last review:** 1 done · 2 done · 3 not yet — <one line on what's left>".>
