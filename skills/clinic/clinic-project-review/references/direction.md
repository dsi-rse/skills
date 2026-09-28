# Overall direction

Two questions about the project rather than the students, plus a risk note. In the report this is
one goal table and at most three one-line bullets (sizing, risk, and one process note if it
matters). A mentor who wants depth will ask.

## 1. Do the tasks serve the project goals?

Start from the goals as the README states them. If the README has no goals section, say that first
and use the best available substitute (the client's problem statement, the mentor's own description
in intake), clearly labeled as a substitute.

One row per goal, in the README's own words. If the README states the goals as one sentence,
split it only at the distinct outcomes it names ("summarize volume and response times … and show
them on the dashboard" → volume · response times · dashboard), keeping its wording; do not invent
sub-goals it does not name.

Build the mapping, then read it both ways. In the report, collapse the task columns into one
("#42, done #17"):

| Goal | Active tasks | Completed this term | Status |
|---|---|---|---|
| Centralize climate data sources | #42, #47 | #17, #23 | advancing |
| Serve data through a queryable interface | — | — | **no task since 2026-08-18** |

- **Orphan tasks** — a task serving no stated goal. Sometimes it is infrastructure that serves all
  of them (fix CI, write the data loader), which is fine and worth naming as such. Sometimes it is
  drift: interesting work that will not appear in the final deliverable. Flag drift explicitly; it is
  the most expensive failure in a ten-week project and the least likely to be noticed from inside.
- **Orphan goals** — a goal with no task advancing it, and for how long. A goal untouched for a
  month with four weeks left in the term is the headline of the whole report.
- **Deliverable check** — if the project has a final deliverable (report, dashboard, model, dataset),
  ask whether the current trajectory produces it in the time left. Say plainly if it does not.

## 2. Are the weekly task sizes right?

Calibrate against this project's own completion history, not intuition. Over the history window,
for each completed task: how long between creation and close, and how much work landed?

| Signal | Reading |
|---|---|
| Most tasks carry over 2+ weeks | too big |
| Work done within the week, but PRs wait days for a first review | size okay; reviewer is the bottleneck |
| Work done within the week, but students are slow to answer review comments | size okay; students need to close out reviews |
| Tasks closed with substantial merged work, weekly | about right |
| Tasks closed in a day or two, repeatedly, with small diffs | too small — the student has idle hours |
| Tasks closed on time but with acceptance criteria quietly unmet | too big, and being absorbed by cutting scope silently |
| One student's tasks are consistently larger than the others' | uneven load; worth naming |

The "criteria quietly unmet" row is the one to watch for. It looks like a healthy board and is not.

Report the sizing judgment **per student as well as overall** when they differ — the fix ("give this
student a bigger slice next week") is per student.

## 3. Process observations

Only when the evidence supports them, and only if it is project-level and not already a student
finding (say each fact once — a student's unreviewed PR belongs in Findings). Put at most one in the
report; the rest can wait for the mentor to ask:

- **Task hygiene** — are tasks written before work starts, or retroactively? Retroactive issues (an
  issue created the same day it is closed, after the commits landed) mean the board is a log, not a
  plan.
- **Review flow** — are PRs getting reviewed, and are comments being answered? A PR open for a week
  with no review is a project problem, not a student problem.
- **Merge discipline** — is work reaching the default branch, or accumulating on branches?
- **Reproducibility** — are reported results backed by committed code and documented data paths?
  A number in a Slack screenshot is not a project artifact.
- **Concentration** — is one person (a strong student, or the mentor) producing most of the work?
  Say it with the numbers and no adjectives.

## 4. Risk note

One short list of things that could derail the project, with what would resolve each. Typical ones:
a data dependency that has been blocked for weeks; a track nobody has touched; an analysis whose
results cannot be reproduced; a single-point-of-failure student holding the only working pipeline;
a deadline that no longer fits the remaining scope.

If there are none, write "no project-level risks visible this week" and move on. Do not manufacture
risk to fill the section.
