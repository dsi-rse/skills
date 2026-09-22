# Designing next week's tasks

You are proposing a **menu**: 2–3 candidate tasks per student, of which the mentor picks one (or
edits one). More options than needed is the point — the mentor knows the client conversation, the
student's interests, and next week's schedule, and you do not.

## The five properties

Every proposed task must satisfy all five. If one cannot, it is not ready to propose.

1. **Independent.** Completable without waiting on another student's unfinished work. If a
   dependency is unavoidable, say what it is and name the fallback ("if the loader is not merged by
   Wednesday, use the sample file in `data/sample/`").
2. **Sized to the week** — roughly 10 hours for an undergraduate data science student, or whatever
   number the mentor gave. Justify the estimate in a phrase, not a paragraph.
3. **Verifiable.** A definition of done a reviewer can check in a couple of minutes: what to run,
   with what input, what the result should be. Written in the style of the repo's task template.
4. **Justified.** One line tying it to a project goal or to a gap this review found.
5. **Concise.** A short description, a definition of done as a bulleted list, optional resources.
   A task nobody reads to the end does not get done.

## Sizing for ten hours

Ten hours for an undergraduate includes reading unfamiliar code, fighting the environment, and
writing up the result. Assume roughly half the nominal throughput of an experienced engineer, and
remember that the first task in an unfamiliar area costs setup time that the second one does not.

| Roughly right for a week | Too big for a week | Too small |
|---|---|---|
| Implement one inference strategy and score it against the existing evaluator | "Build the model pipeline" | Rename variables; fix a typo |
| Add a data loader for one new source, with a test and a DATA.md entry | Integrate three new data sources | Add one assertion to an existing test |
| Reproduce one published baseline metric on our data | Beat the published baseline | Read a paper (no artifact) |
| Profile the slow step and land one measured improvement | "Make the pipeline fast" | Change a constant |
| Build one dashboard view over existing data | Build the dashboard | Adjust a chart color |
| Write the evaluation for one metric, with unit tests on known cases | Design the whole evaluation framework | — |

Two adjustments worth making explicitly:

- **Learning-heavy tasks carry less output.** A task whose point is picking up a new tool should ship
  a smaller artifact, and should say so, so nobody grades it as thin.
- **Split, do not stretch.** If a task is 20 hours, propose its first half as this week's task with a
  real deliverable at the boundary — not the whole thing with "get as far as you can", which
  guarantees a carryover and a vague status next week.

## Parallel tracks

Several students trying different methods on the same question is a feature of clinic projects: it
produces a comparison, spreads risk, and gives everyone something to say in the meeting. When you
propose parallel tracks, make them genuinely comparable and say so in each task:

- Same input data, same evaluation metric, same output format — so the results can be put side by
  side without further work.
- Different approach per student, named in the task ("rule-based baseline" vs. "fine-tuned
  classifier" vs. "off-the-shelf LLM prompt").
- A note in each task: "this runs in parallel with <student>'s <task>; results will be compared on
  <metric> at next week's meeting."

Do not dress up a single task split across two students as parallel tracks. That is a dependency,
and it needs the treatment in property 1.

## Choosing what to propose

Draw candidates from, in rough priority order:

1. **Unblocking the project's biggest risk** from the direction section.
2. **Orphan goals** — a goal with no task advancing it.
3. **Finishing what is nearly done** — an open PR, a task with one criterion left. Landing work
   beats starting work, and it is what makes the board mean something.
4. **The natural next step** in the student's current track, if that track is healthy.
5. **A parallel track** on a question where the right method is genuinely unknown.
6. **Reproducibility and hygiene debt**, when a reported result cannot currently be re-derived.

For a student who was stuck (`student-status.md` §5), match the proposal to the kind of stuck: split
a too-big task, rewrite criteria for an undefined one, swap out a blocked one, or narrow an
over-engineered one. Repeating the same task unchanged for a third week is the one proposal to avoid;
if the work genuinely must continue, propose it **re-scoped** with new criteria and say what changed.

Keep continuity in mind too: a student who spent two weeks learning a library should get to use it.
Rotating everyone through unfamiliar ground every week wastes the ramp-up.

## Format for each proposed task

```markdown
**<Title — a verb and an object, under ~70 characters>**
*Why:* <one line tying it to a goal or a gap this review found>
*Estimate:* ~<n> hours — <one phrase of justification>
*Task:* <2–4 sentences: what to do, where in the repo, with what data>
*Definition of done:*
- <verifiable item — an artifact plus how a reviewer checks it>
- <verifiable item>
*Resources:* <optional — file paths, a paper, a prior issue, a doc link>
*Independence:* <"no dependencies" or the dependency plus its fallback>
```

Write the definition of done the way the repo's clinic task template asks for it, so the mentor can
paste the task straight into an issue with no editing.

## Anti-patterns

- **"Continue working on X."** Not a task. No criteria, no boundary, no way to be done.
- **"Explore" or "investigate" with no artifact.** Exploration is fine, but the task must land
  something — a notebook with conclusions, a written recommendation, a table of results.
- **"Improve the model."** Improve what, measured how, against what baseline?
- **Criteria that would pass with code that never runs on the real data.**
- **A task whose only deliverable is a Slack message or a verbal update.** Clinic work has to be
  visible in the repository.
- **Padding the menu.** Two good options beat three where the third exists to make it three.
- **Proposing what the mentor already assigned.** Check the open issues first.
