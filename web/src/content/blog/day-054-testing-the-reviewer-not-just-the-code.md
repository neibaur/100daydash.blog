---
title: "Day 54 - June 24, 2026: Testing the Reviewer, Not Just the Code"
description: "A Day 54 reflection on maturing a draft PR review skill through eval cases, fixture capture, citation discipline, and human-in-the-loop governance."
pubDate: "2026-06-24"
day: 54
dashboardSlug: "none"
dataSources:
  - "reviewing-pull-requests skill v0.2.0 notes"
  - "haomiantiao PR #33"
  - "haomiantiao PR #28"
  - "review-skill eval case notes"
  - "review-skill fixture and result notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - pull-requests
  - evals
  - specs
  - developer-experience
  - haomiantiao
---

Day 54 was about testing the reviewer.

Not the code reviewer as a person, exactly. The draft
`reviewing-pull-requests` skill.

That distinction matters because a review skill can sound useful very quickly.
It can summarize a diff. It can cite files. It can compare implementation
against a spec. It can give the reassuring shape of process.

But sounding like a reviewer is not the same as being ready to govern review.

Today's work stayed inside that uncomfortable gap. The skill was helpful. It
found real things. It organized real evidence. It also showed that a review can
be directionally useful and still unsafe to automate if it presents its claims
with more precision than the evidence supports.

That was the main lesson.

Governance work is not only writing better rules. It is building evidence that
the rules work, and then being honest about what the evidence does not prove
yet.

## A Real Finding With Bad Coordinates

The day started by looking more closely at PR #33, the M4 serialize/restore
work for `haomiantiao`.

The prior review-skill run had made a code-level observation about this cast:

```text
seed: entry.seed as number
```

The observation itself was legitimate. The cast existed, and it was worth a
human look. The problem was the citation.

The review pinned the issue to:

```text
serialize.ts:99
```

Manual verification showed that line 99 was unrelated error-handling code. The
cast was real, but it lived at line 119.

That made the failure more interesting than a clean hallucination.

The review had not invented the entire issue. It had found a real smell in the
code. But it attached fabricated precision to that smell by citing the wrong
line number.

That is a different category of review risk.

If a review invents a requirement, the failure is easier to name. If a review
finds a real issue but points reviewers to the wrong location, the output can
still feel trustworthy because the underlying concern is not fake. The danger
is subtler: the review artifact looks more checked than it actually is.

I recorded that as a new eval case:

```text
.claude/skills/reviewing-pull-requests/evals/cases/0004-inaccurate-citation.md
```

The case is not "the reviewer made everything up." It is sharper than that:
the reviewer identified a real code concern while overstating its citation
precision.

That is exactly the kind of behavior an eval suite should preserve.

## The Pattern Across Cases

The new case joined two other recent review-quality cases:

- `0002-faithful-findings-m4.md`
- `0003-empty-pr-body-masked.md`
- `0004-inaccurate-citation.md`

Together, they told a more useful story than any one case could.

Case 0002 captured the good version of the skill. Against PR #33, the review
was mostly faithful on substance and spec alignment. It recognized the M4
serialize/restore shape, the replay-based restore model, the expected error
codes, and the decision to keep the engine boundary narrow.

That matters. A review skill that cannot find faithful alignment is not very
useful.

Case 0003 exposed a different problem. The actual PR body for PR #33 was only
the placeholder:

```text
@-
```

The review output still produced a useful description, but it did not make the
missing PR body visible enough. It synthesized a summary from the diff and let
that summary occupy the space where the PR's stated description should have
been.

That is a handoff problem.

A synthesized reviewer summary can be useful. It should not quietly replace a
missing author description. The review should say, plainly, that the PR body is
empty, placeholder, or malformed.

Case 0004 then captured the citation problem: real finding, wrong line.

The pattern across all three cases was clear. The skill was often useful, but
it sometimes made its output look more complete, more sourced, or more precise
than the underlying evidence justified.

That is not a reason to delete the skill.

