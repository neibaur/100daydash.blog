---
title: "Day 59 - June 29, 2026: Turning an Agent Handoff Into a Governed Matchup Screen"
description: "A Day 59 reflection on HaoMiantiao M7 matchup-screen governance, dependency boundaries, B1/B2 implementation slicing, spec fidelity, and validation discipline."
pubDate: "2026-06-29"
day: 59
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao M7 matchup-screen spec"
  - "HaoMiantiao DESIGN.md seeding clarification"
  - "HaoMiantiao B1 implementation notes"
  - "HaoMiantiao B1 review notes"
  - "HaoMiantiao B2 handoff notes"
  - "ChatGPT repo-grounded review notes"
  - "Claude Opus implementation notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - specs
  - haomiantiao
  - code-review
  - dependency-governance
  - nextjs
  - validation
  - developer-experience
---

Day 59 was not a clean little "build the next screen" day.

It was messier than that, and more useful because of it.

HaoMiantiao was moving into M7, the matchup-screen milestone. On paper, that
sounds like a product step: take the app shell from M6, add `/play`, show two
noodle cards, and begin turning the bracket engine into something visible.

But the actual work was less about a screen and more about the loop around
the screen.

The day involved overlapping ChatGPT and Claude Opus sessions, a seeding
clarification, dependency blockers, spec reconciliation, implementation
slicing, review notes, and a fresh B2 handoff. The friction was not a side
effect. The friction was the point.

The implementation loop became the product.

The blockers, review findings, and handoff boundaries were the governance
system doing its job.

## Tightening The Decision Before Code

The day started with a small ambiguity that could have turned into a much
larger implementation mistake.

`DESIGN.md` still carried an open concern around tournament seeding:

- ordered 1v16 seeding
- random seeding each play

That sounds like a product decision, but it is also an engine boundary
decision.

The clarification was narrow and important. Ordered 1v16 ships for M7 because
the engine currently supports deterministic ordered seeding. Random-per-play
is still a future engine milestone.

That means the app should not grow an app-level random flag before the engine
owns the behavior.

This was not a reopened M7 decision. It was a small human-only documentation
clarification so the implementation agents would not improvise around a stale
open question.

That distinction matters.

If an app milestone quietly adds randomness because a design file left a
question hanging, the app starts owning bracket behavior that belongs in the
engine. That is exactly the kind of boundary leak the project has been trying
to avoid.

M7 needed to render the current product contract, not sneak in the next one.

## Splitting M7 Into Governed Slices

The next move was to split M7 into slices that could be reviewed honestly.

B1 was scoped to the initial matchup screen:

- add the `getTournament` accessor
- add `/play`
- turn the landing page Start affordance into a link
- show the round label
- show a progress rail
- render display-only noodle cards

B1 explicitly did not include pick buttons, advance logic, localStorage,
completion UI, or lint plugin wiring.

B2 was reserved for interaction:

- pick and advance behavior
- persistence
- completion acknowledgement
- Next lint wiring
- React Hooks lint wiring

That split was not just line-count management.

It made the review question clearer.

B1 could be judged as the first render path over engine and data behavior. B2
could be judged as the stateful interaction path. If those are merged into
one handoff, every review has to reason about data access, routing, rendering,
interaction, persistence, completion, hydration, and lint changes at the same
time.

That is how a milestone turns into a fog bank.

The split kept the screen from becoming an excuse to blur ownership.

## Letting The Dependency Blocker Block

The first B1 implementation attempt surfaced a real dependency problem.

The app needed to import:

```text
@haomiantiao/engine
@haomiantiao/data
```

But `apps/web` did not yet declare those workspace packages as dependencies.
Under pnpm's strict layout, bare specifier imports are supposed to fail when a
package has not declared what it uses.

That was not busywork.

That was the package manager enforcing the boundary.

The agent correctly stopped instead of reaching for deep relative imports
across package boundaries.

That was the right failure.

Deep imports would have made the implementation "work" by bypassing the
contract the repo uses to keep packages honest. The better fix belonged in a
maintainer dependency PR because dependency and lockfile changes are
maintainer-controlled in this repository.

This is one of the places where agent workflows get interesting.

An unconstrained implementation assistant can often find a way around a
blocker. A governed implementation assistant has to know when the workaround
is the bug.

The blocked B1 attempt was progress because it preserved the boundary that
would matter more later.

## Rebasing Onto The Real Spec

After the dependency and spec work reconciled, B1 was rebased onto current
`origin/main`.

That mattered because the implementation needed to target the real merged
state, not a stale handoff summary.

By then, main included the dependency wiring and the corrected reviewed M7
spec. The implementation could be checked against that actual contract.

B1 stayed intentionally thin.

The app rendered over engine and data behavior instead of becoming its own
bracket logic layer. It stayed under the line-count cap. It added the initial
matchup route, the Start link, the round and progress labels, and display-only
cards without smuggling in B2 behavior.

One spec-fidelity concern did come up.

