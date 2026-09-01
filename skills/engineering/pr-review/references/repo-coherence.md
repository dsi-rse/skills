# Factor checklist: repo coherence

Baseline first: CLAUDE.md, CONTRIBUTING, lint configs, and how neighboring code does it. Coherence findings without a cited baseline are just taste — tag those PREF, not Important.

- Reuse audit: before accepting new helpers/utilities, grep for existing ones (similar names, sibling modules, shared/utils dirs). Duplicated logic is Important; "I'd have named it differently" is PREF.
- Patterns: does the change follow the repo's established patterns for error handling, logging, DI, layering, API shape? Cite the file that sets the pattern.
- Placement: new files in the directories where this repo puts that kind of thing; consistent naming with siblings.
- Abstraction level: engineered enough for the requirement — neither hacky nor speculative generality (interfaces with one implementation, config nobody asked for).
- Dead weight: commented-out code, unused exports, TODO with no ticket, leftover debug logging.
- Docs: public surfaces documented in the same style the repo already uses; README/config docs updated if behavior changed.