It is a reason not to promote it.

## Draft-Only Was The Right Answer

The important decision today was restraint.

The `reviewing-pull-requests` skill stayed draft-only.

That can sound like a non-result if the goal is to graduate every tool as fast
as possible. But that is not the goal. The goal is to make agent-assisted
review more trustworthy over time without accidentally giving a draft procedure
the authority of a proven control.

The evidence did not support promotion.

It supported improvement.

That difference is the whole governance posture I want here. A useful tool can
still need a harness. A helpful review can still need human verification. A
procedural skill can still be immature even if its outputs are better than
starting from a blank page.

Keeping the skill draft-only was not failure. It was the maturity decision the
evidence called for.

## Updating The Skill To v0.2.0

The skill moved to version 0.2.0.

The update focused on the failure modes that the cases had made visible.

First, it added a PR-body-presence criterion. The reviewer now has to check
whether the actual PR body is missing, empty, placeholder text, or malformed.
If it is, the review should flag that as a handoff issue instead of silently
filling the gap with generated prose.

Second, it added citation-discipline guidance. The skill should not cite exact
line numbers unless those line numbers have actually been verified. If exact
line verification is not available, the safer pattern is to cite by symbol,
function, file, or behavioral area.

That may sound less precise, but it is more honest.

A review that says "in `deserializeBracket`, around seed normalization" is
less tidy than a false line citation. It is also much less dangerous.

Third, the output format changed so synthesized summaries are labeled as
synthesized. That keeps the PR's stated description separate from the
reviewer's derived summary.

That distinction matters for bot-authored PRs especially. If the author did
not provide a usable description, the review should not launder the diff into
an apparently normal handoff artifact.

Fourth, the skill gained a reviewer-model line. Future review outputs should
document the best-effort model self-report while still recognizing that the
authoritative model identity belongs to the harness or invocation environment.

That is a small line, but it fits the larger theme. Review artifacts should say
what they know, how they know it, and where the authority actually comes from.

## Keeping Evals With The Skill

The eval structure also moved into the skill directory rather than living at
the repository root.

That gave the review procedure a more coherent home:

```text
.claude/skills/reviewing-pull-requests/evals/cases/
.claude/skills/reviewing-pull-requests/evals/fixtures/
.claude/skills/reviewing-pull-requests/evals/results/
```

That organization is not just tidiness.

The skill, its known cases, captured fixtures, and run results should travel
together. If the skill is copied, audited, promoted, or retired later, the
evidence trail should come with it.

The eval README was clarified around those roles:

- cases are labeled rubrics for known skill behaviors
- fixtures are captured review inputs
- results are outputs from running a specific skill version against fixtures

That separation is useful because each artifact answers a different question.

A case says what behavior matters. A fixture says what the reviewer was given.
A result says what a specific version did with that input.

Without that separation, it is too easy for evals to become vague notes. With
it, the behavior becomes replayable enough to reason about.

## Capturing Fixtures

Fixtures were captured for PR #33 and PR #28 using PR diffs and metadata JSON.

The PR #33 fixture preserved the original placeholder body:

```text
@-
```

That detail mattered. If a fixture normalizes away the messy input, it cannot
test the behavior that failed. The empty-body case only remains meaningful if
the captured input still contains the empty body.

This is one of the small, practical lessons of eval work: the fixture is part
of the truth.

If the fixture is too cleaned up, too current, or too reconstructed, it may no
longer test the original risk. It becomes a story about the failure instead of
an input that can reproduce it.

The PR #33 replay was the cleaner case.

A fresh Sonnet run of the v0.2.0 skill against PR #33 showed that the targeted
fixes worked. It flagged the `@-` body. It labeled its summary as synthesized.
It avoided the bad line-number citation. It preserved the useful spec-review
behavior that made the earlier review valuable in the first place.

That is the kind of result I want from eval-driven skill work.

Do not just add more warnings. Preserve the useful behavior while narrowing
the unsafe behavior.

## When Fixture Drift Changes The Meaning

