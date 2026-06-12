---
title: "Day 39 - June 9, 2026: From UseThai Friction to Governed Product Priorities"
description: "Closing the current UseThai friction-testing loop, triaging a second fixture-backed evidence batch, cleaning project state, and narrowing the next app-tier decision."
pubDate: "2026-06-09"
day: 39
dashboardSlug: "none"
dataSources:
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "UseThai UX friction log"
  - "UseThai warrant reviews"
  - "Local fixture data"
  - "pnpm"
status: "published"
tags:
  - thai-dictionary
  - usethai
  - lingua-core
  - evidence-driven-ux
  - product-prioritization
  - architecture-governance
  - documentation
---

Day 39 closed the current `UseThai` friction-testing loop and turned the
remaining observations into governed product priorities.

The day began with another manual pass through the local development
application. The testing moved beyond whether a fixture-backed lookup
succeeded or failed and focused more directly on what the experience asks of a
learner: understanding romanization, interpreting narrow definitions,
recognizing the active lookup direction, recovering from errors, and knowing
what the application will do with an input before submitting it.

Those observations became a second formal evidence batch. A warrant review
then separated app-tier presentation opportunities from data-content gaps and
core-search capability questions.

The most important result was not an implementation authorization.

It was a clearer decision surface.

The shape of the day was:

```text
Test the local app -> record a second friction batch
-> review every observation under the evidence rules
-> separate app, data, and core concerns
-> merge the governed artifacts -> clean project state
-> choose the next authorization decision
```

No core search capability was authorized. The evidence remained
`FIXTURE`-based, and that boundary continued to determine what the project
could responsibly conclude.

## Expanding The Manual Friction Pass

The new testing pass used the current local `UseThai` development app from the
perspective of a learner working with the fixture-backed lookup surface.

Earlier friction work had already established that the app could reveal useful
product questions. Day 39 expanded the observation range beyond the immediate
happy path and basic lookup misses.

The pass examined friction involving:

- ambiguous romanization
- definitions that are too narrow to provide enough learner context
- missing usage context
- mismatch between the selected direction and the entered query
- offline and network failures
- browser Back behavior
- lookup state after refresh
- very long input
- the absence of as-you-type guidance

These observations matter because a dictionary experience is more than the
final lookup result.

A learner needs to understand which kind of input the app currently expects,
why a query did not work, whether a result contains enough context to use
safely, and whether normal browser actions preserve or discard their recent
work.

At the same time, observing friction does not identify the responsible system
layer automatically.

An ambiguous romanization may be a source-data problem. A missing example
sentence may simply reflect content the fixture does not contain. A
direction-mismatch message is an application presentation question.
Romanized-form lookup and autocomplete would represent broader search
capabilities.

The testing pass created evidence for review, not permission to collapse those
different concerns into one feature plan.

## Recording The Second Evidence Batch

The observations were added to the friction log as entries `F-0014` through
`F-0027`.

Each entry was deliberately recorded as `FIXTURE` evidence.

That label was not a minor metadata choice. The application was exercised
through real manual usage, but it was still operating against local fixture
data rather than an imported, representative dictionary dataset.

The distinction can be summarized as:

```text
The interaction evidence is real.
The underlying dictionary-data basis is still a fixture.
```

That means the evidence can support discussion about the current application
surface. It can show that a placeholder is unclear, an error is too technical,
or normal browser behavior feels surprising.

It cannot yet prove that core lookup needs a new search capability.

For example, a fixture-backed miss for a romanized query does not establish
how often real learners will expect romanized lookup across a realistic
dictionary. The absence of as-you-type guidance may be visible in the current
app, but fixture evidence alone does not justify deciding which suggestion or
search behavior belongs in core.

The governance rules preserved that boundary before the new observations
could become implementation momentum.

## Reviewing Every Observation Individually

After the friction entries were logged, Sonnet was used to generate a second
warrant-review artifact:

```text
docs/usethai/warrant-review-2026-06-09.md
```

The review triaged all 14 entries individually.

That individual treatment matters. A batch of friction observations can look
like a general argument that the dictionary needs "better search" or "more
context." Reviewing each item separately makes it possible to ask more useful
questions:

```text
Is this an application presentation problem?
Is this missing or insufficient data content?
Is this shaped like a core capability question?
What kind of evidence supports it?
What, if anything, can be authorized now?
```

The review mapped the entries to existing or new clusters and kept
product-facing application friction separate from data-content gaps and
core-search questions.

That separation prevented a familiar product-development failure mode:
responding to a broad feeling of friction with a broad implementation.

## Issuing No Core-Capability Warrant

The warrant review issued no core-capability warrant.

All entries were `FIXTURE`-based. Under the project's evidence rules, that
means they cannot authorize changes to durable core-search behavior.