The implementation used a local `findCurrent()` scan instead of the engine's
exported `currentMatch(state)`.

That was not a crisis. The behavior was low risk. But it was still the wrong
direction for the contract M7 was trying to establish.

The spec wanted bracket logic to remain owned by the engine.

So the local scan became a refactor requirement, not because it was obviously
broken, but because it weakened the boundary. The app should ask the engine
for the current match. It should not casually rediscover bracket semantics on
its own.

That is the kind of small fidelity issue that matters in an agent-assisted
codebase.

The app can be thin only if the review is willing to reject tiny bits of
extra cleverness before they harden into pattern.

## What The B1 Review Confirmed

The B1 review was clean in the ways that mattered.

It confirmed the important governance points:

- the implementation respected the line-count cap
- the work had the tests-first shape expected for the slice
- `getTournament()` did not leak validator code into the client path
- the Start affordance flipped from button semantics to a link
- `/play` had a single `h1`

Those sound like little things, but together they show the slice stayed inside
the rails.

The most notable carry-forward note was the bare `"Complete"` fallback in the
`match === null` branch.

In B1, that branch is effectively unreachable because there is no pick or
advance path yet. The screen cannot complete the bracket.

So the right answer was not to polish that placeholder in B1.

The right answer was to carry it into B2, where completion actually belongs.
B2 must replace the placeholder with the M7 completion acknowledgement:
champion naming, progress reaching 15 of 15, and no spillover into M8 or M9
features.

That is a useful review outcome.

Not every note needs to become an immediate fix. Some notes are signals about
where the next slice must close a loop.

## Preparing B2 As A Fresh Handoff

B2 was deliberately prepared as a fresh handoff, not as "keep going in the B1
chat."

That was the right workflow.

B2 depends on merged B1 behavior and on dependency and lint preconditions that
now exist on main. The next agent should start from the repository, not from
the momentum of the previous implementation thread.

The handoff was explicit about the tooling work.

B2 must wire `@next/eslint-plugin-next` and `eslint-plugin-react-hooks` early,
run lint before deeper work, and fix narrowly.

Unexpected repo-wide lint fallout is not permission to refactor the world. It
is not permission to lower gates either. If lint wiring plus required fixes
threatens the 400-line cap, the agent should stop and propose a split rather
than squeeze.

That instruction felt important because lint work has a way of becoming
ambient cleanup.

Ambient cleanup is risky in a milestone whose value depends on precise scope.

B2 is not "make the app prettier." B2 is "turn B1 into the interactive M7
matchup screen without absorbing future milestones or weakening gates."

## The B2 Traps

The B2 handoff also made the technical traps explicit.

Storage access belongs in effects and handlers only. It should never happen at
module scope or during render.

The first client render must match the static build output. Restoring from
`localStorage` happens after hydration.

Persistence should use the M4 serialization format through the engine's
serialize and deserialize path.

`load()` should return `null` on any failure:

- malformed storage
- unsupported serialized version
- invalid state
- `localStorage` exceptions

The pick handler has one especially easy bug.

Compute the next state once, then call:

```ts
setState(nextState);
save(nextState);
```

Do not call `save(state)` after `setState(...)`.

Inside the same handler, `state` is still stale. Persisting it would look
plausible and still be wrong.

B2 also has to replace the B1 `"Complete"` placeholder with the real M7
completion acknowledgement: name the champion, show progress as 15 of 15, and
stop there.

No share flow. No reveal animation. No clipboard. No URL hash. No play-again.

Those are M8 or M9 features.

The point is not to make the finished product feel artificially small. The
point is to keep each milestone honest enough that a reviewer can tell whether
it did the thing it said it would do.

## Why The Day Mattered

Day 59 mattered because it showed the governance loop holding under pressure.

The pressure was real.

There was a product ambiguity around seeding. There was a dependency blocker.
There was stale handoff risk. There was a spec-fidelity issue. There was a
review note that needed to be carried forward without being prematurely fixed.
There was a tempting path to keep one implementation chat rolling into the
next slice.

Any one of those could have turned the day into "the agent got it working."

But "got it working" is not the bar this project is trying to practice.

The better bar is:

- did the implementation stay inside reviewed scope
- did dependencies remain explicit
- did package boundaries hold
- did the app stay thin over engine and data behavior
- did the review distinguish blockers from carry-forward notes
- did the next handoff preserve the actual current repo state

That is the broader 100 Day Dash lesson.

The work is moving from asking an agent to code toward designing the rails
where agents can safely work.

The rails are not decorative.

Today, they caught things.

They caught an app-level randomness temptation before it became a hidden
engine decision. They caught undeclared workspace dependencies before deep
imports crossed package boundaries. They caught a local current-match scan
before the app started owning bracket semantics. They caught a completion
placeholder and routed it to the slice where completion actually belongs.

That is progress.

Not smooth progress.

Better progress.

## Outcome

Day 59 moved HaoMiantiao through the governed B1 implementation loop for M7
and prepared B2 as a fresh, stateful handoff.

