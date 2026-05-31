---
title: "Day 29 - May 30, 2026: Troubleshooting Hardware, Grounding Architecture, and Breaking Phase 14 Open"
description: "Completing a methodical home AC diagnosis while grounding the Lingua Core Platform delivery boundary and opening Phase 14 with warranted route contracts."
pubDate: "2026-05-30"
day: 29
dashboardSlug: "none"
dataSources:
  - "Amana Prestige air conditioner wiring diagram"
  - "Amana 80 SSE furnace wiring diagram"
  - "HVAC electrical diagnostics"
  - "TypeScript"
  - "Vitest"
  - "pnpm"
  - "OpenAI Codex"
  - "Anthropic Claude"
status: "published"
tags:
  - engineering-mindset
  - root-cause-analysis
  - troubleshooting
  - platform-engineering
  - architecture-governance
  - ai-governance
---

Day 29 continued two investigations that looked unrelated on the surface.

The first was physical: finishing the technical troubleshooting of an older
Amana Prestige 2-ton air-conditioning condenser paired with an Amana 80 SSE
gas furnace.

The second was architectural: breaking a Phase 14 deadlock in
`lingua-core-platform` without bypassing the governance rules that had exposed
the gap in the first place.

Both required the same engineering posture:

```text
Isolate the failure -> Verify assumptions -> Respect safety boundaries
-> Ground the next step -> Change only what the evidence warrants
```

The work was not about forcing a quick answer. It was about reducing
uncertainty until the responsible next action became clear.

## Continuing The AC Diagnosis

Day 28 restored furnace control power, replaced questionable thermostat
wiring, and identified an open high-pressure safety switch. Day 29 continued
from that checkpoint.

The diagnostic path had already crossed several layers:

- the fried 3-amp furnace control-board fuse was replaced
- the thermostat's 2-amp slow-blow glass fuse was tested and showed healthy
  resistance around 0.2 to 0.5 ohms
- voltage-drop behavior exposed compromised low-voltage control wiring
- new 18/5 solid copper thermostat wire was pulled through the basement
  joists
- the high-pressure safety loop tested `OL`, or open line

That last result mattered. The high-pressure cutout switch had failed open.
Because the switch belongs to the equipment's safety circuit, it could not be
treated as a disposable obstacle. A temporary control-wiring bypass was used
strictly to gather diagnostic evidence, not as a permanent repair.

With the control path temporarily isolated for testing, the contactor engaged,
the condenser fan ran, and the compressor drew power. Measurements across the
capacitor's `C` and `HERM` terminals showed roughly 325V AC under load.

The electrical behavior was increasingly coherent.

## Moving Beyond The Control Circuit

The next question was whether the compressor itself showed an obvious
electrical winding failure.

Resistance testing across the compressor winding combinations found no open
windings. That did not prove the compressor was mechanically healthy, but it
removed another major branch from the fault tree.

Thermal evaluation then provided the more important signal. Even while the
compressor was drawing power, the indoor evaporator casing remained around
79 degrees Fahrenheit. The system was electrically active without producing
a meaningful cooling effect.

By that point, the remaining likely failure domain had shifted away from
low-voltage controls and toward refrigeration or mechanical behavior:

- total refrigerant loss
- a major refrigerant leak
- internal compressor valve failure

That boundary matters. Refrigerant systems and mechanical compressor failures
require appropriate professional evaluation. The responsible outcome was not
to keep bypassing safety controls or replacing parts speculatively. It was to
document the evidence, narrow the fault domain, and stop at the point where
the next work requires specialized service.

## Engineering Outside Software

The AC troubleshooting reinforced a lesson from Day 28: engineering habits
travel well.

The process remained methodical:

- inspect the system before changing it
- identify the first point where expected behavior stops
- test one assumption at a time
- distinguish a diagnostic bypass from a repair
- respect the protective controls
- move to a new fault domain when the evidence requires it

There was also a useful humility in learning an unfamiliar system. Software
engineers are comfortable being experts inside familiar abstractions. A
physical system removes that comfort quickly. The multimeter results, wiring
diagram, and thermal behavior matter more than confidence.

The goal is not to pretend unfamiliarity does not exist. The goal is to work
carefully enough that unfamiliarity becomes structured learning rather than
reckless improvisation.

## Phase 14 Architectural Deadlock

The `lingua-core-platform` work began from a different kind of stalled system.

Phase 14 had reached an architectural deadlock. Multiple implementation
assessments found no warranted slice to build. Delivery-layer concepts had
been named, but they had not been grounded strongly enough in the
architecture for implementation to proceed without speculation.

The conflict involved three legitimate constraints:

- Documentary Derivation
- No Speculative Extensibility
- delivery-boundary scope

