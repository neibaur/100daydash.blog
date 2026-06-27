---
title: "Day 56 - June 26, 2026: Spec Handoffs, Repo-Grounded Review, and the M5 Data Package"
description: "A Day 56 reflection on HaoMiantiao M5 data-package specification work, repo-grounded cross-agent review, and using documentation as operational memory."
pubDate: "2026-06-26"
day: 56
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao DESIGN.md"
  - "HaoMiantiao PROJECT_STATE.md"
  - "HaoMiantiao M5 data-package spec"
  - "HaoMiantiao PR #39"
  - "HaoMiantiao PR #40"
  - "HaoMiantiao PR #41"
  - "Claude M5 implementation notes"
  - "ChatGPT repo-grounded review notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - specs
  - haomiantiao
  - code-review
  - data-validation
  - developer-experience
---

Day 56 was not mainly a coding day.

It was a handoff day.

That sounds quieter than it felt. The useful work was not adding a visible new
feature to `haomiantiao` in one big motion. It was getting the project ready
for the next feature to be added safely: cleaning up state, drafting the M5
data-package spec, reviewing that spec against the actual repository design,
and deciding how the stacked PRs should be reviewed.

The project had just finished M4, the serialize and restore milestone for the
dependency-free bracket engine. That meant the tempting move was to keep
rolling directly into implementation.

Instead, the better move was to slow down just enough to make the next session
grounded.

That was the theme of the day: using AI systems not only to write code, but to
constrain, review, and hand off work safely.

## Cleaning The Handoff Surface

The first part of the day was about getting `haomiantiao` ready for a fresh
Claude session.

That meant checking the durable project artifacts instead of assuming the next
chat could inherit all the context from the previous one. `DESIGN.md` and
`PROJECT_STATE.md` were the important files.

`DESIGN.md` mostly still held up. The design direction was accurate enough to
continue using it as the source for core shape and milestone intent. It needed
a status pointer more than a rewrite: milestones 0 through 4 were complete,
and M5 was the next milestone.

`PROJECT_STATE.md` was more stale. It still described older milestone state
and did not clearly communicate where the project actually stood after M4.

That distinction mattered because project-state documentation is not just
human memory. In an agent-assisted workflow, it becomes handoff
infrastructure.

A new AI session should be able to ground itself by reading committed files,
not by relying on hidden chat history. If the repo says one thing and the last
conversation says another, the repo has to win. Otherwise the project starts
living in private transcripts instead of durable artifacts.

There was also an open governance item from the prior review work: the 404
CI-gate and per-commit-patch fixture issue around the line-count cap.

That could have become a stall point.

I decided not to let it block M5. The right action was to record it as a
deferred watch item with a concrete tripwire: if another PR is found over the
line cap, pause and investigate why the check missed it.

That felt like the practical balance. Do not ignore the issue. Do not let it
consume the next milestone before there is a fresh signal that the gate is
still failing.

## Starting M5 With A Spec

The next thread was the M5 data-package milestone.

Milestones 1 through 4 had built the dependency-free `packages/engine` core:
seeding, advancing rounds, resolving a champion, and serializing and restoring
bracket state.

M5 moves the project across its first real data boundary.

The milestone is about standing up `packages/data`, creating and loading
`noodles.json`, validating that data against TypeScript types and runtime
invariants, failing the current validation gate on malformed data, and using
fixture-driven tests.

I started a fresh Claude chat for the spec, but the prompt was deliberately
grounded before it asked for drafting.

Claude was told to read the noodles data shape in `DESIGN.md`, check whether
`noodles.json` actually existed yet, read the dependency and size rules in
`AGENTS.md`, and use `specs/m4-engine-serialize-restore.md` as the rigor model.

The instruction was also explicit about scope: do not implement yet. Draft the
spec first, and drive unresolved choices into a Decisions section.

That is a small process choice, but it changes the work.

If the agent jumps straight to implementation, the first version of the code
quietly decides the architecture. If the agent drafts the spec first, the
project gets a reviewable contract before files start moving.

M5 had real decisions to make:

- use a hand-rolled validator or bring in `zod`
- require every launch field to be complete or allow intentional placeholders
- decide how malformed data should fail the current repo gate
- clarify whether TypeScript types or a runtime schema are the source of truth
- decide whether M5 should expose only data and validation or also an engine
  adapter
- define the fixtures that should exist

Claude correctly found that `noodles.json` did not exist yet. It also called
out that TypeScript alone could not enforce the value-level invariants M5
needed: unique seeds, exact count, slug format, round count, and image metadata
rules.

That was the right direction.

The spec was not only describing a package. It was describing how to keep the
package honest.

## Repo-Grounded Cross-Agent Review

The most important workflow improvement of the day was bringing ChatGPT into
the loop as a repository-grounded reviewer.

