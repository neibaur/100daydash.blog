---
title: "Day 33 - June 3, 2026: From Core Platform Architecture to the UseThai Dictionary Shell"
description: "Moving from Phase 15 governance review into the first UseThai application shell, proving a browser-to-core Thai dictionary lookup while exposing search UX limits."
pubDate: "2026-06-03"
day: 33
dashboardSlug: "none"
dataSources:
  - "Astro"
  - "TypeScript"
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "pnpm"
status: "published"
tags:
  - platform-engineering
  - application-shell
  - thai-dictionary
  - architecture-governance
  - search-ux
  - typescript
---

Day 33 marked a real transition point for `lingua-core-platform`.

The recent work had been mostly architectural: phase boundaries, governance
reviews, tenant configuration, canonical language tags, and repository-first
assessments about what the core could justify next. That work mattered. It
kept the platform from turning roadmap language into premature contracts.

Today asked a different question.

```text
Can the platform power a useful user experience?
```

That question changed the shape of the day. Instead of trying to derive
another core artifact, the work moved outward into the first user-facing
`UseThai` dictionary shell. The result was small on purpose: a browser input,
an HTTP request, the existing core lookup engine, and a rendered dictionary
result.

Small was enough. For the first time, the platform proved a complete path from
browser interaction to core lexical behavior and back again.

## Closing The Phase 15 Core Slice Review

The day began with Phase 15 governance review.

The previous Phase 15 work had already delivered the first grounded
implementation direction: tenant identity, enabled-language configuration, and
canonical language tag structure. Those pieces were not invented because Phase
15 sounded broad. They were implemented because the repository had accumulated
enough evidence to defend them.

After that first slice, the responsible question was whether another core
artifact could be derived immediately.

The answer was no.

Several concepts remain important to the future product:

- lessons
- curriculum organization
- content sequencing
- weighting
- visibility
- branding
- richer tenant behavior

But important is not the same as grounded. Those concepts are still
intentionally deferred. They do not yet have enough repository evidence to
become core implementation contracts without speculation.

That conclusion was useful because it prevented Phase 15 from expanding simply
because the platform could imagine more configuration. Tenant identity and
enabled-language configuration were grounded. The next content-organization
slice was not.

The governance result was clear:

```text
No immediately derivable Phase 15 core slice remains.
```

That changed the next move. The platform did not need another architectural
artifact just to keep moving. It needed to validate whether the existing core
could support a real application surface.

## Adding Application-Tier Governance

Before building the UI, the repository needed a lighter rule system for
application work.

The core governance model is intentionally strict. It requires documentary
derivation, explicit phase boundaries, schema-version discipline, ADR-backed
architecture where needed, and careful validation of any reusable platform
contract. That is correct for `src/core`.

It would be too heavy for exploratory application shell work.

So the project introduced `APP_SHELL_GUIDELINES.md` as a lightweight
application-tier governance layer. The goal was not to remove discipline. It
was to put the right kind of discipline at the right boundary.

The application rules are simpler:

- application code lives outside the governed core
- apps consume core behavior only through public barrels
- app work does not require pre-implementation assessments or phase gating
- reusable business rules discovered in app code must be promoted back through
  core governance before becoming platform contracts
- app validation remains required, but it is separate from the core governance
  chain

That boundary matters. A user-facing shell needs room to test workflows,
layouts, requests, and interaction patterns without pretending every UI choice
is a platform law. At the same time, application code should not smuggle new
business rules into the system and then call them architecture.

`APP_SHELL_GUIDELINES.md` gave the project a cleaner split:

```text
Core governs durable platform behavior.
Apps validate user-facing usefulness.
Reusable discoveries move back through core governance deliberately.
```

That made it possible to build the first shell without weakening the rules
that protect the core.

## Building The First UseThai Shell

The main implementation milestone was creating the first user-facing app under
`apps/usethai`.

The goal was intentionally narrow:

```text
Type a Thai word.
Call the existing lexical lookup engine.
Render the dictionary result in a browser.
```

The shell used Astro and TypeScript, with a small application-owned API
endpoint and fixture data. It consumed the lexical core only through public
barrels, which was an important validation of the platform boundary.

The application did not need a distribution build, package publishing step,
new runtime service, database, or export restructuring. A Vite path alias was
enough for the shell to consume the core TypeScript source cleanly.

That was a useful architectural signal. The public barrel structure held up
when a real app tried to use it. The core did not have to be reorganized just
to support the first browser workflow.

The shell itself was modest, but the significance was larger. The platform had
spent many days proving that its contracts could be derived, validated,
serialized, frozen, and governed. Today it began proving that those contracts
could do something visible for a learner.

## Proving The End-To-End Lookup

The most important validation was the complete lookup path:

```text
Browser -> HTTP -> Core Lookup -> Dictionary Result -> Browser
```

The confirmed Thai example was:

```text
Input: กิน
Romanization: kin
Definition: to eat
Part of speech: verb
```

That result matters because it crossed the boundary from architecture into
experience. A user could type `กิน`, send it through the shell, receive the
core lookup result, and see `kin`, `to eat`, and `verb` rendered back in the
browser.

This was the first real end-to-end dictionary demonstration for the platform.
It did not prove the search experience is complete. It did prove that the
platform can support a Thai-to-English lookup workflow all the way through a
browser.

That is a different kind of evidence than a passing unit test. The tests prove
the core behavior under controlled inputs. The app shell proved that the core
can be reached through an actual user-facing path without collapsing the
architecture around it.

## Finding The Search UX Boundary

The browser shell also exposed a limitation quickly: exact-key lookup works,
but it is too restrictive for real dictionary UX.

That is a good discovery. It is exactly the kind of thing a minimal shell is
supposed to reveal.

