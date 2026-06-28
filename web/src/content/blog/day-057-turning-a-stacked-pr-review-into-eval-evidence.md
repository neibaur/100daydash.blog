---
title: "Day 57 - June 27, 2026: Turning a Stacked PR Review into Eval Evidence"
description: "A Day 57 reflection on wrapping HaoMiantiao M5, reviewing stacked data-package PRs with separate agents, and turning review work into reusable eval evidence."
pubDate: "2026-06-27"
day: 57
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao PR #39"
  - "HaoMiantiao PR #40"
  - "HaoMiantiao PR #41"
  - "HaoMiantiao M5 data-package spec"
  - "HaoMiantiao packages/data validation work"
  - "reviewing-pull-requests skill eval notes"
  - "reviewing-pull-requests eval cases 0005 and 0006"
  - "HaoMiantiao M6 app-shell planning notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - code-review
  - evals
  - specs
  - haomiantiao
  - data-validation
  - developer-experience
---

Day 57 was about wrapping the stack without letting the stack blur the review.

The visible work was HaoMiantiao M5: the `packages/data` milestone, the
provisional noodle dataset, the validation gate, and the runtime accessors.

The more interesting work was around the shape of verification.

M5 did not land as one large change. It landed as three stacked PRs, each with
its own intended slice:

- PR #39 for the first M5 slice: package scaffolding, hand-authored types,
  structural validation, `NoodleDataError`, and validation gate wiring
- PR #40 for the second M5 slice: content-field validation, image metadata
  rules, buy-link validation, and content fixtures
- PR #41 for the final M5 slice: the provisional noodle dataset, `getNoodles`,
  `getNoodleById`, and the runtime accessor path

That decomposition was useful. It kept the milestone reviewable.

But it also created a review problem.

A stacked PR is not the same thing as a finished milestone. If a reviewer
looks at PR #39 as if it should contain everything from final M5, the review
will punish the split instead of evaluating the slice. If a reviewer sees PR
#40 without respecting the work below it, it may miss which helpers and
contracts are already established. If PR #41 is reviewed as a standalone data
drop, the runtime boundary can disappear behind the JSON.

So today was not only "finish M5."

It was "learn how to review a stacked spec implementation without
overclaiming."

## Separating Implementation From Verification

One of the clearest process choices was using different agents for different
jobs.

Opus handled implementation and fix work.

Fresh Sonnet sessions handled independent PR reviews.

That separation mattered.

The implementer has a path through the work. It knows why the code ended up
where it did. That context is useful, but it can also make blind spots easier
to repeat. A separate reviewer model starts colder. It has to reconstruct the
change from the PR, the spec, and the repository evidence.

That is not automatically better.

It is just a different lens.

The human job stays the same: own the merge decision, interpret review
findings, protect governed paths, and decide when a reported issue is real,
conditional, already resolved, or not worth locking into a permanent
contract.

That division felt healthy today.

The agents did not become authorities. They became participants in a review
system where the repository, spec, tests, and human judgment still carried the
control points.

## What The Review Found

The Sonnet review loop found no blocking architecture or spec-conformance
issues across the stack.

That was important, but the value was not only the green light. The useful
parts were the targeted follow-ups.

In PR #40, the review caught that `validateImage` needed to emit
`MISSING_IMAGE_METADATA` when `image.src` was present but `alt` or `credit`
was missing, not only when those fields were present as empty strings.

That sounded simple at first.

It was not quite simple, because the right fix depended on understanding the
earlier `str(...)` helper's return contract. Once that helper behavior was
confirmed, the possible `countryCode` double-report concern became
conditional rather than a real bug.

That was a good example of a reviewer needing to hedge honestly.

The visible symptom was in PR #40. The confidence level depended on helper
behavior established in the earlier stack slice. A review that pretends both
things are equally visible overstates its evidence.

The final decision around image metadata was explicit: when `image.src` is
non-empty and `alt` or `credit` is absent, emitting both `MISSING_FIELD` and
`MISSING_IMAGE_METADATA` for the same path is acceptable under the
aggregate-error model and the spec's consolidation latitude.

I chose not to lock in an exact `meta.length === 2` assertion.

