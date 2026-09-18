---
name: model-hunt
description: Runs a disciplined, time-boxed, multi-round search for the best supervised machine-learning model on a dataset — comparing input representations, model families, and hyperparameters, narrowing through staged validation to a gold-standard cross-validation, training a final model, and documenting everything so the results can be re-queried later. Use when the user wants to find, choose, tune, compare, or benchmark predictive models; build a classifier, regressor, or segmenter; run a hyperparameter search, model bake-off, or ablation; or improve an existing model's measured performance.
---

# Model hunt

A **model hunt** is a campaign, not a script. You are given a dataset, a prediction target, an
evaluation metric, and a wall-clock budget, and you must come back with the best model you can find
plus enough evidence to prove it is the best and enough records for someone to re-analyze your
search months later without re-running it.

## Scope

**In scope:** any *supervised* learning problem, any data modality, any prediction type — binary,
multiclass, and multilabel classification; regression and ordinal regression; semantic and instance
segmentation; object detection and keypoint localization; ranking; survival; forecasting;
sequence-to-sequence. Tabular, text, image, audio, video, graph, geospatial, time-series, or a
mixture. The defining criterion is that **the model is a predictive function** learned from labeled
examples and scored by a metric.

**Out of scope** — do not use this skill for these, and say so:

- Unsupervised work whose output is not a scored predictive function (exploratory clustering,
  dimensionality reduction for visualization).
- LLM prompt engineering, agent design, or RAG tuning.
- Applying an already-chosen model to new data (that is inference, not a hunt), or implementing a
  specified non-learned algorithm.
- Data collection, labeling, or cleaning as an end in itself — though cleaning and exclusion
  decisions are absolutely part of a hunt.

If the request is partly in scope, do the hunt for the in-scope part and say plainly what you left
out.

## Principles

These are the things that separate a hunt that produces a trustworthy model from one that produces
a number. Apply them even when the user did not ask for them.

1. **The evaluation metric is the specification.** It determines which model you come back with,
   more than any architecture choice. Never pick one silently. Get it from the user; if they invite
   advice, propose one *with reasoning* and flag it prominently for their review, because a metric
   accepted by default is a requirement never actually stated.

2. **Search input representations, not just hyperparameters.** How the data is presented to the
   model is frequently a larger lever than the model itself, and it is the axis most often skipped.

3. **Stage the search.** Cheap, broad, and speculative first; expensive and rigorous last. A
   gold-standard cross-validation over a hundred configurations is a way of running out of time.

4. **Retain every raw number.** Write per-configuration, per-fold, per-item results to an
   append-only ledger. Decisions must be re-derivable, and a changed metric threshold must cost a
   re-analysis rather than a re-run.

5. **Never eliminate on a difference smaller than its uncertainty.** Every comparison carries an
   error bar. Elimination is irreversible within a budget; be generous early and strict late.

6. **Order the queue most-promising-first.** Assume the campaign may be cut short at any moment.
   At every instant, the work already done should be the most valuable work available.

7. **Saturate the machine.** A single-threaded, CPU-only search on a sixteen-core box with a GPU is
   a bug, not a style choice. Check what hardware you actually have and use it.

8. **Report what failed.** Configurations that lost, and by how much, are results. They are what
   stops the next person from re-running them.

## Reference map

Read these on demand, not all at once.

| Read | When |
|---|---|
| `references/intake.md` | Phase 0 — before asking the user anything |
| `references/search-space.md` | Phase 2 — when enumerating what to try |
| `references/protocol.md` | Phases 2 and 4–7 — rounds, splits, statistics, elimination |
| `references/resources.md` | Phases 1, 3, and throughout — hardware, parallelism, shepherding |
| `references/reporting.md` | Phases 2 and 8 — the ledger schema and the two documentation artifacts |
| `templates/plan.md` | Phase 2, if the user wants a plan file |
| `templates/documentation.md` | Phase 8, for the durable git-committed record |
| `templates/summary.md` | Phase 8, if the user wants a short human-facing summary |

---

## Phase 0 — Intake

Read `references/intake.md` and work through it.

Two rules govern this phase:

**Infer before you ask.** Some things you can find yourself: what data is in the repo, what
frameworks are installed, how many cores the machine has, what prior work exists. Look first, then
confirm what you found rather than asking cold.

**But do not guess the blocking items.** These must come from the user, because a wrong assumption
invalidates the whole campaign:

- the prediction target and task type
- **the evaluation metric**
- **the selection policy** — strict optimization of that metric, or statistical equivalence with a
  fallback criterion (see `intake.md` §C7). Never decide this by default; "highest mean wins" is a
  policy, not the absence of one.
- the unit of independence (what makes two examples non-independent — see `intake.md` §B)
- the wall-clock time-box
- every output path and filename (see `intake.md` §G — assume *nothing* here)

Ask in batches with `AskUserQuestion`, grouping related questions and offering concrete options with
your recommendation first. Do not interrogate the user one question at a time.

## Phase 1 — Reconnaissance

Before planning, find out what you are working with.

**The repo.** Read `AGENTS.md`, `CLAUDE.md`, `README`, and any existing documentation directory.
Check `git log` for what has been tried. If the repo is on GitHub, use the `gh` CLI to read prior
pull requests and issues — earlier model work is often documented there and nowhere else, including
hyperparameters that were already found to be good or bad. **Reuse existing infrastructure rather
than writing a parallel implementation**; if the repo already has a training script, a splitter, or
a metric implementation, drive those.

