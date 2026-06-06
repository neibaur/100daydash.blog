---
title: "Day 35 - June 5, 2026: Maturing UseThai Through Product Evidence"
description: "Strengthening the UseThai application through Cloudflare build support, UI foundations, truthful lookup states, search investigation, governance cleanup, and dataset research."
pubDate: "2026-06-05"
day: 35
dashboardSlug: "none"
dataSources:
  - "Astro"
  - "Cloudflare"
  - "TypeScript"
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "Thai language dataset documentation"
  - "pnpm"
status: "published"
tags:
  - application-development
  - platform-engineering
  - architecture-governance
  - thai-dictionary
  - search-ux
  - data-licensing
  - typescript
---

Day 35 moved `UseThai` further from an application-shell proof and closer to a
product that can teach the platform what users actually need.

The day combined infrastructure stabilization, UI foundation work, truthful
lookup-state design, search investigation, governance cleanup, dataset
licensing research, and product roadmap planning.

The work was broad, but the operating principle stayed narrow:

```text
Improve the application -> observe real behavior -> investigate the boundary
-> record evidence -> avoid promoting assumptions into core contracts
```

That principle mattered most when an expected English phrase lookup
enhancement turned into a more useful architectural discovery. Investigation
showed that core already supports English phrase lookup, while a different
whitespace path revealed an inconsistency between core behavior and an
application-owned diagnostic.

The implementation stopped there.

That restraint kept the application moving without letting product pressure
create architectural drift.

## Establishing A Cloudflare Build Path

The first application infrastructure slice added Cloudflare deployment support
to the Astro application shell.

The application gained the Cloudflare Astro adapter and a server-output
configuration that builds successfully while preserving the lookup endpoint's
server-side behavior. The API route continues to use `prerender = false`, so
the production build path does not quietly convert a dynamic lookup surface
into a static artifact.

The resulting baseline is modest but important:

- the application has an honest server-output build
- SSR endpoint behavior remains intact
- the non-prerendered lookup route remains explicit
- format, lint, Astro check, and build validation pass

This resolved the previously deferred deployment concern without expanding the
application into a larger hosting architecture.

## Keeping Generated Artifacts Out Of Lint

The successful build exposed a smaller validation issue.

Root-level build output was already ignored, but nested application output
under `apps/**/dist` could still be linted unintentionally. That meant a clean
source tree could produce generated files and then fail a later lint run for
reasons unrelated to authored code.

The lint configuration was tightened to ignore:

```text
apps/**/dist/**
```

That exclusion is intentionally narrow. It does not reduce source coverage or
hide application code. It keeps generated build artifacts out of the source
quality boundary.

The result is a more reliable application workflow: lint remains green both
before and after a production build.

## Building A Maintainable UI Foundation

The original UseThai shell proved the lookup path, but most of the page still
lived in a single implementation file.

Day 35 extracted the first maintainable UI foundation:

- `Layout.astro`
- `LookupForm.astro`
- `global.css`

Dynamic result rendering remained in the page itself. No frontend framework
was added, and lookup behavior did not change.

That was the right level of refactoring for the current evidence. Layout and
form structure are already stable enough to separate. The result presentation
is still teaching the project what the product needs, so it remains closer to
the page where that learning is happening.

## Introducing Lightweight Design Tokens

The UI foundation also introduced a small design-token system using CSS custom
properties.

The tokens cover:

- color
- spacing
- typography
- sizing primitives

The goal was not a visual redesign. It was to make future application changes
more consistent and easier to reason about.

A product-facing application needs room to evolve without turning every
spacing or color decision into a one-off value. At the same time, the current
shell is too early for a large design system.

Lightweight tokens provide enough structure without creating another platform
inside the application.

## Improving Thai Typography

Thai readability received focused attention.

Thai script needs enough size and vertical room for stacked tone marks and
upper and lower vowels to remain legible. A type treatment that works for
English body text can make Thai headwords feel cramped or visually ambiguous.

The updated presentation increased Thai headword size and line height while
keeping romanized text at body size.

That improved the hierarchy in a way that reflects the product:

```text
Thai headword -> primary learning object
Romanization and definition -> supporting information
```

This was a small UI change with meaningful product value. The application is
not only displaying data. It is displaying a script that learners need to
inspect carefully.

## Completing The Astro Type-Safety Pass

The application also resolved the remaining Astro TypeScript hints.

Client-rendering callbacks now use the existing public lexical types,
including:

- `LexicalLookupResult`
- `LexicalEntry`
- `LexicalDefinition`

That preserved the application/core boundary. The app did not invent parallel
result shapes just to satisfy TypeScript. It consumed the public lexical types
already available through the governed surface.

Astro check now reports:

```text
0 errors
0 warnings
0 hints
```

That gives the application a cleaner baseline for future UI work.

## Rendering Honest Lookup States

The most important product-facing implementation was truthful lookup-state
handling.

The application now distinguishes:

- loading
- success
- no result
- rejected input
- system failure

