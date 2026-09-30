# Factor checklist: craft

Correctness asks whether it works; coherence asks whether it fits the repo. Craft asks whether it's the right way to do it: the solution an experienced practitioner would reach for, left in a state the next developer, human or agent, can read, trust, and change. Read the whole change before judging any line of it.

- Right approach: is there a simpler or more standard route to the same result (stdlib, platform feature, an already-installed dependency, a well-known idiom)? Hand-rolling something already solved is Important when the homemade version is buggier or harder to maintain, PREF otherwise.
- Root cause: does the change fix the cause, or patch a symptom (a broad `try/except` around the crash, a special case for the one failing input)?
- Shape: the structure follows the problem. Each decision has one home, data flow is easy to trace, and special cases aren't standing in for a better structure.
- Abstraction level: engineered enough for the requirement, neither hacky nor speculative (interfaces with one implementation, config nobody asked for, layers that only forward calls).
- Honest names and signatures: things do what they're called and no more; types make misuse hard. A misleading name is Important; a merely imperfect one is PREF.
- Legible to a cold reader: could someone new, or an agent with only this file in context, change it safely? Watch for hidden coupling, magic values, order-dependent setup, and invariants that live only in the author's head.
- The why is written down: surprising choices, rejected alternatives, and known limits are explained next to the code. Comments that restate the code are noise. A new convention or gotcha belongs where the next person or agent will look (docstring, README, CLAUDE.md/AGENTS.md).
- Consistent within itself: one way of doing each thing across the diff, not two error styles or naming schemes in one PR.
- Unfussy: every finding names a concrete payoff (fewer bugs, a safer next change, faster onboarding). "I'd have written it differently" with no payoff isn't a finding. Most craft findings are PREF or Opinion; Important is for choices that will mislead readers or make the next change risky.
- Convention vs best practice: when the repo's way and the textbook way disagree, consistency usually wins. Don't fault the PR for following the repo; if the convention itself is the problem, raise it as an Opinion.
- Name the good work: an elegant solution, a comment that saves the next reader an hour, a test that documents intent. Specific highlights teach as much as findings do.
