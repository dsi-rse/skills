# Intake: the questions to ask

Work through these groups. For each item you will see *why it matters* and *if the user doesn't
know* — use the latter so the hunt degrades gracefully instead of stalling.

**How to ask.** Batch related questions into a single `AskUserQuestion` call, four at a time at
most. Offer concrete options with your recommendation first and a one-line reason. Never ask about
something you could have discovered by reading the repo — look first, then say "I found X; is that
right?"

**A note on how much to ask.** A user who has done this before will front-load most of this in their
opening prompt. Read it carefully and only ask about what is genuinely missing or ambiguous. A user
who hasn't will need most of the list. Calibrate; do not run the whole questionnaire at someone who
already answered it.

---

## A. The prediction task

**A1. What predicts what?** The target variable (or target mask, or target ranking), and the inputs
the model is allowed to see at prediction time.
*Why:* "allowed to see at prediction time" is the leakage question in disguise. A feature that
exists in the training table but won't exist in production is a trap.
*If unknown:* propose the target from the data's obvious label column and confirm.

**A2. What kind of prediction?** Binary / multiclass / multilabel classification, regression,
ordinal regression, semantic or instance segmentation, detection, keypoint localization, ranking,
survival, forecasting, sequence-to-sequence.
*Why:* determines the metric family, the loss, the model families, and the shape of the CV.
*If unknown:* infer from the target's dtype and cardinality and confirm.

**A3. What is one example?** A row, an image, a pixel, a patient-visit, a document, a time window?
And is the prediction per-example or aggregated over a group?
*Why:* this is what a fold is made of, and it is where subtle mistakes hide (per-pixel metrics
computed on per-image splits, etc.).

**A4. Does the model need to abstain?** Should it be able to say "I don't know" or "none of the
above" when the input doesn't resemble any training class?
*Why:* a standard classifier's output is a probability *conditional* on the input being one of the
trained classes. Removing that conditional is a design decision, not a post-processing step, and it
has to be planned in.
*Options to raise, if this comes up:*
- An explicit "other" / background class trained on held-out non-target examples. Simple, but it
  needs those examples to be genuinely representative of the "other" population, and it quietly
  turns the metric into a K+1-class problem.
- A confidence or out-of-distribution head trained alongside the classifier.
- Thresholding calibrated probabilities (with temperature scaling or similar) and reporting
  coverage-vs-accuracy at several operating points.
- Distance-to-training-distribution in feature space (Mahalanobis, k-NN distance, energy score).
- Deep ensembles or MC-dropout disagreement as an uncertainty signal.

These have genuinely different reputations for different modalities. Say which you recommend and
why, and consider testing more than one — abstention quality is itself something the hunt can
measure (e.g. area under the accuracy-vs-coverage curve).

**A5. What happens to the model afterward?** Research artifact, a table of numbers in a paper, a
service that runs on a schedule, an embedded deployment?
*Why:* this is where the hard constraints in §E come from, and it decides whether "the best model"
means "the most accurate" or "the most accurate that fits."

---

## B. The data

**B1. Where is it, and in what format?** Paths, file formats, and whether it fits in RAM.
*If unknown:* search the repo for data directories, config files with paths, and loader code.
Present what you found.

**B2. How much is there?** Number of examples, features, classes; bytes on disk.
*Why:* everything about round sizing depends on this. Also: below a few thousand examples, transfer
learning and strong regularization dominate; above a few million, throughput dominates.

**B3. Where do the labels come from, and how reliable are they?** Hand-annotated, algorithmically
derived, a proxy variable, another model's output?
*Why:* the metric can never exceed label quality, and if the labels came from another model you are
doing knowledge distillation — which changes what "perfect score" means. Ask whether there is a
confidence or provenance field, and whether it actually refers to what its name suggests.
*If unknown:* look for confidence, source, or annotator columns and ask about them specifically.

**B4. Which examples are disqualified, which are suspect, and which are neither?** Quality flags
usually fall into three tiers and users often haven't separated them:
- **Disqualifying** — drop the example as though it never existed. Corrupt inputs, wrong subject,
  impossible values.
- **Watch-list** — keep for now, but they might be hurting the model. Blurry, partially occluded,
  edge cases. *These are worth testing as a search axis:* "with and without the watch-list rows" is
  a legitimate branch of the hunt, and sometimes a very informative one.
