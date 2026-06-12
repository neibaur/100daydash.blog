---
title: "Day 38 - June 8, 2026: Governance Before Motion"
description: "Turning Thai tone support into an auditable validation path, grounding derived linguistic artifact provenance, cleaning project state, and reassessing UseThai friction readiness."
pubDate: "2026-06-08"
day: 38
dashboardSlug: "none"
dataSources:
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "ADR-0017"
  - "tltk documentation"
  - "Human-annotated validation planning"
  - "pnpm"
status: "published"
tags:
  - thai-dictionary
  - usethai
  - lingua-core
  - architecture-governance
  - validation
  - pronunciation
  - tone-support
---

Day 38 was a governance-before-motion day.

The product desire is easy to state: `UseThai` should eventually provide
tone-aware pronunciation information that helps learners understand how a Thai
word should sound.

The engineering responsibility behind that desire is more demanding. Tone data
cannot simply appear beside a dictionary entry. If it is generated, the
platform needs to know which generator produced it, which version was used,
which headword it came from, how its quality was evaluated, and what remains
unresolved.

The shape of the day was:

```text
Confirm tone as a product requirement -> govern generated-data lineage
-> record provisional product rulings -> persist a validation protocol
-> clean project state -> reassess whether UseThai can gather useful friction
```

No tone-generation pipeline was implemented. No generated tone data was
ingested. No API integration, production dictionary expansion, Phase 16 work,
or Phase 17 work was authorized.

Instead, the day made the future path more auditable before making it visible.

## Starting With The Product Requirement

Day 37 established that tone-aware pronunciation is not merely a decorative
enhancement for `UseThai`.

For a learner, romanization without tone can leave out one of the most
important parts of pronunciation. That makes tone support a real product
requirement.

The first temptation would be to move directly from requirement to
implementation:

```text
Find a generator -> produce tone values -> display them in the app
```

That path would create visible progress quickly, but it would also create
unanswered questions inside the data model.

What produced the value? Which generator version was used? Can the result be
reproduced? Did the generator receive the exact source headword or a transformed
input? What happens when a future generator produces a different result? How
was accuracy evaluated before the value reached the product?

The better first step was to make those questions architectural rather than
incidental.

## Grounding Derived Linguistic Artifact Provenance

The first major outcome was a narrow architectural concept:

```text
derived linguistic artifact provenance
```

This concept describes the lineage of linguistic values that are generated or
precomputed rather than copied directly from a dictionary source.

The grounded use case is intentionally limited to machine-generated
pronunciation and tone surfaces. The required lineage includes:

- generator identity
- generator version
- input headword lineage

The decision also established an important runtime boundary:

```text
Generated tone must be precomputed offline and stored as static data.
Generated tone must not be inferred at runtime.
```

That distinction supports reproducibility and review. A stored result can be
versioned, compared, validated, and replaced through a governed process.
Runtime inference would make dictionary behavior depend on an opaque operation
performed during a user request.

The concept was documented in `ARCHITECTURE.md` and accepted through
`ADR-0017: Derived Linguistic Artifact Provenance`.

The scope stayed narrow. Derived linguistic artifact provenance does not
replace source provenance, and it does not overload the existing
`generatedFrom` artifact-classification marker. Human-curated override and
exception-table provenance also remains deferred.

This was architecture work in service of a future product feature, not the
feature itself.

## Separating Provenance Concepts

One of the day's most useful clarifications was that nearby provenance concepts
should not be collapsed into one field merely because they all describe where
something came from.

`DictionarySourceProvenance` describes source-shaped lineage. It can explain
which dictionary or dataset supplied a record.

A `generatedFrom` marker classifies an internal artifact relationship.

Derived linguistic artifact provenance answers a different question:

```text
Which governed generator, at which version, transformed which input headword
into this stored linguistic value?
```

Keeping those concepts separate prevents a future tone value from looking like
source-authored dictionary data. It also prevents a general artifact marker
from being asked to carry generator identity and reproducibility details it was
not designed to represent.

The architecture now has a name for the responsibility without pretending that
the final storage shape is already authorized.

## Recording Provisional Tone Product Rulings

After the provenance concept was grounded, the next work recorded provisional
product rulings for a future tone-generation path.

The current direction is:

- tone remains a real `UseThai` product requirement
- runtime tone inference remains out
- generated-and-stored offline tone is the intended direction, subject to
  validation and governance
- `tltk` 1.10 G2P is the provisional baseline generator
- IPA with tone digits is the current evaluation and storage-notation
  candidate
- validation should use a human-annotated gold set
- whole-word exact match should be the future product-quality gate
- per-syllable tone accuracy should remain diagnostic-only

These are provisional rulings, not implementation authorization.

The posture is:

