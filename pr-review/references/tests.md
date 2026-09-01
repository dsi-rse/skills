# Factor checklist: test coverage

The question is not "are there tests" but "would these tests fail if the new behavior broke".

- Mapping: each new behavior/requirement → at least one test that exercises it. List uncovered behaviors.
- Assertion strength: tests that assert nothing meaningful (no assert, assert-not-null on something that can't be null, snapshot-everything) are coverage theater — flag them.
- Mutation check (mental or real): pick 2–3 key lines of new logic, imagine inverting them — does any test fail?
- Edge cases: error paths and boundary inputs tested, not just the happy path.
- Test quality: over-mocking that tests the mock; order-dependent tests; sleeps instead of synchronization; shared mutable fixtures.
- Deleted/modified tests: any test weakened or removed to make the suite pass? That's a High until justified.
- Run them (Phase 4): a test you executed is evidence; a test you read is a guess.