- **Not quality flags at all** — annotations that are modeling targets or covariates, not reasons to
  drop anything.

Ask which flags fall in which tier. Record the row count removed by each. If a flag column exists
with free-text or delimited values, enumerate the distinct values and ask about each.

**B5. What makes two examples non-independent?** Same subject, same site, same session, same source
image, adjacent in time, adjacent in space, near-duplicates.
*Why:* **this is the single most common way a model hunt produces a number that is a lie.** Random
k-fold across correlated examples inflates every score, sometimes enormously, and it inflates the
scores of high-capacity models most — so it also picks the wrong winner. It determines whether you
need grouped, spatial, temporal, or plain random CV (§D).
*If unknown:* look for ID columns, timestamps, coordinates, and filename patterns that repeat.
Propose a grouping and explain the consequence of getting it wrong.

**B6. Are there pre-existing splits you must honor?** A published test set, a competition split, a
prior study's folds.
*Why:* comparability with prior results usually beats statistical elegance.

**B7. Are there related datasets?** Another collection of the same kind of data — a different year,
site, instrument, or population.
*Why:* three distinct uses, worth asking about explicitly: (a) *augmentation*, to fill in
underpopulated classes; (b) *transfer*, pretrain on one, fine-tune on the other; (c) *external
validation*, the most convincing evidence of generalization there is. Also ask what differs between
them — scale, color balance, resolution, protocol — because that difference sets how much
invariance the model needs.

**B8. Leakage check.** State explicitly what you looked for and found: features computed after the
outcome, IDs correlated with the target, duplicate or near-duplicate examples that could straddle a
split, preprocessing statistics fitted on all data, target-derived features.
*Why:* the user may know about a leak you can't see, and asking is cheap.

---

## C. The evaluation metric

**This is the most important section. Do not let it go by quickly.**

**C1. What is the metric?** Ask directly and take the answer literally.
*If the user asks for advice:* recommend one, explain *why it matches their stated goal*, and mark
the recommendation prominently in the plan so it is easy to find and override. A metric adopted by
default is a requirement that was never actually stated.

**C2. Should class imbalance be corrected or respected?** These are different goals and the user
means one of them:
- **Corrected** (uniform prior): "I want to distinguish these classes well, regardless of how often
  they happen to appear in my sample." → balanced accuracy, macro-averaged recall/F1, class-weighted
  training, or balanced sampling.
- **Respected** (sample prior): "My sample reflects reality and I want to be right as often as
  possible on real data." → plain accuracy, micro-averaged metrics, weighted F1.

Ask which, in those terms. Do not infer it from the imbalance ratio.

**C3. Partial balancing is legitimate.** The user may want *some* classes balanced and others left
in proportion — for instance, balancing several substantive classes against each other while leaving
a residual or catch-all class at its natural frequency, so the model isn't rewarded for chasing it.
Stock metrics don't do this. **Construct the weighting explicitly** — write the per-class weights out
as a formula, implement it directly, and show the user the weights. Do not reach for macro-F1 just
because it is the nearest named thing.

**C4. Are the error types equally costly?** A false negative and a false positive rarely cost the
same. If they don't, that belongs in the metric (or in a cost matrix), not in a caveat afterward.

**C5. If the metric involves a threshold, is the threshold stable?**
*Why:* a metric like "fraction of cases exceeding 95% agreement" is only meaningful if the
underlying distribution is bimodal around the threshold. If cases pile up right at it, the metric is
mostly measuring noise and small changes flip large fractions of the score.
*What to do:* plan to inspect the distribution — a percentile-per-line text histogram is enough —
report how many cases sit near the boundary, and **retain per-example raw values in the ledger so
the threshold can be changed later and all past experiments re-scored without re-running anything.**
Say this in the plan; the user may well want to revise the threshold once they see the distribution.

**C6. What secondary metrics should be reported alongside?** The primary metric selects the model;
secondary metrics catch pathologies it hides (a balanced-accuracy winner with terrible calibration,
an R² winner with structured residuals).

**C7. How is the winner selected — strict optimization, or equivalence with a fallback?**

This is a genuine choice and the user must make it. Present both:

