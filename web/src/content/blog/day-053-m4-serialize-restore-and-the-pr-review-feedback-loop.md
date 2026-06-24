---
title: "Day 53 - June 23, 2026: M4 Serialize/Restore and the PR Review Feedback Loop"
description: "A Day 53 reflection on haomiantiao M4 serialize/restore work, canonical bracket state encoding, PR review skill evidence, and governance lessons from bot-authored handoff artifacts."
pubDate: "2026-06-23"
day: 53
dashboardSlug: "none"
dataSources:
  - "haomiantiao M4 serialize/restore spec"
  - "haomiantiao PR #33"
  - "haomiantiao review-skill notes"
  - "haomiantiao review-skill eval case drafts"
  - "haomiantiao bot PR metadata notes"
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

Day 53 was a small engine milestone with a much larger governance shadow.

The code work was intentionally narrow: teach the `haomiantiao` bracket engine
how to serialize and restore its state.

No browser storage. No share URLs. No base64 wrapper. No app-layer metadata.
No DOM assumptions. No new dependencies.

Just a pure, framework-free encoding boundary for bracket state.

That was enough.

The more interesting part was what the work revealed around review evidence,
bot-authored PR handoffs, and the difference between an assistant producing a
useful review and a review process becoming trustworthy.

M4 moved the engine closer to future share-hash and localStorage support. It
also gave the review-skill work another concrete case: a PR where the review
appeared faithful to the reviewed spec, but still needed human verification
before its code-level claims could be treated as true.

That is the shape of the lesson.

Canonical state is not just a serialization problem. Review output has state
too. PR metadata has state. Governance artifacts have state. If those things
are going to be trusted later, they need to be explicit, replayable, and
checked against reality.

## Moving The Spec To Decision Mode

The day started with the M4 spec.

At first, the spec still had a draft/open-question shape. It described the
serialize/restore direction, but a few decisions still needed to stop being
questions and become reviewed contract.

That transition matters more than it sounds.

When a spec is still asking questions, it is a planning artifact. Once the
questions are resolved and the status moves to reviewed, the spec becomes the
implementation boundary. It tells the agent what to build, tells the reviewer
what to check, and tells future maintainers what was intentionally left out.

The reviewed decisions were deliberately small and sharp.

M4 would encode replayable bracket inputs and decisions rather than the full
materialized round tree. It would keep exactly three serialization error
codes:

- `MALFORMED`
- `UNSUPPORTED_VERSION`
- `INVALID_STATE`

It would expose only:

- `serializeBracket`
- `deserializeBracket`

The proposed `tryDeserializeBracket` helper was deferred. That was the right
call for this milestone. A result-returning convenience wrapper might be
useful later, but M4 did not need to add another public API shape before the
core boundary existed.

The spec also clarified the most important contract edge: `serializeBracket`
is total only over reachable `BracketState` values created by
`createBracketState` and advanced through `pickWinner`.

Forged or hand-mutated in-memory states are out of contract.

That sentence does useful work. It avoids pretending the serializer has to be
a universal validator for arbitrary objects. The validated boundary is
deserialization. If something comes in from a string, it must be parsed,
checked, rebuilt, and replayed. If code inside the same process forges an
impossible state by bypassing the engine API, that is not M4's responsibility.

The spec stayed equally narrow on identity.

The serialized form would store only engine-level contestant identity:

- `id`
- `seed`

Rich noodle metadata belongs to the later data or app layer. That keeps the
engine from learning about presentation concepts before there is a real app
surface asking for them.

Chronology was another important decision. Interaction chronology is
intentionally not serialized. The canonical pick order is derived by parsed
`(roundIndex, matchIndex)`, not by the order in which the user clicked through
the bracket.

That is a quiet but important restraint. The engine needs to restore the same
bracket decisions. It does not need to preserve the user's interaction diary.

Finally, the spec avoided any TypeScript target or lib change for
`Error.cause`. The implementation could use native cause support if already
available, or a readonly field otherwise. That kept a small engine milestone
from turning into a toolchain milestone.

By the end of that pass, the spec moved to `status: reviewed`.

That made it ready to become the prompt.

## Implementing The Pure Serialize/Restore Boundary

The implementation happened on the bot branch:

```text
feat/engine-serialize-restore
```

That was separate from `main`, which is exactly where this kind of milestone
belongs.

The public surface added to the engine was small:

