<!--
TEMPLATE: durable documentation for a model hunt.

Git-committed, in the directory the user named at intake — do not assume a location.
One file per hunt, or split by phase, whichever matches the repo's convention (ask).

Audience: a FUTURE CLAUDE SESSION that will be asked things like "plot round-2 score
against tree depth" or "what did we conclude about dropout?" — with only this file and
the ledger, no conversation history.

  So: RETAIN THE INTERMEDIATE NUMBERS, not just the conclusion. Verbosity is correct
  here. The failure mode is a beautiful summary that requires re-running the campaign
  to extend. Include the losers and why they lost.

Write this INCREMENTALLY as rounds complete. A crash at hour seventeen must not lose
the record.

Delete this comment and all parenthetical instructions before writing.
-->

# Model hunt: <question> (<date>)

**Campaign ID:** `<run_id>` · **Branch:** `<branch>` · **Ledger:** `<path>`
**Budget:** <time-box> · **Actually used:** <wall-clock>

## 1. The question

<One sentence: what predicts what, on which examples. Then the context: why this model
was wanted, what it will be used for, and what constraints that imposed.>

## 2. Evaluation metric

<The EXACT definition, as a formula or pseudocode. Never just a name — a future session
must be able to recompute it. If the weighting is nonstandard, write out the actual
per-class weights as a table.>

**Rationale:** <why this metric matches the goal; what it deliberately does not reward;
who chose it and whether it was reviewed.>

**Secondary metrics:** <list, with definitions where nonstandard.>

**Selection policy as applied:** <Strict optimization, or equivalence-with-fallback.
If the latter: the band width *k*, the fact that it is measured on the paired per-fold
difference, the fallback criteria in order, and which criterion actually broke the
tie.>

<If the metric is threshold-dependent: the threshold, the distribution of the
underlying quantity around it, how many cases sit near the boundary, and confirmation
that per-example raw values are in the ledger so the threshold can be revised without
re-running.>

## 3. Data

**Source:** <paths, formats, provenance.>

| Step | Rows before | Removed | Rows after |
|---|---|---|---|
| Raw | | | |
| <exclusion 1> | | | |
| <exclusion 2> | | | |
| **Eligible** | | | |

**Target distribution:** <full class counts, or target summary statistics for
regression. Give the numbers, not "imbalanced".>

**Label provenance and reliability:** <where labels came from; whether this is
distillation from another model; any confidence field and what it actually means.>

**Watch-list exclusions:** <flags kept but tested as a search axis, and what the test
showed.>

**Leakage checks performed:** <what you looked for; what you found; what you did.>

## 4. Splits

<Scheme, k, seed, grouping variable, stratification. Why this scheme — what makes
examples non-independent. Path to the persisted assignment and its hash. Confirmation
that every configuration used the identical assignment.>

## 5. Search space

<Every axis and every value considered. A table per axis.>

**Deliberately not tried, and why:** <list — this is what saves the next campaign from
re-deciding.>

**Prior art consulted:** <sources that informed the ranges, with links.>

## 6. Round 1 — <purpose>

**Setup:** <sample size, number of independent replicates, split sizes, candidate
count, wall-clock.>

**Results:** <ALL candidates with their scores and spreads. Not just the survivors —
the whole table. Reference ledger config_ids so the raw rows can be pulled.>

| config_id | family | representation | key settings | score ± spread | outcome |
|---|---|---|---|---|---|

**Eliminated, and why:** <each one, with the score it had and the score it lost to, and
whether the gap exceeded the spread.>

**What was learned about the axes:** <which mattered, which didn't, what that implied
for round 2.>

## 7. Round 2 — <purpose>

<Same structure. Note any candidates added near the promising region, and why.>

## 8. Round 3 — <purpose>

<Same structure. Full data, gold-standard CV, final candidates.>

## 9. Winner

**Configuration:** <complete, every hyperparameter — enough to reconstruct it exactly.>

**Per-fold scores:** <the individual fold values, not just the mean. A future session
will want these.>

| Fold | <primary metric> | <secondary> |
|---|---|---|

**Mean ± standard error:** <value>

**Raw argmax vs. policy winner:** <Both, always, with the metric difference between
them. If they are the same configuration, say so explicitly — that is informative.>

**Tied set** <if an equivalence policy was used — every configuration within the band,
not just the winner. A future session asked "why not the highest-scoring one?" must be
able to answer from this table alone.>

| config_id | <primary metric> ± SE | paired Δ from best ± SE | <fallback criterion 1> | <fallback criterion 2> | selected |
|---|---|---|---|---|---|

**Runner-up outside the tied set:** <configuration and margin; whether the difference
exceeded the uncertainty in the difference.>

**Baseline for comparison:** <trivial baseline score, and the best linear model.>

## 10. Diagnostics

<Confusion matrix summed over folds, per-class precision/recall/support, calibration,
residual analysis, learning curve, feature importances, ablation of the winner, worst-
error exemplars and where they are saved, inference cost. Include the NUMBERS, and
paths to any images.>

## 11. Selection bias

<Which of the three responses was taken — untouched holdout, nested CV, or a stated
caveat. How many configurations reached the final round. If a caveat: say plainly that
the reported score is an optimistic estimate and roughly why.>

## 12. Final model

<Training set, configuration, how size-dependent hyperparameters were scaled from the
fold values, verification that it loads in a fresh process and reproduces a known
prediction.>

## 13. Artifacts

| What | Path |
|---|---|
| Final model | |
| Per-fold models | |
| Preprocessing artifacts | |
| Fold assignment | |
| Results ledger | |
| Diagnostic images | |

## 14. Reproduction

<Hardware, OS, environment, library versions, random seeds, and the exact commands to
re-run each phase. Total compute consumed, and what a re-run would cost.>

## 15. Incidents and re-budgeting

<Every crash: what failed, why, what changed, time lost. Every mid-run deviation from
the plan: what triggered it and what changed. This is the evidence behind "why wasn't
X explored?".>

## 16. What to try next

<Concrete leads for a future campaign, informed by the learning curve and the
diagnostics: is the lever more data, better labels, a different representation, or
more capacity?>
