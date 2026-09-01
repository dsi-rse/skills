# Factor checklist: performance

Anchor findings to realistic inputs — "this is O(n²)" only matters if n gets big. Say what n is.

- N+1: queries or API calls inside loops; missing eager-loading/batching where an ORM is involved.
- Complexity: nested loops over collections that scale with data; repeated linear scans that a dict/set fixes.
- Memory: loading whole files/result sets when streaming is available; unbounded caches; accumulating lists in long-lived scopes.
- I/O: sequential awaits that could be concurrent; missing pagination on list endpoints; chatty loops over the network.
- Hot paths: is the changed code actually hot? Check callers before flagging micro-costs in cold paths.
- Indexes: new query patterns — is there an index for the WHERE/ORDER BY? Migrations adding indexes on big tables: built concurrently?
- Verify when possible: time it, EXPLAIN it, or profile it via the live environment rather than asserting from the code alone.
