# Box data access

Most clinic projects keep their data in a shared Box folder, pointed to by `DATA_DIR` in `.env`.
Check the mentor can read it during Prerequisites, whether or not they chose to run the code:
listing the folder is quick and read-only, and it is what lets you check that the files students'
tasks name actually exist (`student-status.md` §2). It is also access the mentor needs all quarter
to help their students.

Skip this file entirely if the project does not use Box — no `DATA_DIR` in `.env.example`, no data
section in the README pointing at Box.

The Box path is not secret. Print it, and show it to the mentor when diagnosing.

## 1. Find the expected folder

1. The mentor's `.env`, if they have a clone: `grep '^DATA_DIR=' <clone>/.env`.
2. Otherwise `.env.example` in the repo, which has one line per operating system (macOS Box Drive,
   Windows + WSL), and the README's data section.

Expand a leading `~` yourself when checking (`eval echo "$DATA_DIR"` or Python's
`Path(...).expanduser()`).

## 2. Check, read-only

```bash
ls "<DATA_DIR>" && ls "<DATA_DIR>/raw"     # or whatever subfolder the README names
```

Never write to the folder to "test sync" — the template's `make check-data` does, so do not run it
here. Listing, and reading a file's schema, are enough.

## 3. Walk through what's wrong

Work through this with the mentor one step at a time. Most fixes are theirs to do — installing
software, signing in, asking for a share, anything with `sudo` — so tell them exactly what to do,
then re-check.

| What you see | Likely cause | What the mentor does |
|---|---|---|
| No `.env` in their clone | never set up | Copy `.env.example` to `.env` and keep the line for their OS. Offer to do this yourself — `.env` is git-ignored — but ask first. |
| No Box folder at all (`~/Library/CloudStorage/Box-Box` missing on macOS; no `Box` folder in their Windows home) | Box Drive not installed, or not signed in | Install Box Drive (<https://www.box.com/resources/downloads>) and sign in with their UChicago account. |
| Box folder exists, project folder missing | folder not shared with them yet | Check in the Box web app; if it is not there, ask clinic staff or the project lead to share `dsi-core/clinic/<project>`. |
| WSL: `/mnt/Box` missing or empty | Windows Box folder not mounted into WSL | Follow <https://clinic.ds.uchicago.edu/tutorials/box-wsl.html>. The mount needs `sudo`, so they run it themselves (e.g. with `! <command>` in this session). |
| Files listed, but reading one hangs or fails | Box Drive online-only placeholders | Wait for the download, or right-click the folder in Box Drive → *Make available offline*. |
| `DATA_DIR` path looks wrong for their machine | `.env` has the other OS's line, or a typo | Fix the line in `.env`. |

Re-run the `ls` after each fix. Stop after a couple of rounds if it is not converging — go to §4.

## 4. Let them skip, but recommend fixing it

If access does not work, or the mentor would rather not deal with it now, ask with
`AskUserQuestion`:

> I can't read the project's Box folder. Without it I can't check that the data files students'
> tasks depend on exist and have what the tasks need, or run anything on real data. You'll also
> need this access to help your students through the quarter, so I strongly recommend fixing it —
> it usually takes 5–10 minutes. Want to fix it now, or skip it for today?

Options: **Fix it now (Recommended)** and **Skip for today**. On skip, carry on without complaint:
mark data inputs **unverified** in the per-student checks, skip data-dependent code runs, and put
"Box data not accessible — <reason>" in the report's gaps with the one fix most likely to solve it.
Do not raise it again this session.

## 5. Record it

For the report header: **Box access:** yes / skipped — <reason>.