- `serializeBracket(state) => string`
- `deserializeBracket(string) => BracketState`
- `BracketSerializationError`
- `BracketSerializationErrorCode`
- `SERIALIZED_BRACKET_VERSION`

The serialized form is canonical JSON with top-level fields:

```text
{ v, contestants, picks }
```

That shape is intentionally boring.

`v` gives the engine a version boundary. `contestants` records the bracket
inputs. `picks` records the decisions needed to replay the bracket. The
materialized round tree is not serialized.

That last part is the heart of the milestone.

If the engine can rebuild state by calling `createBracketState` and replaying
decisions through `pickWinner`, then restore stays attached to the same rules
as normal gameplay. It does not smuggle in a second state-construction path.

That is the reason replay-based serialization feels stronger than dumping the
current tree. The tree is an output of the engine rules. The serialized data
should be the minimal input needed to reproduce that output.

The canonical ordering rules also stayed clear:

- contestants are sorted by seed
- picks are sorted by parsed `(roundIndex, matchIndex)`

That means two equivalent bracket states should produce the same string. It
also means the serialized form does not depend on incidental object ordering
or click chronology.

The implementation was test-first in a very explicit way.

The first commit added failing tests and deliberately wrong stubs. The second
commit implemented the behavior. That is the useful version of test-first
discipline for this kind of code: make the contract executable before the
implementation tries to satisfy it.

Validation passed with:

```text
pnpm validate
```

Coverage remained above the project floor.

That gave M4 the technical result I wanted: a pure serialize/restore pair for
engine state, with no dependencies and no app-layer concerns mixed in.

## Why Canonical Replay Matters

Serialize/restore can look like plumbing.

In a small bracket engine, it is tempting to treat it as a convenience feature:
turn the object into JSON, then turn JSON back into an object.

That would have been the wrong milestone.

The important question is not "can this object be stringified?" The important
question is "what is the smallest stable contract that can reproduce a valid
bracket state later?"

M4 answered that by choosing replay.

Store the contestants. Store the decisions. Rebuild the bracket through the
same public engine functions that normal code uses.

That choice does a few useful things at once.

It keeps invalid serialized input from becoming trusted engine state. It makes
versioning visible. It gives future app code a stable primitive for local
storage or share links. It avoids locking the serialized format to whatever
the in-memory round tree happens to look like today.

It also keeps the engine honest.

If `deserializeBracket` can only restore by using `createBracketState` and
`pickWinner`, then restore behavior is coupled to the same invariants as
ordinary gameplay. If a future change breaks replay, tests should catch that
as an engine contract problem rather than a UI bug.

This is why the milestone felt bigger than the amount of code.

M4 did not ship a visible feature, but it created the state boundary that
future visible features will depend on.

## Reviewing PR #33

After implementation, PR #33 became the next evaluation point for the
pull-request-review skill.

The PR title was:

```text
feat(engine): serialize and restore a bracket state (M4)
```

This mattered because the previous real review-skill run had produced a useful
review while also fabricating a spec citation. That failure mode needed to
stay in view. A review skill does not become trustworthy because one review
sounds plausible. It becomes more trustworthy when repeated cases show that it
stays grounded in the actual spec and diff.

On the spec axis, this review looked much stronger.

It correctly mapped the implementation back to the reviewed M4 spec. It
identified the expected spec scenarios. It described the three error codes:
`MALFORMED`, `UNSUPPORTED_VERSION`, and `INVALID_STATE`. It described
replay-based restore and canonical ordering. It also noted the `Error.cause`
decision without demanding a TypeScript target or lib change.

That is exactly the kind of review assistance I want from a draft skill.

Not "the tool approves this, therefore it is approved."

More like: "the tool can help organize the comparison between spec, diff, and
tests, then a human still verifies the claims."

That human verification point remained necessary because the review also made
code-level claims. It cited details such as `serialize.ts:99`, described
double-sorting behavior, and referenced commit structure.

Those claims might be correct. They might be useful. But they are not proven
just because the review text says them confidently.

The review appeared faithful on the spec axis. The code-level citations still
needed a human diff check.

That distinction is the whole point.

## Turning Review Behavior Into Evals

The review-skill work then moved from "what did this review say?" to "how do
we preserve what this case teaches?"

I drafted a new evaluation case:

```text
.claude/skills/reviewing-pull-requests/evals/cases/0002-faithful-findings-m4.md
```

The case captures PR #33 as a provisional positive example: faithful findings
against a reviewed spec, pending verification of code-level citations.

