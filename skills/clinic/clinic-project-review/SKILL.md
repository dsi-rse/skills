---
name: clinic-project-review
description: Weekly mentor's review of a UChicago DSI Data Science Clinic project repository. Reads the README, every issue, the commits and pull requests (and, if the mentor opts in, runs the code — with Docker or without), then reports per-student status (did they write tasks, were the tasks well defined, is their work visible on GitHub, is their self-report accurate, are they stuck repeating the same task), judges whether the project's overall direction and weekly task sizes make sense, and proposes a menu of candidate tasks for next week. Use when a mentor, project lead, or instructor asks to review a student project before a weekly meeting — including phrasings like "review my clinic project", "how are my students doing", "weekly project review", "check student progress on this repo", "did my students do their tasks", "what should my students work on next week", or "write next week's clinic tasks".
---

# Clinic project review

A weekly review of one Data Science Clinic project, written **for the mentor** who runs it. You read
the repository the way an attentive mentor would if they had two uninterrupted hours: the project
brief, every issue, the commit and pull-request history, and what each student actually said about
their own week. You come back with three things — where each student stands, whether the project as
a whole is going somewhere, and a menu of tasks worth assigning next week.

The output is meeting material, not a grade. A mentor should be able to read it in five minutes
before a weekly meeting and know exactly what to ask each student.

## Scope

**In scope:** one clinic project repository, one review window (usually the week since the last
team meeting), with enough history loaded to see multi-week patterns.

**Out of scope** — say so and point elsewhere:

- **Line-by-line review of code or a pull request.** That is a different job; use the `pr-review`
  skill. Here you look at *whether* work landed and whether it matches what was claimed, not
  whether the loop should have been a comprehension.
- **Cross-project or program-wide reporting.** This skill reviews one project. Reviewing many
  projects against program rules is a separate administrative job.
- **Evaluating or grading students.** You produce evidence and questions, not assessments of
  ability. If the mentor asks for a grade recommendation, give the evidence and let them decide.

## Principles

1. **Cite everything.** Every statement about a student's week names its evidence — issue number,
   commit SHA, PR number, comment timestamp. An uncited claim in this report is a bug, because the
   mentor may repeat it to the student's face. Make each piece
   of evidence a clickable link if possible.

2. **Absent on GitHub is a finding, not a verdict.** A student with no commits may have spent the
   week reading papers, wrestling with Box access, or working locally without pushing. Report
   exactly what you can see — "no pushes or issue comments in the window" — and let the mentor
   supply the rest. Visible progress on GitHub is itself a clinic requirement, so the observation
   stands on its own without you guessing at a cause.

3. **A self-report is a hypothesis.** When a student says a task is done, open the diff. Most
   inaccuracy is not dishonesty — it is an honest "done" that means "done in my notebook", or a
   merged PR that quietly dropped half the acceptance criteria. Check, then describe the gap
   neutrally.

4. **Read-only unless asked.** Never create, edit, close, label, or comment on issues, never push,
   never open or merge a pull request, unless the mentor explicitly asks for that specific action.
   Proposing next week's tasks means *writing them in the report*, not filing them. Running the
   project's code (only if the mentor opts in) happens in a throwaway copy on the mentor's machine
   and changes nothing on GitHub or in the shared data folder.

5. **Patterns beat snapshots.** "Stuck in a loop" and "tasks are too big" are only visible across
   several weeks. Load history past the review window and compare.

6. **Say which claims you verified.** Distinguish what you confirmed by reading an artifact from
   what you inferred. Mark the difference in the report; a mentor acting on an inference should know
   it is one.

7. **The task menu is the part that gets used.** Vague tasks are the single most common failure in
   clinic projects, and a vague proposal from you becomes a vague issue. Every proposed task is
   concrete, independently workable, sized to the week, and tied to a project goal.

8. **Be brief and kind.** Critique the work and the process, never the person. Short sentences,
   plain words, no jargon the mentor would have to decode.

9. **Short beats complete.** Mentors skim. Aim for a report that reads in two minutes: tables for
   anything repeated per student or per goal, one line per finding, no prose that restates a table.
   Leave out anything that is fine — "yes" in a table cell is enough. Budget: about 800 words for a
   three-student project, link definitions excluded; scale with the roster. Say each fact once. If
   a draft runs longer, cut before sending.

## Reference map

Read these on demand, not all at once.

