# Factor checklist: correctness

Check the change against the stated requirements first, because working code can still solve the wrong problem.

- Requirements: does each acceptance criterion map to visible behavior in the diff? List any that don't.
- Edge inputs: empty, None, or zero; a single element; the maximum size; negative numbers; unicode; duplicate keys.
- Boundaries: off-by-one errors in ranges, slicing, and pagination; inclusive versus exclusive ends; time zones and daylight saving time in date math.
- Error paths: what happens when a dependency call fails, times out, or returns partial data? Does the code swallow errors, handle them twice, or log them without enough context to debug?
- State: can this run twice safely (is it idempotent)? If it fails partway through, what does it leave behind?
- Types and nulls: do the type annotations, including which values can be None, match what the code does at runtime? Does any cast hide a mismatch?
- Falsify before reporting: check callers' contracts and existing guards. The "missing check" is often three lines above the hunk, or a caller already handles it.