Until now, a lot of cross-agent review had depended on pasted summaries. That
can work, but it is soft. The reviewer sees what I decide to paste. It may
miss the shape of the actual repo, the exact wording of a design file, or the
absence of a file that the summary implies exists.

Yesterday, ChatGPT was connected to the private
`neibaur-labs/haomiantiao` repository and confirmed it could inspect repo
metadata and files.

That immediately changed the quality of review.

Claude's initial M5 spec draft had a subtle but important data-contract issue.
It flattened tournament fields at the root.

ChatGPT compared the draft against the actual `DESIGN.md` and pointed out
that the root data shape was not flattened. The intended shape was:

```ts
{
  tournament,
  noodles,
}
```

That is the kind of issue that can slip through if the reviewer only sees a
natural-language summary. "Tournament data and noodles data" sounds close
enough until the contract becomes code. At that point, root shape matters.

The feedback went back to Claude. Claude accepted the correction, revised the
spec, renamed the root type to `NoodleData` to avoid reintroducing the
flattening ambiguity, and flipped the spec to reviewed.

That was the moment the multi-agent loop felt more real.

Claude drafted. ChatGPT reviewed against the repository. Claude revised. The
spec became the shared contract.

No single agent had to be treated as the source of truth. The repository and
the spec carried the authority.

## The M5 Contract

The final M5 decisions were concrete.

Use a hand-rolled validator. Do not add `zod` or any new dependency for this
milestone.

Keep the root shape exactly:

```ts
{
  tournament,
  noodles,
}
```

Hard validate the tournament and bracket invariants:

- `size === 16`
- `noodles.length === 16`
- `rounds.length === 4`
- canonical seed order, where `noodles[i].seed === i + 1`

Allow intentionally incomplete launch data. Empty `nameZh`, image
placeholders, and `buy[]` are acceptable.

But image metadata still has a rule: if `image.src` is non-empty, then
`image.alt` and `image.credit` must also be non-empty.

Keep lookup behavior simple. `getNoodleById` returns `Noodle | undefined`.

Do not add a noodle-to-engine `Contestant` adapter in M5. That belongs later,
when the project is ready to connect the data package to the engine package.

Keep validation separate from runtime accessors, so `getNoodles` and
`getNoodleById` do not drag validator code into the client path.

Make malformed data fail `pnpm validate`, since the repo does not yet have a
root build script.

And if the provisional dataset threatens the 400-line cap, split the
implementation into stacked PRs.

That last decision ended up mattering.

## Implementation As Stacked PRs

The M5 implementation was completed as three stacked, tests-first PRs.

That was the right shape for the line cap and for review clarity.

PR #39 handled the package scaffolding, types, `NoodleDataError`, structural
validation, and validation-gate wiring.

PR #40 added content-field validation.

PR #41 added the provisional 16-entry `noodles.json` dataset plus
`getNoodles` and `getNoodleById`.

That split kept each PR understandable. It also avoided turning the data file,
validator rules, package boundary, and runtime accessors into one oversized
review blob.

This is where governance rules start to feel less like overhead and more like
design tools.

The dependency limit pushed the project toward a hand-rolled validator. The
line cap pushed the implementation into stacked PRs. The test-first rule
pushed the validator and accessors into fixture-driven checks. The validation
gate forced malformed data to fail in the normal workflow, not in a special
side path.

Those constraints shaped the work before implementation started.

That is the part I want to keep.

The rules did not merely judge the result after the fact. They helped create a
better result.

## Reviewing The Stack

The final planning decision was about review.

The M5 work existed as three stacked PRs, and each PR had a different base and
scope. That means the pull request review skill should be run once per PR, not
once over all three at the same time.

Otherwise the review is likely to produce false findings.

For example, if PR #39 intentionally handles only package structure and
structural validation, a cumulative review might complain that content-field
validation is missing even though that belongs to PR #40. If PR #40 does not
include the provisional dataset, that is not a defect if PR #41 owns it.

Stacked PRs need scoped review.

A separate cumulative milestone-conformance pass may still be useful after
the stack is visible, but that is a different review mode. The per-PR skill run
should respect each PR's base and intended scope.

That is another small but important control point.

Review tools need to understand not only what changed, but where the change
sits in the stack. Otherwise they punish the very decomposition that made the
work reviewable.

## Why The Day Mattered

Day 56 mattered because it was another step away from ad hoc agent usage and
toward an actual multi-agent development loop.

The interesting part was not simply that Claude could draft a spec or
implement PRs. The interesting part was the workflow around that ability:

- documentation became operational memory for the next session
- the spec became the shared contract between agents
- Claude drafted and implemented within repo constraints
- ChatGPT reviewed with actual repository access
- governance rules shaped the work before code landed
- review planning adapted to stacked PR reality

