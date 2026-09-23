# Running the PR

The clinic's reproducibility test is literal: someone with no context clones the repo, follows the
documented setup, and gets the same results. This file is how you play that person.

## 1. Fresh clone

Work in a scratch directory, never in the TA's checkout. Their working tree has data, virtual
environments, and cached outputs that a new teammate would not.

```bash
SCRATCH=<scratch dir>/clinic-pr-<n>
gh repo clone <owner>/<repo> "$SCRATCH"
cd "$SCRATCH"
gh pr checkout <n>
git log --oneline origin/<base>..HEAD
```

Also check whether the branch is behind the base branch (`git rev-list --count HEAD..origin/<base>`).
The clinic standard is that working branches stay current with `main`. More than a few commits
behind is worth a suggestion; a merge conflict is a requested change.

## 2. Follow the README exactly

Do the setup steps in the order written, and nothing else. Every time you have to guess, improvise,
or fix something to get further, that is a finding for the checklist ("README says `make build` but
there is no Makefile"). Then do the minimum fix needed to keep going, and note what you did.

**Data.** Most clinic data is gitignored and lives somewhere private.

- If the README documents where data comes from and you can reach it, follow it.
- If you can't, and the TA gave you a local copy, use it and record the path.
- If neither, anything that needs the data is **could not verify**. Don't fake the data.
- If the README doesn't say where the data comes from at all, that is a failure of
  "newly added code has clear documentation" (or of reproducibility, if the PR reports results).

**Secrets.** If the code needs an API key, it should be read from the environment or a gitignored
`.env` documented in the README. A key committed in the diff is a requested change, top of the list.
Don't copy a key into the scratch clone without asking the TA.

## 3. Docker

The clinic requires that committed code runs in Docker. Students may develop locally or in a
devcontainer, but the Docker path must work.

```bash
docker build -t clinic-pr-<n> .
docker run --rm -v "$PWD":<workdir> clinic-pr-<n> <command>
```

Use whatever `make` targets or `docker compose` services the README documents instead, if any. The
mount path and working directory come from the Dockerfile and README — don't guess.

- No Dockerfile in the repo → fail on "runs in Docker" (unless the project is documented as
  cluster-only, in which case check the conda or micromamba environment file instead).
- Build fails → fail, with the error line.
- New imports that aren't in `pyproject.toml` (or the environment file) → fail. Typically this shows
  up as an `ImportError` inside the container even though it worked on the student's laptop.
- Docker isn't available on this machine → could not verify, and fall back to running with the
  project's documented environment so the other checks still get done. Say that you did.

## 4. Notebooks, all of them, in order

Run every notebook in the repo, not only the ones in the diff, inside the container. Order is the
one the README gives; otherwise directory then filename order (numbered prefixes like `01_`, `02_`
exist for this reason). Later notebooks often read files earlier ones write.

```bash
jupyter nbconvert --to notebook --execute <notebook> \
  --output-dir <scratch>/executed --ExecutePreprocessor.timeout=600
```

Write executed copies to a separate directory — don't overwrite the student's notebooks. If
`jupyter` isn't in the image, that is itself worth noting; install `nbconvert` in a throwaway layer
to keep going.

- A notebook that errors → fail, with the notebook, the cell number, and the error's last line.
- A notebook that only runs if you first run a notebook the README doesn't mention → fail on
  sequential run; the fix is documenting the order.
- A notebook that takes hours (full model training, big scrapes) → run it with a small sample if the
  code allows it, or ask the TA. Don't silently skip it.
- If the student committed outputs, compare key reported numbers in the committed outputs to your
  executed copy. A different number is evidence for the reproducibility item.

## 5. Tests and lint

Inside the container, or the documented environment:

```bash
pytest -q                        # or whatever the README / Makefile uses
ruff check .
ruff format --check .            # if the repo uses ruff format
pre-commit run --all-files       # if .pre-commit-config.yaml exists
```

When something fails, rerun it on the base branch (`git worktree add ../base origin/<base>`). A
failure that already existed on `main`
is not this PR's fault; say so and don't request it as a change.

Then look for shortcuts in the diff — these are checklist items, not lint output:

```bash
git diff origin/<base>...HEAD --diff-filter=D --name-only          # deleted files, incl. tests
git diff origin/<base>...HEAD -- '*test*'                           # removed or weakened tests
git diff origin/<base>...HEAD | grep -nE '^\+.*(noqa|type: ignore|pytest\.mark\.skip|xfail)'
git diff origin/<base>...HEAD -- pyproject.toml ruff.toml .ruff.toml setup.cfg .pre-commit-config.yaml
git diff origin/<base>...HEAD -- AGENTS.md CLAUDE.md '.github/*'
```

## 6. Record everything

Keep a list of each command and its one-line outcome as you go. It goes into the TA notes so the TA
can rerun anything they doubt. Delete the scratch clone and Docker image when done, unless the TA
wants to poke at it.
