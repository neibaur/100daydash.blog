---
title: "Day 60 - June 30, 2026: Closing M7 by Reviewing the Review"
description: "A Day 60 reflection on closing HaoMiantiao M7 through persistence, fallback testing, accessibility cleanup, reviewer grounding, and milestone governance."
pubDate: "2026-06-30"
day: 60
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao M7 matchup-screen implementation notes"
  - "HaoMiantiao B2a and B2b handoff notes"
  - "HaoMiantiao PR #57 notes reported by Opus"
  - "Sonnet PR review notes reported by Opus"
  - "HaoMiantiao AGENTS.md and CLAUDE.md policy checks reported by Opus"
  - "HaoMiantiao M7 governance planning notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - haomiantiao
  - code-review
  - accessibility
  - persistence
  - evals
  - nextjs
  - validation
---

Day 60 was the day HaoMiantiao M7 closed by reviewing more than the code.

The visible milestone was the matchup screen becoming durable. The `/play`
experience could save bracket progress, survive a reload, fall back safely
when storage was missing or broken, and return a completed run to the champion
panel.

That is product progress.

But the more important lesson was smaller and stranger: the milestone did not
close just because the implementation landed.

It closed because the review loop itself was checked.

The day was about persistence, accessibility, validation, and acceptance
criteria. It was also about asking whether a review suggestion was actually
grounded in repository policy or only sounded policy-shaped.

That distinction mattered.

Agent-assisted development works best when reviewers are taken seriously. It
also works best when reviewers are not treated as oracles.

Day 60 was a useful reminder that governance is not obedience. Governance is
the habit of checking claims against the source of truth before turning them
into work.

## Letting The Split Be A Success

M7 B2 had already split into B2a and B2b.

That could have been framed as a failure. The original B2 slice had grown
large enough to hit the repository's change-size guardrail, so the agent
paused and asked for guidance instead of pushing through an oversized pull
request.

That is exactly what the guardrail is for.

A line-count cap is not useful because it makes every slice magically small.
It is useful because it forces a decision at the moment when a slice stops
being honestly reviewable.

The agent could have tried to squeeze more work into the PR. It could have
treated the cap as an inconvenience. Instead, the work narrowed.

B2a kept one part of the interaction path. B2b became the milestone-closing
persistence slice.

That made the split governance evidence, not process failure.

The next question was whether B2b should continue in the same Opus chat or
start fresh.

The decision was to start fresh.

B2b was cleanly bounded. It needed to cold-read the merged B2a state and the
current repository rather than carry forward assumptions from the earlier
combined B2 plan. That is one of the places where fresh context is not just a
convenience. It is a safety feature.

The repository had moved. The slice had narrowed. The next agent should
reason from that reality.

## What B2b Needed To Prove

B2b's job was focused but consequential.

It needed to make `/play` durable without making it magical.

The required behavior was straightforward:

- save bracket state to `localStorage` on each pick
- restore bracket state on mount
- use the existing M4 serialize and restore format
- treat missing, malformed, unsupported-version, or unreadable storage as
  safe fallback paths
- confirm that a completed run reloads into the champion completion panel
- avoid storage reads during render or initialization
- complete the cumulative M7 acceptance pass across B1, B2a, and B2b

That last point was important.

B2b was not just "add localStorage."

It was the slice that had to prove M7 as a whole. B1 gave the route and
display shell. B2a gave the interactive advance behavior. B2b had to preserve
that behavior across browser sessions and close the milestone against the
reviewed acceptance criteria.

The storage boundary also carried a hydration risk.

If the app reads storage during render, the static export and first client
render can diverge. That is the kind of bug that hides behind "it works on my
machine" until a static build, hydration, or browser environment exposes it.

So the rule stayed explicit: storage belongs in effects and handlers, not at
module scope, not during initialization, and not as part of the first render
contract.

The persistence feature was not allowed to weaken the app's static-export
discipline.

## Folding Accessibility Into The Right Slice