That is a different posture than "ask an AI to write code."

It treats the agent as one participant in a governed system. The repo carries
the durable state. The spec carries the contract. Tests and validation gates
carry the enforcement. Human review owns the judgment. Cross-agent review adds
another lens, but it does not replace the repository as source of truth.

That feels like the direction this whole project has been moving.

The more capable the agents get, the more important the surrounding
constraints become.

## Outcome

Day 56 moved `haomiantiao` from post-M4 cleanup into a reviewed M5
data-package spec, then into implementation and review planning.

The day started by checking `DESIGN.md` and `PROJECT_STATE.md` for handoff
staleness. `DESIGN.md` mostly remained accurate, but needed a current status
pointer: milestones 0 through 4 were done, and M5 was next.
`PROJECT_STATE.md` was more stale and needed to reflect the actual
post-M4 project state.

The open 404 CI-gate and per-commit-patch fixture issue was captured as a
deferred watch item rather than allowed to block M5. The tripwire is clear: if
a PR is found over the line cap again, pause and investigate why the check
missed it.

Then a fresh Claude session drafted `specs/m5-data-package.md` from repository
context instead of hidden chat memory. The prompt required Claude to read the
noodles data shape in `DESIGN.md`, confirm that `noodles.json` did not yet
exist, read dependency and size rules in `AGENTS.md`, and use the M4 spec as
the rigor model.

ChatGPT was then connected to the private `neibaur-labs/haomiantiao`
repository and used as a repo-grounded reviewer. That caught a real spec issue:
Claude's first draft flattened tournament fields at the root, while the actual
design requires a `{ tournament, noodles }` root shape. Claude accepted the
feedback, revised the spec, renamed the root type to `NoodleData`, and marked
the spec reviewed.

The final M5 decisions were intentionally narrow: no new dependencies, a
hand-rolled validator, exact `{ tournament, noodles }` root shape, hard checks
for 16 noodles, four rounds, size 16, canonical seed order, allowed launch
placeholders, image metadata rules for non-empty image sources, no engine
adapter yet, and validation separated from runtime accessors.

The implementation then landed as three stacked, tests-first PRs: #39 for
package scaffolding and structural validation, #40 for content-field
validation, and #41 for the provisional dataset plus accessors.

The final review-planning decision was to run the pull request review skill
once per PR rather than once across the whole stack. A later cumulative
milestone-conformance pass may still be useful, but each stacked PR deserves a
review against its own base and scope.

## Definition Of Done

Day 56 reached an M5 handoff and review-planning checkpoint:

- reviewed `DESIGN.md` for current architectural accuracy
- reviewed `PROJECT_STATE.md` for stale milestone state
- identified `PROJECT_STATE.md` as the more stale handoff artifact
- kept `DESIGN.md` mostly intact, with a needed status pointer from M4 to M5
- treated documentation as handoff infrastructure for fresh AI sessions
- deferred the 404 CI-gate and per-commit-patch fixture issue without losing it
- defined a tripwire for future line-cap failures
- started a fresh Claude chat for the M5 data-package spec
- grounded the prompt in `DESIGN.md`, `AGENTS.md`, and the M4 spec
- confirmed `noodles.json` did not yet exist
- required spec drafting before implementation
- captured M5 open questions in a Decisions section
- clarified that TypeScript alone cannot enforce value-level invariants
- connected ChatGPT to the private `neibaur-labs/haomiantiao` repository
- used ChatGPT as a repo-grounded reviewer rather than a pasted-summary reviewer
- caught the incorrect flattened root shape in the initial M5 spec draft
- restored the intended `{ tournament, noodles }` root data shape
- renamed the root type to `NoodleData`
- marked the M5 spec reviewed after correction
- chose a hand-rolled validator with no new dependencies
- hard-validated `size === 16`, `noodles.length === 16`, and `rounds.length === 4`
- required canonical seed order with `noodles[i].seed === i + 1`
- allowed incomplete launch placeholders such as empty `nameZh`, images, and `buy[]`
- required `image.alt` and `image.credit` when `image.src` is non-empty
- kept `getNoodleById` returning `Noodle | undefined`
- deferred any noodle-to-engine `Contestant` adapter
- kept validation separate from runtime accessors
- made malformed data fail `pnpm validate`
- split M5 implementation into stacked PRs to respect the line cap
- completed PR #39 for package scaffolding, types, errors, structural validation, and gate wiring
- completed PR #40 for content-field validation
- completed PR #41 for the provisional 16-entry dataset and accessors
- decided to run the pull request review skill once per stacked PR
- preserved the option for a later cumulative milestone-conformance pass
- reinforced the broader workflow: specs as contracts, docs as memory, and
  agents as participants in a governed development loop
