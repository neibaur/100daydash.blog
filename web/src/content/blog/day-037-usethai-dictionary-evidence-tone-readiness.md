---
title: "Day 37 - June 7, 2026: Turning Thai Dictionary Friction into Product and Data Decisions"
description: "Using manual UseThai testing to separate app-tier UX improvements from core search work, assess Volubilis ingestion readiness, and establish tone as a governed product requirement."
pubDate: "2026-06-07"
day: 37
dashboardSlug: "none"
dataSources:
  - "Astro"
  - "TypeScript"
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "Volubilis Thai-English dictionary data"
  - "pnpm"
status: "published"
tags:
  - application-development
  - evidence-driven-ux
  - thai-dictionary
  - data-ingestion
  - data-licensing
  - pronunciation
  - architecture-governance
---

Day 37 moved `UseThai` from showing lookup screens to producing evidence that
can guide real product and data decisions.

Manual testing exposed concrete learner friction. The first UX friction review
separated app-tier improvements from fixture limitations and unwarranted core
search work. A real-data spike turned Volubilis from a vague candidate into a
dataset with measurable ingestion challenges. Tone also moved from a possible
enhancement into a product requirement that needs a governed technical path.

The shape of the day was:

```text
Test the app -> record friction -> authorize only the narrow app-tier fix
-> inspect real dictionary data -> define tone and licensing gates
-> prepare the next governance decision
```

The most important result was discipline. The application is now useful enough
to reveal meaningful friction, but observed friction does not automatically
authorize a new core capability.

## Turning Manual Lookup Tests Into Evidence

The day began with manual testing through:

```text
pnpm --filter usethai dev
```

The tests confirmed several important lookup states:

- Thai-to-English lookup for `กิน` returned the Thai headword, romanization,
  and English definition.
- English-to-Thai lookup for `old` returned two Thai entries: `เก่า` and `แก่`.
- English-to-Thai lookup for `to eat!` returned no exact match because the
  current lookup remains punctuation-sensitive.

These results showed both product progress and useful friction.

The successful `กิน` lookup demonstrated the working happy path. The `old`
results showed that returning multiple valid entries is not enough when a
learner cannot easily distinguish between them. The `to eat!` miss showed how
an exact-key rule that is technically predictable can still surprise a user.

The app is no longer only an abstract shell. It can now surface specific
dictionary behavior that can be observed, discussed, and triaged.

## Building The First Meaningful UX Friction Batch

The manual tests fed the first substantial batch of observations into the UX
friction log.

The evidence covered both lookup directions:

- English query-form mismatches such as `eat`, `eating`, or
  punctuation-attached forms when a fixture contains only `to eat`
- Thai query-form mismatches involving phrases, sentences, whitespace, or
  punctuation-attached words
- present-but-hard-to-use results such as `old` returning both `เก่า` and `แก่`
  without enough disambiguating context
- romanization without tone information
- common words missing from the small seed fixture

The categories matter because these observations do not all describe the same
problem.

A missing fixture entry is not evidence that lookup needs fuzzy matching. Two
valid results with insufficient learner context are not a tokenizer defect. A
punctuation-attached query miss may reveal product friction without proving
which layer should eventually address it.

The friction log keeps those distinctions visible.

## Issuing No Core Search Warrant

The warrant review produced an important non-decision:

```text
No core search warrant was issued.
```

The evidence remained fixture-based. That was not enough to authorize fuzzy
search, stemming, punctuation normalization, tokenizer expansion, or a wider
search architecture.

This restraint protects the platform from converting every observed app
friction into durable core behavior. Before search capability expands, the
project needs stronger evidence from real data and repeated learner behavior.

The review did identify one narrow issue that was clearly actionable at the
application tier: the page chrome should communicate the selected lookup
direction.

## Completing Direction-Aware App Chrome

The document title and on-page heading now react to the selected lookup
direction.

That resolves the earlier mismatch where the page chrome did not clearly
reflect whether the user was performing Thai-to-English or English-to-Thai
lookup.

The implementation stayed deliberately within the application tier:

- no core behavior changed
- no lookup behavior changed
- the direction-aware chrome works in the neutral awaiting-input state
- the application continues consuming core through the public lexical barrel
- the multi-entry `old` result was confirmed as a data-content issue rather
  than a dropped-field rendering defect

This closed the first immediately actionable issue from the fixture friction
batch without promoting presentation behavior into core.

## Moving From Fixture UX To Real-Data Readiness

The day then shifted from app behavior to the data that could eventually power
it.

Earlier research had characterized Volubilis as a weak or mostly Thai-French
candidate. Project-specific review and a direct data-shape spike showed that
conclusion was unreliable.

The spike inspected `VOLUBILIS Database.xlsx` version 25.3 from November 2025.
The file contains 114,177 rows across 15 columns.

Several findings make Volubilis a serious Thai-English candidate:

- Thai headwords, romanization, and POS or type fields are broadly populated.
- English glosses are present for roughly 93% of rows.
- The data contains more than 102,000 distinct Thai headwords.
- About 8,591 Thai headwords appear in multiple rows.
- Roughly 7.5% of Thai headwords contain whitespace.
- English gloss cells often contain multiple semicolon-separated senses.
- POS or type data uses 73 tags, far more than the current core POS enum.
- Some enrichment fields are too sparse to assume they belong in an initial
  ingestion path.

These findings replaced a vague data-source question with bounded engineering
questions.

Duplicate headwords will need a merge policy. Whitespace-bearing headwords
conflict with the current Thai lexical-key policy. Multi-sense gloss cells
need explicit parsing rules. The source POS vocabulary needs a governed
mapping rather than being forced into the smaller core enum.

