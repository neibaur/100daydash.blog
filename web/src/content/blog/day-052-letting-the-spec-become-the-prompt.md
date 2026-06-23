---
title: "Day 52 - June 22, 2026: Letting the Spec Become the Prompt"
description: "A Day 52 reflection on haomiantiao M3 engine advancement, spec-driven development, PR review skill lessons, and turning governance feedback into eval and audit records."
pubDate: "2026-06-22"
day: 52
dashboardSlug: "none"
dataSources:
  - "haomiantiao M3 engine advance spec"
  - "haomiantiao PR #28"
  - "haomiantiao review-skill notes"
  - "haomiantiao audit and eval notes"
  - "haomiantiao governance cleanup notes"
status: "published"
tags:
  - haomiantiao
  - ai-agents
  - agentic-engineering
  - specs
  - governance
  - typescript
  - testing
  - developer-experience
---

Day 52 was not a flashy feature day.

It was better than that in a quieter way.

Most of the work stayed inside `haomiantiao`, and the main outcome was my
first complete pass through a spec-driven development loop that actually felt
real: write and review the spec, land it as the source of truth, have an agent
implement against the committed artifact, review the result against that same
artifact, disposition the findings, and record the governance lessons.

That is a different shape from "prompt the agent to build a thing."

The spec became the prompt.

That shift matters because it turns agent work from a private conversation
into a repository artifact. The implementation is no longer trying to satisfy
whatever I happened to write in a chat window. It is trying to satisfy a
reviewed contract that future reviewers, agents, and humans can all read.

The loop is still not mature. Today exposed that too. The review skill helped,
but it also fabricated a spec citation. The governance docs got sharper, but
they also showed where enforcement, convention, and judgment still need to be
kept separate.

That made the day useful.

Not polished. Useful.

## Aligning Governance With Enforcement

The day started with governance cleanup rather than implementation.

I reviewed suggested changes around `AGENTS.md`, security enforcement, and
agent behavior. The important thread was not whether the docs sounded strict.
It was whether the written contract matched the enforcement that actually
exists.

That distinction is easy to blur.

For example, it is tempting to write something like "ESLint enforces this" as
a shorthand for "this rule is part of the repository standard." But that can
become an overclaim. Some rules are enforced by ESLint. Some are enforced by
CI scans. Some are enforced by scripts. Some remain contract and judgment
rules that humans and agents are expected to follow even though no single tool
can prove them.

Those categories should not be collapsed.

If a rule is enforced by ESLint, say that. If it is enforced by a CI scan, say
that. If it is a governance contract, say that too. Pretending every rule has
the same enforcement surface makes the repo look more automated than it is,
and that is a bad kind of confidence.

This also connected to the review-skill setup.

I continued refining the boundary between human-only governance work and
agent-eligible implementation work. Files such as `AGENTS.md`, protected CI
configuration, and review-skill procedures can influence future agent behavior
and repository authority. They are not ordinary implementation surfaces.

That does not mean agents can never help with them. It means they should not
casually own them.

The practical lesson was simple: governance documentation needs to describe
both the rule and the enforcement reality. A rule that depends on human
judgment is still a real rule, but it should not be described as if a linter
is catching it.

## The M3 Spec Became The Implementation Prompt

The major technical work was Milestone 3 for the `haomiantiao` bracket engine:
advancing winners, transitioning between rounds, detecting a champion, and
guarding illegal states.

The source of truth was:

```text
specs/m3-engine-advance.md
```

This was the first time I treated a spec file as the implementation prompt
instead of writing a long custom instruction block for the coding agent.

The workflow was the point:

- planning, spec work, and governance happen first
- the reviewed spec is committed to `main`
- the coding agent reads the spec from the repository
- the implementation PR links back to the spec
- review happens against the spec, not just against general expectations

That last part changed the feel of the work.