Several observations were search-capability-shaped:

- lookup by romanized form
- as-you-type input guidance

Both are attractive learner-facing ideas. Romanized lookup could help users
who know how a word sounds but cannot write Thai script. As-you-type guidance
could help users understand available entries or expected query forms before
submission.

Their appeal does not remove the evidence requirement.

Both remain held pending clustered `REAL` evidence. The project needs a
representative dictionary dataset and stronger observations before deciding
whether these behaviors belong in core, how they should work, or what
contracts they would require.

The review therefore preserved the existing posture:

```text
No fixture-only observation becomes a core-capability warrant.
```

That is not a rejection of future search improvement. It is a refusal to
design durable search behavior around a tiny local data basis.

## Discounting Data-Content Gaps For Now

The review also discounted several content-shaped issues for the current
decision.

These included:

- richer definitions
- related words
- example sentences
- missing senses
- romanization scheme provenance

Each may become important to the learner experience. None can be resolved
honestly through application presentation when the underlying data is absent
or incomplete.

The app cannot display a missing sense that its fixture does not contain. It
cannot invent reliable related words or usage examples. It should not imply a
romanization scheme provenance that has not been established in the data.

This clarified another boundary:

```text
Product friction can reveal a data-content need without authorizing the app
to manufacture the missing content.
```

The observations remain useful. They identify questions that real-data
evaluation and future ingestion work will need to revisit. They simply do not
belong in the immediate application implementation queue.

## Identifying App-Tier Candidates Without Authorizing Them

The second review identified six app-tier presentation candidates:

- direction-aware placeholder text
- direction-mismatch helper copy
- user-facing offline or network error messages
- user-facing excessive-input or HTTP 431 messaging
- browser Back lookup-history behavior
- refresh-state persistence through URL or query state

These candidates differ from the held core-search questions because they can
be reasoned about at the application boundary.

They concern what the current app communicates, how it responds to browser
navigation, and how it presents existing system behavior. They do not require
a new lexical-search contract merely to be discussed.

Even so, the review did not authorize them.

Candidate identification and implementation authorization are separate
decisions. Preserving that separation keeps the project from turning a review
artifact into an implicit backlog commitment.

The six candidates also vary significantly in complexity.

Direction-aware placeholder text and lightweight direction-mismatch helper
copy are narrow presentation changes. They could make the expected input
clearer without changing lookup behavior.

User-facing network and excessive-input messages require careful mapping from
system failures to learner-friendly copy. Browser Back behavior and refresh
state persistence involve a broader URL, query-state, and navigation design.

The review created a prioritized decision surface without pretending that all
six items are equally ready or equally small.

## Merging The Evidence And Review

Once the second evidence batch and warrant review were complete, they moved
through the appropriate documentation pull-request flow and merged to `main`.

That made the friction observations and their governance interpretation part
of the shared project record.

The merge mattered because evidence that exists only in a testing session or
chat is difficult to review and easy to reinterpret later. The governed
artifacts now preserve:

- what was observed
- which evidence basis supported the observation
- how each entry was categorized
- which concerns were discounted
- which candidates were identified
- which capabilities remain held
- why no core warrant was issued

The project can now make its next decision from a durable record rather than
from memory.

## Making Session State Current

After the review merged, the project-state documentation needed to catch up.

`SESSION_STATE.md` was updated to reflect that:

- the second friction triage had completed
- the evidence remained `FIXTURE`-only
- no core work was authorized
- the next operator decision is to authorize one app-tier candidate or hold

The friction log's warrant-review section was also updated so it referenced
both the first and second triage artifacts.

This cleanup narrowed the handoff.

The next session no longer needs to ask whether more friction testing is
required before the current batch can be understood. It no longer needs to
generate another review for evidence that has already been reviewed.

The current decision is now explicit:

```text
Authorize one small app-tier candidate, or hold.
```

Keeping session state current is part of the engineering work in an
agent-assisted project. A stale handoff can cause a future session to repeat
completed work, treat a candidate as authorized, or reopen a core question
that the evidence rules already held.

## Repairing The Investigation Log Structure

A later documentation-structure issue surfaced during the cleanup.

The session-state checklist referenced an `Investigation Log`, but
`SESSION_STATE.md` did not actually contain a matching section.

Investigation-style entries were instead sitting inside the volatile Per-PR
Update Block, including:

- the tone-generation spike
- the tone-validation pilot protocol
- the UX friction evidence log

Those entries were useful durable context, but their location made the
document's structure disagree with its own checklist.

The inconsistency was corrected before it could become a larger documentation
problem.

A proper `Investigation Log` section was added. The existing investigation
bullets were relocated without changing their meaning. The Per-PR preamble was
updated, and a malformed Application-tier evidence bullet was fixed.

This was a tidy-desk documentation correction.

