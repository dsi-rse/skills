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

`<name>` is a short label with no spaces — `A`, `B`, `C`, or `alex`. Matching is case-insensitive
(`[Student:a]` is student `A`). Write it anywhere in:

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

Sample repos carry files that describe what each role was *meant* to do — the seed script
(`docs/seed/`), a pre-generated sample review (`docs/sample-review.md`), the session runbook's
role notes. Do not open them, and never use them as evidence. The exercise is whether the review
finds the problems from the issues, commits, and PRs alone; knowing the intended failure in advance
turns it into a confirmation of the script. (The README and project docs are fine, as in any review.)

## Roster

Build the roster from the distinct tags plus the real logins that did untagged work. The Phase 0
roster confirmation is still blocking, but for tagged students the mapping is **tag ↔ the login
that played it**, not real name ↔ login — there is no real name and no login of their own. Confirm
it like: *"Students: A, B, C (tags, played by `tspread`), plus `jdoe` and `mlee`. `tspread` is the
facilitator — right?"*

In the report, head each tagged student's section `### Student A (played by @tspread)` in place of
the template's `### <Student name> (`<login>`)`, and use `Student A` in the at-a-glance table.

Everything else in the review — the checks, the direction section, the task menu — runs unchanged.