Without a spec, review can drift into taste, memory, or whatever the reviewer
assumes the feature was supposed to do. With a committed spec, the reviewer
has something concrete to test the implementation against.

That does not make review automatic. It makes review more accountable.

It also raises the standard for the spec itself. If the spec is vague, the
implementation inherits that vagueness. If the spec omits an ordering rule,
the review cannot pretend the rule was already there. If the spec uses one
name and the implementation uses another, that mismatch is now visible.

This is the responsibility side of spec-driven development.

The spec is not ceremony. It is a contract. If I want the agent to implement
the contract, I have to make the contract precise enough to be implemented.

## Building The Pure Engine Loop

PR #28 implemented the M3 engine work in `packages/engine`.

The implementation introduced a playable bracket state machine with a small
set of public concepts:

- `BracketState`
- `BracketRound`
- `BracketMatch`
- `MatchId`

The public API stayed deliberately pure:

- `createBracketState`
- `currentMatch`
- `pickWinner`
- `champion`
- `isComplete`

That shape fits the project. `haomiantiao` is still aiming for a static,
client-side product path. The engine should be easy to test, easy to import,
and free of UI assumptions.

One important implementation choice was that `createBracketState` delegates to
the existing `seedRoundOfSixteen` behavior instead of duplicating seeding
logic. That kept M3 focused on advancement rather than reimplementing the
rules from the earlier engine slice.

`pickWinner` became the main state transition function. It is immutable, and
it throws a typed `BracketAdvanceError` for invalid advancement operations.

The error codes are intentionally specific:

- `UNKNOWN_MATCH`
- `MATCH_DECIDED`
- `NOT_A_COMPETITOR`

Those names are small, but they matter. They give tests, UI code, and future
reviewers a stable way to distinguish invalid operations instead of treating
every failure as a generic exception.

The engine also materializes rounds lazily.

That means the next round appears when the prior round has enough decided
winners to create it. The state stores round indexes rather than UI-facing
round names, which keeps presentation language out of the core engine.

By the end of the implementation pass, validation passed with tests and
coverage above the configured floor.

That was the visible engineering result: M3 completed the pure bracket-engine
loop.

But the more interesting part was what happened after.

## Reviewing The Reviewer

After PR #28, I ran the `reviewing-pull-requests` skill in a fresh session.

That was the first real exercise of the review-skill loop against a meaningful
implementation PR.

The result was useful, but not clean.

The review produced feedback worth considering. It also surfaced a serious
process issue: it fabricated a spec citation. The review claimed the spec
already said `pickWinner` could decide any undecided materialized match in any
order.

That was not actually present in the spec at the time.

This is exactly why the review skill is still draft-only and advisory.

A review skill can sound authoritative very quickly. It can cite files. It can
use the language of requirements. It can produce findings that look grounded.
But the output still has to be checked against the actual spec and diff.

In this case, the fabricated citation was not a reason to throw away the
workflow. It was a reason to improve the workflow.

I recorded the issue as an eval case so future promotion of the skill can be
based on evidence instead of trust. A review skill that invents requirements
needs a test case for that failure mode.

That is the healthier loop:

```text
review produces a questionable finding
compare it against the spec and diff
accept, reject, or clarify the finding
record the failure mode as an eval
improve the procedure before trusting it more
```

The review skill helped, but it did not get authority just because it helped.

That distinction is becoming one of the core themes of this whole project.

## Clarifying The Contract

The fabricated citation pointed at a real ambiguity.

The intended behavior was that `pickWinner` may decide any undecided match in
an already materialized round. It is not restricted to only the match returned
by `currentMatch`.

`currentMatch` is a convenience function. It returns the next undecided match
in play order. It is not an ordering guard.

That distinction needed to be explicit.

So the follow-up work clarified the contract and hardened the tests. A
regression test was added for an out-of-order materialized round-0 pick. That
keeps the intended behavior from being accidentally narrowed later.

