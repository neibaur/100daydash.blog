---
title: "Day 36 - June 6, 2026: Resolving Contract Contradictions and Moving Into Evidence-Driven UX"
description: "Resolving a lexical lookup contract contradiction through ADR governance, integrating the corrected behavior into UseThai, and shifting toward evidence-driven UX maturation."
pubDate: "2026-06-06"
day: 36
dashboardSlug: "none"
dataSources:
  - "Astro"
  - "Cloudflare"
  - "TypeScript"
  - "Vitest"
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "ADR-0016"
  - "pnpm"
status: "published"
tags:
  - application-development
  - platform-engineering
  - architecture-governance
  - evidence-driven-ux
  - thai-dictionary
  - search-ux
  - typescript
---

Day 36 began as another application-maturation day and became something more
important.

The `UseThai` shell continued becoming a real product surface. Its deployment
baseline improved, its components became easier to maintain, its Thai
typography became more readable, and its lookup states became more honest.

That application work then exposed a contradiction in the governed core
contract.

Instead of hiding the contradiction behind another app-side condition, the
work stopped at the architectural boundary, investigated the history, resolved
the inconsistency through `ADR-0016`, integrated the corrected behavior back
into the application, and then deliberately moved away from premature search
capability work.

The shape of the day was:

```text
Mature the app -> expose a contract contradiction -> investigate history
-> govern the correction -> integrate the real core behavior
-> collect UX evidence before proposing new capability
```

This was not simply a feature day. It was a day when the application became
useful enough to reveal an architectural truth, and governance was disciplined
enough to respond without losing the product momentum that surfaced it.

## Establishing A Green Application Infrastructure Baseline

The day continued the infrastructure work around `apps/usethai`.

The Astro Cloudflare adapter was wired into the application, establishing a
real green server build while preserving the server-rendered lookup endpoint.
The build path now reflects the actual application architecture rather than
assuming a static-only surface.

The validation boundary also became more reliable. ESLint hygiene was improved
by ignoring nested application build output under:

```text
apps/**/dist/**
```

That keeps generated assets outside the authored-source lint boundary without
weakening checks on application code.

The resulting application baseline passed:

- format
- lint
- Astro check
- server build

Infrastructure work can feel secondary to visible product behavior, but this
baseline matters. Evidence gathered from an application is only trustworthy
when the application itself has a repeatable, green build and validation path.

## Improving The UseThai UX Foundation

The application shell also became easier to evolve.

Page structure was extracted into:

- `Layout.astro`
- `LookupForm.astro`
- `global.css`

The separation stayed intentionally small. Stable page and form structure
moved into reusable application components, while result behavior remained
close to the page where the product is still learning what users need.

Lightweight CSS design tokens were added for color, spacing, typography, and
sizing. They provide enough consistency for continued UX work without
prematurely creating a full design system.

Thai-script readability received particular attention. Headwords gained a
larger visual treatment and more generous line height so tone marks and upper
and lower vowels have room to remain legible.

That is not decorative polish. In a Thai dictionary, script readability is a
functional requirement.

The remaining Astro check hints were also resolved, leaving the application
with a clean type-check baseline.

## Making Lookup States Honest

The shell gained a more complete set of lookup states:

- loading
- success
- no match
- rejected input
- empty or awaiting input
- system failure

These states make the application more truthful.

A query with no matching entry is not the same as invalid input. Invalid input
is not a server failure. An empty form should not be presented as a failed
lookup. A product that collapses those states may look simpler internally, but
it gives users less useful information and gives the project worse evidence
about where friction actually occurs.

The improved state model also made the next problem visible. The application
could present a whitespace-rejection diagnostic, but investigation showed that
the diagnostic was not coming from the core contract it appeared to represent.

## Discovering The Contract Contradiction

A planned app-side improvement for English phrase lookup triggered the deeper
investigation.

The expected problem was that a phrase such as:

```text
"to eat" -> กิน
```

needed new application behavior.

Repository evidence showed otherwise. Core already supported English phrase
lookup. The application endpoint was blocking whitespace-bearing queries
before they could reach that existing behavior.

