# The search space: what to vary

## 0. Four axes, and which one matters

Every model hunt varies some combination of:

1. **Input representation** — how the data is presented to the model.
2. **Model family** — the class of function being fitted.
3. **Capacity and architecture** — how big and how shaped.
4. **Optimization and regularization** — how it is fitted and how overfitting is restrained.

The dominant axis differs by problem, and knowing which one you are in saves a lot of budget:

| Situation | Usually dominant |
|---|---|
| Tabular, moderate n | 2 and 4 — family choice and regularization |
| Tabular, many weak features | 1 and 4 — feature construction and regularization |
| Images, small n (< ~10k) | 1 and 2 — preprocessing, and pretrained vs. from-scratch |
| Images, large n | 3 and 4 |
| Text / embeddings | 1 — how fields are combined and encoded |
| Segmentation / dense prediction | 1 and 3 — resolution, and architecture depth |
| Severe class imbalance | the metric and the sampling strategy, above all four |

**Everything below is a prior, not a limit.** Before fixing ranges, search prior art for the specific
modality and task — published baselines, model-hub cards, competition write-ups, the repo's own
history. A well-established starting point for your exact problem beats a generic range. The
concrete numbers here are for orientation when nothing better is available; the *named techniques*
age better than the numbers do, and library defaults move, so verify against current documentation
rather than trusting a remembered API.

---

## 1. Input representation

**This axis is skipped most often and pays best.** Treat competing representations as first-class
candidates: they belong in the enumeration next to the model families, not in a preprocessing
function that everyone assumes is correct.

### Generic

- **Feature scaling** — none, standardize, robust-scale, quantile/rank transform, log or
  signed-log for heavy tails. Trees don't care; everything else does. Fit *inside* the fold.
- **Missing values** — drop rows, drop columns, impute (mean/median/model-based), or use a family
  that handles them natively (most gradient-boosting implementations do). *Add an explicit
  missing-indicator column* and test it: missingness is often informative.
- **Categorical encoding** — one-hot, ordinal, target/mean encoding (with in-fold fitting, or it
  leaks), hashing, learned embeddings, or native categorical support.
- **Target transforms** for regression — log, Box-Cox, or Yeo-Johnson for skewed targets; remember
  to invert before scoring, and note that the metric on the transformed scale is a different metric.
- **Feature selection** — all features, top-k by importance, or a domain-chosen subset. Worth one or
  two candidates when the feature count is large relative to n.
- **Dimensionality reduction** — PCA, LDA, or a learned projection as a preprocessing step,
  especially when features are high-dimensional and correlated. LDA-style bases that maximize
  between-group over within-group variance are useful when a meaningful grouping exists that isn't
  the target.

### Images and other dense inputs

- **Background suppression.** If a mask or an ROI is available, test masking the background (to a
  constant, to the mean, to noise) against leaving it in. Backgrounds carry both nuisance variation
  and, occasionally, genuine signal — including spurious signal from acquisition artifacts, which is
  a leak, not a feature.
- **Mask-only vs. mask-plus-appearance.** When the shape alone might be sufficient, test the mask as
  the sole input against the masked image, against stacking the mask as an extra channel. These can
  differ a lot, and the answer is rarely obvious in advance.