| Read | When |
|---|---|
| `references/evidence.md` | Phase 1–2 — the exact data to pull and how to attribute it |
| `references/training-mode.md` | Prerequisites §2 — only when the repo is `clinic-YYYY-sample` (mentor training) |
| `references/box-access.md` | Prerequisites §4 — checking the mentor can read the project's Box data |
| `references/running-code.md` | Phase 2b — running the code, with or without Docker (only if the mentor opted in) |
| `references/student-status.md` | Phase 3 — the per-student checks and how to judge each |
| `references/direction.md` | Phase 4 — goal alignment and task sizing |
| `references/task-design.md` | Phase 5 — what makes a good next-week task |
| `templates/report.md` | Phase 6 — the report skeleton |

---

## Prerequisites — before Phase 0

Every evidence step goes through the GitHub CLI, and a broken `gh` fails quietly: an unauthenticated
or unauthorized call returns empty lists, and an empty issue list reads exactly like a team that did
nothing. Confirm access first, and stop if it fails.

### 1. GitHub CLI is installed and logged in

```bash
gh auth status
```

- **`gh: command not found`** — stop. Point the mentor to <https://cli.github.com> and ask them to
  come back once `gh --version` works.
- **Not logged in** — `gh auth login` is interactive, so you cannot run it for them. Ask the
  mentor to run it in their own terminal (Terminal on macOS, PowerShell on Windows); the defaults
  are fine: GitHub.com, HTTPS, log in with a web browser. Then re-run `gh auth status` yourself.
- **Project boards** — `gh project item-list` needs an extra scope: `gh auth refresh -s read:project`,
  also run by the mentor in their terminal. Ask for this only if you reach that step and the team
  uses a board.

Do not continue until `gh auth status` shows a logged-in account. Note the mentor's login — their
own commits and comments must not be counted as a student's.

### 2. Find the project repository

If the working directory is a clone, use it:

```bash
git rev-parse --show-toplevel 2>/dev/null && gh repo view --json nameWithOwner,url
```

If that returns a `dsi-rse/clinic-*` repo, confirm it in one line ("Reviewing
`dsi-rse/clinic-2026-glaciers` — right?") and move on.

Otherwise — not in a git repository, or in one that isn't a clinic project — ask which project they
mentor. List this year's clinic repos, most recently active first, so the current quarter's projects
come before last quarter's:

```bash
year=$(date +%Y)
gh repo list dsi-rse --limit 1000 --json name,description,pushedAt \
  --jq ".[] | select(.name | startswith(\"clinic-$year-\")) | [.pushedAt[0:10], .name, (.description // \"\")] | @tsv" \
  | sort -r
```

Private repos appear only if the mentor has access, so the list is partly filtered already. There
are usually more than four, so print it as a numbered list in plain text rather than through
`AskUserQuestion`, and ask the mentor to reply with a number **or paste a link to their repo**.
Accept any form — `https://github.com/owner/repo`, `owner/repo`, an SSH URL — and normalize to
`owner/repo`. If the list is empty (early January, or no org access yet), say so and ask for the
link.

Then check access to the chosen repo:

```bash
gh repo view <owner/repo> --json nameWithOwner,viewerPermission
```

**Training repos.** If the repo name is exactly `clinic-<year>-sample`, it is a mentor-training
project where one person may play several students. Switch to training mode
(`references/training-mode.md`): students come from `[student:<name>]` tags in issue titles, PR
titles, commit messages, and comments, not from GitHub logins. Tell the mentor you are doing so. In
any other repo, ignore these tags.

A "could not resolve" error on a repo that exists means the mentor's account lacks access, or the
token is not SSO-authorized for the org. Say so and stop; ask them to sort out access with clinic
staff. Never run the review against a repo you cannot fully read.

### 3. Ask whether to run the code

Ask this now, before any evidence gathering, because the answer decides whether you need a local
clone and how long the review takes. First check quietly what the machine has — `docker info`,
`uv --version`, `python3 --version` — so you can tell the mentor what will happen. Then ask with
`AskUserQuestion`, explaining the cost in plain words:

> Do you want me to run the project's code as part of the review? That means installing the
> project's Python packages on your computer (usually a few hundred MB to a couple of GB) and running
> the tests plus any results students reported this week. It adds roughly 15–30 minutes and will use
> a noticeable amount of CPU and memory while it runs. Nothing is pushed or changed on GitHub.
> [If Docker is missing:] You don't have Docker, which the project normally uses — I can run it
> without Docker and will note where that might give different results.
> If you skip this, I'll check students' claims by reading the code only, and the report will list
> what couldn't be verified.

Offer **Yes, run it** and **No, read-only**. Record the answer; do not ask again later in the
session. On a no, skip Phase 2b entirely and add "code was not run" to the report's gaps.

### 4. Check Box data access

If the project keeps its data in Box (`DATA_DIR` in `.env.example`), check the mentor can read it,
following `references/box-access.md` — whether or not they chose to run the code. List the folder
read-only; if it fails, walk the mentor through the likely cause (Box Drive not installed, folder
not shared, WSL mount missing). They may skip it, but recommend strongly that they fix it: without
it you cannot check that students' data inputs exist, and they will need the access all quarter.

### 5. Offer to make the choice stick

A mentor who started outside a repo will be asked again next week. Offer once, after the repo is
confirmed:

> Want me to clone this to `~/clinic/<repo>`? Next week, start the session in that folder and I'll
> pick up the project without asking. A local clone also gives fuller commit history across branches.

Running the code does not need this clone — it uses its own temporary copy in the scratchpad
(`references/running-code.md` §2) — so the answer here is purely about convenience next week.

Then tell them how to start there on the surface they are using: in the desktop app, pick the
folder when creating the session; in VS Code, open the folder; in the terminal,
`cd ~/clinic/<repo> && claude`.

Clone only on a yes. If they decline, carry on; they will pick from the list again next time.

Clone over HTTPS with `gh` as the credential helper, so it works without SSH keys and without
touching the mentor's global git config (`gh repo clone` would follow their `git_protocol` setting,
which may be SSH):

