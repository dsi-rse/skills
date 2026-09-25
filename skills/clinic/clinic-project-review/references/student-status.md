# Per-student status checks

Five checks per student. Each gets a verdict, the evidence behind it, and — where it would help —
one question for the mentor to ask in the meeting.

Use three verdicts and nothing fuzzier: **yes**, **partly**, **no**. Add **unclear** only when the
evidence genuinely cannot settle it, and then say what would settle it.

A standing rule for all five: you are describing artifacts, not diagnosing people. "No pushes in the
window" is an observation. "Disengaged" is a diagnosis, and not yours to make.

---

## 1. Did they create tasks for the week?

The clinic model has students writing their own weekly task issues. Check for issues **created by
the student** (or assigned to them) with creation timestamps in the review window.

| Verdict | Looks like |
|---|---|
| yes | one or more task issues created in the window, assigned to them |
| partly | created, but after the meeting/deadline, or created by the mentor and merely assigned to them |
| no | no new issues; they are still working from an issue created weeks ago |

Two things to note when true:

- **Carryover is not the same as no task.** A student continuing an unfinished task from last week
  has a task; they just did not write a new one. Say which case it is — it matters for check 5.
- **Mentor-authored tasks** are a legitimate project choice, not a student failure. If *all* tasks
  in the repo are mentor-authored, that is a project-level observation for the direction section,
  not a mark against each student.

## 2. Did their tasks have clear acceptance criteria?

Judge each task issue the student wrote in the window against the repo's own task template — usually
a **Definition of Done** section, or an **Acceptance** list.

The test is operational: **could a reviewer verify "done" in a couple of minutes without asking the
student anything?** They need to know what to run, with what input, and what the result should be.

| Verdict | Looks like |
|---|---|
| yes | criteria name a concrete artifact and how to check it: "`load_normals(zip)` returns a DataFrame with one row per month; tested in `tests/test_io.py`" |
| partly | a Definition of Done section exists but is restating the title: "IDW interpolation implemented correctly" |
| no | no criteria at all, or a bare title like "work on the dashboard" |

Common near-misses worth flagging as *partly*:

- A criterion with no verifiable output ("explore the data", "understand the model").
- A criterion depending on a file not in the repo ("see my notebook") — the reviewer cannot find it.
- Criteria that would pass with code that never runs on real data.

**Check the named inputs exist and contain what the task needs.** A well-written task can still be
impossible: the file it names is not in the data folder, or it lacks the column the task depends on
(a per-capita task on a table with no population). For every input a task names:

1. Look for it where the repo says data lives — `DATA.md`, the README's data section, a data
   dictionary, `data/` in the repo.
2. If a schema or data dictionary lists its columns, check the fields the task needs are there.
3. If the mentor opted in to running the code and `DATA_DIR` is set, read the file's schema
   read-only (`running-code.md` §3) — the only way to be sure.
4. If none of those is possible, say the input is **unverified** rather than assuming it is fine.

A missing input or field makes the criteria *partly* at best, whatever their wording, and it is
often the real explanation for a stuck or over-claimed task — say so in the student's section.

Quote the weakest criterion verbatim, short. A mentor coaching a student on task writing needs the
actual sentence, and a quoted line lands better than a paraphrase.

## 3. Are the results visible on GitHub?

Visibility means one of: commits pushed (any branch), a PR opened or merged, or a **substantive**
follow-up comment on the issue — results, a finding, a blocker, a number. "Working on it" is not a
substantive comment.

| Verdict | Looks like |
|---|---|
| yes | pushes or a merged PR in the window, or a follow-up comment with actual results |
| partly | pushes to a branch with nothing reported, or a report with nothing pushed; a PR open and untouched for days |
| no | nothing in the window |

Then, for coding tasks, note separately whether the work **reached the default branch**. A closed
issue whose code sits unmerged on a branch is not done, and this is the most common mismatch between
the issue board and reality.