Exact lookup is valuable as a deterministic baseline. If the user types the
exact known headword, the platform can return the expected entry. But real
users rarely interact with a dictionary only through perfect keys. They may
type prefixes, partial words, alternate romanization attempts, incomplete
English definitions, or slightly wrong queries.

The next planning effort needs to evaluate:

- prefix search
- fuzzy matching
- partial-word matching
- tokenizer integration
- how much search explainability should be exposed to the UI

That work is not done yet. Today did not add fuzzy search or a production
tokenizer flow. It clarified that exact lookup is the current working baseline
and that a useful dictionary experience will need a broader search strategy.

That distinction matters. The milestone was not "search is solved." The
milestone was "the shell now shows where search has to improve."

## Discovering The English-To-Thai Gap

The more interesting limitation appeared in English-to-Thai lookup behavior.

Single-word English definitions worked as expected:

```text
rice -> ข้าว
water -> น้ำ
```

Multi-word definitions did not work the same way. Searching for `to eat` could
not return the Thai entry for `กิน`, even though the dictionary definition
stored for that entry is `to eat`.

The issue was not mysterious once the boundary was inspected. English-to-Thai
indexing keys definitions using the full lowercased definition string, but the
lookup layer rejects queries containing whitespace.

That creates a mismatch:

```text
Index contains: "to eat"
Lookup accepts: no whitespace queries
Result: the indexed phrase cannot be queried directly
```

This is exactly the kind of architectural learning that only becomes obvious
when a user-facing path exists. A core lookup function can be correct inside
its narrow rules and still produce an awkward experience once a human begins
typing natural queries into a browser.

The next search planning effort will need to decide how English phrases should
be tokenized, normalized, indexed, and queried. It may be that definition
lookup should support phrase queries. It may be that the search subsystem
should index individual tokens and phrase-level evidence separately. It may be
that fuzzy and prefix behavior should be language-aware.

Those are future decisions. Today only established the problem clearly enough
to plan responsibly.

## Improving Application Validation

The day also improved application validation around the new shell.

Application work is outside the core governance chain, but it still needs
quality gates. The app should build, typecheck, lint, and validate through its
own appropriate tools.

Several cleanup items followed from that:

- Astro validation checks were added for the application tier
- TypeScript issues surfaced by Astro validation were investigated and fixed
- lint failures caused by generated `.astro` artifacts were resolved
- generated artifact ignore and cleanup behavior was tightened
- application validation remained separate from core validation

That last point is important. The app should not weaken the governed core by
pretending UI checks are core validation. It also should not avoid validation
just because it is exploratory.

The useful boundary is:

```text
Core validation protects durable platform contracts.
Application validation protects user-facing integration.
```

Both matter. They just answer different questions.

## From Architecture Artifact To User Experience

The biggest change today was not the amount of code. It was the direction of
the question.

For many recent days, the dominant question had been:

```text
Can we derive another architectural artifact?
```

Today, the better question became:

```text
Can the platform power a useful user experience?
```

The answer is now yes, in the first narrow sense. The platform can support a
Thai dictionary lookup in a browser. It can accept `กิน`, route the request
through HTTP, invoke the governed core lookup path, and render a result with
romanization, definition, and part of speech.

That does not make the dictionary complete. It does not solve search quality,
tokenization, ranking, fuzzy matching, examples, learning flows, or English
phrase lookup. But it does move the project across an important threshold.

The core is no longer only an architecture to be reasoned about. It is a
platform that can be used by an application.

## Outcome

Day 33 shifted `lingua-core-platform` from pure core architecture work toward
the first user-facing UseThai experience.

Phase 15 governance review concluded that no immediately derivable core slice
remains after tenant identity, enabled-language configuration, and canonical
language tag work. Instead of forcing another artifact into the core, the
project introduced `APP_SHELL_GUIDELINES.md` to govern application-tier work
with a lighter boundary.

The first `apps/usethai` shell then proved an end-to-end browser lookup:
`กิน` returned romanization `kin`, definition `to eat`, and part of speech
`verb`.

The shell also revealed the next useful problems. Exact-key lookup is
functional but too restrictive for real UX. Prefix, fuzzy, and partial-word
search need evaluation. English-to-Thai lookup works for single-word
definitions such as `rice` and `water`, but multi-word definitions such as
`to eat` expose a mismatch between full-definition indexing and whitespace
rejection in the lookup layer.

The day ended with a more honest product direction. The next work should not
pretend the dictionary search layer is complete. It should evaluate how the
existing search and tokenizer infrastructure can support the kind of flexible
lookup behavior a real learner will expect.

## Definition Of Done

Day 33 reached a meaningful application-shell checkpoint:

- reviewed Phase 15 governance after the first implementation slice
- confirmed no immediately derivable additional Phase 15 core slice remains
- kept deferred content, curriculum, sequencing, weighting, visibility, and
  branding concepts out of core contracts
- introduced `APP_SHELL_GUIDELINES.md` as lightweight app-tier governance
- clarified that apps live outside `src/core` and consume core behavior through
  public barrels
- created the first `apps/usethai` user-facing dictionary shell
- wired browser input through an HTTP endpoint into the core lexical lookup
- validated `กิน` as an end-to-end lookup returning `kin`, `to eat`, and
  `verb`
- confirmed the existing public barrel structure supports app consumption
- discovered exact-key lookup is useful but too restrictive for real UX
- identified prefix, fuzzy, and partial-word search as the next evaluation
  area
- discovered the English-to-Thai multi-word definition limitation around
  whitespace rejection
- improved Astro, TypeScript, lint, generated-artifact cleanup, and app
  validation behavior
- preserved the separation between application validation and the core
  governance chain

The day closed with the platform doing something visible: not just explaining
why its architecture exists, but using that architecture to answer a learner's
first dictionary query.