- **Strict optimization.** The highest mean primary metric wins, full stop. Appropriate when
  reporting a benchmark number, when comparability with a published result matters more than
  anything else, or when no secondary criterion is meaningful for this problem. *Say the downside
  plainly when offering it:* with many candidates and a modest dataset, the raw maximum reliably
  selects the configuration with the most favorable noise, and its margin over the runner-up is
  often smaller than the uncertainty in that margin.

- **Equivalence with a fallback** *(recommended default)*. Configurations statistically
  indistinguishable from the best are declared **tied**, and a secondary criterion chooses among
  them. This is the *one-standard-error rule* from the decision-tree and regularization-path
  literature, and it usually returns a smaller, more robust model at negligible metric cost.

*Why it matters:* without an explicit answer, "best" silently means "highest mean" — strict
optimization by default, chosen by nobody.

If they choose equivalence, two follow-ups:

**C7a. How wide is the equivalence band?** *k* standard errors from the best.
- *k* = 1 is the classical one-standard-error rule.
- Larger *k* (2, 2.5) declares more ties and leans harder on the fallback criterion.
- *k* = 0 collapses to strict optimization.

**Be explicit about which standard error**, and say so in the plan: it is the standard error *of the
paired per-fold difference* between the two configurations, not each configuration's own standard
error. Because every configuration ran on identical folds, the paired quantity is the correct one
and it is typically much smaller — the two readings can differ by enough to change a tie set from
three configurations to thirty. See `protocol.md` §3.

**C7b. What is the fallback criterion, and in what order?** Do not assume simplicity. Offer a menu
and let the user order it:
- fewer parameters, or smaller serialized size
- faster inference — latency or throughput
- cheaper or faster to train
- **lower fold-to-fold variance** (robustness rather than peak score)
- better calibration, or a better secondary metric
- more interpretable, or easier to describe and defend
- fewer dependencies, or a family already deployed elsewhere in the stack

*Default if the user has no preference:* fewer parameters → simpler to describe → cheaper to run.

*Distinguish this from §E2.* A criterion that is a **hard requirement** (must fit in 50 MB, must
respond in 10 ms) is a **filter on the search space**, applied before the search. §C7b is for
**preferences among models that are all already acceptable**. Ask which one a stated constraint is;
users often state a hard limit and a soft preference in the same breath.

**Regardless of the policy chosen, report both winners** — the raw argmax and the policy winner —
with the metric difference between them. It costs nothing, it shows the user exactly what the policy
bought or cost, and it lets them overrule it without re-running anything.

---

## D. Validation protocol

**D1. Which splitting scheme?** Follows directly from B5:
- **Random k-fold** — only when examples are genuinely independent.
- **Grouped k-fold** — all examples sharing a subject/site/source stay in the same fold.
- **Spatial CV** — spatially blocked folds (blocks, hexagons, buffered leave-one-out) when
  observations are spatially autocorrelated. Random CV on spatial data is a well-documented way to
  overstate skill substantially.
- **Temporal / forward-chaining** — train on the past, test on the future, always, when time
  ordering matters.
- **Stratified** — layered on top of any of the above to keep class proportions stable, which
  matters most with rare classes.

**D2. What is the gold standard for the final round?** Number of folds (10 is common; 5 when
expensive), repeated or not.

**D3. Can you afford an untouched holdout?** A test set that is never looked at until the very end.
*Why:* see `protocol.md` §4 — selecting the best of N configurations by the same CV that reports its
score biases that score upward. A holdout, or nested CV, is the honest fix. If neither fits the
budget, that's a legitimate choice, but it must be stated as a caveat in the documentation rather
than omitted.

---

## E. Model families and constraints

**E1. Which model families are in scope?** Offer the list and let them prune it. Typical spread:
random forests, gradient-boosted trees, neural networks (MLP / CNN / transformer as the modality
dictates), transfer learning from pretrained or foundation models, linear or generalized-linear
models, k-NN, Gaussian processes, and a trivial baseline.
*If the user names only one:* ask whether they want a cheap comparison against one or two others.
It is often a few minutes' work and it is the only way to know whether the chosen family was
actually the right call.
*Always include a trivial baseline* (majority class, mean, nearest neighbor) whether or not it is
requested. Without it, no improvement is interpretable.

