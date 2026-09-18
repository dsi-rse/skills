<!--
TEMPLATE: model-hunt plan file.

Written immediately after the user approves the plan, IF they asked for one.
The filename and location are whatever the user chose at intake — do not assume.
This file is NEVER git-tracked; add it to .gitignore.

Purpose: a copy of the approved plan the user can paste somewhere (a PR comment, an
issue, a lab notebook) alongside their own prompt, as a record of intent.

It must also be self-sufficient: a DIFFERENT session or model may execute from it,
without your context. Anything you leave implicit will be guessed at.

Delete this comment and every parenthetical instruction below before writing.
-->

# Model hunt: <one-line description of the question>

**Date:** <date> · **Branch:** <branch> · **Budget:** <wall-clock time-box>

## The question

<One sentence: what predicts what, on which examples. Then two or three sentences of
context: why this model is wanted and what it will be used for.>

## Evaluation metric

> ⚠️ **Review this.** <Include this callout only if you chose or modified the metric
> rather than being handed it. State plainly what you chose and that it drives which
> model gets selected.>

<The exact definition — a formula or pseudocode, not a name. If the weighting is
nonstandard, write out the actual per-class weights. Then the rationale: why this
metric matches the stated goal, and what it deliberately does not reward.>

**Secondary metrics reported alongside:** <list>

**Selection policy:** <One of the two. Do not default silently — the user chose this.>

<EITHER: "Strict optimization — highest mean <metric> wins; no fallback criterion is
applied." Note whether the margin over the runner-up is expected to exceed the noise.>

<OR: "Equivalence with a fallback — configurations within <k> standard errors of the
best are tied; among them, prefer <the user's criteria, in their order>." State that
the standard error is that of the *paired per-fold difference*, not each
configuration's own.>

Both winners will be reported — the raw argmax and the policy winner — with the metric
difference between them.

## Data

| | Count |
|---|---|
| Total examples | |
| minus <exclusion 1> | |
| minus <exclusion 2> | |
| **Eligible** | |

<Target distribution or summary. Any watch-list exclusions being tested as a search
axis rather than applied unconditionally. Anything known about label provenance and
reliability.>

## Splits

<Scheme (random / grouped / spatial / temporal), k, seed, grouping variable,
stratification. Why this scheme: what makes examples non-independent.>

The fold assignment is computed once, persisted to `<path>`, and read by every
configuration, so that all comparisons are paired.

**Selection-bias handling:** <untouched holdout / nested CV / stated caveat — and why.>

## Search space

### Axis 1 — input representation
<values>

### Axis 2 — model family
<values, including the trivial baseline>

### Axis 3 — architecture and capacity
<values, per family>

### Axis 4 — optimization and regularization
<values, per family>

**Round 1 candidate list** (ordered most-promising-first):

| # | config_id | family | representation | key settings | est. cost |
|---|---|---|---|---|---|
| 1 | | | | | |

<Include the deliberately speculative candidates and mark them as such.>

**Not being tried, and why:** <list>

## Rounds

| Round | Data | Validation | Candidates in → out | Est. wall-clock |
|---|---|---|---|---|
| 1 | | fixed splits × <n> replicates | | |
| 2 | | <k>-fold CV | | |
| 3 | all eligible | <k>-fold CV | | |
| final model | all eligible | — | 1 | |

<Cost estimates should come from a timing probe, not a guess. Say which they are.>

**Re-budgeting policy:** if behind, <what gets cut first>. The final round is not
weakened without telling the user.

## Machine and parallelism

<Cores, RAM, GPU model and VRAM, disk free on the output volume. Framework versions,
and confirmation that the GPU is actually usable by the installed build. Planned
worker/thread counts. What gets precomputed and cached once.>

## Outputs

| What | Where | Git |
|---|---|---|
| Final model | | |
| Per-fold models | | |
| Preprocessing artifacts + fold assignment | | |
| Results ledger | | |
| Durable documentation | | committed |
| <secondary outputs> | | |

**Git rules:** <branch, commit policy, what must never be committed, hooks to satisfy.>

## Shepherding

Progress checked every <n> minutes: process alive, CPU/GPU utilization consistent with
what should be running, log advancing, nothing blocked on input, disk not filling.
Crashes are diagnosed, fixed, resumed from checkpoint, and recorded.

## Open questions

<Anything the user should decide, or anything you will resolve under a stated
assumption. If none, say so.>