B2b also inherited a review warning from B2a.

There was a nested `aria-live` issue around the completion branch.

That could have been postponed as polish. It was not.

The reason was simple: B2b already reopened the completion branch. It was the
natural place to fix the accessibility structure because the persistence
slice had to prove a completed run could reload into the champion panel.

That is the good kind of scope expansion.

It was not a random cleanup. It was not "while I am here" formatting drift. It
was a review finding tied directly to the code path B2b needed to exercise.

The speculative `useCallback` suggestion from review was treated
differently.

That suggestion anticipated a future effect dependency problem that did not
yet exist. Turning it into code immediately would have added ceremony around
a future shape rather than fixing a present issue.

So one review note was required cleanup, and the other stayed out.

That is the judgment I want these loops to keep practicing. The question is
not "did a reviewer say something?" The question is "does this finding belong
to the current contract?"

For the live-region issue, yes.

For speculative memoization, no.

## The Reported Review Result

After B2b was implemented, Opus reported that Sonnet reviewed the PR and
effectively approved it.

The reported review findings were the right kind of boring:

- persistence and fallback paths were tested
- the nested live-region issue had been addressed
- `afterEach` localStorage hygiene was present
- the change stayed under the repository's line-count cap
- coverage remained above the required floor
- the cumulative M7 Gherkin pass mapped the milestone acceptance criteria

That is what a milestone-closing review should sound like.

It should not only say "the feature works." It should connect the
implementation back to the acceptance criteria, the fallback behavior, the
accessibility cleanup, the test hygiene, and the review-size constraint.

M7 did not close because `/play` could save state.

It closed because the stateful path had been walked deliberately.

The fallback cases mattered as much as the happy path. Missing storage should
not crash. Malformed storage should not crash. Unsupported serialized versions
should not crash. Unreadable storage should not crash.

A completed bracket also had to stay completed after reload.

That detail feels small until it is wrong.

If a user finishes a bracket, reloads, and lands back at the opening matchup,
the app has technically persisted something but failed the product experience.
Persistence is not just storing bytes. It is restoring the user's place in
the story.

For M7, that story ends at the champion panel.

## The Two Nits

The review left two non-blocking nits.

The first was straightforward: a redundant `window.localStorage.clear()` lived
in the per-file test setup even though shared `vitest.setup.ts` already
cleared storage in `afterEach`.

That was easy to accept.

The cleanup was non-behavioral, and removing it reduced duplicate test setup
without changing the actual isolation guarantee. Opus reported a small
follow-up commit:

```text
test(web): remove redundant storage cleanup
```

The change kept `vi.restoreAllMocks()`, which still belonged in the per-file
cleanup.

The second nit was more interesting.

A reviewer questioned whether multi-line JSDoc in `persistence.ts` violated a
supposed one-line comment or docstring rule.

That sounded plausible.

It also needed to be checked.

This is where the day sharpened.

Instead of blindly applying the review suggestion, the agent was asked to
verify the rule against canonical repository files.

Opus reported that no binding "one short line max" rule existed in
`CLAUDE.md` or `AGENTS.md`. The wording appeared inside PR-review skill eval
fixtures, not as repository policy. Existing source files such as
`advance.ts` and `serialize.ts` already used multi-line JSDoc with `@throws`.

So the `persistence.ts` JSDoc stayed.

That was the right outcome.

The lesson was not "ignore review comments about style."

The lesson was that style comments need a source of authority. If the
canonical repo policy says one thing, follow it. If existing code establishes
a local convention, respect it. If the only source is an eval fixture from a
different context, do not promote it into binding policy by accident.

A reviewer can be directionally helpful and still misattribute the rule.

The job is to verify.

## Reviewing The Reviewer

That JSDoc question turned the day from implementation wrap-up into
governance evidence.

It showed a useful failure mode for agent review loops.

Reviewers can blend sources.

A model may remember a principle from a skill fixture, a style preference, or
a previous repo and present it as if it is a local rule. The review can sound
confident because the idea is not absurd. Short comments often are better
than long comments. Over-documentation is real. Local style matters.

