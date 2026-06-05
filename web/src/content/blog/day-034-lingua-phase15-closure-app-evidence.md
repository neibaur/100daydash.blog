---
title: "Day 34 - June 4, 2026: Closing Phase 15 and Grounding Application-Tier Evidence"
description: "Closing Phase 15 through ADR-0015, grounded English-to-Thai phrase lookup, lexical key normalization, barrel inventory, and UseThai application evidence gathering."
pubDate: "2026-06-04"
day: 34
dashboardSlug: "none"
dataSources:
  - "TypeScript"
  - "Vitest"
  - "Astro"
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "pnpm"
status: "published"
tags:
  - platform-engineering
  - architecture-governance
  - application-evidence
  - thai-dictionary
  - search-ux
  - typescript
---

Day 34 closed the loop that Day 33 opened.

The previous work proved that `lingua-core-platform` could power a real
browser lookup through the first `UseThai` shell. It also exposed the first
honest application friction: exact-key lookup worked, but natural dictionary
queries immediately pushed against the boundary of what the core currently
supports.

Today did not respond by opening another core phase.

It responded by finishing the current one responsibly.

The shape of the day was:

```text
Close Phase 15 -> Ground phrase lookup -> Normalize lexical keys
-> Inventory public barrels -> Gather app friction evidence
-> Validate the UseThai build surface -> Keep Phase 16 pending
```

That sequence matters. The project is now learning from a user-facing app, but
the governance rule remains the same: application evidence can suggest future
core work, but it does not automatically authorize it.

## Closing Phase 15 Through ADR-0015

The main governance milestone was Phase 15 closure.

Phase 15 began as a configuration and boundary phase. It clarified tenant
identity, enabled-language configuration, canonical language identity,
application-tier boundaries, and the public surfaces that application code can
use without reaching into core internals.

By Day 34, the remaining defensible Phase 15 work had become narrow enough to
close. The repository no longer needed to keep Phase 15 open just because
future product concepts still exist.

`ADR-0015` captured that closure.

The important conclusion was not that every future dictionary, curriculum, or
search capability is complete. It is not. The conclusion was smaller and more
useful:

```text
Phase 15 is complete under current repository evidence.
Phase 16 remains pending authorization.
Application-tier evidence gathering is the next near-term focus.
```

That is a healthy boundary. A phase should close when its warranted work is
done, not when every imaginable adjacent feature has been named.

The repository still expects richer search, lessons, examples, and learner
flows later. Those ideas need evidence before they become durable core
contracts.

## Grounding English-To-Thai Phrase Lookup

Day 33 found a precise lookup mismatch.

English-to-Thai indexing could contain a full definition phrase such as
`to eat`, but the lookup layer rejected whitespace in queries. That meant an
indexed phrase could exist while still being unreachable through the user
path.

Day 34 turned that from a UX complaint into a grounded implementation slice.

The key distinction was that phrase lookup is not fuzzy search. It is not
ranking. It is not synonym expansion. It is not a general natural-language
search engine.

It is deterministic lookup for a phrase that the lexical index already knows.

That made the implementation defensible. The platform was not inventing a new
search subsystem. It was allowing an already indexed English phrase key to be
queried through the same governed lookup path.

That is the kind of change the repository should be willing to make after an
application shell reveals a real integration gap:

```text
Observed app friction -> inspect existing core evidence
-> identify a narrow grounded mismatch -> implement only that mismatch
```

The result moved English-to-Thai lookup from single-token definitions toward
phrase-capable deterministic lookup without claiming that broader search
quality is solved.

## Defining The Lexical Key Normalization Policy

Phrase lookup also forced a clearer lexical key normalization policy.

A dictionary lookup system needs to decide what counts as the same key before
it can safely expand query behavior. Otherwise every new app friction point
can become a one-off transformation.

The policy that emerged keeps normalization intentionally conservative:

- trim surrounding query whitespace
- case-fold English lookup keys
- normalize internal whitespace for English phrase keys
- preserve Thai headword identity as an exact lexical key
- avoid stemming, synonym expansion, fuzzy matching, and transliteration as
  implicit normalization

That last part matters most.

Normalization is not search intelligence. It is the deterministic cleanup
needed to make already supported lookup keys usable. Fuzzy search, prefix
matching, tokenizer behavior, ranking, and explanatory search results remain
separate questions.

This keeps the platform from hiding new product behavior inside a helper
function with a harmless-looking name.

## Completing The Barrel Surface Inventory

The day also completed the public barrel surface inventory.

That was a necessary checkpoint after the first `apps/usethai` integration.
If application code is supposed to consume the core through public barrels,
the repository needs to know whether those barrels actually expose the
surfaces an app can use.

The inventory validated the boundary rather than bypassing it.

The goal was not to make every internal module public. It was to confirm that
the public import surface is coherent enough for the application tier to use
without reaching through private paths.

That distinction protects both sides of the system:

- core modules can keep their internal organization private
- application code gets a stable consumption surface
- future missing exports can be treated as explicit boundary decisions
- app friction cannot quietly become private-core coupling