The important part is that the case is not merely "the review said LGTM."

That would be too shallow.

The real signal is that this review avoided the earlier failure mode. It did
not appear to invent a spec requirement. It aligned the review around the
actual M4 decisions: replay encoding, three error codes, no
`tryDeserializeBracket`, engine-level identity only, canonical ordering, and
no toolchain bump for `Error.cause`.

That makes it useful evidence.

Not final proof. Evidence.

The case should only graduate to a clean pass after the human diff check
confirms that the code-level details are real. Until then, it remains a
provisional positive case.

That is the posture I want for review tooling: evidence-building instead of
victory laps.

## The Empty PR Body Problem

PR #33 also exposed a separate governance issue.

The title was good. The body was not.

The actual PR body was effectively empty or malformed:

```text
@-
```

That would be a problem on its own, but the more interesting failure was how
the review process handled it.

The review-skill output synthesized its own "Description" from the diff. That
summary was useful as a reviewer aid, but it also masked the fact that the
actual PR description was missing.

Those are not the same thing.

A PR's stated description is part of the handoff artifact. It tells reviewers
what the author claims changed, why it changed, and how to evaluate it. A
reviewer's synthesized summary is a separate artifact. It can help orient the
review, but it should not quietly replace a missing PR body.

That led to another evaluation case draft:

```text
.claude/skills/reviewing-pull-requests/evals/cases/0003-empty-pr-body-masked.md
```

The lesson is direct: review tooling should distinguish between the PR's
actual stated description and the reviewer's synthesized description.

If the PR body is missing or malformed, the review should say so.

This is especially important for bot-authored PRs. The `neibaur-ai-bot-1`
setup correctly handled attribution and labels. PR #33 had the expected
`ai-assisted` label and bot attribution. That part of the governance path
worked.

But the malformed body showed that metadata still needs verification.

Bot identity and labels are not enough. The handoff has to be readable too.

## Governance Artifacts Are Products

The day kept circling back to the same idea: governance artifacts are not just
notes around the work. They are part of the product surface for future work.

The M4 spec was a product. It changed from draft questions into reviewed
decisions.

The serializer was a product. It created a canonical state boundary.

The PR review was a product. It produced structured claims that needed to be
checked.

The eval cases were products. They converted review behavior into testable
evidence.

The PR body was a product. Its malformed content created a handoff failure.

That framing may sound heavy for a small bracket-engine change, but it is
practical. Agent-assisted development creates more artifacts, faster. Specs,
diffs, review summaries, labels, branch names, PR bodies, generated evals, and
audit notes can all look polished even when some piece of them is wrong or
missing.

The answer is not to distrust everything forever.

The answer is to make trust incremental.

A reviewed spec earns more authority than a chat prompt. A passing validation
run earns more confidence than an untested patch. A review skill with evals
earns more confidence than a review skill with only a nice `SKILL.md`. A
bot-authored PR with correct labels and a real description earns more trust
than one with labels but a malformed body.

Trust should come from artifacts that survive checking.

## Why The Day Mattered

Day 53 mattered because M4 put a durable state boundary underneath future
features.

The bracket engine can now express its state as canonical JSON and rebuild it
through the same public rules that normal gameplay uses. That is the right
foundation for later share-hash and localStorage work.

But the day also mattered because the surrounding process became more
testable.

The spec moved to reviewed status. The implementation followed the spec
without widening the milestone. Validation passed. The review skill produced a
stronger spec-faithful review than the prior run. The eval suite gained a
provisional positive case and a new failure-mode case around empty PR bodies.

That is a useful pattern.

Code passes checks. Review output becomes evidence. Governance gaps become
eval cases. Bot metadata gets verified instead of assumed.

The human control point stays in the loop.

That is the part I want to keep repeating. The goal is not to make review
skills sound more authoritative. The goal is to make the whole system better
at showing what has actually been checked and what still needs human judgment.

## Outcome

Day 53 moved `haomiantiao` through the M4 serialize/restore milestone.

I started by finalizing the M4 spec, converting it from draft/open-question
mode into reviewed decision mode. The reviewed contract accepted the
replay/decisions encoding model, kept exactly three serialization error codes,
deferred `tryDeserializeBracket`, clarified the reachable-state boundary for
`serializeBracket`, treated forged in-memory states as out of contract, stored
only engine-level contestant `id` and `seed`, left rich noodle metadata to a
later layer, made interaction chronology intentionally non-serialized, and
avoided any TypeScript target or lib change for `Error.cause`.

