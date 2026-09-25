# <Project name>: week of <ISO start> → <ISO end>

<repo url> · reviewed <date> · history <ISO start> → <ISO end> · Box: <yes / skipped / n/a> · Code: <Docker / uv / pip / not run>
*(Training repos only:)* Training mode: students read from `[student:…]` tags, played by @<login>.
<If any: "Excluded: <n> commits by <mentor/facilitator/bot>.">

## Students

| Student | Tasks | Criteria | Visible | Accurate | Repeating | Ask |
|---|---|---|---|---|---|---|
| <name> | yes [#42] | partly | yes [PR #45] merged | partly [report-a] ▶ | no | <one short question> |
| <name> | no | — | no | — | yes, wk 3 [#38] | <one short question> |

▶ = checked by running the code · ? = inferred, not seen directly · — = no task to judge.

## Findings

The *why* behind a table cell, only where the cell alone would leave the mentor asking "what
happened?". Never restate the verdict; a cell that says it all gets no line. Most important first.

- **<name>:** <the specific gap, e.g. "PR #45 skips the daily-normals case in the criteria"> ([#45])
- **Good:** <name> — <one notable thing done well>

## Direction

| Goal | Tasks | Status |
|---|---|---|
| <goal> | #42, done #17 | advancing |
| <goal> | — | **no task since <date>** |

- **Sizing:** <too big / right / too small> — <evidence, a few words>
- **Risk:** <risk> — <fix>

## Code run

| Ran | On | Result |
|---|---|---|
| `pytest` | `main` @ `a1b2c3d` | 14 passed |

Not Docker: <only differences that could change a result, one line; omit if none>. Skipped: <what, why>.
*(If not run: "Not run (read-only). Unverified: <claims>." — one line, no table.)*

## Next week

Options for each student; pick one each. Say which to expand into a full issue.

| # | Student | Task | Hrs | Done when | Why |
|---|---|---|---|---|---|
| A1 | <name> | <verb + object> | ~8 | <artifact + check>; PR merged | <goal or gap> |
| A2 | <name> | <verb + object> | ~6 | <artifact + check> | <goal or gap> |

<One line for dependencies, parallel tracks (and their shared metric), or fallbacks — omit if none.>

## Not seen

<Comma-separated: Slack, Box, stale clone, meeting days, code not run, …>

[#42]: <issue url>
[PR #45]: <pr url>
[report-a]: <url of the student's weekly-report comment>
