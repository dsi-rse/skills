# Protocol: rounds, splits, statistics, elimination

## 1. The round structure

Cost per configuration rises as the candidate count falls. Each round has a **different purpose**,
and confusing the purposes is what makes campaigns run out of time.

| | Round 1 | Round 2 | Round 3 (final) |
|---|---|---|---|
| **Purpose** | *eliminate* the clearly bad | *rank* the survivors | *select and report* |
| **Candidates** | everything, tens to hundreds | a handful to a dozen | 2–5 |
| **Data** | a subset | a larger subset | all eligible data |
| **Validation** | fixed train/val/test splits, repeated over ≥3 independently drawn subsets | light CV (3-fold is typical) | the user's gold standard (often 10-fold) |
| **Precision needed** | just enough to see large gaps | enough to order things | enough to defend the winner |
| **Budget share** | ~20–30% | ~20–30% | ~40–50% |

Then **the final model**: retrain the winner on all eligible data (§7).

Three rounds is the common shape, not a law. Two is right for a small space or a short budget; four
is right when round 1 reveals that the interesting variation lives somewhere unexpected. Say which
you chose and why.

### Round 1 in detail

The repeated-subset design matters. Draw the subset **at least three times independently**, run
every candidate on all three, and use the spread across those draws as your error bar. A single
subset gives you a ranking with no uncertainty attached, which is exactly the thing that causes bad
eliminations.

Size the subsets so that (a) a full pass over all candidates fits comfortably in the round's budget
share, and (b) the subset is large enough that the metric can actually separate good from bad. If
every candidate scores identically, the subset is too small — a metric with no resolving power
eliminates nothing and wastes the round. Check this early with two or three candidates before
launching all of them.

### Round 2 in detail

Now you have a small set of survivors and enough data per evaluation to trust the ordering. This is
also where you learn **which axes matter** — if every surviving configuration shares a value on some
axis, fix it and spend the freed budget elsewhere; if an axis is producing large spreads, sample it
more densely. Adding candidates *near* the promising region is legitimate and encouraged; adding
back candidates eliminated in round 1 is not, unless you have a specific reason to believe round 1
misjudged them (say so if you do).

### Round 3 in detail

Full data, the gold-standard scheme, a handful of candidates, and no changes to the protocol once it
starts. This round's numbers are the ones that get reported, so it must be run exactly as planned.
If time pressure forces a change here, **tell the user** rather than silently reducing the fold
count.

---

## 2. Splits and data hygiene

**Compute the fold assignment once, persist it, and have every configuration read the same file.**
This is not a convenience; it is what makes comparisons paired (§3) and what makes results across
rounds joinable.

- **Match the split to the dependence structure** identified at intake (`intake.md` §B5): random
  k-fold only for genuinely independent examples; grouped k-fold when examples share a subject,
  site, session, or source; spatially blocked folds under spatial autocorrelation; forward-chaining
  when time ordering matters. Getting this wrong inflates every score, and it inflates
  high-capacity models most — so it does not merely overstate the winner, it *picks the wrong one*.
- **Stratify** on the target (and on important covariates) within whatever scheme you chose. With
  rare classes this is the difference between meaningful folds and folds that don't contain the
  class at all.
- **Fit every preprocessing step inside the training fold** — scalers, imputers, encoders, target
  encoders, feature selectors, PCA/LDA bases, class weights, vocabulary. Anything fitted on all the
  data before splitting is leakage, and target encoding is the most dangerous of these by a wide
  margin.
- **Augment training folds only.** Never evaluate on augmented examples; never let augmented copies
  of a test example appear in training.
- **Early stopping needs its own split**, carved from *within* the training fold. Stopping on the
  test fold turns cross-validation into a very slow form of cheating.
- **Check for duplicates and near-duplicates** that could straddle a split boundary; deduplicate or
  group them.
- **Record the split assignment hash** in every ledger row, so you can always prove two results are
  comparable.

---

## 3. Statistics