That was intentional.

The current behavior is acceptable. The exact number of reported metadata
errors for that path does not need to become a permanent contract today.

In PR #41, the review found a different kind of cleanup. An unsafe assertion:

```ts
const data = noodlesJson as NoodleData;
```

was replaced with a type-checked assignment:

```ts
const data: NoodleData = noodlesJson;
```

That is the kind of tiny TypeScript change that matters because it changes the
direction of trust. The first form tells the compiler to believe the code. The
second asks the compiler to check the imported data against the declared type.

The same PR also had a larger JSDoc and comment style concern around
`getNoodleById`. That got simplified rather than expanded.

The final cleanup was almost comically small, but it said exactly what the
runtime boundary needed to say:

```ts
// Gate-validated at pnpm validate; no validator code in the client bundle.
```

That comment captured the intended contract better than a longer explanation.

## Reviewing The Stack In Order

The merge order mattered.

PR #39 had to land first. Then PR #40. Then PR #41.

Each base needed to be checked or retargeted as the parent PR landed. That is
ordinary stacked-PR mechanics, but it becomes more important when agents are
in the loop.

An agent can review a diff. It can compare a PR to a spec. It can find local
issues. But if the base branch is wrong, the review context is wrong. If the
reviewer treats a slice as the whole milestone, the findings can be wrong even
when the code observations are accurate.

That is the central tension with stacked work.

Decomposition makes implementation and review smaller. But the reviewer has
to understand the decomposition.

Today, the overall stack held together. The final validation reported for PR
#41 HEAD was green: `pnpm validate` passed with 5 test files, 73 tests, and
coverage above the 80/80 floor.

That result mattered less as a victory lap and more as evidence that the
stack had arrived at the intended gate.

M5 was effectively complete and merged.

`packages/data` now has the typed data package, validation, accessors, a
provisional 16-entry dataset, and validation wiring.

## Turning Review Into Eval Evidence

The second major thread was turning the review run itself into skill-eval
evidence.

This was the first stacked and partial-spec distribution exercised by the
`reviewing-pull-requests` skill.

The existing eval cases covered important behavior:

- fabrication
- faithful single-PR review
- PR-body masking
- citation precision

But they did not cover this newer risk: a reviewer judging one stack slice
against the full final milestone.

That is a distinct failure mode.

It is possible for a reviewer to be faithful to the final spec and still
unfair to the PR in front of it. PR #39 should not be reported as missing PR
#40's content-field validation if PR #39 is explicitly scoped to structural
validation. PR #40 should not be condemned for not carrying PR #41's
provisional dataset.

So I drafted and refined two new eval cases.

The first was:

```text
0005-stacked-partial-spec.md
```

That case checks whether the reviewer scopes PR #39 to its actual slice and
does not falsely report downstack M5 requirements as missing.

The second was:

```text
0006-cross-pr-visibility-hedging.md
```

That case checks whether the reviewer honestly hedges when a concern depends
on helper code from another PR, while still identifying a visible true
positive.

Those are exactly the kinds of cases the skill needs if it is going to review
real agent-authored work. Real work is not always one PR against one complete
spec. Sometimes the implementation is stacked, partial, and moving through
review while neighboring slices are still in flight.

If the eval harness only tests clean single-PR scenarios, it will miss that.

## Fixture Truth And Result Truth

The fixture plan also became more concrete.

The goal was to capture PR fixtures directly from GitHub into:

```text
.claude/skills/reviewing-pull-requests/evals/fixtures/pr-0039
.claude/skills/reviewing-pull-requests/evals/fixtures/pr-0040
.claude/skills/reviewing-pull-requests/evals/fixtures/pr-0041
```

Each fixture needs `meta.json` and PR diff files.

That sounds procedural, but fixture fidelity is the difference between an eval
that tests a real failure mode and an eval that only tells a story about one.

The review work also forced a documentation audit.

The eval README and `results/0.2.0.md` needed updates so the corpus did not
become stale or overstate itself.

The key audit distinction was between:

```text
origin-run observed pass
```

and:

```text
blind replay verified pass
```

Those are not the same claim.