The PR #28 replay was messier.

The run was useful, but it was not a faithful replay of case 0001.

The fixture had drifted from the original failure state. The spec and diff had
evolved after the original review. The old fabricated requirement had become
an actual documented requirement by the time this newer run happened.

That changes the meaning of the result.

If the original failure was "the review claimed the spec required something it
did not require," but the current fixture now includes that requirement, the
current fixture no longer tests the original failure. It tests something else.

I could have tried to reconstruct a historical fixture.

I decided not to do that today.

Instead, I treated the PR #28 run as useful current evidence, skipped a
faithful 0001 replay for now, and kept the skill draft-only. If the same kind
of fabrication recurs, it can be captured from a fresh, faithful input.

That restraint matters too.

Eval work can become fake certainty if the inputs are not honest. A replay
that is not actually replaying the old conditions should not be dressed up as
proof that the old issue is fixed.

## Useful Findings Still Need Judgment

The PR #28 run still surfaced real governance observations.

One was mechanical and concrete: the merged PR had 404 additions even though
the PR checklist reported 379. That means the 400-line cap had been exceeded
by 4 lines.

That finding pointed toward a future improvement. A mechanical CI line-count
gate would be more reliable than self-reported line counts in PR text.

That is exactly the kind of thing review assistance can help uncover. The
skill noticed a mismatch that is easy for a human to miss when reading a
large-enough PR.

But the same run also produced a questionable best-practice suggestion
involving a `shouldMaterialize` identifier.

Manual checking found that the exact name did not exist in the repository.
That left open whether the review was merely proposing a name for a refactor
or whether it had invented part of its premise.

That ambiguity is enough to keep the brakes on.

Again, the review was not useless. It found useful governance signal. It also
needed human interpretation before any claim could become authoritative.

That is the draft-only boundary in practice.

## Why Fabricated Precision Is Dangerous

The most useful phrase from today was fabricated precision.

It is different from inventing a whole issue.

Fabricated precision happens when an artifact gives a claim more exactness
than the evidence supports: a wrong line number, a too-confident source label,
an unlabeled synthesized summary, a model identity presented as authoritative
when it was only self-reported, or a replay result treated as historical proof
when the fixture has drifted.

That kind of mistake is dangerous because it can hide inside otherwise useful
work.

A fabricated issue makes you distrust the artifact quickly. A real issue with
bad coordinates can make you trust the artifact too much.

That is why citation discipline matters. It is why fixture capture matters. It
is why results need versioned context. It is why synthesized summaries need
labels. It is why the skill should stay draft-only until the evidence is much
better.

The point is not to make every review slower.

The point is to make review artifacts honest about their confidence.

## Human-In-The-Loop Governance

Today's work connected directly to the larger human-in-the-loop governance
model I have been building.

The review skill is allowed to help. It can structure the review. It can call
attention to missing PR metadata. It can compare the implementation against a
spec. It can point out likely risks. It can generate a synthesized summary
when the author did not provide one.

But it should not silently become the reviewer of record.

The human still owns the judgment call. The harness owns the authoritative
execution context. The fixture owns the captured input. The result owns what a
specific version produced. The case owns the behavior being evaluated.

That division of responsibility is the governance system.

The skill is one part of it, not the whole thing.

## Why The Day Mattered

Day 54 mattered because the review-skill work became more evidence-shaped.

The day began with something that looked almost like success: the PR review had
found a real code concern. Then manual verification exposed the overconfidence
inside that success. The issue existed, but the citation was wrong.

That changed the lesson.

The question was no longer "did the review help?" It did. The question was
"can this review artifact be trusted at the level of precision it presents?"
Not yet.

That led to a better skill version, a clearer eval structure, captured
fixtures, cleaner result roles, and a more honest promotion decision.

The day did not end with a trusted automated reviewer.

It ended with a better draft reviewer and a clearer understanding of what the
draft reviewer can and cannot be trusted to do.

That is progress.

## Outcome