The bot implementation on `feat/engine-serialize-restore` added a pure
serialize/restore pair for bracket state: `serializeBracket`,
`deserializeBracket`, `BracketSerializationError`,
`BracketSerializationErrorCode`, and `SERIALIZED_BRACKET_VERSION`. The
serialized form is canonical JSON with `{ v, contestants, picks }`.
Contestants are sorted by seed, picks are sorted by parsed
`(roundIndex, matchIndex)`, and restore rebuilds through `createBracketState`
before replaying decisions through `pickWinner`.

The implementation stayed test-first. The first commit added failing tests and
deliberately wrong stubs. The second commit implemented the behavior.
`pnpm validate` passed, coverage stayed above the project floor, and no
dependencies, storage behavior, URL behavior, base64 encoding, DOM access, or
app-layer metadata concerns were added.

I then reviewed PR #33,
`feat(engine): serialize and restore a bracket state (M4)`, and used it as a
second evaluation point for the draft PR-review skill. The review appeared
faithful on the spec axis, correctly describing the expected scenarios, three
error codes, replay-based restore, canonical ordering, and `Error.cause`
decision. I still treated code-level claims as needing human verification.

Finally, I drafted two review-skill eval cases. Case 0002 captures PR #33 as a
provisional positive example for faithful findings against a reviewed spec.
Case 0003 captures the empty or malformed PR body problem, where the actual PR
body was `@-` but the review output synthesized its own description and risked
masking the missing handoff artifact.

The day ended with M4 technically complete and the review/governance loop more
explicit about what it can and cannot prove.

## Definition Of Done

Day 53 reached a serialize/restore and review-evidence checkpoint:

- finalized the M4 serialize/restore spec
- moved the M4 spec from draft/open-question mode to `status: reviewed`
- accepted the replay/decisions encoding model
- kept exactly three serialization error codes: `MALFORMED`,
  `UNSUPPORTED_VERSION`, and `INVALID_STATE`
- deferred `tryDeserializeBracket`
- kept the M4 public API to `serializeBracket` and `deserializeBracket`
- clarified that `serializeBracket` is total only over reachable
  `BracketState` values created by `createBracketState` and advanced with
  `pickWinner`
- treated forged or hand-mutated in-memory states as out of contract
- serialized only engine-level contestant identity: `id` and `seed`
- left rich noodle metadata to the later data or app layer
- made interaction chronology intentionally non-serialized
- used canonical pick order by parsed `(roundIndex, matchIndex)`
- avoided any TypeScript target or lib change for `Error.cause`
- implemented M4 on the bot branch `feat/engine-serialize-restore`
- added `serializeBracket(state) => string`
- added `deserializeBracket(string) => BracketState`
- added `BracketSerializationError`
- added `BracketSerializationErrorCode`
- added `SERIALIZED_BRACKET_VERSION`
- used canonical JSON with top-level `{ v, contestants, picks }`
- sorted contestants by seed
- sorted picks by parsed `(roundIndex, matchIndex)`
- stored bracket inputs and decisions instead of the materialized round tree
- rebuilt restored state through `createBracketState`
- replayed restored decisions through `pickWinner`
- kept deserialization as the validated boundary
- followed a test-first implementation sequence
- added failing tests and deliberately wrong stubs before implementation
- passed `pnpm validate`
- kept coverage above the project floor
- avoided dependencies, storage, URL, base64, DOM, and app-layer concerns
- confirmed PR #33 had the expected `ai-assisted` label and bot attribution to
  `neibaur-ai-bot-1`
- reviewed PR #33,
  `feat(engine): serialize and restore a bracket state (M4)`
- observed that the PR-review skill correctly mapped the implementation back
  to the reviewed M4 spec
- treated the review as useful assistance rather than human-review discharge
- noted that code-level review claims still required human diff verification
- drafted eval case 0002 for faithful M4 findings against a reviewed spec
- kept eval case 0002 provisional until cited code details are verified
- discovered the malformed PR body value `@-`
- identified that the review-skill output masked the missing PR description by
  synthesizing its own description
- drafted eval case 0003 for the empty PR body masking failure mode
- reinforced that review tooling should distinguish between a PR's stated
  description and a reviewer-generated summary
- kept human review as the control point for code claims, PR metadata, and
  governance artifacts