The endpoint also fabricated:

```text
LEXICAL_KEY_WHITESPACE_REJECTED
```

instead of consuming that diagnostic from core.

The contradiction was precise:

- core declared the diagnostic code
- reporting infrastructure already recognized it
- the application presented it as if it came from core
- `composeLexicalLookup` threw on Thai-to-English whitespace instead of
  returning it
- the app pre-guard prevented legitimate English phrase queries from reaching
  core

This was not merely an inconvenient conditional. It was a disagreement between
the public diagnostic vocabulary, the lookup implementation, and the
application integration.

The tempting response would have been to adjust the app guard until the
desired phrase query worked. That would have preserved the contradiction and
made the endpoint responsible for interpreting more of the core contract.

The work stopped instead.

That pause protected both the architecture and the application. It allowed the
repository to resolve the actual contract rather than accumulating a more
polished workaround.

## Investigating The Historical Behavior

Historical investigation showed that the throw-based whitespace behavior was
not recent drift.

It had existed since the Phase 10 lexical foundation.

That finding changed the character of the decision. The repository was not
simply correcting an accidental regression. It was reconciling a durable
implementation invariant with a public diagnostic contract that had evolved
around it.

The investigation separated two valid concerns:

```text
Index construction:
Whitespace-invalid lexical keys remain a fail-fast invariant.

Lookup time:
User-provided whitespace rejection belongs in the returned lookup diagnostic
contract.
```

Keeping those concerns distinct made the resolution smaller and clearer.
Index-building rules did not need to become permissive just because runtime
lookup needed to return an honest diagnostic.

## Governing The Resolution Through ADR-0016

`ADR-0016` recorded the decision:

> Lexical Lookup th→en Whitespace Rejection Surfaced as a Returned Diagnostic

The governed direction was to:

- preserve the public lookup contract
- preserve the existing diagnostic code
- preserve the reporting infrastructure
- return `LEXICAL_KEY_WHITESPACE_REJECTED` from lookup
- retain fail-fast whitespace validation during index construction

A minimal `ARCHITECTURE` clarification grounded lookup-time whitespace
rejection in the lexical lookup diagnostic contract. `SESSION_STATE` was also
corrected so it described the current inline whitespace guard accurately
rather than referring to the older `assertNoWhitespace` wording.

The decision did not invent a new status or broaden the schema.

The section 9 assessment confirmed that the existing result model was already
sufficient. No new field, type, schema literal, diagnostic code, or status was
needed.

That is a useful sign of a well-scoped architectural correction: the existing
contract had enough expressive capacity. The implementation needed to honor it.

## Implementing The Corrected Core Behavior

The implementation changed `composeLexicalLookup` so Thai-to-English
whitespace rejection returns:

```text
code: LEXICAL_KEY_WHITESPACE_REJECTED
severity: warning
path: ["query"]
status: not-found
```

The result uses the existing `not-found` status union. The correction therefore
fits the established lookup result model while making the diagnostic source
truthful.

Validation remained green after the change.

The core baseline moved to:

- 859 tests
- 62 test files
- 92.79% statement coverage

The governed core correction merged through:

```text
PR #181: fix(lexical): surface th→en whitespace rejection as returned diagnostic
```

The important outcome was not only that an exception became a returned result.
The diagnostic vocabulary, implementation behavior, and reporting path now
agree.

## Letting UseThai Consume The Real Contract

With the core contradiction resolved, `apps/usethai` could simplify.

The endpoint whitespace pre-guard was removed. Whitespace-bearing queries can
now reach core, and the application consumes the real returned diagnostic
instead of fabricating one.

This corrected several behaviors at once:

- English phrase lookup now works through the UI
- `"to eat"` can resolve to `กิน`
- Thai whitespace rejection comes from core
- rejection severity is the core-provided `warning`, not an app-authored
  `error`
- the endpoint no longer duplicates diagnostic ownership

Empty and whitespace-only input remains neutral. It stays in the
awaiting-input state and does not call core.

