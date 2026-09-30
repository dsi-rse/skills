# Factor checklist: repo coherence

Start from the baseline: CLAUDE.md, AGENTS.md, CONTRIBUTING, lint configs, and how neighboring code does the same thing. If you can't cite a baseline for a coherence finding, tag it PREF, not Important.

- Reuse audit: before accepting a new helper or utility, grep for existing ones (similar names, sibling modules, shared or utils directories). Duplicated logic is Important.
- Patterns: does the change follow the repo's established patterns for error handling, logging, dependency injection, layering, and API shape? Cite the file that sets each pattern.
- Placement: do new files sit in the directories where this repo keeps that kind of file, with names that match their siblings?
- Leftovers: commented-out code, unused exports, TODOs with no ticket, debug logging.
- Docs: do public APIs have docs in the repo's usual style? If behavior changed, did the README or config docs change with it?