```bash
git clone -c credential.helper='!gh auth git-credential' \
  https://github.com/<owner/repo>.git ~/clinic/<repo>
```

The `-c` writes the helper into the clone's own config, so later `git fetch` runs in that folder
authenticate the same way.

## Phase 0 — Intake

**Infer before asking.** You can usually find: the repository (settled in Prerequisites), the
project brief and goals (README), the likely roster (README student
list, issue assignees, commit authors), and the likely meeting cadence (the weekly burst of issue
creation timestamps). Look first, then confirm what you found.

Ask for the rest in **one batch** with `AskUserQuestion`:

1. **Review window** — default: since the last team meeting, inferred from the issue history;
   fall back to the last 7 days. Offer both.
2. **Roster and GitHub logins** — show the mapping you inferred (real name ↔ login; in training
   mode, tag ↔ the login that played it) and ask the mentor to correct it. **This is blocking**: attributing one student's work to another is the
   worst thing this skill can do. Also ask who is *not* a student — mentors, TAs, and external
   collaborators commit to these repos too, and their work must not be counted as a student's.
3. **Expected weekly hours per student** — default 10.
4. **History depth for pattern checks** — default 4 weeks.
5. **Off-GitHub context** — anything you could not see: a student was ill, a task was reassigned in
   Slack, the team agreed to pause a track, data access was broken all week. This routinely explains
   the most alarming-looking finding in the whole report.
6. **Where to write the report** — a path, or inline in the conversation. Assume nothing.

If the mentor has already answered some of these, do not re-ask; recap the full set in two lines and
move on.

## Phase 1 — Load the project

Follow `references/evidence.md`. In short: README and project docs, every issue with its body,
comments, and open/close timestamps, every pull request with its review thread, and the commit log
over the history window, attributed per author.

Then report back, briefly, before doing any analysis:

