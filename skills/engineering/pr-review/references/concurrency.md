# Factor checklist: thread and async safety

- Shared mutable state: what state do multiple threads, tasks, or requests touch? Look at module-level mutables, singletons, and class attributes used as instance state.
- Races: check-then-act sequences on files, dicts, or database rows (time-of-check to time-of-use bugs); read-modify-write without atomicity; double initialization.
- Locks: is the granularity right, is the ordering consistent so nothing deadlocks, and is every lock released on all paths (context managers, try/finally, defer)?
- Async code: blocking calls (sync I/O, sleep, heavy CPU work) inside async handlers; missing awaits; fire-and-forget tasks whose exceptions nobody sees; cleanup that breaks when a task is cancelled.
- Database concurrency: do transactions cover multi-step invariants? Does the isolation level fit the read pattern? Would SELECT ... FOR UPDATE or an optimistic retry fit better?
- Confidence: concurrency bugs rarely show up in a single run. Reason from the possible interleavings and state your confidence, because one passing test doesn't show the race is gone.