An origin run can show that the skill behaved well in the session where the
case was discovered or refined. A blind replay is stronger evidence that the
skill behaves correctly when run fresh against a captured fixture. Both can be
useful. They should not be labeled as the same level of proof.

That distinction feels small until it is missing.

Then an eval corpus starts sounding more certain than it is.

## What M5 Leaves Behind

M5 now feels effectively complete.

The data package exists. The validation path exists. The accessors exist. The
provisional dataset exists. The validation wiring exists.

There are still follow-ups, but they are follow-ups rather than blockers.

One is the PR #40 fixture naming and pre-fix snapshot question. If the eval
case depends on pre-fix behavior, the fixture needs to preserve the right
state and say exactly what it preserves.

Another is whether the large `shape-defects.json` fixture should be split
later. It may be fine for now, but it is worth watching.

The repeated pattern of milestones landing at or near the 400-line cap is
also worth watching. The cap is doing useful work by forcing decomposition,
but repeated near-cap PRs may be a signal that the milestone slices should be
designed even earlier around review units.

That is not a failure.

It is feedback from the process.

## Preparing For M6

The next milestone is M6, the app shell.

That changes the shape of the work.

M5 stayed inside data-package boundaries. M6 introduces the app tier and
likely needs Next.js and React dependencies.

That matters because the repo governance is clear: agents should not install
dependencies directly. They should propose them, explain why they are needed,
and let me install them as maintainer.

So the next phase should start with a fresh spec-drafting chat, not a
dependency install.

The grounding set is clear:

- `DESIGN.md`
- ADRs
- `PROJECT_STATE.md`
- the completed M5 spec

That is the right starting shape.

The app shell should begin from durable project context, not from the momentum
of the previous implementation chat.

## Why The Day Mattered

Day 57 mattered because M5 became more than a data milestone.

It became a review milestone.

The project now has a typed `packages/data` path with validation, accessors,
and provisional data. But the more transferable lesson was how to review that
work across a stack without collapsing the slices into one undifferentiated
blob.

Different agents played different roles. Opus implemented and fixed. Fresh
Sonnet sessions reviewed. Human judgment made the governance decisions.

The review found no blocking architecture or spec-conformance problems, but it
did find useful targeted issues. Some were code changes. Some were comment
changes. Some were not changes at all, but decisions about what not to turn
into permanent contract.

And then the review became eval material.

That is the part I want to keep.

The best agent workflows do not only produce code. They leave behind evidence
about the workflow itself: what worked, what needed hedging, where the harness
was too narrow, and which future cases need to exist so the next run can be
judged more honestly.

M5 added data.

It also made the review process more testable.

## Outcome

Day 57 wrapped the HaoMiantiao M5 data-package stack and turned the review
process into new evaluation material for the `reviewing-pull-requests` skill.

The M5 implementation was reviewed across PR #39, PR #40, and PR #41. PR #39
covered package scaffolding, hand-authored types, structural validation,
`NoodleDataError`, and validation gate wiring. PR #40 covered content-field
validation, image metadata rules, buy-link validation, and content fixtures.
PR #41 covered the provisional 16-entry dataset, `getNoodles`,
`getNoodleById`, and the runtime accessor path.

Opus handled implementation and fix work. Fresh Sonnet sessions handled
independent PR reviews so the reviewer was not the same model that had
implemented the stack. Human judgment stayed responsible for merge decisions,
protected-path governance, and interpreting findings.

The reviews found no blocking architecture or spec-conformance issues across
the overall stack. They did surface targeted follow-ups: `validateImage`
needed to emit `MISSING_IMAGE_METADATA` when `image.src` was present but
`alt` or `credit` was absent, PR #41 needed to replace an unsafe
`noodlesJson as NoodleData` assertion with a checked `const data: NoodleData =
noodlesJson`, and the runtime data comment was simplified to the validation
boundary it actually needed to communicate.

One project decision was recorded clearly: under the aggregate-error model,
it is acceptable for a non-empty `image.src` with missing `alt` or `credit` to
emit both `MISSING_FIELD` and `MISSING_IMAGE_METADATA` for the same path. I
did not lock in an exact `meta.length === 2` assertion because that exact
count should not become a permanent contract.

