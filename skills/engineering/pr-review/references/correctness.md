# Factor checklist: correctness

Verify against the stated requirements first — code can be flawless and still solve the wrong problem.

- Requirements: does each acceptance criterion map to visible behavior in the diff? List any that don't.
- Edge inputs: empty/None/zero, single element, max size, negative numbers, unicode, duplicate keys.
- Boundaries: off-by-one in ranges, slicing, pagination, inclusive/exclusive ends, timezone/DST in date math.
- Error paths: what happens when the dependency call fails, times out, or returns partial data? Are errors swallowed, double-handled, or logged with enough context?
- State: can this run twice safely (idempotency)? Partial failure mid-operation — what's left behind?
- Nullability & typing: do the type annotations match actual runtime behavior? Any casts hiding a lie?
- Falsify before reporting: check callers' contracts and existing guards — the "missing check" is often three lines above the hunk or enforced upstream.
