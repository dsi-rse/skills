# Running the project's code

Reading a diff tells you what a student wrote. Running it tells you whether it works. This step is
**optional** and only happens if the mentor said yes in Prerequisites §3. Everything else in the
review works without it; the report just says which claims were checked by reading only.

## 1. Choose the environment

Clinic repos are built to run in Docker (`Dockerfile`, `docker-compose.yaml`, `make` targets), but
many mentors do not have Docker installed. Detect what is available, in this order, and use the
first that works:

```bash
docker info >/dev/null 2>&1 && echo docker-ok     # installed AND the daemon is running
command -v uv && uv --version
command -v python3 && python3 --version
```

| Available | Use | Fidelity |
|---|---|---|
| Docker, daemon running | `docker compose build`, then `docker compose run --rm <service> <cmd>` | matches what students and CI use |
| `uv` (no Docker) | `uv sync`, then `uv run <cmd>` | same locked package versions; different OS underneath |
| Only `python3` | `python3 -m venv .venv` + `pip install -e .` + dev tools by hand | lockfile ignored; versions may drift |
| Nothing usable | do not run; note it in the report | — |

- **Docker installed but not running** (`docker info` fails, `docker --version` works) — tell the
  mentor they can start Docker Desktop, or you can carry on without it. Do not wait on them.