**E2. Are there hard deployment constraints?** Maximum model size, inference latency, target hardware
(edge device, CPU-only server, no network), memory ceiling, license restrictions on pretrained
weights, interpretability or auditability requirements, offline/air-gapped operation.
*Why:* these are *filters on the search space*, applied before the search, not tie-breakers after
it. A constraint discovered at the end invalidates the winner.

**E3. Are there approaches the user already knows fail, or already knows work?** Prior experiments in
this repo or in the literature the user has read.
*Why:* the cheapest configuration is one you don't have to run. Check prior PRs and issues too.

---

## F. Time-box and resources

**F1. How much wall-clock time?** A hard number.
*Why:* every round-sizing decision derives from it. Without one, the hunt has no shape.
*If unknown:* offer brackets — a couple of hours (one round, narrow), overnight (the full
three-round shape), a couple of days (three rounds with a wide round 1 and an external validation).

**F2. What hardware?** Probe it yourself first (`resources.md` §1), report what you found, and ask
the user to confirm — especially whether the GPU is yours to use exclusively and whether other jobs
will be competing.

**F3. Attended or unattended?** Will the user be around to answer questions mid-run?
*Why:* determines whether a mid-run ambiguity should block and ask, or resolve itself under a stated
assumption and flag it in the log. An unattended run that blocks on a question wastes the whole
night.

**F4. How often should progress be checked?** See `resources.md` §4. Roughly every twenty minutes is
a reasonable suggestion for a long unattended run.

---

## G. Outputs — ask about every one; assume nothing

**Do not presume any filename or directory.** Conventions differ; several of these artifacts are
optional. Ask, and use exactly what the user says.

**G1. Where do the model artifacts go?** Final model, per-fold models, preprocessing artifacts
(scalers, encoders, vocabularies), the fold assignment itself.
*Why:* weights are usually too large for git, and often belong on a shared or synced volume outside
the repo. Ask; don't put them somewhere by default. Confirm there is disk space (`resources.md` §1).

**G2. Where does the durable documentation go, and what is that directory called?** The detailed,
git-committed record.
*Why:* its primary consumer is a *future Claude session* answering questions like "make a table of
round-2 results by depth." Some repos use a docs directory, some use a notes directory, some use
the PR body, some use something else entirely. Ask. Also ask whether one file per hunt or one file
per phase suits their existing convention better.

**G3. Do you want a plan file?** A copy of the approved plan written to a file so it can be pasted
somewhere else (a PR comment, an issue, a lab notebook). Optional. If yes: **what filename?** It is
**never git-tracked** — it duplicates content that lives elsewhere.

**G4. Do you want a short summary file at the end?** Optional. If yes: **what filename?** Also
**never git-tracked**. It is a brief, human-readable summary of the final results for pasting into a
comment — see `reporting.md` §4, and note the strong warning there about keeping it short.

**G5. Where do secondary outputs go?** Prediction CSVs, diagnostic images, plots, confusion matrices,
directories of examples sorted for visual inspection. Ask whether these are wanted and where they
belong; large or numerous ones usually should not be git-tracked.

**G6. Git discipline.**
- Which branch? May you create one, or must you stay on the current one?
- May you commit? May you push?
- Append-only history (no rebasing, no force-pushing)?
- What must never be committed — size limits, data files, weights, generated images?
- Are there pre-commit hooks or linters to satisfy before committing?

*Why:* a hunt generates a lot of files, some of them large, and the user usually has a specific
branch and a specific policy. Getting this wrong is annoying to undo.

---

## H. Autonomy

**H1. Decide or ask?** When a judgment call comes up mid-run — an unexpected data problem, a
configuration that won't converge, a metric that behaves strangely — should you stop and ask, or
decide under a stated assumption and record it?
*Recommend:* decide and record, for anything reversible; stop and ask for anything that would
invalidate results already computed.

**H2. Stop at the plan, or run the whole thing?** Some users plan with one session and execute with
another. Ask which. If stopping at the plan, make the plan self-sufficient (`SKILL.md` Phase 2) —
the executing session will not have your context.

**H3. Anything the user wants to review before it runs?** The metric implementation, the candidate
list, the exclusion counts, the fold assignment. Offer; these are the four things most worth a
second pair of eyes, and all four are cheap to show.
