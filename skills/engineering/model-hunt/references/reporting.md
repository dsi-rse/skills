# Reporting: the ledger and the two documents

## 1. Two audiences, opposite goals

A model hunt produces (at most) three written artifacts. Two of them have **opposite** design goals,
and conflating them is the most common reporting mistake.

| Artifact | Audience | Git | Length | Optional? |
|---|---|---|---|---|
| **Durable documentation** | a *future Claude session* querying the results | **committed** | as long as it needs to be | no |
| **Short summary** | a *human* reading a comment thread | **never tracked** | a screenful or two | yes — ask |
| **Plan file** | a *human*, for the record | **never tracked** | moderate | yes — ask |

**Do not presume filenames or directories for any of these.** The user chooses them at intake
(`intake.md` §G). Some repos use a docs directory, some a notes directory, some the PR body. Ask,
and use exactly what they say.

---

## 2. The results ledger

An **append-only, machine-readable** record: one row per *(configuration × fold or replicate)*.
JSONL is recommended — it appends safely, tolerates schema growth, survives partial writes, and
streams into a dataframe in one line. CSV is acceptable when the fields are fixed and flat.

**Never overwrite it. Never hold results only in memory. Write the row the moment the evaluation
finishes.**

### Fields

**Identity**
- `run_id` — this campaign
- `config_id` — stable identifier encoding the axis values (`search-space.md` §3)
- `round` — 1, 2, 3, `final`, `smoke`
- `timestamp` — ISO 8601, when the evaluation finished

**Configuration**
- `family` — random_forest, gbdt, mlp, cnn, …
- `representation_id` — which input representation, and a hash of its preprocessing parameters
- `hyperparameters` — the **complete** dict, not a summary
- `n_parameters`, `serialized_bytes` — model size
- **the value of every fallback criterion** the user named in `intake.md` §C7b — inference latency,
  training cost, fold-to-fold variance, calibration error, dependency count, whatever it is. If a
  criterion may decide the winner, it has to be recorded for *every* candidate at the time it runs;
  reconstructing it afterward means reloading and re-timing models that may no longer exist.
- `code_version` — git SHA or equivalent

**Split**
- `fold` — index, or `holdout`, or the replicate number in round 1
- `split_scheme` — random / grouped / spatial / temporal, k, seed
- `split_hash` — hash of the actual assignment, proving comparability
- `n_train`, `n_val`, `n_test`

**Results**
- `primary_metric` — name and value
- `secondary_metrics` — a dict
- **`raw_detail`** — the per-class, per-item, or per-bin values needed to *recompute* any metric
  later: the confusion matrix, per-class counts, the per-example agreement fractions behind a
  threshold metric, residual summary statistics, a calibration histogram. **This field is what makes
  a changed threshold cost minutes instead of a re-run** (`protocol.md` §6). If the per-example
  detail is too large to inline, write it to a side file and store the path here.

**Cost and status**
- `wall_seconds`, `peak_memory_mb`, `device`
- `status` — `ok`, `error`, `oom`, `timeout`, `skipped`
- `error_message` — when not `ok`

A failed configuration gets a row with `status: error`. A configuration that failed has **not been
evaluated**, and must never be treated as one that scored badly (`protocol.md` §5).

---

## 3. The durable documentation

Git-committed, in the directory the user named.

**Its primary consumer is a future Claude session** answering questions like *"plot round-2 score
against tree depth,"* or *"make a table of every configuration that used the concatenated
representation,"* or *"what did we conclude about dropout?"* That session will have the ledger and
this document and nothing else — no conversation history, no memory of the reasoning.

Therefore: **retain the intermediate numbers, not just the conclusion.** Verbosity is correct here.
The failure mode is a beautiful summary that requires re-running the campaign to extend.

Use `templates/documentation.md`. It must contain:

1. **The question**, in one sentence, and the date and campaign identifier.
2. **The metric, verbatim** — its exact definition as a formula or pseudocode, any nonstandard
   weighting written out with the actual weights, and the rationale for choosing it. Never just its
   name.
3. **The data** — source, total count, every exclusion with its row count before and after, the
   final eligible count, and the class distribution or target summary.
4. **The split construction** — scheme, k, seed, grouping variable, stratification, and the path to
   the persisted assignment.
5. **The search space** — every axis and every value considered, plus what was deliberately *not*
   tried and why.
6. **Per-round results** — for each round: what ran, the score of each candidate with its
   uncertainty, which candidates were eliminated, **and why each one was eliminated**. Include the
   losers. This is a large fraction of the document's lasting value: it is what stops the next
   campaign from repeating the same experiments.