```text
baseline, then validate
```

It is not:

```text
ship because a generator exists
```

No dependency was added. No generator was integrated. No validation run was
performed. No generated pronunciation records, provenance schema, override
table, or precompute pipeline was created.

Recording those boundaries is what keeps an exploratory direction from quietly
becoming a production commitment.

## Designing A Human-Only Validation Path

The next question was how to learn whether the provisional baseline is good
enough.

The validation approach keeps ground truth human-only. A licensed
pronunciation-dictionary comparison path remains closed for this track.

That decision avoids turning a quality test into an unclear licensing
dependency. It also makes the evaluation question more direct: how closely
does the generated learner-facing pronunciation match carefully annotated
human judgments?

The planning work selected a composite future quality structure:

- an overall whole-word exact-match gate
- an independent floor for irregular or failure-prone items
- per-syllable tone accuracy as diagnostic context only
- segmentation divergence as a first-class finding

Whole-word exact match matters because a learner sees and relies on the whole
pronunciation surface. A generator that is usually correct at the syllable
level but frequently produces one wrong syllable may still create a poor
product experience.

At the same time, an overall score can hide weaknesses concentrated in
difficult categories. The independent irregular-stratum floor is intended to
make those weaknesses visible.

No numeric acceptance threshold was set. Thresholds should follow pilot
evidence rather than be invented before the project understands the error
distribution.

## Persisting The Pilot Protocol Without Running It

The most concrete planning artifact was:

```text
docs/validation/tone-validation-pilot-protocol.md
```

The protocol records how a future pilot should be performed without authorizing
the pilot itself.

The planned pilot target is 240 items. Approximately 70 to 75 percent of the
sample should come from irregular or failure-prone categories, with the
remaining 25 to 30 percent providing a regular contrast stratum.

The six planned irregular or failure categories are:

- loanwords
- proper nouns
- ambiguous or irregular spellings
- compounds
- implicit or unwritten vowels
- leading-consonant or false-cluster cases

Items should use a primary stratum label with lightweight overlap flags. A
subset should be double-annotated, prioritizing difficult categories, and a
single independent adjudicator should resolve disagreements under a written
segmentation-versus-tone rule.

The `tltk` comparison would use `th2ipa` IPA-with-tone-digit output. Syllable
separators would be normalized out for whole-word exact match. Per-syllable
tone accuracy would only be calculated where segmentation agrees.

The protocol also preserves a deliberate decision boundary around machine
learning alternatives. ML comparison remains deferred unless the pilot shows
that `tltk` is clearly weak and a candidate can satisfy runnable-environment,
determinism-at-pin, and model-version-pinning requirements.

The pilot remains calibration-only and unauthorized. Persisting a protocol is
not the same as executing it.

## Keeping Local Spike Work Out Of Validation

The day also resolved a small but practical validation problem.

The repository uses `.spike-local/` for throwaway local spike artifacts. Git
already ignored that directory, but ESLint did not. A local virtual environment
under `.spike-local/venv/` could therefore cause lint to inspect third-party
files and fail for reasons unrelated to the repository's authored source.

The ESLint ignore block was aligned with the existing Git ignore behavior by
excluding:

```text
.spike-local/**
```

A temporary lint probe confirmed the exclusion worked, and the probe was
removed before the tooling change was committed.

This was a small cleanup, but it protects the quality signal. Validation should
report problems in the project, not in disposable local spike dependencies.

## Making Session State Operative Again

The governance work created another kind of friction: the `Next action` field
in `.claude/SESSION_STATE.md` had grown too large to function as a next action.

It was carrying the actual next step alongside durable tone rulings,
derived-provenance history, validation methodology, prior spike context,
fixture triage, deferred scope, and future authorization gates.

A docs-only cleanup reduced that field to an operative statement:

- pilot execution remains unauthorized
- continue gathering real `UseThai` lookup friction
- Phase 16 and Phase 17 remain pending authorization
- the required HANDOFF section 9 audit must happen before either phase
- derived-provenance-shape assessment remains gated on future tone-validation
  whole-word exact-match results

The durable context was preserved in the appropriate completed and deferred
sections. The immediate next action became readable again.

This kind of cleanup is easy to dismiss because it does not change product
behavior. In an agent-assisted project, however, session state is part of the
operating system. A bloated next action increases the chance that a future
session confuses historical context with present authorization.

## Returning To UseThai Friction Readiness

With the governance path clearer, the day returned to the current safe product
lane: gathering `UseThai` lookup friction.

That lane has a real limitation.

The application currently has a very small seed bank and no API integrations.
It can support constrained testing of:

- direction switching
- page heading and document title behavior
- empty-input behavior
- Thai-to-English whitespace rejection
- English-to-Thai whole-phrase lookup for known fixture entries
- no-result messaging
- diagnostic rendering
- raw-query echo
- the general clarity of the lookup shell