Day 54 matured the draft `reviewing-pull-requests` skill through evals,
fixtures, and citation discipline rather than promotion.

I started by manually verifying a PR #33 review finding about
`seed: entry.seed as number`. The concern was real, but the review cited it at
`serialize.ts:99`, while the cast actually appeared at line 119. That made the
failure a case of fabricated precision rather than a fully invented issue.

I recorded that behavior as
`.claude/skills/reviewing-pull-requests/evals/cases/0004-inaccurate-citation.md`
and grouped it with the recent faithful-findings and empty-PR-body cases. Taken
together, the cases showed that the skill was useful but not yet safe to treat
as an authority.

The skill moved to version 0.2.0 with targeted fixes: a PR-body-presence
criterion, citation-discipline guidance, explicit labeling for synthesized
summaries, and a reviewer-model line for best-effort model self-reporting.

I kept the eval structure under the skill directory so cases, fixtures, and
results travel with the procedure they evaluate. The eval README now
distinguishes those roles: cases define known behaviors, fixtures preserve
review inputs, and results capture outputs from a specific skill version
against those inputs.

Fixtures were captured for PR #33 and PR #28. The PR #33 fixture preserved the
original `@-` placeholder body, which allowed a fresh Sonnet run of v0.2.0 to
show the targeted fixes working: the review flagged the missing PR body,
labeled its summary as synthesized, avoided the bad line-number citation, and
kept the faithful spec review behavior.

The PR #28 run was useful but not treated as a faithful replay of case 0001
because the fixture had drifted from the original failure state. The same run
still surfaced governance signal around a 404-addition PR exceeding a
self-reported 379-line checklist value, suggesting a future mechanical
line-count CI gate. It also produced a questionable suggestion around a
nonexistent `shouldMaterialize` identifier, reinforcing the need to keep the
skill draft-only and human-reviewed.

The day ended with the review skill improved, the eval harness clearer, and
the promotion decision more honest: useful, but still draft-only.

## Definition Of Done

Day 54 reached a PR-review-skill eval checkpoint:

- manually verified the PR #33 review finding around `seed: entry.seed as number`
- confirmed the cast was real but cited at the wrong line
- classified the issue as fabricated precision rather than a fully fabricated
  finding
- added eval case 0004 for inaccurate citation behavior
- grouped case 0004 with the faithful-findings and empty-PR-body cases
- recognized the pattern that useful review output can still overstate its
  evidence
- kept the `reviewing-pull-requests` skill draft-only
- updated the skill to version 0.2.0
- added PR-body-presence review criteria
- required empty, placeholder, malformed, or missing PR bodies to be flagged
- added citation-discipline guidance
- required exact line citations to be used only when verified
- allowed symbol, function, file, or behavior-area citations when exact lines
  are not verified
- labeled synthesized summaries as synthesized
- separated the PR's stated description from reviewer-generated summaries
- added a reviewer-model line for best-effort model self-reporting
- kept authoritative model identity with the harness or invocation context
- organized eval material under the skill directory
- clarified the roles of `cases/`, `fixtures/`, and `results/`
- captured PR #33 and PR #28 fixtures from diffs and metadata JSON
- preserved the PR #33 placeholder body value `@-` in the fixture
- ran the v0.2.0 skill against the PR #33 fixture
- confirmed the run flagged the placeholder body
- confirmed the run labeled its summary as synthesized
- confirmed the run avoided the bad line-number citation
- confirmed the run preserved useful spec-alignment behavior
- ran the v0.2.0 skill against the PR #28 fixture
- treated the PR #28 run as useful current evidence rather than a faithful
  replay of case 0001
- declined to overclaim a fixed historical failure from a drifted fixture
- observed the 404-addition versus 379-reported-line-count mismatch on PR #28
- identified a future mechanical CI line-count gate as more reliable than
  self-reported PR checklist values
- manually checked that `shouldMaterialize` did not exist in the repository
- kept questionable best-practice suggestions under human review
- reinforced human-in-the-loop governance for agent-assisted PR review