When the verdict is *no*, report it flatly and add the mentor's question rather than a theory:
"nothing visible on GitHub between 2026-09-15 and 2026-09-22 — worth asking what they worked on and
whether something blocked them." Principle 2 exists because this is the check most likely to be
wrong about a person while being right about the repository.

## 4. Is their description of progress accurate?

The check that takes real work and returns the most value. Collect every claim the student made in
the window — issue comments, PR descriptions, commit messages, the act of closing an issue — then
open the artifacts and compare.

Procedure for each claim:

1. Find the specific artifact it refers to (commit, file, PR, notebook, output).
2. Read the actual change, not the message describing it (`git show <sha>`, `gh pr diff <n>`).
3. Check it against the task's own acceptance criteria, one criterion at a time.
4. Where the claim is about a *result* — an accuracy number, a row count, a runtime — check that the
   code that produced it is in the repo and that the number appears in a committed output, a notebook
   output cell, or a PR comment. A reported metric with no committed path to reproducing it is a
   finding regardless of whether it is true.
5. If the mentor opted in to running the code (`running-code.md`), run the test or script behind the
   claim and mark the verdict **verified by running**. A failure seen only in a non-Docker run is
   *unclear*, not *no*, unless the cause is plainly the student's code. If the code was not run, a
   claim like "the pipeline works" can be at most **yes (by reading)** — say so.

| Verdict | Looks like |
|---|---|
| yes | claims match the artifacts; criteria met as described |
| partly | directionally true but overstated — "added tests" is one trivial assertion; "pipeline works" works on one hand-made input; three of four criteria met |
| no | the claimed artifact does not exist, or the work does the opposite of what was claimed |

Write gaps as the difference between two observable things, and keep the tone neutral: "#42 was
closed as done; the PR that implements it (#45) is still open, and the daily-normals case in the
Definition of Done is not covered by `test_io.py`." That sentence is useful in a meeting. "Student
overstated their progress" is not, and it makes the review a prosecution.

Assume good faith. By far the most common cause of a mismatch is a different notion of "done", not
deception — and the fix is a conversation about the definition, which is exactly what the mentor is
about to have.

## 5. Is the student stuck in a loop?

Look across the **history window**, not the review window. Signals, roughly in order of strength:

- The same issue open for more than two weeks, especially with no new comments.
- An issue closed and then reopened, or a new issue whose title and body substantially restate an
  earlier one.
- Successive weekly tasks that are the same work renamed ("build the scraper" → "finish the
  scraper" → "get the scraper working").
- Commits over multiple weeks touching the same file with no net progress — rewrites rather than
  additions, or churn where lines added ≈ lines deleted week after week.
- Repeated comments naming the same blocker across weeks ("still can't access the Box data").

| Verdict | Looks like |
|---|---|
| no | tasks advance; each week builds on the last |
| partly | one task ran long, with visible progress and a plausible reason |
| yes | two or more weeks on substantively the same work with little visible movement |

When the answer is *yes*, the useful output is the diagnosis of **what kind** of stuck, because each
has a different fix:

| Kind | Sign | Fix to suggest |
|---|---|---|
| Blocked | waiting on data, access, a credential, another student | mentor unblocks it, or the task is swapped |
| Too big | the task was really four tasks | split it; scope next week's smaller |
| Undefined | no criteria, so it can never be finished | rewrite the acceptance criteria |
| Over-engineering | endless refactoring toward an unrequested general solution | narrow to the simplest thing that answers the question |
| Out of depth | the task needs a skill they do not have yet | pair them, or trade for an adjacent task plus a learning goal |

Two weeks on a genuinely hard problem with visible weekly progress is not a loop. Say so when that
is the case — a mentor should not be alarmed by a hard task being hard.

---

## Writing each student's section

A few lines, not a dossier:

1. **One-line summary** of the week.
2. **The five checks**, each with its verdict and a linked reference. Skip the ones with nothing to
   say beyond "yes" — a report that spends four lines confirming everything is fine buries the one
   thing that is not.
3. **What is notably good.** Say it. Mentors have limited attention for praise-gathering and
   students rarely hear it.
4. **The question to ask in the meeting**, if there is one. One is usually enough.