The completed inventory gave the repository a better map of what the core is
actually offering to application consumers.

## Adding The UseThai Friction Evidence Harness

With Phase 15 closed, the most useful near-term work moved outward to
`apps/usethai`.

The application-tier friction evidence harness gives the project a practical
way to record how the shell behaves under real lookup attempts. This is
deliberately different from declaring a new core phase.

The harness is a way to collect evidence, not a way to smuggle roadmap items
into the core.

It can capture questions like:

- which lookup inputs succeed
- which inputs fail despite feeling reasonable to a learner
- which failures are caused by app UX
- which failures suggest missing reusable core behavior
- which cases are still too speculative to promote

That makes the next governance decision better. Instead of asking whether
Phase 16 sounds useful, the repository can ask what repeated application
friction actually proves.

## First Friction Evidence Pass

The first friction evidence pass produced a useful, modest result.

The existing Thai lookup path still works. English single-word lookup remains
useful. The newly grounded English phrase lookup closes the specific `to eat`
style mismatch from Day 33.

The pass also kept the limits visible.

Exact deterministic lookup is still a baseline, not a full search experience.
The app continues to need evidence around:

- prefix queries
- partial-word queries
- fuzzy misspellings
- tokenizer-assisted lookup
- no-result messaging
- how much explanation a learner should see when a query fails

Those are not completed features.

They are evidence categories.

That framing is important because it prevents the first pass from becoming
too triumphant. The dictionary is becoming more usable, but application-level
search friction is still the right place to learn before opening another
core implementation phase.

## Validating The UseThai Astro Surface

The `UseThai` shell also surfaced dependency and build-validation findings.

The app exists outside the main `web` package, so the repository cannot assume
that the normal blog validation path proves the application shell. The shell
needs its own Astro-aware dependency and build validation story.

That finding is valuable even when it feels procedural.

An application can call the core correctly and still be under-validated if its
own framework dependencies, generated artifacts, typechecking, or build
commands are not represented clearly. The right answer is not to fold the app
back into the core. It is to make application validation explicit at the
application boundary.

The governance split remains:

```text
Core validation protects durable platform contracts.
UseThai validation protects the user-facing integration surface.
```

The build findings therefore became part of the evidence workflow rather than
a reason to reopen Phase 15.

## Evidence-Driven Governance

Day 34 clarified the operating model for the next stretch of work.

The project should not open Phase 16 just because Phase 15 is complete. A
completed phase creates room to decide, not pressure to keep implementing
core artifacts.

The better workflow is:

```text
UseThai app friction -> repeated evidence -> repository-first assessment
-> authorization decision -> narrow core slice, if warranted
```

That workflow keeps the architecture responsive without making it reactive.
The application can move quickly enough to find real learner friction. The
core can remain strict enough that only repeated, grounded, reusable behavior
becomes platform contract.

That is the balance the project has been trying to learn: build visible
things, let them teach the repository, and promote only what the evidence can
carry.

## Outcome

Day 34 completed Phase 15 and established the next working posture.

`ADR-0015` recorded the closure. English-to-Thai phrase lookup moved from a
known application gap into a grounded deterministic lookup capability. The
lexical key normalization policy became clearer, especially around the
difference between conservative key cleanup and broader search intelligence.

The public barrel surface inventory was completed, giving `apps/usethai` a
cleaner application-consumption map. The first application-tier friction
evidence harness and evidence pass began turning real lookup behavior into
governance input.

The UseThai Astro dependency and build validation findings also clarified
that the app tier needs explicit validation of its own surface rather than
borrowing confidence from core checks or the blog build.

The day ended with a restrained but important state:

```text
Phase 15 is complete.
Phase 16 is not yet authorized.
The near-term focus is application-tier evidence gathering in apps/usethai.
```

That is exactly where the project should be. The next core phase should open
because application evidence justifies it, not because the calendar is ready
for another phase label.

## Definition Of Done

Day 34 reached a meaningful phase-closure and evidence checkpoint:

- closed Phase 15 under current repository evidence
- recorded the closure through `ADR-0015`
- kept Phase 16 pending authorization
- grounded English-to-Thai phrase lookup as deterministic lookup rather than
  fuzzy search
- implemented the narrow phrase-lookup path exposed by the `UseThai` shell
- clarified lexical key normalization policy
- preserved broader prefix, fuzzy, tokenizer, and ranking behavior as future
  evidence questions
- completed the public barrel surface inventory
- reinforced that application code should consume core behavior through public
  barrels
- added the application-tier friction evidence harness in `apps/usethai`
- completed the first friction evidence pass
- identified remaining application search friction without overstating it as
  completed work
- captured UseThai Astro dependency and build-validation findings
- preserved the distinction between core validation and app-tier validation
- established evidence gathering as the near-term focus before authorizing
  another core phase

The work closed with a useful kind of restraint: the core phase is complete,
the application is now teaching the project where users feel friction, and the
next architecture decision can wait for evidence strong enough to deserve it.
