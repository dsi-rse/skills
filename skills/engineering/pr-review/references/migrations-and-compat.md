# Factor checklist: migration safety and backwards compatibility

Find out how the project ships before using this list. With rolling deploys or several running instances, old code runs against the new schema for a while, and most items below concern that overlap. For a library, the API compatibility item matters most. A script or single-user tool runs one version at a time, so check rollback and data safety there and skip expand/contract.

- Expand/contract: does the PR split destructive steps (dropping or renaming a column or table, narrowing a type, adding NOT NULL without a default) across releases? A rename becomes add, backfill, switch, and then drop in a later release.
- Locks: does this database engine lock the table during an ALTER on a large table? Does the migration create indexes concurrently and batch long backfills?
- Rollback: is there a down migration, or a documented reason there isn't one? Can data migrations run twice safely?
- Old code, new schema: can the version currently deployed still read and write during the rollout?
- API compatibility: removed or renamed fields, changed types or meanings, new required parameters, and changed status codes or errors all break existing callers. Additive changes are safe. Anything else needs versioning or a deprecation period.
- Serialized data: can new code still parse queue messages, database rows, and files that old code wrote?
- Configuration: do new required environment variables or flags have a safe default or a documented deploy order?
