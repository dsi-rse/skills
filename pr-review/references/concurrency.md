# Factor checklist: thread/async safety

- Shared mutable state: what's accessed from multiple threads/tasks/requests? Module-level mutables, singletons, class attributes used as instance state.
- Races: check-then-act sequences (TOCTOU) on files, dicts, DB rows; read-modify-write without atomicity; double-initialization.
- Locks: correct granularity, consistent ordering (deadlock), released on all paths (use context managers / try-finally / defer).
- Async correctness: blocking calls (sync I/O, sleep, heavy CPU) inside async handlers; forgotten awaits; fire-and-forget tasks with swallowed exceptions; cancellation safety around cleanup.
- DB concurrency: transactions around multi-step invariants; correct isolation for the read pattern; SELECT ... FOR UPDATE vs optimistic retry.
- Reproduce with care: concurrency bugs rarely show in single runs — reason from the interleaving and state your confidence rather than claiming certainty from one green test.