The stacked PR order mattered: #39, then #40, then #41. Each base needed to be
checked or retargeted as the parent PR landed. The final validation reported
for PR #41 HEAD was green: `pnpm validate` passed with 5 test files, 73 tests,
and coverage above the 80/80 floor.

The review run also became skill-eval evidence. I drafted or refined
`0005-stacked-partial-spec.md` to test whether the reviewer scopes PR #39 to
its slice instead of falsely reporting downstack requirements as missing, and
`0006-cross-pr-visibility-hedging.md` to test whether the reviewer hedges
honestly when a concern depends on helper behavior from another PR while still
identifying a visible true positive.

The fixture plan now points to captured GitHub inputs under
`.claude/skills/reviewing-pull-requests/evals/fixtures/pr-0039`, `pr-0040`,
and `pr-0041`, each with metadata and diff files. The eval README and
`results/0.2.0.md` need to distinguish origin-run observed passes from blind
replay verified passes so the corpus does not overstate itself.

M5 is now effectively complete. `packages/data` has the typed data package,
validation, accessors, provisional dataset, and validation wiring. The next
phase is M6, the app-shell milestone, which should begin with fresh
spec-drafting grounded in `DESIGN.md`, ADRs, `PROJECT_STATE.md`, and the
completed M5 spec. Because M6 likely introduces Next.js and React
dependencies, agents should propose those dependencies rather than install
them directly.

## Definition Of Done

Day 57 reached the M5 stack-review checkpoint:

- reviewed the M5 work as three stacked PRs
- kept PR #39 scoped to package scaffolding, types, structural validation,
  `NoodleDataError`, and validation gate wiring
- kept PR #40 scoped to content-field validation, image metadata rules,
  buy-link validation, and content fixtures
- kept PR #41 scoped to the provisional dataset, `getNoodles`,
  `getNoodleById`, and runtime accessors
- used Opus for implementation and fix work
- used fresh Sonnet sessions for independent PR review
- kept human judgment responsible for merge decisions and protected-path
  governance
- confirmed the review loop found no blocking architecture or
  spec-conformance issues across the stack
- fixed the PR #40 `validateImage` behavior for missing `alt` or `credit`
  when `image.src` is present
- confirmed the `countryCode` double-report warning was conditional and not a
  real bug once helper behavior was understood
- accepted aggregate reporting of both `MISSING_FIELD` and
  `MISSING_IMAGE_METADATA` for the same image metadata path
- avoided locking in an exact `meta.length === 2` assertion
- replaced the PR #41 `noodlesJson as NoodleData` assertion with a checked
  `const data: NoodleData = noodlesJson`
- simplified the `getNoodleById` JSDoc and comment style
- collapsed the runtime data comment to the validation-gate boundary
- respected stacked merge order: #39, then #40, then #41
- checked or retargeted PR bases as parent PRs landed
- recorded the final PR #41 HEAD validation as green
- captured that `pnpm validate` passed with 5 test files, 73 tests, and
  coverage above the 80/80 floor
- treated M5 as effectively complete and merged
- recorded that `packages/data` now has types, validation, accessors, a
  provisional 16-entry dataset, and validation wiring
- identified stacked partial-spec review as a new eval failure mode
- drafted or refined eval case `0005-stacked-partial-spec.md`
- drafted or refined eval case `0006-cross-pr-visibility-hedging.md`
- planned GitHub-captured fixtures for PR #39, PR #40, and PR #41
- noted the need for fixture metadata and diff files
- identified the audit distinction between origin-run observed pass and blind
  replay verified pass
- noted that eval README and `results/0.2.0.md` need to avoid stale or
  overstated claims
- carried forward the PR #40 fixture naming and pre-fix snapshot question
- carried forward the possible future split of `shape-defects.json`
- kept watching the repeated near-400-line milestone pattern
- prepared to move into M6 as an app-shell milestone
- noted that M6 likely requires Next.js and React dependencies
- preserved the governance rule that agents propose dependencies and the
  maintainer installs them
- planned to start M6 with fresh spec drafting grounded in durable project
  artifacts