I also cleaned up the test helper `expectAdvanceError` so the tested function
is invoked exactly once.

That seems small, but it is the kind of test hygiene that matters in state
transition code. A helper that calls the function under test more than once
can accidentally hide mutation problems, produce confusing failures, or make a
test pass for the wrong reason.

Finally, the implementation parameter `targetId` was renamed to `matchId` so
the code matched the spec and JSDoc.

That is a small naming correction, but in this workflow names carry more
weight. If the spec says `matchId`, the implementation should not casually use
a different name for the same concept unless there is a good reason.

Spec-driven development makes those mismatches easier to see.

## Cleaning Up The Spec Path

There was one plain repository hygiene issue too.

The M3 spec had accidentally landed under:

```text
specs/specs/m3-engine-advance.md
```

That was wrong.

The canonical path is:

```text
specs/m3-engine-advance.md
```

I cleaned that up so the spec now lives where future contributors and agents
should expect it.

This kind of path cleanup is not exciting, but it matters more in a
spec-driven workflow than it would in an ad hoc workflow. If specs are the
source of truth, their location is part of the contract. A duplicate
`specs/specs` path is a small signal that the system is not quite aligned.

The path is fixed now.

## Recording The Governance Lessons

The day also produced two documentation records.

The first was the eval case for the fabricated spec citation from the review
skill.

The second was an audit note about contrasting agent behavior when blocked
operations appeared.

That contrast was useful.

In one case, an agent routed around a failed PR-body edit by using a different
API path. In another case, an agent correctly stopped and reported when
updating a branch would require a force-push, which the contract forbids
agents from doing.

The difference was not random.

Agents are more likely to stop correctly when the rule is explicit. They are
more likely to improvise around a blocked operation when the contract does not
clearly say whether that workaround is allowed.

That does not mean every possible behavior can be prewritten. It does mean
high-risk boundaries deserve plain language.

Force-pushes are a good example. If the rule says agents must not force-push,
then an agent has a clean stopping point when a branch update requires one.
There is no need to guess whether the workaround is clever or unsafe.

The broader lesson is that governance should be specific where the failure
mode is specific.

## Why The Day Mattered

Day 52 mattered because the full loop started to work.

Not perfectly. Not automatically. But enough to show the shape:

```text
spec -> implementation -> review skill -> follow-up fixes -> eval/audit record
```

That is a meaningful shift from prompt-driven implementation.

The old pattern is easy to understand: write a detailed prompt, ask the agent
to implement it, review the diff, and keep moving.

The new pattern is more durable: write the contract, commit the contract, let
the agent implement against the contract, and review against the same contract.

That makes the work easier to audit later. It also makes it easier to improve
the process because failures leave artifacts. A vague spec can be revised. A
review hallucination can become an eval case. A blocked-operation mismatch can
become an audit note. A naming mismatch can be corrected in code and docs.

The cost is that specs now matter more.

They have to be precise. Review findings have to be grounded. Governance docs
have to distinguish between enforcement, convention, and judgment. Agent
skills have to earn trust through evals instead of borrowing authority from
their filenames.

That is a lot of responsibility for a day that did not ship a browser UI.

But it is the kind of responsibility I want before the UI exists.

## Outcome

Day 52 completed the first real spec-driven development pass for
`haomiantiao`.

I started by tightening governance language around `AGENTS.md`, security
enforcement, and agent behavior. The main correction was to avoid overclaims:
not every rule is enforced by ESLint, and the docs should distinguish between
ESLint enforcement, CI scans, script checks, and human or agent judgment.

The main implementation work was M3 for the bracket engine. The committed
`specs/m3-engine-advance.md` file became the implementation prompt. PR #28
then added a pure bracket state machine in `packages/engine`, including
`BracketState`, `BracketRound`, `BracketMatch`, `MatchId`,
`createBracketState`, `currentMatch`, `pickWinner`, `champion`, and
`isComplete`.

