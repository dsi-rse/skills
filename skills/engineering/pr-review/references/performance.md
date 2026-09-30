# Factor checklist: performance

Tie each finding to realistic input sizes. "This is O(n²)" matters only if n gets big, so say what n is.

- N+1 queries: a query or API call inside a loop; missing eager loading or batching when the code uses an ORM.
- Complexity: nested loops over collections that grow with the data; repeated linear scans that a dict or set would replace.
- Memory: loading whole files or result sets when streaming is available; caches with no size limit; lists that keep growing in long-lived objects.
- I/O: sequential awaits that could run concurrently; list endpoints without pagination; loops that make one network call per item.
- Hot paths: does the changed code run often enough to matter? Check the callers before flagging small costs in code that rarely runs.
- Indexes: does each new WHERE or ORDER BY pattern have an index? Do migrations that add indexes to big tables build them concurrently?
- Measure when you can: time it, run EXPLAIN on the query, or profile it in the live environment (within the approved actions). Report the measurement, or say that the finding comes from reading the code.