But "this might be too much comment" is not the same claim as "this violates
the repository's one-line docstring rule."

One is judgment.

The other is policy.

Policy needs a citation.

That was the most important part of Day 60 for me. Not the JSDoc itself. The
JSDoc was tiny. The important part was refusing to let a plausible review
claim become a fake rule.

The same review loop handled the accessibility warning differently because
that finding was grounded in the actual code path and belonged to the current
slice.

That contrast is the point.

When the reviewer is right, fold the finding in.

When the rule is not real, leave the code alone and record the lesson.

## The Reported Closeout

Opus reported the final PR as #57.

Because those PR details are from the implementation notes rather than this
repository, I am treating them as reported facts, not independently verified
repo history.

The reported validation set was:

```bash
pnpm validate
pnpm --filter @haomiantiao/web build
pnpm -r --if-present run build
```

Opus reported coverage remained around 97.55% statements and 94.19% branches.
It also reported the final changed-line count as 235 added and 9 deleted, for
244 total changed lines.

That matters because the line-count cap had already forced the B2 split. The
final B2b slice still needed to show it stayed reviewable after the follow-up
cleanup.

The conclusion was that no second full PR review was necessary after the tiny
non-behavioral storage cleanup.

That feels right.

Review has a cost. Re-reviewing a small removal of duplicate test cleanup can
look rigorous while mostly adding ritual. The better judgment was to
understand the nature of the change, preserve the original review evidence,
and merge through GitHub rather than pushing directly to main.

The next action was a human-owned merge of PR #57, not an agent shortcut.

## The Follow-Up Work Stays Separate

The later planning stayed disciplined.

There are two follow-up governance PRs, and they should not be collapsed into
the M7 implementation closeout.

One is a docs/project-state PR.

That should record M7 completion in `docs/PROJECT_STATE.md` and only update
`docs/DESIGN.md` if it is genuinely stale.

The other is a skill and eval-corpus PR.

That should capture useful review signals from the M7 run:

- the nested live-region catch
- the at-cap B2 split judgment
- the JSDoc-rule-versus-repo-precedent question as a reviewer-grounding
  lesson

Those are different governance concerns.

Project state tells the repository where the product is.

Skill evals teach the review harness how to behave next time.

Mixing them would make the work harder to review and easier to overclaim.

That separation is also what keeps M8 from starting with muddy context.

Before the next milestone begins, M7 needs to be recorded accurately and the
review lessons need to be captured in the right place. But neither one needs
to be smuggled into the implementation PR that closed the screen.

## Why The Day Mattered

Day 60 mattered because it made the matchup screen feel less temporary.

HaoMiantiao moved from a playable interaction to a durable one. A bracket can
survive reload. Broken storage can fail safely. A completed run can come back
to the champion panel. The completion UI had its accessibility issue cleaned
up where it naturally belonged.

That is a real product step.

But the bigger lesson was about review authority.

M7 did not close just because an agent implemented persistence. It closed
because the acceptance criteria were mapped, the fallback paths were tested,
the accessibility finding was handled, the slice stayed under review-size
limits, and the final nits were sorted by evidence.

The storage cleanup was accepted because it was clearly redundant.

The JSDoc change was rejected because the supposed rule was not actually a
repository rule.

That is the kind of review loop I want more of.

Not defensive. Not obedient. Grounded.

The reviewer is part of the system. The reviewer is not the system.

The system is the repository, the spec, the tests, the policy files, the
existing code, the validation results, and the human judgment that ties those
pieces together.

Today, that system held.

## Outcome

Day 60 closed the HaoMiantiao M7 matchup-screen milestone through the B2b
persistence slice and the final review loop around it.

M7 B2 had already split into B2a and B2b because the original slice reached
the repository's change-size guardrail. That split was treated as successful
governance behavior. The agent paused, asked for guidance, and narrowed the
work instead of forcing an oversized PR through review.

