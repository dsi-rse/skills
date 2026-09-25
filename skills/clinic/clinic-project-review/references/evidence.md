# Evidence gathering

Everything in the report traces back to something pulled here. Pull once, record it, then interpret.

Two rules for every command below:

- **An error is not an empty result.** `gh` prints GraphQL and permission errors to stderr and can
  still leave you with no data. Check each pull actually returned JSON before reading "no PRs" or
  "no issues" as a finding.
- **Filter JSON with `gh`'s built-in `--jq` or with Python.** A standalone `jq` is often not
  installed; do not pipe into it.

## 1. Define the windows

Two time windows, and they are different:

- **The review window** — the week under review. Default: from the previous team meeting to now.
  Infer the meeting day from the weekly clustering of issue creation and closing timestamps; the
  clinic rhythm usually leaves a visible spike. Fall back to the last 7 days.
- **The history window** — for pattern checks (repetition, task sizing, stalled goals). Default
  4 weeks, i.e. the review window plus the three before it.

Record both windows in ISO dates at the top of the report. Every "last week" statement is meaningless
without them, and a mentor reviewing on a Tuesday for a Thursday meeting needs to know which days
you counted.

## 2. What to load

### The repository

```bash
gh repo view --json name,description,url,pushedAt,defaultBranchRef
```

- `README.md` — the project brief, the goals, and the student list. This is the reference point for
  every judgment about direction. Read it fully.
- Any `PROJECT_SETUP.md`, `TUTORIAL.md`, `DATA.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`,
  `docs/` — these tell you what students were told to do and how the project is meant to run.
  (In a training repo, skip the answer-key files listed in `training-mode.md`.)
- `.github/ISSUE_TEMPLATE/` — the task template defines what a well-formed task looks like *in this
  repo*. If it has a "Definition of Done" section, that is the standard you judge acceptance
  criteria against, not a generic one.

If the README has no project brief, no goals, or no student list, note it. The brief and goals are
the clinic staff's responsibility, and their absence is worth one line in the report for the mentor 
to report it. The student list is the students' responsibility and the mentor should know if someone is missing.

### Every issue

```bash
gh issue list --state all --limit 500 \
  --json number,title,author,assignees,labels,state,createdAt,updatedAt,closedAt,url,body,comments
```

`comments` carries each comment's author, body, and timestamp — the follow-up posts that show
progress. For an issue that matters, get its full event history (assignment changes, reopenings,
cross-references from commits and PRs):

```bash
gh api "repos/<owner>/<repo>/issues/<n>/timeline" \
  --jq '.[] | {event, actor: .actor.login, created_at, commit_id, source: .source.issue.number}'
```

Reopenings and reassignments are the cleanest signal for the repetition check.

### Every pull request

```bash
gh pr list --state all --limit 200 \
  --json number,title,author,createdAt,updatedAt,mergedAt,closedAt,state,isDraft,url,body,additions,deletions,changedFiles,headRefName,reviews,comments
```

Do not add `commits` or `files` to that bulk query: GitHub sizes the query by its limits, and those
two fields push it over the node cap, so it fails outright on every repo. Fetch them per PR, for the
PRs in the review window:

```bash
gh pr view <n> --json files,commits,mergeCommit \
  --jq '{files: [.files[].path], merge: .mergeCommit.oid, commits: [.commits[] | {sha: .oid[0:7], authors: [.authors[].login], msg: .messageHeadline}]}'
```

For each PR in the review window, note whether it was merged (not just opened), who reviewed it,
whether review comments were answered, and what it actually touched. "Merged to the default branch"
is the standard for a coding task being complete.

### The commits

```bash
git log --since="<window start>" --pretty='%h|%an|%ae|%aI|%s' --no-merges
git log --since="<window start>" --numstat --pretty='%h|%an|%aI|%s' --no-merges   # sizes
git shortlog -sne --since="<window start>"                                        # per-author totals
```

If there is no local clone, or the clone is stale, go through the API instead:

```bash
gh api "repos/<owner>/<repo>/commits?since=<ISO>&per_page=100" \
  --jq '.[] | {sha: .sha[0:7], login: .author.login, name: .commit.author.name, date: .commit.author.date, msg: (.commit.message | split("\n")[0])}'
```