That separation matters because these states mean different things to a user.

A no-match result is not a system failure. Rejected input is not the same as a
missing lexical key. A loading state should not look like an empty result.

Treating them separately makes the application more useful and gives the
friction evidence harness better observations. The UI can now show what
happened without flattening every unsuccessful lookup into a generic error.

## Mapping Lexical Diagnostics

The state work also mapped lexical diagnostics into user-facing presentation.

The current diagnostic set includes:

- `LEXICAL_KEY_NOT_FOUND`
- `LEXICAL_KEY_WHITESPACE_REJECTED`
- `LEXICAL_INDEX_EMPTY`

The application gained diagnostic-specific copy, severity-aware presentation,
and generic fallback handling.

This creates a clearer product surface, but it also raised an architectural
question. A user-facing diagnostic is most trustworthy when it represents
behavior genuinely emitted by the governed core. If the app fabricates a
diagnostic to hide a core exception path, the UI may look coherent while the
contract underneath it is not.

That concern became central during the search investigation.

## Preserving Exact-Lookup Honesty

The application search path was explicitly reviewed to confirm what it does
and does not support.

The current behavior remains exact-key lookup.

The review confirmed the absence of:

- prefix matching
- fuzzy matching
- substring matching
- autocomplete
- suggestions
- "did you mean" behavior

That is not a failure of the application. It is an honest representation of
the governed search capability currently available.

The UI should not imply flexibility that the lookup system does not provide.
Product polish becomes misleading when it promises behavior that the core
cannot defend.

## Investigating English Phrase Lookup

The planned search enhancement was English phrase lookup:

```text
"to eat" -> กิน
```

The expected task was to implement support for the phrase. Investigation
showed that this assumption was wrong.

Core already supports English phrase lookup. Both of these queries resolve:

```text
"to eat"
"to   eat"
```

That means core already tolerates multiple internal spaces for English phrase
lookups. No application-side whitespace normalization is required.

This refined the previous understanding of the lookup boundary. The missing
capability was not English phrase lookup after all.

The investigation found a different issue: Thai whitespace queries do not
produce `LEXICAL_KEY_WHITESPACE_REJECTED` from core. They currently throw an
exception. The application endpoint avoids that path by fabricating the
whitespace-rejected diagnostic before invoking core.

That creates an application/core contract inconsistency:

```text
Core behavior: exception
Application presentation: rejected-input diagnostic
Source of diagnostic: application endpoint
```

Removing the endpoint guard would expose the exception and bypass the newly
implemented rejected-input UX. Keeping the guard preserves special-case
application behavior and a diagnostic that core does not genuinely emit.

An application-only workaround would make the boundary less trustworthy.

So the planned implementation was intentionally halted.

## Letting Investigation Change The Plan

The likely next question is whether whitespace rejection should become a
genuine lexical diagnostic owned by core rather than an exception path.

If future repository evidence warrants that change, it could allow:

- core to own the rejection diagnostic
- application logic to simplify
- fabricated endpoint diagnostics to be removed
- English phrase lookup to remain available naturally
- rejected-input UX to reflect a real governed contract

None of that was authorized today.

No core slice was opened. No application workaround was added. The discovery
was recorded as evidence for a future repository-first assessment.

This was the most important result of the day. Investigation did more than
avoid unnecessary implementation. It exposed the actual inconsistency before
the application embedded it more deeply.

## Refining Barrel And Search Evidence Governance

The tokenizer and search barrel inventory was also reviewed and refined.

The update separated two questions that had begun to blur:

```text
Does the capability exist?
Can the application reach it through public barrels?
```

Capability verdicts now distinguish:

- `EXPORTED`
- `PRESENT - NOT APP-REACHABLE`
- `NOT PRESENT`

Reachability classifications remain:

- `APP-REACHABLE`
- `INTERMEDIATE`
- `LEAF-ONLY`
- `INTERNAL`

This creates a more reliable denominator for application planning. A
capability can exist somewhere in the repository without being a legitimate
application dependency. Likewise, an exported symbol does not automatically
mean the app should use every lower-level leaf directly.

The inventory now describes both presence and reachability more clearly.

## Reducing Session-State Maintenance

The governance documents received a maintainability cleanup.

The session-state fields:

- `Branch at last update`
- `Commit at last update`

were replaced with:

- `Last merged PR`

That is a practical improvement. Branch names and commit hashes become stale
quickly as work merges and moves. A merged pull request is a more stable
reference for the completed unit of work.

The cleanup also updated next-action tracking, removed duplicate
application-tier learning entries, and synchronized `NEW_CHAT_SESSION.md`.

The result is less maintenance burden and a clearer starting point for future
human-and-agent sessions.

## Closing The Search-Friction Evidence Cycle

The friction-harness evidence was reviewed to determine what future search
work is actually justified.

The evidence supports future investigation into:

- deterministic prefix matching
- deterministic fuzzy matching
- deterministic non-exact matching

It does not authorize implementation.

