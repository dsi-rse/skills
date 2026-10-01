# Factor checklist: test coverage

Ask whether each test would fail if the new behavior broke.

- Mapping: each new behavior or requirement should have at least one test that exercises it. List the ones that don't.
- Assertion strength: flag tests that check nothing meaningful, such as a test with no assert, an assert-not-null on a value that can't be null, or a snapshot of everything. They raise coverage without catching bugs.
- Mutation check: pick 2 or 3 key lines of new logic and imagine inverting them, or actually invert them. Does any test fail?
- Edge cases: do tests cover error paths and boundary inputs, not only the happy path?
- Test quality: mocks so heavy that the test only checks the mock; tests that depend on run order; sleeps instead of proper synchronization; fixtures that tests share and modify.
- Deleted or modified tests: did the PR weaken or remove a test to make the suite pass? Rate that High until the author justifies it.
- Running: run the tests if you can, and say in each finding whether you ran the test or only read it.
