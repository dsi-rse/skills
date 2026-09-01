#!/usr/bin/env python3
"""Diff triage for PR review: group changes by area, size the PR, and flag
generated/vendored files that should be excluded from review scope.

Usage: python map_diff.py <base-branch> [head-ref]
Run from inside the repo. Uses the merge base (three-dot diff semantics).
Outputs markdown to stdout.
"""
import re
import subprocess
import sys
from collections import defaultdict

GENERATED_PATTERNS = [
    r"(^|/)package-lock\.json$", r"(^|/)yarn\.lock$", r"(^|/)pnpm-lock\.yaml$",
    r"(^|/)Cargo\.lock$", r"(^|/)poetry\.lock$", r"(^|/)uv\.lock$",
    r"(^|/)Gemfile\.lock$", r"(^|/)composer\.lock$", r"(^|/)go\.sum$",
    r"\.min\.(js|css)$", r"\.map$", r"\.pb\.(go|py|rb|cc|h)$", r"_pb2(_grpc)?\.py$",
    r"(^|/)(dist|build|out|vendor|node_modules|__generated__|\.next)/",
    r"\.snap$", r"\.generated\.", r"(^|/)migrations?/.*\.sql$",  # flag, still review
]
# migrations are flagged as "review with care", not excluded
EXCLUDE_IDX = len(GENERATED_PATTERNS) - 1


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"git failed: {' '.join(args)}\n{r.stderr.strip()}\n"
                 "Check the base branch name (try origin/<base>) and that you're inside the repo.")
    return r.stdout


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base, head = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "HEAD")
    spec = f"{base}...{head}"

    numstat = sh("git", "diff", "--numstat", spec)
    rows = []
    for line in numstat.strip().splitlines():
        add, dele, path = line.split("\t", 2)
        binary = add == "-"
        rows.append((0 if binary else int(add), 0 if binary else int(dele), path, binary))

    generated, migrations, reviewable = [], [], []
    for add, dele, path, binary in rows:
        pats = [p for p in GENERATED_PATTERNS if re.search(p, path)]
        if pats and re.search(GENERATED_PATTERNS[EXCLUDE_IDX], path):
            migrations.append((add, dele, path))
        elif pats or binary:
            generated.append((add, dele, path, "binary" if binary else "generated"))
        else:
            reviewable.append((add, dele, path))

    areas = defaultdict(lambda: [0, 0, 0])
    for add, dele, path in reviewable + migrations:
        area = path.split("/")[0] if "/" in path else "(root)"
        a = areas[area]
        a[0] += add; a[1] += dele; a[2] += 1

    total = sum(a for a, d, p in reviewable) + sum(d for a, d, p in reviewable)
    tier = "small" if total < 150 else "medium" if total <= 800 else "large"

    print(f"# Diff triage: {spec}\n")
    print(f"**Reviewable churn:** {total} lines across {len(reviewable) + len(migrations)} files → suggested tier: **{tier}**")
    if total > 400:
        print("\n> ⚠️ Over ~400 reviewable lines — consider suggesting a split before deep review.")
    print("\n## Areas\n\n| Area | Files | +Lines | -Lines |\n|---|---|---|---|")
    for area, (add, dele, files) in sorted(areas.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        print(f"| {area} | {files} | +{add} | -{dele} |")
    if migrations:
        print("\n## Migrations / SQL (review with extra care)\n")
        for add, dele, path in migrations:
            print(f"- {path} (+{add}/-{dele})")
    if generated:
        print("\n## Excluded from review scope (generated/binary)\n")
        for add, dele, path, why in generated:
            print(f"- {path} ({why})")
        excl = " ".join(f"':!{p}'" for _a, _d, p, _w in generated)
        print(f"\nSuggested pathspec exclusions:\n```\ngit diff {spec} -- . {excl}\n```")
    print("\n## Commit narrative\n")
    print("```")
    print(sh("git", "log", "--oneline", f"{base}..{head}").strip())
    print("```")


if __name__ == "__main__":
    main()