The day started by resolving a DESIGN.md seeding ambiguity. Ordered 1v16
seeding ships for M7 because the engine currently supports deterministic
ordered seeding. Random-per-play remains a future engine milestone, not an
app-level flag. That clarification was handled as a small human-only docs
update rather than a reopened M7 decision.

M7 was split into governed slices. B1 covered `getTournament`, `/play`, the
landing-page Start link, round label, progress rail, and display-only noodle
cards. B1 excluded pick buttons, advance logic, localStorage, completion UI,
and lint plugin wiring. B2 was reserved for interaction, persistence,
completion acknowledgement, and Next/React Hooks lint wiring.

The first B1 implementation attempt found a real dependency blocker:
`apps/web` needed `@haomiantiao/engine` and `@haomiantiao/data` as declared
workspace dependencies before bare specifier imports would work under pnpm's
strict layout. The agent stopped instead of using deep relative imports. The
right fix belonged in a maintainer dependency PR because dependency and
lockfile changes are maintainer-controlled.

After dependency and spec reconciliation, B1 was rebased onto current
`origin/main`. The implementation was checked against the real merged spec,
stayed under the line-count cap, and kept the app as a thin renderer over
engine and data behavior. The main spec-fidelity concern was a local
`findCurrent()` scan that should use the engine's exported
`currentMatch(state)` instead.

The B1 review was clean but left carry-forward notes. It confirmed line-count
discipline, tests-first shape, `getTournament()` without validator leakage,
the Start role flip from button to link, and a single `h1` on `/play`. The
notable non-blocking note was the `"Complete"` fallback in the `match ===
null` branch. That branch is effectively unreachable in B1, so B2 should
replace it with the real M7 completion acknowledgement instead of fixing it
inside B1.

B2 was prepared as a fresh Opus handoff because it depends on merged B1 and on
main's dependency and lint preconditions. The handoff requires wiring
`@next/eslint-plugin-next` and `eslint-plugin-react-hooks` early, running lint
before deeper work, fixing narrowly, and stopping to propose a split if lint
wiring plus required fixes threatens the 400-line cap.

The B2 technical traps were made explicit: no storage access at module scope
or render time, first client render must match static output, localStorage
restore happens after hydration, persistence uses the M4
serialize/deserialize format, `load()` returns `null` on all failure modes,
and the pick handler must persist `nextState`, not stale `state`.

B2 must also replace the B1 `"Complete"` placeholder with champion naming,
progress reaching 15 of 15, and no M8 or M9 features such as share, reveal
animation, clipboard, URL hash, or play-again.

## Definition Of Done

Day 59 reached the M7 B1-to-B2 governance checkpoint:

- clarified the DESIGN.md seeding ambiguity before implementation
- kept ordered 1v16 seeding as the M7 behavior
- left random-per-play as a future engine milestone
- avoided an app-level random flag before engine support exists
- treated the seeding clarification as human-only docs cleanup
- split M7 into B1 and B2 implementation slices
- scoped B1 to the initial matchup screen
- included `getTournament` in B1
- included `/play` in B1
- included the landing-page Start link in B1
- included round label and progress rail in B1
- included display-only noodle cards in B1
- excluded pick buttons from B1
- excluded advance logic from B1
- excluded localStorage from B1
- excluded completion UI from B1
- excluded lint plugin wiring from B1
- reserved B2 for interaction and persistence
- reserved B2 for completion acknowledgement
- reserved B2 for Next and React Hooks lint wiring
- identified the missing `apps/web` workspace dependencies as a real blocker
- avoided deep relative imports across package boundaries
- kept dependency and lockfile changes maintainer-owned
- rebased B1 onto current `origin/main`
- checked implementation against the real merged M7 spec
- kept B1 under the line-count cap
- kept the app thin over engine and data behavior
- identified local `findCurrent()` as a spec-fidelity concern
- carried forward the requirement to use `currentMatch(state)`
- confirmed the B1 review found no blocking issues
- confirmed `getTournament()` avoided validator leakage
- confirmed the Start affordance became a link
- confirmed `/play` used a single `h1`
- treated the B1 `"Complete"` fallback as a B2 carry-forward note
- prepared B2 as a fresh handoff rather than a continuation chat
- required early wiring of `@next/eslint-plugin-next`
- required early wiring of `eslint-plugin-react-hooks`
- required lint to run before deeper B2 work
- kept unexpected lint fallout narrow
- required a split proposal if lint work threatens the 400-line cap
- required storage access only in effects or handlers
- required hydration-safe localStorage restore
- required M4 serialize/deserialize persistence
- required `load()` to return `null` for every storage failure mode
- required the pick handler to save `nextState`, not stale `state`
- required B2 to replace the completion placeholder
- required champion naming in the completion acknowledgement
- required progress to reach 15 of 15 at completion
- deferred share, reveal animation, clipboard, URL hash, and play-again
- preserved the larger lesson: agent implementation works best when the rails
  are designed before the agent starts moving