Look at commits on **all branches**, not just the default one — a student pushing to a feature
branch is making work visible even before a PR exists. Fetching into the mentor's clone is fine: it
only updates remote-tracking refs (`origin/*`) and never touches their files or local branches.
Do nothing else in their clone.

```bash
git fetch --all --prune
git log --all --since="<window start>" --pretty='%h|%an|%aI|%d %s' --no-merges
```

If the fetch fails on authentication — typically an SSH remote (`git@github.com:...`) on a machine
without SSH keys — do not change the remote or the mentor's git config. Treat the clone as stale and
use the API, branch by branch:

```bash
gh api "repos/<owner>/<repo>/branches?per_page=100" --paginate --jq '.[].name'
gh api "repos/<owner>/<repo>/commits?sha=<branch>&since=<ISO>&per_page=100" --paginate \
  --jq '.[] | {sha: .sha[0:7], login: .author.login, date: .commit.author.date, msg: (.commit.message | split("\n")[0])}'
```

The same commit shows up on every branch that contains it; dedupe by SHA.

### Anything else that shows work

Project boards (`gh project item-list`, if the team uses one), issue cross-references from other
repos, releases, and CI runs (`gh run list`) when a student's task was about getting the pipeline
green. Do not go hunting far — but if the mentor mentioned a second repo, load it.

## 3. Attribution — get this right

The report assigns work to named people. Misattribution is the failure mode with real consequences.

- **Training repos** (`clinic-<year>-sample`) attribute by `[student:<name>]` tag first; see
  `training-mode.md`. Everywhere else, ignore those tags.
- **Build the map explicitly**: real name (from the README roster) ↔ GitHub login ↔ commit author
  name and email. Students commonly commit under a personal email, a laptop default name
  (`jsmith@Jane-MacBook-Air.local`), or `noreply@github.com` for web-UI edits.
- **Resolve, then confirm.** Present the map in Phase 1 and let the mentor fix it. Never guess a
  mapping into the report; if a commit author cannot be tied to a person, list it as unattributed.
- **Exclude non-students.** Mentors, TAs, external collaborators, bots (`dependabot`,
  `github-actions`, `pre-commit-ci`) and AI-agent co-authors all appear in these histories. Count
  only the roster. Note when a mentor or TA authored a substantial share of the week's commits —
  useful context, not a student result.
- **Co-authored commits**: check `Co-authored-by:` trailers so paired work counts for both students.
- **Pushed ≠ authored.** A student who merges someone else's PR has not written that code.

## 4. The evidence ledger

One row per artifact, grouped by student. Build it before interpreting anything.

| Student | When (ISO) | Kind | Ref | One-line description | Notes |
|---|---|---|---|---|---|
| Jane Smith | 2026-09-16 | issue created | #42 | "Add IDW interpolation for daily normals" | has Definition of Done |
| Jane Smith | 2026-09-18 | commits (3) | `a1b2c3d`..`e4f5a6b` | interpolation module + test | on branch `jane/idw`, not merged |
| Jane Smith | 2026-09-19 | issue comment | #42 | claims done, links notebook | notebook not in repo |

Kinds worth distinguishing: `issue created`, `issue closed`, `issue reopened`, `issue comment`,
`commits`, `PR opened`, `PR merged`, `PR review given`, `review comment answered`.

Two rules:

- **Timestamps are UTC from the API.** Do not convert casually; a task created "Friday night" versus
  "Monday morning" changes the on-time verdict, so state the date and let the mentor read the day.
- **Substance, not count.** Three commits fixing a typo in a README are not a week of work, and one
  400-line commit implementing an evaluator is. Record sizes (`--numstat`) and glance at the diff
  before characterizing volume. Never report commit counts alone as a measure of effort.

## 5. What you could not see

Keep a running list of gaps: private repositories, data in Box, results shared in Slack, a linked
Google Doc, a stale local clone, API results truncated by a limit, code that was not run (the
mentor chose read-only) or was run without Docker. Report the list. A mentor who
knows what you missed can trust the rest.