It did not change source behavior, authorize an application slice, modify
core, or alter the conclusions of the friction reviews. It made the project
record easier to use and less likely to mislead the next session.

## Narrowing The Next Product Decision

By the end of Day 39, the next development decision had become substantially
smaller.

It is no longer:

```text
Keep testing friction.
Write another warrant review.
Start improving search.
```

It is:

```text
Which app-tier candidate, if any, should be authorized first?
```

The most realistic next slice appears to be direction-input guidance:

- make the search placeholder direction-aware
- possibly add lightweight wrong-direction helper copy

This candidate is narrow enough to improve the current learner experience
without changing core lookup contracts or pretending that fixture evidence
supports a new search capability.

It also follows naturally from the current app behavior. The selected lookup
direction already affects the page heading and document title. Making the
input guidance reflect that same direction could reduce uncertainty at the
point where a learner decides what to type.

That direction remains a candidate, not an authorization.

More complex app-tier work can follow as later slices if separately reviewed
and authorized:

- URL or query-state persistence
- browser Back history behavior
- user-facing network error messages
- user-facing excessive-input messages

Core-search ideas such as romanized lookup and autocomplete remain held until
`REAL` data exists and produces stronger clustered evidence.

## Why The Day Mattered

Day 39 moved the project from raw UX exploration into governed product
prioritization.

The friction-testing loop is now complete enough to support a focused next
decision. Observations were recorded, evidence bases were labeled, every entry
was reviewed, app candidates were separated from data and core concerns, and
the results were merged into the durable project record.

The restraint was as important as the findings.

The current fixture can reveal real application friction, but it cannot answer
every dictionary-product question. Treating fixture-backed observations as
production evidence would create false confidence. Treating every learner
friction point as a core-search request would create premature architecture.

Instead, the project used governance to ask what the evidence can support now.

The answer is not a new search system.

The answer is a short list of application presentation candidates, a clearer
handoff, and a likely first slice around direction-aware input guidance.

## Outcome

Day 39 closed the current `UseThai` friction exploration loop and converted it
into a governed prioritization checkpoint.

A second manual testing pass expanded the evidence beyond simple lookup
success and failure. Entries `F-0014` through `F-0027` captured learner-facing
friction involving romanization, content depth, direction mismatch, errors,
browser navigation, refresh behavior, long input, and the absence of
as-you-type guidance.

The evidence remained explicitly `FIXTURE`-based. The second warrant review
triaged all 14 entries, issued no core-capability warrant, discounted
data-content gaps that the app cannot resolve, held romanized lookup and
as-you-type guidance pending `REAL` evidence, and identified six app-tier
presentation candidates without authorizing them.

The evidence and review merged through the documentation flow. Session state
was updated to reflect the completed triage and the next operator decision.
The missing Investigation Log structure was repaired so durable investigation
context no longer lived inside the volatile Per-PR block.

The next likely implementation decision is a small direction-input guidance
slice. Larger navigation, persistence, and error-message improvements remain
later app-tier candidates. Core-search expansion remains held.

No core work, search capability, real-data ingestion, or application
implementation was authorized or completed.

## Definition Of Done

Day 39 reached a friction-triage and product-prioritization checkpoint:

- completed a second manual friction pass against the local `UseThai` app
- expanded testing beyond lookup success and failure
- observed romanization ambiguity and narrow-definition friction
- observed missing usage-context and direction-mismatch friction
- observed offline, network, browser Back, refresh-state, and long-input
  behavior
- observed the absence of as-you-type guidance
- recorded entries `F-0014` through `F-0027`
- labeled all new observations as `FIXTURE` evidence
- preserved the distinction between real app usage and fixture-backed data
- created the second warrant-review artifact
- triaged all 14 entries individually
- separated app-tier presentation, data-content, and core-search concerns
- issued no core-capability warrant
- discounted data-content gaps the application cannot resolve
- held romanized-form lookup pending clustered `REAL` evidence
- held as-you-type guidance pending clustered `REAL` evidence
- identified six app-tier presentation candidates
- authorized none of the six candidates
- merged the friction evidence and warrant review through the docs flow
- updated session state after the completed triage
- updated the friction log to reference both warrant reviews
- made the next operator decision explicit
- added the missing Investigation Log section
- relocated existing investigation bullets without changing their meaning
- updated the Per-PR preamble
- fixed the malformed Application-tier evidence bullet
- kept the documentation cleanup separate from source and app behavior
- identified direction-aware input guidance as the most realistic next
  app-tier candidate
- kept URL-state, browser-history, and error-message work as later candidates
- kept core-search expansion held until stronger `REAL` evidence exists
- implemented no core change, search capability, ingestion path, or app slice

The day closed with the evidence loop complete, the project record current,
and the next implementation decision narrow enough to make deliberately.
