# DSI RSE Skills

Shared [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for the UChicago DSI Research Software Engineering team.

## Using a skill

Copy (or symlink) a skill's directory into your skills folder:

```bash
# available in every project
cp -r pr-review ~/.claude/skills/

# or per-project
cp -r pr-review your-project/.claude/skills/
```

Claude Code picks it up automatically — invoke by name (e.g. `/pr-review`) or just describe the task and the skill's `description` triggers it.

## Available skills

| Skill | What it does |
|---|---|
| [`pr-review`](pr-review/) | Structured multi-agent PR review with HIPPO severity tags (High, Important, Personal preference, Opinion). Gates, diff mapping, verification by running, fan-out reviewers, false-positive filtering. |

## Contributing a skill

A skill is a directory containing a `SKILL.md` with frontmatter:

```markdown
---
name: my-skill
description: One paragraph saying what it does AND when to trigger it — include the phrasings users actually type.
---

# My Skill

Instructions Claude follows when the skill is invoked...
```

Optionally add `references/` (docs loaded on demand) and `scripts/` (helper scripts). Use `pr-review/` as the model. Open a PR to add yours.