**The data.** Load it, or a sample. Establish: row/example count; feature count and types; label
distribution (print it — imbalance changes the metric conversation); missingness; the exclusion
flags or quality columns and how many rows each removes; the identity of any grouping column; and
obvious leakage vectors (an ID that encodes the target, a feature computed after the outcome,
duplicate examples straddling a split boundary).

**The machine.** Probe it per `references/resources.md` §1. Confirm the GPU is not only present but
actually usable by the installed framework build.

Report a short summary of all three to the user before proceeding.

## Phase 2 — Plan ◀ safe session boundary

Write a plan that a *different session or a different model* could execute without asking you
anything. This is a real boundary: campaigns are often planned in one session and run in another.

The plan must contain:

- **The question**, in one sentence: what predicts what, on which rows.
- **The metric, verbatim**, with its rationale and its exact definition — including any nonstandard
  weighting, written out as a formula or as pseudocode, not named. If you chose or modified it,
  mark it clearly for the user's review.
- **The selection policy**: strict optimization, or equivalence with a fallback — and if the
  latter, the band width *k*, the statement that it is measured on the paired per-fold difference,
  and the fallback criteria in the user's order (`references/protocol.md` §3).
- **The eligible dataset**: exclusions applied, with row counts before and after each.
- **The split construction**: the kind of split, the seed, and the guarantee that the same fold
  assignment is reused by every configuration.
- **The full candidate enumeration**, from `references/search-space.md`, organized by axis, with the
  round-1 set explicitly listed and ordered most-promising-first.
- **The round budget**: how many rounds, what sample size and validation scheme each uses, how many
  candidates survive each, and the measured or estimated wall-clock cost of each. Estimates should
  come from a timing probe, not from a guess.
- **The ledger schema** (`references/reporting.md` §2).
- **Artifact paths and filenames**, exactly as the user specified them in intake.
- **Git rules**: which branch, whether to commit, what may not be committed.
- **What is deliberately not being tried**, and why.

If the user asked for a plan file, write it now to their chosen filename using `templates/plan.md`,
and make sure it is not git-tracked.

## Phase 3 — Harness and smoke tests

Build the machinery, then prove it works before spending the budget.

- **The ledger**: append-only, one record per configuration × fold. Never overwrite; never keep
  results only in memory.
- **Resumability**: checkpoint after every configuration. A crash must resume, not restart.
- **Fixed splits**: compute the fold assignment once, persist it, and have every configuration read
  it. Paired comparisons over identical folds are enormously more sensitive than unpaired ones.
- **Smoke test every branch of the search space** at tiny scale — a handful of examples, one epoch,
  smallest sizes. Include the model save/load round-trip and the final-model code path, which are
  the paths that most often go unexercised until the very end. *A crash fourteen hours in, on a code
  path nobody ran, is the most expensive failure mode in this entire workflow.*
- **Time a representative configuration from each family** at realistic scale, and use those numbers
  to size the rounds. Revise the plan if the measurements contradict the estimates.

## Phases 4–6 — The rounds

Follow `references/protocol.md`. The shape:

| Round | Data | Validation | Purpose |
|---|---|---|---|
| 1 | subset | fixed splits, ≥3 independently drawn subsets | **eliminate** the clearly bad; measure spread |
| 2 | larger subset | light CV (e.g. 3-fold) | **rank**; learn which axes matter |
| 3 | all eligible data | the user's gold-standard CV (e.g. 10-fold) | **select and report** |

Round 1 should include a few genuinely speculative configurations. It is the only round cheap enough
to be wrong in.

Throughout, **shepherd the run** (`references/resources.md` §4): on the cadence agreed at intake,
verify that something is running, that CPU and/or GPU utilization is consistent with what should be
running, that the log advanced, that nothing is blocked waiting for input, and that the disk is not
filling. Fix crashes and resume. Unexplained idleness is a bug to investigate, not a thing to wait
out.

And **re-budget dynamically**: at each round boundary, and periodically within rounds, recompute
remaining time against measured cost per configuration. Behind schedule — cut candidates or shrink
samples, but never quietly weaken the final round; tell the user instead. Ahead of schedule — add
candidates around whatever looks promising.

## Phase 7 — Final model

Train the winning configuration on all eligible data and save it to the path from intake. Also save
the per-fold models from the final round, so the reported score remains reproducible and so
ensembling stays available. Record the exact configuration, the code version, the environment, and
the random seeds alongside the weights.

If the user asked for downstream artifacts — inference integration, prediction files, diagnostic
images for visual inspection — produce them now.

## Phase 8 — Documentation

Two artifacts with **opposite goals**. Read `references/reporting.md`; the short version:

- **The durable documentation** (git-committed, in the directory the user named) is written for a
  *future Claude session* that will be asked things like "plot round-2 score against tree depth."
  It must therefore carry the intermediate numbers, not just the conclusion. Verbosity is correct
  here.
- **The short summary** (never git-tracked, if the user wanted one) is written for a *human reading
  a GitHub comment*. Brief. Main points only. **The habitual failure is making this far too long** —
  no per-configuration tables, no methodology essay. What was searched, what won, the headline
  number with its uncertainty, one or two surprises, where the artifacts are, and a pointer to the
  detailed docs.

Write the durable documentation *incrementally as rounds complete*. A crash at hour seventeen must
not lose the record.