- **No `uv`** — ask once whether to install it (<https://docs.astral.sh/uv/getting-started/installation/>;
  it installs into the user's home folder, no admin rights). If they decline, use plain `python3`.
- **Never install Docker, a system Python, or system packages** (`apt`, `brew install gdal`, …) on
  the mentor's behalf. If a dependency needs one, record it as a gap.
- The template pins a Python version (`requires-python` in `pyproject.toml`, the `FROM` line in the
  `Dockerfile`). `uv` downloads the right one automatically. With plain `python3`, check the version
  matches; if it does not, say so rather than forcing an install.

## 2. Run in a separate throwaway clone

Never run code in the mentor's clone (if they have one): it may hold their own changes, and its
remote may use SSH, which fails on machines without SSH keys. Make a separate clone in the
scratchpad over HTTPS, with `gh` supplying credentials — this works whether or not the mentor has a
clone, and whatever their SSH setup:

```bash
git clone -q -c credential.helper='!gh auth git-credential' \
  https://github.com/<owner/repo>.git <scratch>/run
```

Then check out each thing you want to run, one at a time, in that same clone:

| What | How to get it |
|---|---|
| Default branch | already checked out |
| A branch that still exists | `git -C <scratch>/run switch --detach origin/<branch>` |
| An open PR (including from a fork) | `git -C <scratch>/run fetch -q origin pull/<n>/head && git -C <scratch>/run switch --detach FETCH_HEAD` |
| A merged PR whose branch was deleted | its merge commit on the default branch (`gh pr view <n> --json mergeCommit`), which is what actually landed; use `pull/<n>/head` as above only if you need the pre-merge state |

Re-run `uv sync` (or rebuild) after each switch if `pyproject.toml` or `uv.lock` changed. Delete
`<scratch>/run` when done.

**Read before you run.** Student code runs with the mentor's permissions. Before running a script
or `make` target, read it. Skip — and note — anything that:

- **writes to or deletes from `DATA_DIR`.** That is usually a shared Box folder; a bad path can
  damage data for the whole team. Reading is fine.
- pushes, deploys, sends email or Slack messages, or calls a paid API.
- needs secrets the mentor has not already placed in `.env`. If the mentor has a clone with a
  `.env`, copy it into `<scratch>/run`. The `DATA_DIR` path is not secret and is fine to print; do
  not print any other values (API keys, tokens). With no `.env`, or if the mentor skipped Box
  access (`box-access.md`), skip every data-dependent run and note it.

## 3. What to run

Tell the mentor before you start: *"Installing packages and running the tests now — this may take
10–20 minutes and will use a fair amount of CPU and memory. Nothing is pushed or changed on
GitHub."* Budget about 20 minutes of running in total; stop and report what finished rather than
letting a long job run on.

In order, stopping where the evidence is sufficient:

1. **Install.** `docker compose build` or `uv sync`. A failed install on the default branch is
   itself a project-level finding (reproducibility).
2. **The test suite** on the default branch, then on each branch with work in the review window:
   `pytest -q` (via `docker compose run --rm <service>` or `uv run`).
3. **Data access**, if `DATA_DIR` is set: list the folder and load one input file read-only
   — read only its structure, not the whole file:
   `uv run python -c "import pyarrow.parquet as pq, sys; f = pq.ParquetFile(sys.argv[1]); print(f.schema_arrow); print(f.metadata.num_rows)" <file>`.
   Do **not** run the template's
   `make check-data` / `scripts/check_data.py` — it writes a sync-test file into Box. Run only its
   reading part, the same way you would treat any script under the "read before you run" rule.
4. **Claimed results.** For each claim in the ledger that a run can settle — "the loader works",
   "accuracy is 0.82", "the notebook runs end to end" — run the specific script, test, or notebook
   (`jupyter nbconvert --to notebook --execute --output <scratch>/out.ipynb <nb>`) and compare.
5. **Skip long jobs.** Model training, full-data pipelines, or anything the README says takes hours:
   do not run it. Run on a sample if the code supports one, otherwise mark the claim "not run".

## 4. Where a local run differs from Docker

A result from a non-Docker run is evidence, not proof. When you did not use Docker, check which of
these apply to *this* repo and list only those in the report:

| Difference | Why it matters | How to spot it |
|---|---|---|
| Operating system | The image is Debian Linux; the mentor is likely on macOS or Windows. Compiled packages, file paths, and shell commands can behave differently. | `FROM` line; `subprocess`/shell calls in the code |
| System libraries | `apt-get install` lines in the `Dockerfile` (GDAL, libpq, ffmpeg, …) are not on the mentor's machine. | `RUN apt-get` in the `Dockerfile` |
| Data path | Compose mounts `DATA_DIR` at `/data` and sets `DATA_DIR=/data`; locally it is the Box path from `.env`. Code that hard-codes `/data` breaks locally but works in Docker. | `grep -rn '"/data' src scripts notebooks` |
| `PYTHONPATH` / working dir | The image sets `PYTHONPATH=/project/src` and runs from `/project`. Imports that only work because of that may fail locally, or vice versa. | `ENV` lines in the `Dockerfile` |
| Case-insensitive filesystem | macOS and Windows ignore filename case; Linux does not. `import Utils` for `utils.py` passes locally and fails in Docker and CI. | an import or path whose case differs from the file on disk |
| Shared memory / resources | Compose may set `shm_size` (e.g. 16 GB, for PyTorch data loaders); the mentor's laptop may have less RAM or no GPU. | `shm_size`, `deploy.resources`, CUDA in the code |
| CPU architecture | Apple Silicon (arm64) vs. the amd64 image; a few packages ship different builds or none. | `uname -m` |
| Package versions | Only with plain `pip`: `uv.lock` is ignored, so versions can drift from what students run. | compare `pip freeze` with `uv.lock` for failing packages |

Read a failure with this table in mind. A test that fails locally for one of these reasons is a
**possible** environment difference, not a student bug — say "fails locally; may pass in Docker
because <reason>", and do not mark a student's claim inaccurate on that basis alone. A test that
**passes** locally usually passes in Docker too, but the case-sensitivity and `/data` rows are the
common exceptions. If CI runs the tests (`gh run list`), its result is the tiebreaker.

## 5. Record it

For the report's **Code run** section: the environment used (Docker / `uv` / `pip` / not run), the
commits and branches run, one line per thing run with pass/fail and a link, the differences from
Docker that apply, and anything skipped with the reason. Feed each result into the matching
ledger row and into the report-accuracy check (`student-status.md` §4), marking those verdicts
**verified by running**.