- **Canonical orientation vs. augmentation.** Two rival strategies for the same problem, and both
  should be tried rather than assumed:
  - *Canonicalize*: rotate/translate/scale every example to a standard pose (for instance by the
    principal axis of the object's mask, or by detected landmarks). Shrinks the ROI, shrinks the
    model, needs less data — but fails on examples where the canonicalization itself fails, and
    discards genuine orientation signal if there is any.
  - *Augment*: leave the pose alone and generate rotated/flipped/shifted copies during training.
    Robust, needs no pose estimator, but needs more capacity and more epochs.
  - Also: canonicalize *and* augment mildly, which is often the best of both.
- **Crop extent and resolution.** After canonicalization, how tight can the ROI be? Measure the
  distribution of object extents and pick a crop that contains, say, the 99th percentile. Resolution
  is usually the strongest single cost/accuracy dial in an image hunt — put two or three values in
  the search.
- **Augmentation strength** — geometric (flip, rotate, scale, shear, elastic), photometric
  (brightness, contrast, hue, blur, noise), occlusion-based (cutout, random erasing), and mixing
  (mixup, cutmix). Strength is a real hyperparameter, and too much is as harmful as too little.
  Apply to training folds only.
- **Absolute position in a translation-invariant architecture.** Convolutions deliberately discard
  absolute position, but sometimes position is genuinely informative (the object of interest is
  always roughly here; the artifact is always at the edge). Ways to reinstate it, all testable:
  coordinate channels appended to the input; a positional-embedding input to the head; a skip
  connection from a low-resolution positional map; or concatenating raw coordinates into the dense
  head. Test with and without — leaking position can also destroy generalization to data collected
  under a different setup, so it should be an explicit branch, not a default.
- **Color space and channel selection** — RGB, grayscale, HSV/LAB, single informative channel,
  domain-specific band combinations. Cheap to test, occasionally decisive.

### Text and embeddings

- **Field combination**, when several text fields are available. These are genuinely different and
  routinely differ in performance:
  - concatenate the strings with a delimiter, then encode once;
  - concatenate in the *other order* — encoders are not order-invariant, and this is a free
    candidate;
  - encode each field separately and concatenate the resulting vectors;
  - encode each field separately and feed them to separate towers that merge later (see §2.5);
  - one field alone, as a baseline that sometimes wins.
- **Encoder choice** — a general sentence-embedding model, a domain-specific one, or fine-tuning the
  encoder itself. Encoding is often the expensive step: compute embeddings once, cache them, and
  reuse across every downstream configuration (`resources.md` §3).
- **Classical text features** as a cheap baseline — TF-IDF over word or character n-grams into a
  linear model is a strong, fast floor and occasionally beats embeddings on short, formulaic text.
- **Normalization** — casing, punctuation, stemming, deduplication, and any domain-specific
  normalized form the repo already computes. A derived field can outperform the field it was derived
  from, by surfacing the pertinent tokens more readily; if such a field exists, test it.

### Time series and sequences

- Window length, stride, and horizon; lag features; rolling aggregates; differencing and
  detrending; seasonal decomposition; Fourier or wavelet features; and the choice between a
  windowed tabular framing and a sequence model.

---

## 2. Model families and their scales

Include a **trivial baseline** always: majority class, stratified random, global mean, or
1-nearest-neighbor. Every other number in the report is interpreted relative to it.

### 2.1 Random forests

The reliable workhorse: nearly untunable, embarrassingly parallel, rarely the worst thing tried, and
a good sanity check that the pipeline itself is sound.

- number of trees: enough that the score plateaus — a few hundred typically; more only costs time
- max depth: unlimited, or a moderate cap when overfitting shows
- max features per split: the classic defaults (√p for classification, p/3 for regression) plus one
  higher and one lower value
- min samples per leaf: 1, and a few larger values as the main regularizer
- class weighting: none, balanced, or the bespoke weights the metric implies
- extremely-randomized-trees variants as a cheap extra candidate

### 2.2 Gradient-boosted trees

Usually the strongest family on tabular data, and often on embedding vectors too. Multiple mature
implementations exist with different strengths (histogram-based ones for speed, some with excellent
native categorical handling, some with GPU training); try more than one if the budget allows,
because they are not interchangeable.

- **learning rate × number of trees trade the same quantity.** Low rate plus many trees plus early
  stopping is the reliable recipe; search the rate over roughly an order of magnitude and let early
  stopping choose the count instead of gridding it.
- tree size: depth for depth-wise growth, leaf count for leaf-wise growth — a small range of
  shallow-to-moderate values
- row subsampling and column subsampling, each somewhere in the range from about half to all
- minimum child weight / minimum samples per leaf
- L1 and L2 regularization, over a log-spaced range including zero
- **always use early stopping on a validation split carved from within the training fold** — never
  from the test fold

### 2.3 Linear and generalized-linear models

Logistic/linear regression with L1, L2, or elastic-net penalty, regularization strength log-spaced
over several orders of magnitude. Fast, interpretable, and a much better floor than the trivial
baseline. If a linear model on raw features nearly matches your deep model, that is important
information about the problem, not an embarrassment.

### 2.4 Multilayer perceptrons

For tabular data and for embedding vectors.

- **depth**: 1–4 hidden layers. Deeper rarely helps on tabular data without residual connections.
- **width**: scale relative to input dimensionality — same order as the input, and a factor of two
  or four either side. A funnel (narrowing toward the output) and a constant width are both worth a
  candidate.
- **activation**: a modern rectifier variant; the differences are small, so fix it unless you have
  budget to spare.
- **normalization**: batch norm, layer norm, or none. Layer norm is the safer default with small
  batches.
- **dropout**: from none to about half, on hidden layers; this is usually the most effective single
  regularizer here.
- **residual / skip connections**: essential past ~3 layers, worth testing even at 2.
- **weight decay**: log-spaced, including zero.
- **learning rate**: log-spaced over two or three orders of magnitude — the most important single
  neural-network hyperparameter by a wide margin. Pair with a schedule (cosine or one-cycle) and a
  short warmup.
- **batch size**: a few values; interacts with learning rate, so scale them together rather than
  gridding independently.
- **epochs**: let early stopping on the in-fold validation split decide.
- **label smoothing** for classification; **class-weighted or focal loss** under imbalance.

### 2.5 Multi-tower / late-fusion architectures

When the input arrives as several distinct vectors (two embeddings, an embedding plus tabular
features, an image plus metadata), you have a structural choice worth testing:

- **early fusion** — concatenate everything at the input and use one trunk;
- **late fusion / multi-tower** — a separate small trunk per input, concatenated before the head;
- **intermediate fusion** — merge partway.

Tower depth and width are per-tower hyperparameters. Note that a single-tower network is *not* an
optimally-tuned two-tower network with a tower removed: if you change the fusion strategy, re-tune,
because the good hyperparameters move.

### 2.6 Convolutional networks from scratch

Appropriate when the data is unlike anything pretrained (unusual channels, non-photographic
imagery), or when the deployment constraint forbids a large backbone.

- **blocks**: 3–5 conv blocks for small inputs; roughly one more per doubling of input resolution.
  A useful rule is to have enough downsampling that the final feature map is small (single digits
  per side) before the head.
- **kernel size**: 3×3 throughout is the standard; a larger first-layer kernel (5–7) helps when the
  input is large and high-frequency detail is not the signal.
- **channels**: start modest (16–32) and double per block, capping a few hundred.
- **downsampling**: max-pool, average-pool, or strided convolution — worth one candidate each.
- **head**: global average pooling into 0–2 dense layers is the modern default and drastically
  reduces parameters versus flattening; test flatten-plus-dense too when spatial position matters.
- **regularization**: batch norm, dropout (spatial dropout in conv blocks, ordinary dropout in the
  head), weight decay, and augmentation — with little data, augmentation dominates.

### 2.7 Transfer learning and pretrained backbones

**Rule of thumb: below roughly ten thousand labeled images, a pretrained backbone with a small
trained head beats training from scratch, usually by a lot.** Test it even when the domain looks
unrelated to the pretraining data; low-level features transfer further than intuition suggests.

Testable variants, roughly in order of increasing cost:

- frozen backbone → linear probe on the extracted features (extract once, cache, and the sweep over
  heads becomes nearly free)
- frozen backbone → small MLP head
- fine-tune the last block or two, with a low learning rate
- full fine-tune with discriminative (layer-wise) learning rates
- vary the backbone family and size: convolutional versus attention-based, small versus large

Also consider domain-specific foundation models where they exist for your modality — biological,
medical, remote-sensing, audio, chemical, geospatial. **Check what is currently available rather
than relying on a list**; this area moves fast, model hubs are the authority, and licensing varies.
Verify the license permits your use before building on it.

If the deployment target is constrained, look specifically for efficiency-oriented backbones
(mobile- and edge-class architectures); the accuracy cost is often small and the size cost is an
order of magnitude.

### 2.8 Dense prediction and segmentation

- **Encoder-decoder (U-Net family)**: depth, base channel width, skip-connection structure, and the
  choice of a pretrained encoder versus a from-scratch one (pretrained encoders usually win).
- **Loss**: cross-entropy, Dice, Focal, Tversky, boundary losses, and combinations — the choice
  interacts strongly with class imbalance between foreground and background, so it is a real search
  axis, not a default.
- **Output stride / resolution**: full-resolution output versus predicting coarse and upsampling.
- **A structural alternative worth enumerating as its own branch**: instead of predicting the mask
  end-to-end, predict a *location* (a few points, a box, a coarse heat map) and hand it to a general
  segmentation model as a prompt. This trades a hard dense-prediction problem for an easy
  localization problem plus a dependency. Compare the two branches **under the same final metric**,
  even if the cheap early rounds evaluate them by proxies (e.g. "are the predicted points inside the
  target region?") — a proxy metric is fine for elimination, but the final comparison must be
  apples-to-apples.
- **Post-processing** as part of the model: largest-connected-component selection, morphological
  cleanup, hole filling, minimum-area thresholds. Cheap, often worth several points, and easy to
  forget to include in the evaluated pipeline.

### 2.9 Others worth a candidate when cheap

k-nearest-neighbors (a surprisingly strong baseline on good embeddings); support vector machines
with an RBF kernel (small n, moderate dimensionality); Gaussian processes (small n, and you get
calibrated uncertainty); naive Bayes on text; and for sequences, temporal convolutions, recurrent
networks, and transformers.

### 2.10 Ensembling

Once the final round has produced per-fold models, averaging the top few *distinct* configurations
often beats the single best one, at the cost of size and complexity. Worth reporting as an extra
line even when the deployment constraint rules it out — it bounds how much headroom the single model
is leaving on the table.

---

## 3. Enumerating candidates

**Full factorial is almost always infeasible, and mostly wasted.** Instead:

- **Coarse grid** over the two or three axes you expect to interact or dominate.
- **Random or Latin-hypercube sampling** over the rest. For a fixed budget, random search reliably
  beats grid search over more than a couple of dimensions, because most hyperparameters don't matter
  and grid search spends its budget re-measuring them.
- **Sequential / model-based optimization** (Bayesian optimization, Hyperband, successive halving)
  is a good fit for later rounds, when the space has narrowed and each evaluation is expensive. Do
  not start with it: it needs a well-defined space, and early rounds are for finding out what the
  space should be.
- **One-factor-at-a-time is a trap** when factors interact — and depth, width, learning rate,
  regularization, and batch size all interact. It is acceptable only for genuinely separable
  choices (which color space; which delimiter).
- **Budget-share by axis.** Spend candidates in proportion to expected effect, using §0's table.
  Don't spend forty configurations tuning an MLP's width if the real question is whether to use
  pretrained features at all.
- **Sort the queue by expected value.** Most-promising-first, always, so an interrupted round still
  answers the important question.
- **Include a few genuinely speculative candidates in round 1.** Something structurally unusual, an
  unlikely representation, a family nobody expected to work. Round 1 is the only round cheap enough
  to be wrong in, and its purpose is partly to be surprised. Two or three is enough.
- **Give each candidate a stable identifier** that encodes its axis values, and use it as the key in
  the ledger, the checkpoint filenames, and the documentation, so results stay joinable across
  rounds.