**Report mean ± standard error over folds**, not the mean alone and not the best fold. The standard
error is `std / sqrt(n_folds)`; note in the documentation that CV folds are not fully independent
(they share training data), so this understates the true uncertainty somewhat — it is a useful
relative measure, not a rigorous confidence interval.

**Compare paired.** Because every configuration ran on the identical folds, compare them
fold-by-fold: compute the per-fold *difference* between two configurations and test whether its mean
differs from zero. This is far more sensitive than comparing two independent means, because it
cancels the fold-to-fold difficulty variation that usually dominates the spread. Two configurations
whose error bars overlap heavily can still be reliably ordered by a paired comparison.

For a formal test, a paired t-test or Wilcoxon signed-rank over folds is adequate; with repeated CV
the corrected resampled t-test is better. But most decisions here do not need a p-value — they need
an effect size compared against a spread, and honesty about which comparisons were pre-planned.

**Correct for multiplicity, at least in spirit.** If you compare fifty configurations, the best one
is expected to look good partly by luck. That is what §4 is about, and it is why the tie-break rule
exists.

**Apply the selection policy** agreed at intake (`intake.md` §C7). The user chose one of two:

**Strict optimization** — the highest mean primary metric wins. Nothing further is applied. Still
report the runner-up and its margin, and state whether that margin exceeds the uncertainty in the
margin, so the reader can see how arbitrary the choice was. When it doesn't, say so: "the winner
beat the runner-up by less than the noise" is an honest and useful sentence.

**Equivalence with a fallback** — the *one-standard-error rule*, generalized:

1. **Build the tied set.** A configuration is tied with the best if its paired per-fold difference
   from the best is within *k* standard errors of zero.

   **Use the standard error of the paired difference**, `std(per_fold_differences) / sqrt(n_folds)`
   — *not* each configuration's own standard error, and not the quadrature sum of the two. Because
   every configuration ran on identical folds (§2), fold difficulty cancels in the difference, and
   the paired standard error is typically several times smaller. Using the wrong one is not a
   rounding difference: it can inflate a tied set from a few configurations to nearly the whole
   candidate list, at which point the fallback criterion — not the metric — is silently selecting
   the model.

2. **Order the tied set** by the user's fallback criteria, in the order they specified (§C7b).
   These may be parsimony, inference cost, training cost, fold-to-fold variance, calibration,
   interpretability, or anything else they named. Do not substitute parsimony because it is the
   usual choice.

3. **Record the entire tied set**, not just the winner — with each member's primary metric, its
   paired difference from the best, and its value on each fallback criterion. A future session
   asked "why not the one with the highest score?" must be able to answer from the documentation.

**Under either policy, report both winners**: the raw argmax and the policy winner, with the metric
difference between them. If the policy cost measurable performance, the user should see that number
and be free to overrule it — which they can do from the ledger, without re-running anything.

Record which criterion broke each tie.

---

## 4. Selection bias — say it out loud

**Choosing the best of N configurations using the same cross-validation that reports its score
inflates that score.** The winner is the configuration whose true quality plus whose lucky noise is
highest, so the reported number is an optimistic estimate of what you will see on new data. With
many candidates and a small dataset, the inflation can be substantial.

Three honest responses, in order of preference:

1. **An untouched holdout**, set aside before the hunt begins and evaluated exactly once at the end.
   Cheap, simple, and it costs only the data it consumes.
2. **Nested cross-validation** — the entire selection procedure re-run inside each outer fold. This
   is the rigorous answer and it is expensive; it also estimates the *procedure's* performance
   rather than any single model's.
3. **State the caveat.** If neither fits the budget, say plainly in the documentation that the
   reported score is a selection-biased estimate, note how many configurations reached the final
   round, and note that the bias grows with that number.

The one unacceptable option is to report the winning CV score as if it were an unbiased estimate of
future performance. Choose one of the three and write it down.

---

## 5. Elimination rules

