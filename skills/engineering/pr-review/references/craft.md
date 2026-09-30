# Factor checklist: craft

Craft asks whether the change solves the problem the way an experienced practitioner would, and whether the next developer, human or agent, can read it and change it safely. The correctness reviewer checks whether the code works, and the repo coherence reviewer checks whether it matches the repo's patterns. Read the whole change before judging any line of it.

- Right approach: is there a simpler or more standard way to get the same result, such as the standard library, a platform feature, an installed dependency, or a common idiom? Rewriting something already solved is Important when the homemade version is buggier or harder to maintain, and PREF otherwise.
- Root cause: does the change fix the cause, or patch a symptom (a broad `try/except` around the crash, a special case for the one failing input)?
- Shape: is each decision made in one place? Is the data flow easy to trace? Would a better structure remove any of the special cases?
- Abstraction level: is the design as complex as the requirement needs and no more? Flag hacks, and flag speculative flexibility such as interfaces with one implementation, config nobody asked for, and layers that only forward calls.
- Accurate names and signatures: do functions do what their names say and nothing more? Do the types make misuse hard? A misleading name is Important. A name that's merely not ideal is PREF.
- Legible to a new reader: could someone new, or an agent with only this file in context, change it safely? Look for hidden coupling, magic values, setup that must run in a certain order, and invariants the code relies on but never states.
- The why is written down: a comment next to the code explains surprising choices, rejected alternatives, and known limits. Comments that restate the code add nothing. A new convention or gotcha belongs where the next person or agent will look, such as a docstring, the README, CLAUDE.md, or AGENTS.md.
- Internal consistency: does the diff do each thing one way? Two error styles or two naming schemes in one PR counts as a finding.
- Payoff: every finding names a concrete benefit, such as fewer bugs, a safer next change, or faster onboarding. "I'd have written it differently" with no benefit isn't a finding. Most craft findings are PREF or Opinion. Save Important for choices that will mislead readers or make the next change risky.
- Convention versus best practice: when the repo's way and common best practice disagree, consistency usually wins. Don't fault the PR for following the repo. If the convention itself is the problem, raise it as an Opinion.
- Good work: report it as a highlight and say specifically what's good, such as an elegant solution, a comment that will save the next reader time, or a test that documents intent.
