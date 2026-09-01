# Factor checklist: migration safety & backwards compatibility

Assume deploys are rolling: old code and new schema (and vice versa) WILL coexist. Every finding here is about that window.

- Expand/contract: destructive steps (drop/rename column or table, narrowing types, adding NOT NULL without default) must be split across releases. Rename = add + backfill + switch + drop later.
- Locks: ALTERs on large tables — does this engine lock? Indexes created concurrently? Long backfills batched?
- Rollback: is there a down path, or a documented reason there isn't? Data migrations: idempotent and re-runnable?
- Old code vs new schema: can the currently deployed version still read/write during rollout?
- API compatibility: removed/renamed fields, changed types or semantics, new required params, changed status codes/errors — all breaking for existing clients. Additive is safe; everything else needs versioning or deprecation.
- Serialized data: messages in queues and rows written by old code — can new code still parse them?
- Config/env: new required env vars or flags — deploy order documented? Sane default?