The repository's governance model was doing its job. It prevented the
implementation from inventing a route layer merely because Phase 14 expected
one. The absence of a warranted slice was not a productivity failure. It was
evidence that the architecture had not yet carried enough information.

That shifted the work from implementation pressure to architectural
grounding.

## Grounding The Delivery Boundary

`ARCHITECTURE.md` was updated with a Delivery Boundary Layer. The work also
grounded Static Content Address as a legitimate architectural concept and
aligned `ADR-0013` with the clarified model.

The key clarification was that delivery route contracts could derive directly
from the Phase 13 projections. That made the Phase 14 boundary concrete
without widening it speculatively.

The change was modest in the right way. It did not invent a new runtime,
transport framework, or general-purpose extensibility mechanism. It
documented the architectural relationship that the next implementation slice
needed to follow.

Once that grounding existed, the first warranted route contract became
visible:

```text
ReadingPrimitiveSearchProjectionRouteDeliveryContract
```

The implementation added 18 tests, updated the schema literal and barrel
exports, and refreshed `SESSION_STATE.md` and `CLAUDE.md`. Validation remained
green at a baseline of roughly 788 tests across 58 files with 92.67% coverage.

The important part was not simply that a contract landed. The contract could
now explain why it was allowed to exist.

## Opening The Parallel Route Slices

With the first route contract grounded, the second parallel slice could be
assessed against evidence rather than analogy alone:

```text
WritingPrimitiveSearchProjectionRouteDeliveryContract
```

That implementation also added 18 tests, made an append-only barrel export
update, refreshed documentation, and passed validation. The resulting
baseline reached roughly 806 tests across 59 files with 92.7% coverage.

A third route contract was then assessed and authorized:

```text
SpellingEntrySearchProjectionRouteDeliveryContract
```

The spelling route raised a useful identity-field question. That concern was
resolved by checking the derivation boundary carefully. The route contract
derives from `SpellingEntrySearchProjection`, not directly from
`SpellingEntry`. The existing projection already defines the relevant
delivery shape.

That distinction is exactly why governance-driven implementation matters.
Similar-looking slices should still be assessed individually. Structural
parallelism is useful evidence, but it is not permission to skip derivation.

## Governance As A Debugging Tool

The Phase 14 deadlock initially looked like blocked implementation. In
practice, it was an architectural diagnostic result.

The governance constraints exposed the actual failure:

```text
Named delivery concept
-> insufficient architectural grounding
-> no warranted implementation slice
-> architecture clarification
-> documentary derivation restored
-> route contracts authorized
```

That is closely related to the AC investigation.

When the outdoor unit failed to start, the right move was not to keep
replacing components. It was to measure the control path and locate the open
circuit. When Phase 14 could not produce a justified slice, the right move was
not to force code into the repository. It was to inspect the architecture and
locate the missing derivation boundary.

In both cases, the constraint was useful. Safety controls protected the HVAC
equipment. Governance controls protected the platform architecture.

Bypassing either one casually would have made the system harder to trust.

## Outcome

Day 29 closed with more clarity in both domains.

The AC troubleshooting reached a responsible technical boundary. The
low-voltage path was restored, the failed safety switch was identified, the
compressor windings showed no open combinations, and the system's inability
to cool was narrowed to likely mechanical or refrigerant-related causes.

`lingua-core-platform` moved from Phase 14 deadlock into grounded delivery
work. The architecture now defines the delivery boundary more clearly. Static
Content Address has an explicit place in the model. Two warranted route
contracts landed with validation green, and a third parallel spelling route
contract was assessed and authorized.

The shared lesson was simple: progress is not the same as motion.

Sometimes the fastest responsible way forward is to stop trying to implement
the next thing and identify the missing piece of the model. Once the system is
understood more accurately, the next step usually becomes smaller, safer, and
easier to defend.

## Definition Of Done

Day 29 reached a meaningful completion point:

- the 3-amp furnace board fuse replacement remained verified
- the thermostat's 2-amp slow-blow fuse tested healthy
- the compromised thermostat wiring was replaced with 18/5 solid copper cable
- the high-pressure safety loop tested open
- the contactor, condenser fan, and compressor behavior were isolated
- capacitor `C` and `HERM` terminals showed roughly 325V AC under load
- compressor winding combinations showed no open circuits
- the indoor evaporator casing remained around 79 degrees Fahrenheit
- remaining AC failure modes were narrowed to mechanical or refrigerant
  causes requiring appropriate service
- the Delivery Boundary Layer was grounded in `ARCHITECTURE.md`
- Static Content Address and `ADR-0013` were aligned with the clarified model
- reading and writing route delivery contracts landed with 18 tests each
- the spelling route delivery contract was assessed and authorized
- the platform validation baseline remained green at roughly 806 tests across
  59 files with approximately 92.7% coverage

The day was a practical reminder that quality gates are not friction to work
around. They are instruments for finding the real problem.
