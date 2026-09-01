# DSI RSE Skills

Shared [agent skills](https://www.skills.sh/) for the UChicago DSI Research Software Engineering team. Works with Claude Code, Cursor, Codex, and 70+ other agents.

## Install

**Via the skills CLI** (any agent):

```bash
npx skills add dsi-rse/skills                                  # interactive picker
npx skills add dsi-rse/skills --skill pr-review -a claude-code # one skill, one agent
npx skills add dsi-rse/skills --list                           # see what's available
npx skills update                                              # refresh later
```

**As a Claude Code plugin** (managed, auto-updating):

```bash
claude plugin marketplace add dsi-rse/skills
claude plugin install dsi-rse-skills@dsi-rse
```

**Manually**: copy a skill's directory into `~/.claude/skills/` (global) or `your-project/.claude/skills/` (per-project).

## Available skills

| Skill | Invocation | What it does |
|---|---|---|
| [`pr-review`](skills/engineering/pr-review/) | user- or model-invoked | Structured multi-agent PR review with HIPPO severity tags (High, Important, Personal preference, Opinion). Gates, diff mapping, verification by running, fan-out reviewers, false-positive filtering. |

## Contributing a skill

A skill is a directory under `skills/<category>/` containing a `SKILL.md` with frontmatter:

```markdown
---
name: my-skill
description: One paragraph saying what it does AND when to trigger it — include the phrasings users actually type.
---

# My Skill

Instructions the agent follows when the skill is invoked...
```

Optionally add `references/` (docs loaded on demand) and `scripts/` (helper scripts). Use `skills/engineering/pr-review/` as the model. Open a PR to add yours.