- **Eliminate only when the gap exceeds the spread.** If candidate A beats candidate B by less than
  the uncertainty in their difference, you have not learned that A is better.
- **Be generous early, strict late.** A round-1 elimination is irreversible within the budget, and a
  wrongly-eliminated candidate is a silent, permanent error. Keep the borderline cases; you can
  afford to in round 2, and you cannot un-drop them.
- **Keep survivors diverse across families.** A naive "take the top k by mean" frequently returns k
  variants of the same model. Guarantee a slot for the best member of each major family that is
  still competitive, even if it is not in the top k overall. Families behave differently at full
  data scale than at subset scale — trees in particular often look worse than they are on small
  subsets, and neural networks often look better.
- **Judge a candidate as bad only if it is consistently bad** across every replicate or fold. A
  candidate that is worst on one subset and middling on the others is noise, not a loser.
- **Distinguish "bad" from "broken."** A configuration that scored terribly because it failed to
  converge, ran out of memory, or hit a bug has not been evaluated. Mark it as an error in the
  ledger, not as a low score, and either fix it or record it as untested.
- **Record every elimination** with its round, its score, and the score it lost to. This is a large
  fraction of the campaign's lasting value.

---

## 6. Threshold-dependent and composite metrics

If the primary metric involves a threshold ("the fraction of cases exceeding 95% agreement"), the
metric is only trustworthy when the underlying distribution is bimodal around that threshold.

- **Inspect the distribution.** A percentile-per-line text histogram of the underlying per-example
  quantity is enough: it shows immediately whether cases fall off sharply past the threshold or pile
  up against it.
- **Report how many cases sit near the boundary**, every round. A metric where 30% of cases are
  within a hair of the threshold is measuring noise.
- **Retain the per-example raw values in the ledger**, always. This is what lets the threshold be
  revised later and *every past experiment re-scored without re-running anything.* A user who sees
  the distribution frequently wants to move the threshold; that request should cost minutes, not a
  new campaign.
- **Composite metrics** with several thresholds may need each one set separately, since the
  underlying distributions differ. Say so, and keep the components separately in the ledger so any
  combination can be recomputed.

---

## 7. The final model

Retrain the winning configuration on **all eligible data** — the cross-validated score estimates how
well the *procedure* generalizes; the model you ship should use every example you have.

- Save the per-fold models too. They make the reported score reproducible, they enable an ensemble
  comparison, and they are the only way to audit the number later.
- Save alongside the weights: the exact configuration, the code version (git SHA), the environment
  and library versions, the random seeds, the preprocessing artifacts, and the fold assignment.
- Where hyperparameters depend on dataset size (number of boosting rounds chosen by early stopping,
  number of epochs), scale them sensibly for the larger training set rather than reusing the fold
  value verbatim — the mean across folds, scaled by the size ratio, is a reasonable convention.
  Say which convention you used.
- Verify the saved model loads in a fresh process and reproduces a known prediction. Do this before
  declaring the phase complete.

---

## 8. Dynamic re-budgeting

The time-box is a constraint, not an aspiration. Manage it actively.

- **Measure, don't estimate.** After the first few configurations of a round, you know the real cost
  per configuration. Recompute the round's projected finish from measurements and act on it.
- **Check at every round boundary, and periodically within rounds** — the same cadence as the
  shepherding loop (`resources.md` §4).
- **If behind:** cut the least-promising candidates first, then shrink round-2 sample sizes, then
  reduce the number of round-1 replicates. Never silently weaken the final round; if the final round
  will not fit, tell the user and let them choose between fewer folds, fewer candidates, and more
  time.
- **If ahead:** add candidates around the promising region, add a replicate for tighter error bars,
  or add the external-validation or holdout evaluation you couldn't originally afford.
- **Keep the queue sorted most-promising-first at all times**, so a hard stop at any moment leaves
  the most valuable possible set of completed work.
- **Log every re-budgeting decision** with its timestamp, its trigger, and what changed. When the
  final report explains why some branch was never explored, this is the evidence.
