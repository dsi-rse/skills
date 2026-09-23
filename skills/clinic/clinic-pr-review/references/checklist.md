# The clinic PR checklist

Every item gets one verdict — **pass**, **fail**, **could not verify**, or **n/a** — and one line of
evidence (a command outcome, a file and line, a cell number). Items are about **what this PR
changes**: an old problem elsewhere in the repo is not this student's fault this week. Mention it as
a suggestion at most.

These items come from the clinic's coding standards. Where the repo's `AGENTS.md` sets a stricter
or different rule, the repo wins; say which rule you applied.

---

## Notebooks

### 1. All notebooks run in order on a fresh clone

After following the README setup, every notebook in the repo runs top to bottom, in the documented
order, with no manual steps in between. Checked by `running.md` §4.

- **Fail:** any error; any notebook that needs an undocumented step first (a file you had to
  create, a notebook you had to run out of order, a hard-coded path like `/Users/alex/...`).
- **Also fail:** `!pip install` or `!conda install` cells. Dependencies belong in `pyproject.toml`
  (or the environment file), or the notebook works only on the author's machine.
- **Could not verify:** data not reachable; say which notebooks were blocked and which ran.

### 2. Functions live in modules, not notebooks

Notebooks call code; modules define it. Any `def` or `class` in a notebook cell should move into a
module (commonly `utils/` or the project's package) and be imported. So should any block of logic
that is copy-pasted between cells or notebooks, or that is long enough that it obviously *should* be
a function.

- **Fail:** new `def` / `class` in a notebook, or new duplicated logic across notebooks.
- A one-line `lambda` passed to `.apply` is fine.
- In the requested change, name the destination module ("move `clean_dates` and `drop_outliers` to
  `utils/cleaning.py` and import them") so the student doesn't have to design the refactor.
- Check that the modules the functions moved into are reasonably organized: grouped by purpose, not
  one `utils.py` with everything, and not a new module per function.

### 3. Notebook names say what they show

A reader should know from the filename what a notebook demonstrates or explores.

- **Fail:** `Untitled.ipynb`, `test.ipynb`, `scratch.ipynb`, `notebook2.ipynb`, names with `v2`,
  `final`, dates, or people's names, or names with spaces or punctuation.
- Good: `02_eda_permit_timelines.ipynb`, `baseline_logistic_regression.ipynb`.
- Also look for a markdown cell at the top saying what the notebook is for. Missing is a suggestion,
  not a fail, unless `AGENTS.md` requires it.

---

## Code

### 4. The committed code runs in Docker

The Dockerfile builds, the new code runs inside the container, and any new dependency is declared
(with a version) in `pyproject.toml` or the environment file. Checked by `running.md` §3.

### 5. New code is documented and has a clear purpose

- Every new function has a docstring saying what it does and what it expects (types, required keys,
  assumptions). Follow the repo's docstring format if it has one.
- Function and file names say what they do.
- The README (or the relevant subdirectory README) says how to run anything new that is meant to be
  run, and explains any new non-code files committed (configs, annotation spreadsheets, exports).
- New scripts separate definition from execution: importable modules don't execute code at import,
  and entry points use `if __name__ == "__main__":`.
- **Fail** when a new teammate could not tell what a new piece of code is for or how to run it.

### 6. No dead code

- Commented-out code blocks.
- Functions, files, or notebooks that nothing uses (search for callers before calling it dead).
- Leftover debugging (`print(df.head())` in a module, `breakpoint()`), unreachable branches, and
  duplicated old versions of a function (`clean_data_old`).
- `try` / `except` that swallows errors silently (`except: pass`) — not dead code exactly, but the
  same kind of hidden problem; the clinic standard says code should never silently break.

### 7. The code is tested

New logic in modules has tests that would **fail if the logic broke** — not just tests that call the
function and assert nothing, or assert only that the output is not `None`.

- **Fail:** new module functions with non-trivial logic (parsing, cleaning rules, feature
  computation, metrics) and no tests.
- Pure plotting code and notebook exploration don't need unit tests.
- If the repo has no test setup at all, the requested change is to add a minimal one (`tests/`
  plus `pytest` in the dependencies) with a first test for the new logic — keep it that small.
- Tests run and pass in Docker (item 4).

### 8. Deleted or changed tests are justified

For every removed test, removed assertion, loosened tolerance, or new `skip` / `xfail`, find out
why. Legitimate: the behavior was intentionally changed or removed, and the PR or issue says so.
Not legitimate: the test failed and deleting it was the fastest way to green.

- **Fail:** a test removed or weakened with no reason in the PR description, commit message, or a
  code comment — or with a reason that doesn't hold ("test was flaky" when it fails every time).
- Report every instance to the TA, even when justified, in the TA notes.

### 9. Ruff changes are justified

New `# noqa` comments, new entries in ruff's `ignore` / `per-file-ignores`, lowered settings, or
removed pre-commit hooks.

- **Pass:** a narrow ignore with a stated reason that holds (`# noqa: E402` after a required
  `sys.path` setup, explained in a comment).
- **Fail:** blanket `# noqa`, a rule ignored repo-wide to silence one file, or no reason given.
- The requested change is usually "fix the underlying issue and remove the ignore", naming the rule.

### 10. `AGENTS.md` was followed, and changes to it are flagged

Read the repo's `AGENTS.md` (and `CLAUDE.md` or similar) and check the diff against each rule it
states — layout, naming, where data lives, how to run things, anything project-specific.

- **Fail:** the diff breaks a rule in `AGENTS.md`. Quote the rule.
- **Always flag, pass or fail:** any change to `AGENTS.md`, `CLAUDE.md`, or other agent instruction
  files, in the TA notes. These govern how everyone's coding assistant behaves in the repo and should
  be a deliberate team decision, not a side effect. It's a requested change only if the edit weakens
  a rule to make this PR pass, or wasn't discussed in the PR description.
- If there is no `AGENTS.md`, mark n/a and note it as a suggestion for the TA (not the student).

---

## Direction

### 11. The PR links its issue

The PR body references the task issue with a closing keyword (`Closes #12`) so the issue closes on
merge. Check `closingIssuesReferences`.

- **Fail:** no linked issue, or it links an unrelated one. The fix is one line; say exactly which.

### 12. The PR does what the task asked

Go through the issue's acceptance criteria one by one and mark each **met**, **partly met**, or
**not met**, citing the file or output that shows it.

- **Fail:** any criterion not met without an explanation in the PR or issue. A PR can be a
  reasonable partial step — then the PR description should say which criteria remain, and the
  verdict is pass with a note.
- Also note large changes the task didn't ask for. Unrelated drive-by changes make a PR harder to
  review; the usual request is to move them to their own PR.
- If the issue has no checkable acceptance criteria, you can't judge this item: mark could not verify
  and tell the TA — that's a task-writing problem for the mentor, not a code problem for the student.

---

## Data science

Only for PRs that report numbers, train models, or produce results. Otherwise n/a.

### 13. Reported results are reproducible

- The data used is documented: which file or source, which version or download date, and any
  filtering applied.
- The steps are documented or scripted: someone can get from raw data to the reported number by
  following the repo, not by asking the student.
- Rerunning gives the same numbers. Compare your executed notebooks (`running.md` §4) to the numbers
  in the PR description, committed outputs, or linked slides.
- Randomness is seeded where possible (`random_state=` on splits and models, `np.random.seed` /
  `torch.manual_seed`, sampling calls), and anything that can't be made deterministic (GPU training,
  external APIs, LLM calls) is noted next to the result.
- **Fail:** a number you can't reproduce, a number with no documented path to it, or unseeded
  randomness behind a reported result.

### 14. No leakage between train and test

Look for information from the test set reaching training. The common forms in clinic work:

- Scaling, imputing, encoding, or feature selection **fit on the full dataset before the split**.
  These belong inside a pipeline fit on training data only.
- Hyperparameters or model choice tuned on the test set. There should be a validation set or
  cross-validation for that, with the test set used once at the end.
- Random splits on data with time order (forecasting, anything where the future is predicted) or
  with groups (the same person, building, or document appearing on both sides).
- Duplicate or near-duplicate rows landing in both train and test.
- Features that encode the target (an outcome date, a status field filled in after the fact).

Also worth a suggestion when you see it: a metric reported without a baseline (majority class, last
value, simple average), and accuracy numbers that are implausibly high for the problem — both are
often a sign of leakage the student hasn't spotted.

- **Fail:** any leakage that affects a reported result. Explain it in one sentence of plain English
  ("the scaler learns the mean of the test rows, so the model has seen a bit of the test data") and
  give the fix.
