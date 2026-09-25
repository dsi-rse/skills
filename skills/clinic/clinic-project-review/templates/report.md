# Weekly project review: <project name>

**Review window:** <ISO start> → <ISO end> (<n> days) · **History reviewed:** <ISO start> → <ISO end>
**Repository:** <url> · **Reviewed:** <date>
*(Training repos only:)* **Training mode:** students read from `[student:…]` tags, not GitHub logins.
**Box access:** <yes / skipped — reason / not used by this project>
**Code run:** <Docker / uv without Docker / pip without Docker / not run (mentor chose read-only)>

## The project in brief

<Two or three sentences: the client, the problem, what a finished version looks like.>

**Goals (from the README):**
1. <goal>
2. <goal>

## This week at a glance

| Student | Tasks written | Work visible | Report accurate | Repeating a task | Ask them about |
|---|---|---|---|---|---|
| <name> | yes (#42) | yes (3 commits, PR #45) | partly | no | the untested daily-normals path |
| <name> | no | no | — | yes (3rd week on #38) | what is blocking the scraper |

---

## Per student

### <Student name> (`<login>`)
*(Training repos: `### Student A (played by @<login>)`.)*

<One line summarizing the week.>

- **Tasks written:** <verdict> — <evidence with links>
- **Acceptance criteria:** <verdict> — <evidence; quote the weakest criterion if it is weak>
- **Visible results:** <verdict> — <commits, PRs, comments; whether work reached the default branch>
- **Report accuracy:** <verdict> — <the claim, the artifact, and the gap if there is one>
- **Repetition:** <verdict> — <how many weeks, and which kind of stuck if stuck>
- **Good work:** <what was notably well done, if anything>
- **Question for the meeting:** <one question>

*(Repeat per student. Skip any check with nothing to say beyond "yes".)*

---

## Direction

**Tasks against goals**

| Goal | Active tasks | Completed | Status |
|---|---|---|---|
| <goal> | #42 | #17, #23 | advancing |
| <goal> | — | — | no task since <date> |

<One paragraph: orphan tasks, orphan goals, whether the trajectory reaches the deliverable in the
time left.>

**Task sizing:** <too big / about right / too small, overall and per student where they differ, with
the completion evidence behind the call.>

**Process notes**

- <one line each, only where the evidence supports it>

**Risks**

- <risk> — <what would resolve it>

---

## Code run

*(If the code was not run, replace this section with one line: "Code was not run — the mentor chose
a read-only review. Claims that working code or a result exists were checked by reading only:
<list the claims>.")*

**Environment:** <Docker | uv, no Docker | pip, no Docker> on <OS>, commit `<sha>` of <branches>

| What ran | Branch / commit | Result |
|---|---|---|
| install | `main` @ `a1b2c3d` | ok |
| `pytest` | `main` @ `a1b2c3d` | 14 passed |
| `pytest` | `jane/idw` @ `e4f5a6b` | 1 failed — `test_daily_normals` (link) |
| `scripts/evaluate.py` (claimed 0.82 in #42) | `jane/idw` | reproduced 0.82 |

**Differences from a Docker run that could matter here** *(only when Docker was not used)*:
- <e.g. "`src/io.py` hard-codes `/data`; ran with `DATA_DIR` from `.env` instead — may behave differently in Docker">
- <e.g. "Dockerfile installs GDAL via apt; not available locally, so `test_geo.py` was skipped">

**Skipped:** <long jobs, scripts that write to Box, anything needing missing secrets — with reason>

---

## Proposed tasks for next week

A menu — pick one per student, or edit one.

### <Student name>

**<Option 1 title>**
*Why:* <one line>
*Estimate:* ~<n> hours — <justification>
*Task:* <2–4 sentences>
*Definition of done:*
- <verifiable item>
- <verifiable item>
*Resources:* <optional>
*Independence:* <no dependencies / dependency plus fallback>

**<Option 2 title>**
<same shape>

*(Repeat per student. Note explicitly where two proposals are meant to run as parallel tracks and
on what metric their results will be compared.)*

---

## What I could not see

- <private repo, Box data, Slack thread, stale clone, truncated query>
- <code not run (read-only review), or runs that could not reproduce the Docker environment>

*Verdicts marked "inferred" rest on reasoning rather than a directly observed artifact. Verdicts
marked "verified by running" were checked by executing the code; "fails locally" results from a
non-Docker run may be environment differences rather than bugs.*
