# Training mode (sample repos only)

Mentor training runs on a fake project where one facilitator plays several students from a single
GitHub account. Normal attribution would lump all of that work under one login — and, since the
facilitator is usually a mentor, exclude it entirely. Training mode instead reads the student from a
tag the facilitator writes into each artifact.

## When it applies

Only when the repository name matches `clinic-<four-digit year>-sample` exactly (for example
`dsi-rse/clinic-2026-sample`). Check the name, not the README.

In **every other repo, ignore the tags completely** and attribute by login as usual. Otherwise one
student could write `[student:someone-else]` and move work between people in a real review.

Say it at the top of the Phase 1 recap and in the report header: *"Training mode: students are read
from `[student:…]` tags, not GitHub logins."*

## The tag

```
[student:<name>]
```

`<name>` must match a student listed in the README's roster — e.g. `A` for "Student A", or
`alex` for "Alex Kim". Matching is case-insensitive (`[Student:a]` is student `A`). A tag naming
nobody on the README roster is not a student — it is usually documentation of the syntax
(`[student:X]`) — so ignore it and do not add it to the roster. Write it anywhere in:

| Artifact | Where the tag goes | Example |
|---|---|---|
| Issue | title | `Week 2 tasks – [student:A]` |
| Pull request | title or body | `Add requests_per_type [student:A]` |
| Commit | message (subject or body) | `Add requests_per_type summary (#12) [student:A]` |
| Comment (issue or PR) | anywhere in the body | `## Weekly Report — Week 2 [student:A]` |

## Inheritance, for untagged artifacts

The facilitator will forget a tag sometimes. When an artifact has no tag and is authored by the same
login as the tagged artifacts, take the student from, in order:

1. **Comment** → the issue or PR it is on.
2. **Commit** → the PR it belongs to; else a branch named `<name>/…` that matches a tagged student.
3. **Pull request** → the issue it closes or links (`Closes #n`).

Mark inherited attributions *(inherited from #n)* in the ledger.

## Untagged work with nothing to inherit

Fall back to normal attribution by login. One rule, applied in order:

1. **Tagged** → the tagged student, whatever login made it.
2. **Inherited** → the student it inherits from (above).
3. **Author is a real student on the roster** (a mentor at the session playing themselves from
   their own account) → that student, as in any review.
4. **Author is the facilitator, a mentor, or a bot** → not student work; excluded like any mentor's.
   Mention the count in one line ("3 setup commits by the facilitator, excluded").
5. **Anyone else** → **unattributed**. Do not guess.

## Do not read the answer key

Facilitator materials that describe what each role was *meant* to do — the seed script, a
pre-generated sample review — are kept out of sample repos (in `dsi-rse/clinic-automation`). If a
sample repo still contains one (a `seed` script, a `sample-review.md`), do not open it, keep it
out of any `git show` or diff you read, and never use it as evidence. The session runbook
(`docs/SESSION.md`) is fine to read. The exercise is whether the review
finds the problems from the issues, commits, and PRs alone; knowing the intended failure in advance
turns it into a confirmation of the script. (The README and project docs are fine, as in any review.)

## Roster

Take the students from the README's roster, as in any review. For each, find the tag that names
them and the login that played it; add any real mentors-as-students whose own logins did untagged
work. The Phase 0 roster confirmation is still blocking, but for tagged students the mapping is
**README name ↔ tag ↔ the login that played it** — they have no login of their own. The
facilitator is never a student in their own right; their login appears only as "played by".
Confirm it like: *"Students: A, B, C (tags, played by `tspread`), plus `jdoe` and `mlee`. `tspread`
is the facilitator — right?"*

In the report, write tagged students as `Student A` in the tables; the header's training-mode line
says who played them (`played by @tspread`).

Everything else in the review — the checks, the direction section, the task menu — runs unchanged.