That distinction preserves a good application responsibility. The form can
recognize that no lookup has been requested without trying to reinterpret a
non-empty query that belongs to the core lookup contract.

The integration merged through:

```text
PR #182: fix(usethai): remove lookup whitespace pre-guard and consume core diagnostics
```

The app became more capable because it became less controlling. Removing the
special case allowed existing phrase behavior through and made rejected input
more truthful.

## Reconciling Governance And Session State

After the implementation work, governance records were synchronized with the
new repository state.

`SESSION_STATE` now reflects both merged changes:

- `#181` resolved the core lookup contradiction
- `#182` integrated the corrected behavior into `UseThai`

`ADR-0016` is recorded as implemented. Application-tier learnings now reflect
real diagnostic consumption, phrase lookup availability, and the removal of
diagnostic fabrication.

The wider phase state remains deliberately unchanged:

```text
Phase 15: complete
Phase 16: unauthorized
Active core slice: none
```

Resolving one core contradiction did not become an excuse to open a new
architecture phase. The correction was authorized because existing contracts
disagreed, not because the project had decided to expand the platform.

## Establishing An Evidence-Only UX Friction Log

With the core boundary reconciled, the work turned back toward the
application.

The next step was not to propose prefix matching, fuzzy search, substring
search, autocomplete, or suggestions.

It was to improve the evidence.

`docs/usethai/ux-friction-log.md` was developed as an evidence-only record. The
log separates observed friction from proposed solutions and distinguishes:

- `FIXTURE` evidence
- `REAL` evidence
- confirmed-present entries
- confirmed-absent entries
- entries whose presence is still unknown

Friction is categorized descriptively, including:

- `QUERY-FORM-UNMATCHED`
- `ENTRY-ABSENT`
- `RESULT-PRESENT-HARD-TO-USE`
- `DIAGNOSTIC-UNCLEAR`

These categories avoid prematurely turning every difficult lookup into a
search-capability request.

A query can fail because the form is unexpected, because the entry is absent,
because the result exists but is hard to use, or because the diagnostic is
unclear. Each cause suggests a different kind of future work. Treating them
all as evidence for fuzzy search would hide the actual product problem.

Future search capabilities remain unwarranted until real usage evidence
supports them.

## Planning Evidence-Driven UX Maturation

The application planning pass reviewed the relevant governance and product
documents, including:

- `NEW_APP_SESSION`
- `SESSION_STATE`
- `APP_SHELL_GUIDELINES`
- `ARCHITECTURE`
- `DATA_SOURCES`
- `CLAUDE`
- the UX friction log

The review confirmed that the next direction is application-tier UX
maturation and evidence gathering, not core architecture work.

A no-code UX assessment focused on:

- P1-1 result rendering
- P1-2 diagnostic legibility
- P1-3 query and direction echo

The assessment produced a useful correction to the roadmap. Result rendering
mostly already exists. The current fixture data simply does not exercise
multi-definition and homograph or multi-entry paths well enough to make those
rendering behaviors observable.

Fixture enrichment is therefore likely to be more useful than rewriting the
result UI. Adding at least one multi-definition entry and one
homograph/multi-entry key would expose the paths the application already
supports.

The largest meaningful UX gap is diagnostic presentation.

The application routes on real diagnostic code and severity, but the
explanatory text is app-authored. The preferred direction became Policy B:

```text
Use app-friendly copy as the primary message.
Use the core diagnostic message as a fallback for unsupported future codes.
```

That policy respects both audiences. The app can explain known conditions in
learner-friendly language without becoming brittle when core introduces a
future diagnostic the app does not yet recognize.

## Expanding The Validation Guardrail

The work also clarified the validation boundary for future application-tier
changes.

Root validation alone does not prove that `apps/usethai` is healthy. The app
has an Astro-specific check and build surface that needs to be validated
explicitly.

Future app-tier work should run:

```text
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm validate
pnpm --filter usethai check
pnpm --filter usethai build
```

This is a practical governance improvement. The project now has a clearer
definition of what it means for an application change to be green, and future
sessions are less likely to borrow false confidence from unrelated root
checks.