- **The project in three sentences** — the client, the problem, and what a finished version looks
  like — plus the project goals as the README states them. If the README has no brief or no goals,
  say so: that is a finding in its own right, and everything downstream ("do the tasks serve the
  goals?") rests on it.
- **The roster** you will use, with logins.
- **What you could not load** — a private linked repo, a Box folder, a Slack thread, a dead link.

Confirm this with the mentor. A wrong project understanding here contaminates every later judgment.

## Phase 2 — Build the evidence ledger

Before interpreting anything, assemble the raw record: for each student, every artifact in the
window with its timestamp and a one-line description — issues created, issues closed, comments
posted, commits pushed, PRs opened, reviewed, or merged. Keep it as a table
(`references/evidence.md` §4 gives the columns).

This ledger is what makes the report auditable and what keeps you from writing an impression as a
fact. Build it even for a small project; it takes one pass and prevents the characteristic failure
of this review — a confident sentence about a student's week that the evidence does not support.

## Phase 2b — Run the code (only if the mentor opted in)

Follow `references/running-code.md`. In short: use Docker if it is installed and running, otherwise
`uv`, otherwise plain `python3`; run each branch in a separate throwaway clone; install, run the tests,
then run the specific scripts behind this week's claimed results. Read each script before running
it and skip anything that writes to the shared data folder, pushes, or deploys. Keep it to about 20
minutes of running.

When you ran without Docker, list the differences that could change the result (operating system,
missing system libraries, the `/data` path mapping, filename case) and treat a local-only failure
as *possibly environmental*, not as a student error.

## Phase 3 — Per-student status

Work through `references/student-status.md` for each student. The five checks:

| Check | Question |
|---|---|
| Tasks created | Did they write task issues for the week, on time? |
| Acceptance criteria | Could a reviewer verify "done" without asking them anything? |
| Visible results | Did work show up on GitHub — pushes, PRs, or a substantive follow-up comment? |
| Report accuracy | Does what they claimed match what the artifacts show (and, if run, what the code does)? |
| Repetition | Is this the same task they had last week, and the week before? |

For each, record the verdict, the evidence, and — where useful — **one question the mentor should
ask in the meeting**. Those questions are frequently the most valuable output of the review.

## Phase 4 — Overall direction

Follow `references/direction.md`. Two judgments, both about the project rather than the students:

- **Do the tasks serve the goals?** Map each active task to a project goal. Surface orphan tasks
  (serving no stated goal) and orphan goals (no task advancing them, for how long).
- **Are the weekly task sizes right?** Calibrate against completion history, not against your
  intuition. Chronic carryover means too big; tasks closed on day two with time to spare means too
  small. Both are common and both are fixable.

Add a short risk note if something threatens the project as a whole — a blocked data dependency, a
track nobody has touched in a month, an analysis whose results nobody can reproduce.

## Phase 5 — Next week's task menu

Follow `references/task-design.md`. For each student, propose **one or two candidate tasks** — a
menu, not an assignment: the mentor knows things you do not and will pick. Each task must be:

- **Independent** — completable without waiting on another student's unfinished work.
- **Sized to roughly 10 hours** for an undergraduate data science student (or the mentor's number),
  with the estimate justified in a phrase.
- **Verifiable** — a definition of done a reviewer can check quickly, in the style of the clinic
  task template.
- **Justified** — one line tying it to a project goal or to a gap this review found.
- **Concise.** A task nobody reads to the end does not get done.

Parallel tracks are welcome: several students attacking the same question with different methods is
a feature of clinic projects, not duplicated effort. Say explicitly when two proposals are meant to
be run in parallel and how their results will be compared.

## Phase 6 — Report

Write the report using `templates/report.md`, and nothing the template does not ask for — no
per-student prose sections, no evidence ledger, no restating the project brief. The ledger and full
per-check reasoning stay in your working notes; the mentor can ask for any of it.

Then, and only then, offer follow-ups:

- Expand a chosen task into the full issue text (`task-design.md`, "Full issue text").
- File the chosen tasks as GitHub issues (using the repo's clinic task template, assigned to the
  student) — **on explicit request only**, and show the exact text before creating anything.
- Draft the meeting agenda from the mentor's questions.
- Drill into any one finding with the full diff.

### Writing it

The mentor reads this between meetings, and may paste pieces of it into Slack or into an issue.
So: plain words, active voice, fragments are fine, every claim linked. Use reference-style links
(`[#42]`, `[report-b]`) with the definitions in one block at the end, so tables stay narrow.
What each Students cell links to: **Tasks** → the task issue; **Visible** → the strongest artifact
(merged PR, else open PR, else commit; nothing for "no"); **Accurate** → the student's report
comment; **Repeating** → the earlier issue it repeats. Say "no commits since
Tuesday (`a1b2c3d`)", not "engagement appears suboptimal". Cut hedges, adverbs, and restatements.
Where you are unsure, write the question for the mentor to ask instead of a guess.

| Instead of | Write |
|---|---|
| "The weekly report marks both criteria `complete` ("works on my machine"), but there is no function, export, or PR to check." | "Reported done; no branch, PR, or commit." |
| "Volume by type has landed; response times — half of the stated goal — has no task, even though the dates are in the data." | a table row: `Response times · — · no task yet` |