Volubilis is not drop-in ready, but it is realistic enough to keep evaluating.

## Making Tone A Product Requirement

The day's most important learner-facing decision was that tone should be
treated as required for `UseThai`.

Romanization without tone is significantly less useful to a non-native Thai
learner. A learner may be able to approximate consonants and vowels from a
romanized form while still missing the tone that determines how the word
should actually be pronounced.

Visual tone information can support pronunciation learning now and create a
stronger foundation for future pronunciation or text-to-speech features.

The feasibility review clarified a likely technical direction:

- runtime tone inference should remain out of scope
- tone-marked pronunciation should likely be generated offline and stored
- generated tone must be treated as derived linguistic data, not source
  dictionary data
- generated artifacts need provenance
- accuracy must be validated against a curated or licensed reference set
- loanwords, compounds, ambiguous spellings, proper nouns, and implicit vowels
  may require an override layer

This turns tone generation into more than a display enhancement. It creates a
new data-governance responsibility.

Before implementation, the platform likely needs an ADR or equivalent
architecture grounding for derived linguistic artifacts. At minimum, that
model should preserve:

```text
generator identity
generator version
input headword lineage
```

That provenance would make generated pronunciation data versioned,
reproducible, and reviewable rather than an unexplained field committed beside
source data.

## Preserving Commercial Optionality

The data-source review also clarified the project's licensing posture:

```text
UseThai should remain commercial-capable and ShareAlike-cautious.
```

The product may eventually support ads, memberships, donations, sponsorships,
or another revenue path. A CC BY-SA source such as Volubilis may still be
usable, but ingestion should not begin until the legal and product
implications are explicitly reviewed and accepted.

That posture does not reject open data. It prevents the project from
accidentally committing to obligations before understanding their effect on
the product and its derived artifacts.

The current decision remains narrow:

- Volubilis remains a candidate.
- Volubilis is not approved for ingestion.
- ShareAlike implications remain a gate.
- Normalized dictionary records should not be committed prematurely.
- Generated tone artifacts should not be committed prematurely.
- Commercial optionality should be preserved.

## Separating The Decisions

Day 37 reinforced that several adjacent concerns must remain separate:

```text
App-tier presentation can improve quickly.
Fixture friction does not automatically authorize core search work.
Real-data ingestion remains gated by shape, policy, and licensing.
Tone is product-critical but must be derived through a governed process.
```

That separation is what allows the project to move without confusing motion
with authorization.

The direction-aware heading could be completed because the evidence clearly
supported an app-tier fix. Search expansion stopped because fixture evidence
could not justify it. Volubilis remained a candidate because the spike showed
real potential, but ingestion stayed closed because important transformation
and licensing questions remain. Tone became a requirement without pretending
that the generation and validation model is already settled.

## Why The Day Mattered

Day 37 crossed an important product boundary.

The question is no longer only:

```text
Can the app show lookup results?
```

It is now:

```text
What does real use reveal, and what does that evidence actually justify?
```

The app shell is mature enough to expose meaningful learner friction. The
first friction cycle produced a real application improvement. Dataset research
turned uncertainty into concrete ingestion questions. Tone moved from a
nice-to-have idea into a product requirement with a plausible governed path.

The most important result was not a large code change. It was a clearer method
for making the next decision.

## Outcome

Day 37 moved `UseThai` from fixture demonstration toward evidence-driven
product discovery and real-data readiness.

Manual lookup testing confirmed the happy path, exposed exact-key punctuation
friction, and showed the learner-context problem in multi-entry English
results. The UX friction review kept those observations separate and declined
to authorize speculative core search work.

Direction-aware page chrome resolved the first clearly actionable app-tier
issue without changing lookup behavior. The Volubilis spike established a
serious candidate dataset while identifying duplicate-headword, whitespace,
multi-sense, POS-mapping, and licensing gates.

Tone became a product requirement. The likely path is offline generation with
explicit provenance, validation, and an override strategy rather than runtime
inference.

The project is now positioned for its next major decision: how to govern
derived pronunciation and tone data before moving toward real dictionary
ingestion.

## Definition Of Done

Day 37 reached an evidence, data-readiness, and product-governance checkpoint:

- manually tested the current `UseThai` lookup shell
- confirmed Thai-to-English lookup for `กิน`
- confirmed English-to-Thai multi-entry results for `old`
- confirmed the punctuation-sensitive no-match behavior for `to eat!`
- recorded query-form, result-context, romanization, and fixture-coverage
  friction
- kept fixture evidence separate from real-data evidence
- issued no warrant for fuzzy search, stemming, punctuation normalization,
  tokenizer expansion, or broader core search work
- completed direction-aware document title and page heading behavior
- kept the direction-aware improvement within the application tier
- confirmed the `old` ambiguity is a data-content issue
- reviewed Volubilis as a serious Thai-English candidate
- inspected the 114,177-row, 15-column Volubilis data shape
- identified duplicate-headword, whitespace, sense-splitting, POS-mapping, and
  sparse-enrichment ingestion questions
- kept Volubilis unapproved for ingestion
- established tone as a product requirement
- kept runtime tone inference out of scope
- identified offline generation and storage as the likely tone path
- identified provenance, validation, and override requirements for derived
  linguistic artifacts
- preserved a commercial-capable and ShareAlike-cautious licensing posture
- kept normalized dictionary records and generated tone artifacts out of the
  repository until their gates are resolved

The day closed with a more useful application, a better understanding of real
dictionary data, and a clearer boundary between what the evidence supports now
and what still needs governance.