The engine advances winners immutably, materializes rounds lazily, detects the
champion, stores round indexes rather than UI labels, delegates initial
seeding to `seedRoundOfSixteen`, and throws `BracketAdvanceError` with
specific error codes for invalid operations.

After implementation, I ran the draft `reviewing-pull-requests` skill in a
fresh session. The review was useful, but it also fabricated a spec citation
about `pickWinner` ordering behavior. I checked that claim against the actual
spec and diff, treated the review output as advisory, and recorded the failure
as an eval case.

The follow-up clarified the intended contract: `pickWinner` may decide any
undecided match in an already materialized round, while `currentMatch` is only
a convenience for play-order discovery. I added a regression test for an
out-of-order materialized round-0 pick, refactored `expectAdvanceError` so the
tested function runs once, and renamed `targetId` to `matchId`.

I also fixed the accidental `specs/specs/m3-engine-advance.md` path so the M3
spec now lives at `specs/m3-engine-advance.md`, and I recorded audit notes
about agent behavior around blocked operations and explicit contract coverage.

The day ended with M3's pure engine loop complete and the process around it
more honest than it was at the start.

## Next Step

M3 completes the pure engine loop, but there is still no browser surface to
validate manually.

The next milestone should be intentionally boring: M4 should scaffold the web
app without trying to build the playable bracket UI yet.

The target is:

- `apps/web`
- Next.js static export
- workspace wiring
- validation scripts
- a minimal page proving the app starts
- a smoke test proving the web app can import the engine

That is enough.

M4 should prove the application shell exists and can consume the engine. M5
can then wire the engine into a minimal clickable bracket UI.

## Definition Of Done

Day 52 reached a spec-driven-development checkpoint:

- reviewed suggested governance changes around `AGENTS.md`, security
  enforcement, and agent behavior
- clarified the difference between ESLint enforcement, CI scan enforcement,
  script enforcement, and contract or judgment rules
- continued refining the boundary between human-only governance work and
  agent-eligible implementation work
- treated `specs/m3-engine-advance.md` as the authoritative M3 implementation
  spec
- used the committed spec as the coding-agent prompt
- linked the implementation work back to the spec through PR #28
- implemented the M3 bracket engine advancement behavior in `packages/engine`
- introduced `BracketState`, `BracketRound`, `BracketMatch`, and `MatchId`
- exposed `createBracketState`, `currentMatch`, `pickWinner`, `champion`, and
  `isComplete`
- delegated initial state creation to `seedRoundOfSixteen`
- kept `pickWinner` immutable
- added `BracketAdvanceError` for invalid advancement operations
- used `UNKNOWN_MATCH`, `MATCH_DECIDED`, and `NOT_A_COMPETITOR` error codes
- materialized rounds lazily
- stored round indexes rather than UI-facing round names
- passed validation after implementation with tests and coverage above the
  configured floor
- ran the draft `reviewing-pull-requests` skill in a fresh session
- found useful review feedback and one fabricated spec citation
- verified that the claimed `pickWinner` ordering language was not present in
  the spec at the time
- kept the review skill advisory rather than authoritative
- recorded the fabricated citation as an eval case
- clarified that `pickWinner` may decide any undecided match in an already
  materialized round
- clarified that `currentMatch` is a convenience function, not an ordering
  guard
- added a regression test for an out-of-order materialized round-0 pick
- refactored `expectAdvanceError` so the tested function is invoked exactly
  once
- renamed `targetId` to `matchId` to match the spec and JSDoc
- moved the M3 spec from `specs/specs/m3-engine-advance.md` to
  `specs/m3-engine-advance.md`
- added an audit note about contrasting agent behavior around blocked
  operations
- reinforced that explicit contract coverage helps agents stop correctly at
  high-risk boundaries
- identified M4 as a boring web-app scaffold milestone before any clickable
  bracket UI work
