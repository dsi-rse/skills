<!--
TEMPLATE: short summary of a finished model hunt.

Written at the end, IF the user asked for one. Filename and location are whatever
they chose — do not assume. This file is NEVER git-tracked.

Audience: a HUMAN scrolling a comment thread. Not a future Claude session.

  ⚠️  KEEP IT SHORT. A screenful or two. This is the single most-violated rule in
      this skill. Having just done many hours of careful work, the instinct is to
      show all of it — resist. Everything you are tempted to add is already in the
      durable documentation, which is where it belongs.

  DO NOT include: a table of every configuration, the full hyperparameter grid, the
  methodology, fold-by-fold numbers, an environment listing, or the debugging
  narrative. If you start writing one of those, move it to the documentation and
  link there instead.

Delete this comment and all instructions before writing.
-->

# <Question, in a few words> — results

**Searched:** <one or two sentences: which families and axes, how many configurations,
how many rounds, total compute.>

**Winner:** <the configuration in a phrase — "gradient-boosted trees on the
concatenated-string representation" — not a parameter dump.>

**<Metric name>:** **<value> ± <uncertainty>** (<k>-fold CV), versus <baseline value>
for <the baseline>. <Runner-up in half a sentence, with its margin, if it was close.>

**Notable:**
- <A genuinely interesting finding — something that mattered unexpectedly, or didn't
  matter that you expected to.>
- <At most one more.>

**Artifacts:** final model at `<path>`; per-fold models at `<path>`; full details in
`<documentation path>`.

<One line, only if the user needs to decide something.>