No core slice was authorized. No app-side workaround was justified. The
search-friction evidence cycle closed with a clearer set of research questions
and the current exact-key boundary intact.

That is evidence-driven governance doing useful product work. The application
identified friction, the repository investigated it, and the outcome remained
proportional to what the evidence could prove.

## Researching Thai Dataset Licensing

The day also included substantial research into candidate Thai language
datasets and learning-surface resources.

The investigation covered:

- LEXITRON and NECTEC
- Volubilis
- SCB-MT-EN-TH-2020
- PyThaiNLP
- Thai WordNet
- Tatoeba
- Thai character-reference resources

Volubilis became more promising than previous assumptions suggested. Available
evidence indicates multilingual coverage, Thai-English support, and a
CC BY-SA 4.0 license.

LEXITRON remains potentially the most valuable source and the highest-risk
licensing candidate. Conflicting licensing signals still require verification
before it can become an approved source.

The PyThaiNLP review reinforced an important distinction:

```text
Library license is not corpus license.
```

Each bundled or reachable dataset needs its own provenance and licensing
assessment. Treating a library ecosystem as one licensed asset would create
false confidence.

The research also identified plausible future sources for example sentences
and character references. Thai stroke-order data remains an unresolved gap.

No candidate was approved for ingestion.

## Expanding Data-Source Planning

The research prepared a broader expansion of `DATA_SOURCES.md`.

The planned documentation work includes:

- candidate registry expansion
- provisional audit records
- licensing findings
- verification threads
- learning-surface source tracking

Candidates prepared for evaluation include:

- SCB-MT-EN-TH-2020
- PyThaiNLP
- Thai WordNet
- Tatoeba
- OFL-licensed Thai fonts

The distinction between candidate and approved source remains explicit.

No provenance was fabricated, and no dataset was approved for ingestion
before its licensing and intended use could be verified.

## Turning Toward Product Planning

The day ended with a clearer application-planning direction.

Enough architectural reconnaissance now exists to spend more time on the
user-facing experience while continuing to respect core boundaries.

The next planning areas include:

- search-page UX
- result presentation
- pronunciation display
- navigation
- mobile responsiveness
- search history
- overall usability

The planning approach starts by inventorying the current UI, validating the
application baseline, and prioritizing the next UX work against real product
friction.

That does not mean architectural governance is finished. It means the
application has enough structure to become a stronger source of evidence.

## Outcome

Day 35 matured the `UseThai` application across infrastructure, UI, type
safety, lookup-state honesty, search evidence, governance, and data-source
research.

The Cloudflare adapter and Astro server-output configuration established a
green production build path while preserving the dynamic lookup route.
Generated application build artifacts were excluded from lint without reducing
source coverage.

The UI gained extracted layout and form structure, lightweight design tokens,
improved Thai typography, fully typed client-rendering callbacks, and distinct
loading, success, no-result, rejected-input, and system-failure states.

Most importantly, investigation showed that core already supports English
phrase lookup and multiple internal spaces. The actual inconsistency is that
Thai whitespace queries throw from core while the application endpoint
fabricates a rejection diagnostic. Implementation stopped so that behavior
could be assessed at the correct architectural boundary.

The search-friction evidence cycle closed without authorizing prefix, fuzzy,
or other non-exact matching. Dataset research expanded the candidate picture
without approving ingestion or inventing provenance.

The day marked a real transition toward product maturation: not by abandoning
governance, but by using a better application to generate better evidence.

## Definition Of Done

Day 35 reached a meaningful application-maturation checkpoint:

- added the Cloudflare Astro adapter
- established a green Astro server-output build
- preserved SSR endpoint behavior and `prerender = false`
- excluded `apps/**/dist/**` generated artifacts from lint
- confirmed lint remains green before and after builds
- extracted `Layout.astro`, `LookupForm.astro`, and `global.css`
- introduced lightweight color, spacing, typography, and sizing tokens
- improved Thai headword typography and vertical spacing
- typed client-rendering callbacks with public lexical types
- reduced Astro check output to zero errors, warnings, and hints
- added distinct loading, success, no-result, rejected-input, and failure states
- mapped lexical diagnostics into user-facing presentation
- preserved no-match results as non-error states
- confirmed the application still performs exact-key lookup only
- verified that core already supports English phrase lookup
- verified that core tolerates multiple internal spaces in English phrases
- discovered the Thai-whitespace exception path
- identified the application endpoint's fabricated whitespace diagnostic
- halted implementation before adding an app-only workaround
- refined the barrel inventory around capability and reachability
- replaced stale branch and commit session-state fields with `Last merged PR`
- closed the current search-friction evidence cycle without authorizing a new
  core slice
- researched Thai dataset and learning-surface candidates
- preserved LEXITRON licensing verification as unresolved
- identified Volubilis as a more promising candidate
- kept all dataset candidates unapproved for ingestion
- prepared the next product-planning focus around learner-facing UX

The work closed with a stronger application and a more accurate architectural
model. The next product decisions can now begin from evidence the application
actually produced.
