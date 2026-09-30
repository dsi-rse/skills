# Clinic review — {{YYYY-MM-DD}}

Window: {{since}} to {{until}} · Repos: {{n}} · TA review depth: {{mode, plus overrides}} · Data: `{{DIR}}`

## Summary

<!-- One row per repo plus ALL, copied from summarize.py --json "stats". Keep column order. -->
| repo | students active/total | issues opened / closed | AC clear | PRs opened / merged / closed unmerged | median days to merge | median days to TA review | TA-reviewed before merge | open PRs | unmerged branches |
|---|---|---|---|---|---|---|---|---|---|
| **ALL** | | | | | | | | | |

Flag counts: {{flag=n, ...}}

## Flags

<!-- Group by repo, then by flag. Several subjects per flag go in one row. Evidence is a link
or a value, never a sentence. Include the source column from summarize.py. -->
| repo | flag | subjects | evidence | source |
|---|---|---|---|---|

## Flagged projects

<!-- Only repos with flags. At most 5 bullets each, facts only. -->
### {{repo}}
- Students: {{login: last push YYYY-MM-DD, issues n, PRs n}} …
- Default branch: last merge {{date}} (#n); {{k}} unmerged branches; protected {{yes/no}}
- Checklist (latest main-states row, {{mode}}): fail {{items}}; cnv {{items}}
- Merged PRs this window: {{#n failing items}} …
- Issues this window: {{#n ac_clarity}} …

## Judged this run

- Issues judged: {{n}} ({{very_clear/clear/unclear/very_unclear counts}})
- PR checklists: {{done n / skipped n}}, by mode {{…}}
- main-states rows appended: {{n}}

## Gaps

<!-- Fetch errors, apply.py rejections, repos skipped in Phase 2, cnv reasons grouped. -->
- {{…}}