It cannot yet support strong conclusions about:

- broad dictionary coverage
- realistic search expectations
- prefix, substring, or fuzzy behavior
- whether a miss comes from UX, exact-key behavior, or missing data
- learner-facing completeness across tone, romanization, examples, parts of
  speech, and multiple senses
- Thai-English dictionary behavior at production scale

That changes the meaning of the next action.

The next friction pass should not pretend to be full dictionary-product
testing. It should be a constrained pass against the current tiny seed set,
with a second question running alongside it:

```text
Can the current fixture coverage produce useful evidence, or is the evidence
pipeline itself blocked by insufficient realistic lookup coverage?
```

That is friction-readiness work. It helps determine whether the application can
keep learning from its current data or whether a small, governed app-tier
demo-data strategy needs to be considered before deeper UX conclusions are
possible.

## Why The Day Mattered

Day 38 did not produce a flashy feature.

It produced a trustworthy path toward one.

Tone support moved from a valid product desire into a set of governed
questions:

```text
What generated this value?
Which version generated it?
Which input did it derive from?
How will humans evaluate it?
What product-quality measure matters?
Which difficult categories need independent scrutiny?
What evidence must exist before implementation is authorized?
```

ADR-0017 gave generated linguistic data an architectural lineage concept. The
provisional product rulings established a baseline-and-validate posture. The
pilot protocol made the future evaluation reproducible without pretending that
it had already been run.

Project-state cleanup kept those decisions from obscuring the actual next
action. The return to `UseThai` friction testing then exposed a practical
truth: evidence gathering is possible, but the current seed data limits what
the evidence can prove.

The work made future motion safer because it made today's boundaries clearer.

## Outcome

Day 38 turned tone support from a vague future feature into an auditable,
governed path.

Derived linguistic artifact provenance was grounded through architecture
documentation and `ADR-0017`, with generator identity, generator version, and
input headword lineage established as the minimum conceptual requirements.
Generated tone remains an offline, stored-data concern rather than a runtime
inference behavior.

Provisional product rulings recorded `tltk` 1.10 as the baseline generator
candidate, IPA with tone digits as the current notation candidate, a
human-annotated gold set as the validation source, and whole-word exact match
as the future product-quality gate.

The tone-validation pilot protocol persisted an exploratory 240-item
methodology with irregular-category emphasis, regular contrast, subset
double-annotation, independent adjudication, segmentation-divergence reporting,
and explicit ML-comparison gates.

Local spike workspace hygiene improved the reliability of lint validation.
Session-state cleanup made the immediate next action operative again.

The day ended back at the `UseThai` app tier, with a clearer understanding that
friction testing can continue but must remain honest about the limitations of
the current tiny seed set.

No tone generation, validation execution, generated data, ingestion, API
integration, production dictionary expansion, Phase 16 work, or Phase 17 work
was implemented.

## Definition Of Done

Day 38 reached a tone-governance and friction-readiness checkpoint:

- confirmed tone-aware pronunciation as a real `UseThai` product requirement
- kept runtime tone inference out of scope
- grounded derived linguistic artifact provenance
- accepted `ADR-0017`
- established generator identity, generator version, and input headword
  lineage as the required provenance concept
- kept source provenance, artifact classification, and derived linguistic
  artifact provenance separate
- kept human-curated override and exception-table provenance deferred
- recorded `tltk` 1.10 G2P as the provisional baseline generator
- recorded IPA with tone digits as the current evaluation and storage-notation
  candidate
- selected a human-annotated gold-set path
- kept licensed-reference dictionary comparison closed for this track
- selected whole-word exact match as the future product-quality gate
- kept per-syllable tone accuracy diagnostic-only
- selected a composite future quality structure with an irregular-stratum
  floor
- deferred numeric thresholds until after pilot evidence
- persisted the tone-validation pilot protocol
- planned a 240-item calibration-only pilot
- emphasized irregular and failure-prone categories in the planned sample
- included a regular contrast stratum
- established subset double-annotation and independent adjudication
- made segmentation divergence a first-class planned finding
- kept ML comparison gated and deferred
- kept pilot execution unauthorized
- aligned ESLint with the local spike workspace ignore policy
- reduced the session-state next action to an operative statement
- kept Phase 16 and Phase 17 pending authorization
- returned to constrained `UseThai` friction gathering
- identified the current tiny seed bank as a limit on realistic friction
  evidence
- reframed the next product question around friction readiness
- implemented no tone pipeline, generated tone data, ingestion, API
  integration, or production dictionary expansion

The day closed with fewer visible features and substantially better footing for
the feature work that may eventually follow.