7. **The winner** — complete configuration, **per-fold scores** (not just the mean), mean ± standard
   error, which tie-break rule was applied if any, and the runner-up with its margin.
8. **Diagnostics** — see §5.
9. **The selection-bias statement** (`protocol.md` §4) — which of the three responses you took, and
   how many configurations reached the final round.
10. **Artifacts** — paths to the final model, the per-fold models, the preprocessing artifacts, the
    fold assignment, and the ledger.
11. **Reproduction** — environment, library versions, hardware, seeds, and the commands to re-run.
12. **Incidents and re-budgeting** — crashes, their causes, time lost, and every mid-run change to
    the plan with its trigger (`protocol.md` §8).
13. **Total compute consumed**, and what a re-run would cost.

**Write it incrementally, as each round completes.** A crash at hour seventeen must not lose the
record. Append round sections as they finish; write the summary sections at the end.

---

## 4. The short summary

Only if the user asked for one. **Never git-tracked.** Filename as they specified.

Its audience is a human scrolling a comment thread. It should be **a screenful or two**.

> ⚠️ **The habitual failure here is making this far too long.** The natural instinct — having just
> done many hours of careful work — is to show all of it. Resist. A comment nobody reads communicates
> nothing, and every detail you are tempted to add is *already in the durable documentation*, which
> is exactly where it belongs. If you find yourself adding a per-configuration table, a methodology
> section, or a paragraph of caveats, move it to the documentation and link there instead.

Include, briefly:

- **What was searched** — one or two sentences. Families and axes, candidate count, rounds.
- **What won** — the configuration, in a phrase, not a parameter dump.
- **The headline number** — with its uncertainty, and against the baseline.
- **One or two surprises** — the genuinely interesting findings. What mattered that you didn't
  expect to; what didn't matter that you did.
- **Where things are** — artifact paths, and a pointer to the detailed documentation.
- **Anything needing a decision** — one line, if the user must choose something.

Do **not** include: a table of every configuration, the full hyperparameter grid, the methodology,
the fold-by-fold numbers, an environment listing, or a narrative of the debugging.

Use `templates/summary.md`.

---

## 5. Diagnostics worth producing

Beyond the primary metric, these are broadly useful and cheap once the models exist. Choose what
fits the task; put the numbers in the documentation and any images in the user's chosen output
directory.

- **Learning curve** — score versus training-set size. The most informative single diagnostic
  available: it tells you whether the lever is *more data* or *a better model*, and it directly
  informs whether the next campaign is worth running.
- **Per-fold spread** — the individual fold scores. A high mean with enormous variance is a
  different situation from a slightly lower mean with tight folds, and only the folds show it.
- **Confusion matrix**, summed over folds, for classification. Normalized by true class when
  imbalanced. Which confusions dominate is usually the most actionable output of the whole campaign.
- **Per-class metrics** — precision, recall, and support per class. Aggregate metrics hide classes
  that fail completely.
- **Calibration** — reliability curve or expected calibration error, whenever the probabilities will
  be used as probabilities (thresholded, ranked, or fed downstream).
- **Residual analysis** for regression — residuals against predicted value and against key features.
  Structure in the residuals means a missing feature or a missing interaction.
- **Worst-error exemplars** — the examples the model gets most wrong, saved for human inspection.
  This routinely surfaces label errors and data problems that no metric reveals, and it is worth the
  small effort even when nobody asked.
- **Threshold histograms** — a percentile-per-line text histogram of any quantity a threshold metric
  depends on (`protocol.md` §6).
- **Feature importance** for tree models; permutation importance is more trustworthy than the
  built-in split-based measures, which are biased toward high-cardinality features.
- **Ablation of the winner** — the winning configuration with one component removed at a time. Turns
  "this works" into "this works *because of* X," and it is far cheaper after the fact than as part
  of the search.
- **Inference cost** — latency and model size, always, when there is any deployment constraint.

---

## 6. Git discipline

Follow exactly what the user specified at intake (`intake.md` §G6). Absent instruction, default to
the conservative reading:

- Stay on the current branch. Do not create, switch, rebase, or force-push.
- Commit only small, text-like files: code, documentation, configuration, the fold assignment.
- **Never commit** model weights, cached tensors, prediction dumps, generated image directories, or
  the ledger if it has grown large — and add them to `.gitignore` instead.
- Ensure the plan file and the short summary are gitignored; they duplicate content that lives
  elsewhere.
- Run whatever linters or pre-commit hooks the repo configures before committing.
- Commit as you go, at round boundaries, rather than in one lump at the end.