B2b started in a fresh Opus chat because it was a clean, well-bounded slice.
The fresh session could cold-read merged B2a state rather than carry stale
assumptions from the earlier combined B2 plan.

B2b focused on `/play` persistence: save bracket state to `localStorage` on
each pick, restore state on mount, use the M4 serialize and restore format,
fall back safely for missing or bad storage, reload a completed run into the
champion panel, and avoid storage reads during render or initialization.

The B2a nested `aria-live` warning was carried into B2b as required cleanup
because B2b reopened the completion branch. The speculative `useCallback`
suggestion was skipped because it anticipated a future effect problem that
did not exist yet.

Opus reported that Sonnet reviewed PR #57 and effectively approved it. The
reported review confirmed that persistence and fallback paths were tested,
the nested live-region issue was addressed, localStorage test hygiene was
present, the change stayed under the line-count cap, coverage remained above
the required floor, and the cumulative M7 Gherkin pass mapped the milestone
acceptance criteria.

Two non-blocking nits remained. The redundant per-file
`window.localStorage.clear()` was removed in a small follow-up commit reported
as `test(web): remove redundant storage cleanup`, while keeping
`vi.restoreAllMocks()`. The multi-line JSDoc in `persistence.ts` was left
unchanged after Opus reported that no binding one-line docstring rule existed
in `CLAUDE.md` or `AGENTS.md` and that existing source files already used
multi-line JSDoc with `@throws`.

Opus reported that `pnpm validate`, `pnpm --filter @haomiantiao/web build`,
and `pnpm -r --if-present run build` passed after the cleanup. It also
reported coverage around 97.55% statements and 94.19% branches, with a final
changed-line count of 235 added and 9 deleted.

No second full PR review was considered necessary after the tiny
non-behavioral cleanup. The next step was to merge PR #57 through GitHub, not
push directly to main.

The remaining governance work was deliberately split into two human-owned
follow-ups: a project-state docs PR to record M7 completion, and a separate
skill/eval-corpus PR to capture review lessons from the nested live-region
catch, the B2 split decision, and the JSDoc policy-grounding question.

## Definition Of Done

Day 60 reached the M7 closeout checkpoint:

- confirmed Day 60 follows Day 59 for June 30, 2026
- treated the B2a/B2b split as successful change-size governance
- kept B2b as a fresh Opus handoff
- grounded B2b in merged B2a state rather than stale combined-slice context
- scoped B2b to `/play` persistence
- saved bracket state to `localStorage` on each pick
- restored bracket state on mount
- used the existing M4 serialize and restore format
- treated missing storage as a safe fallback path
- treated malformed storage as a safe fallback path
- treated unsupported serialized versions as a safe fallback path
- treated unreadable storage as a safe fallback path
- avoided storage reads during render or initialization
- confirmed a completed run reloads to the champion panel
- completed the cumulative M7 acceptance pass across B1, B2a, and B2b
- carried the nested `aria-live` warning into B2b as required cleanup
- skipped speculative `useCallback` work that did not match a present issue
- used review evidence to confirm persistence and fallback test coverage
- used review evidence to confirm localStorage test hygiene
- used review evidence to confirm the line-count cap held
- used review evidence to confirm coverage remained above the required floor
- removed redundant per-file `window.localStorage.clear()` setup
- kept `vi.restoreAllMocks()` where it still belonged
- verified the JSDoc style warning against canonical repository policy
- found no binding one-line docstring rule in the reported policy check
- treated eval-fixture wording as non-binding for repo code style
- preserved multi-line JSDoc where it matched existing source precedent
- treated PR #57, validation results, coverage, and line count as Opus-reported
  facts rather than independently verified local repo history
- avoided a second full review for a tiny non-behavioral cleanup
- kept the merge path human-owned through GitHub
- planned a separate docs/project-state PR for M7 completion
- planned a separate skill/eval-corpus PR for review lessons
- kept M8 out of scope until M7 state and review evidence are recorded