## Why The Application Work Mattered

The most valuable result of Day 36 was not phrase lookup by itself.

The application became mature enough to reveal that a public diagnostic,
runtime behavior, and endpoint integration disagreed. That contradiction had
survived because each layer looked plausible in isolation:

- the code existed
- the diagnostic existed
- the UI could display it
- tests around neighboring behavior were green

Only the real application path made the disagreement obvious.

That is one of the strongest arguments for building product surfaces alongside
platform architecture. Applications are not merely consumers waiting for core
work to finish. They are instruments that reveal whether the platform's
contracts make sense when someone actually tries to use them.

Governance then determines what happens with that evidence.

On Day 36, it prevented an app workaround, preserved a useful public contract,
corrected a historical inconsistency, and returned the project to UX work
without authorizing speculative search architecture.

## Outcome

Day 36 moved `UseThai` and the Lingua Core Platform through an important
transition.

The application infrastructure reached a green Cloudflare server-build
baseline. The UX foundation became more maintainable, Thai typography became
more readable, and lookup states became more honest.

That product work exposed a real core/app contradiction. Core supported
English phrase lookup, but the app blocked whitespace-bearing queries and
fabricated a diagnostic that core declared but did not return on the relevant
path.

The repository stopped at the correct boundary, investigated the historical
behavior, resolved the contradiction through `ADR-0016`, and implemented the
existing diagnostic contract without expanding the result schema. `UseThai`
then removed its pre-guard, consumed the real core diagnostic, and gained
working phrase lookup through the UI.

The day ended by shifting deliberately toward evidence-driven UX maturation.
The friction log now separates observation from solution, real evidence from
fixture evidence, and missing entries from unclear diagnostics. Result
rendering will be evaluated through richer fixtures, while diagnostic
legibility has emerged as the strongest current UX opportunity.

No new core phase was authorized. No speculative search capability was added.

The application matured, taught the architecture something true, and then
returned to gathering evidence.

## Definition Of Done

Day 36 reached a governed application-and-core reconciliation checkpoint:

- wired the Astro Cloudflare adapter into `apps/usethai`
- established a green server build while preserving the SSR lookup endpoint
- excluded nested `apps/**/dist/**` output from ESLint
- confirmed application format, lint, Astro check, and build validation
- extracted `Layout.astro`, `LookupForm.astro`, and `global.css`
- introduced lightweight CSS design tokens
- improved Thai headword readability and line height
- cleared remaining Astro check hints
- added honest loading, success, no-match, rejected-input, awaiting-input, and
  system-failure states
- confirmed core already supports English phrase lookup
- identified the endpoint whitespace pre-guard
- identified application-fabricated `LEXICAL_KEY_WHITESPACE_REJECTED`
- traced the throw-based behavior to the Phase 10 lexical foundation
- added and implemented `ADR-0016`
- preserved index-construction whitespace validation as fail-fast
- returned lookup-time whitespace rejection through the diagnostic contract
- reused the existing `not-found` status and existing result schema
- reached 859 tests across 62 files with 92.79% statement coverage
- merged the core correction through PR `#181`
- removed the `UseThai` endpoint whitespace pre-guard
- stopped fabricating lookup diagnostics in the application
- enabled English phrase lookup through the UI
- consumed core-provided warning severity
- preserved empty and whitespace-only input as neutral awaiting-input state
- merged the application integration through PR `#182`
- reconciled `SESSION_STATE` and recorded `ADR-0016` as implemented
- kept Phase 15 complete and Phase 16 unauthorized
- established an evidence-only UX friction log
- separated observed friction from proposed solutions
- kept prefix, fuzzy, substring, autocomplete, and suggestion work
  unauthorized
- assessed result rendering, diagnostic legibility, and query-direction echo
- identified fixture enrichment as the next way to expose existing rendering
  paths
- selected app-friendly diagnostic copy with core-message fallback as the
  preferred policy
- documented the need for both root and app-specific validation on future
  `UseThai` work

The day closed with stronger application behavior, a more truthful core
contract, and a better method for deciding what UX work should happen next.
