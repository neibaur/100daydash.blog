---
title: "Day 40 - June 10, 2026: App-Tier Discipline and Governed Game Foundations"
description: "Advancing UseThai through a tightly governed app-tier slice while turning Terminal Run from a loose concept into an implementation-ready educational game plan."
pubDate: "2026-06-10"
day: 40
dashboardSlug: "none"
dataSources:
  - "Lingua Core Platform"
  - "UseThai application shell"
  - "UseThai friction triage"
  - "Terminal Run architecture planning"
  - "Claude"
  - "pnpm"
status: "published"
tags:
  - usethai
  - lingua-core
  - app-tier-development
  - game-design
  - architecture-governance
  - ai-governance
  - security
  - scope-discipline
---

Day 40 advanced two very different projects through the same engineering
discipline.

`UseThai` moved forward through a deliberately narrow application-tier
improvement after its second friction triage. `Terminal Run` moved from a
loose game idea into a governed, implementation-ready project plan.

In both cases, progress came from deciding what the work was allowed to be
before allowing implementation momentum to define it.

For `UseThai`, that meant authorizing direction-aware presentation guidance
without reopening core search behavior. For `Terminal Run`, it meant defining
a simulated educational terminal, reducing the initial scope, and placing
security, accessibility, AI governance, and cost discipline into the design
before the first playable slice.

The shape of the day was:

```text
Confirm the authorized layer -> tighten the implementation boundary
-> deliver or define the smallest meaningful slice
-> preserve held scope -> prepare the next governed handoff
```

The projects were at different stages, but both became more mature by refusing
to confuse a compelling idea with unlimited authorization.

## Continuing The Governed UseThai App-Tier Workflow

The `Lingua Core Platform` work began by confirming the current project state.

Phase 15 remains complete. No new core slice is authorized. Phase 16 and Phase
17 remain pending authorization behind the required HANDOFF section 9 audit.
The active work lane therefore remains the operator-authorized app-tier
presentation candidates produced by the second `UseThai` friction triage.

That state mattered before reviewing any proposed implementation.

The second triage had identified a direction-guidance problem through two
observations:

- the Cluster 1 residual showed that the input placeholder still presented a
  Thai example when the selected direction was English to Thai
- `F-0019` in Cluster 12 showed that a query entered in the wrong script for
  the selected direction could silently reach a not-found result without a
  lightweight explanation

Both observations pointed toward application presentation.

Neither authorized a different lookup contract.

That distinction became the central constraint for the next Claude prompt.

## Tightening The Direction-Guidance Prompt

The proposed prompt was reviewed and tightened before implementation.

The authorized behavior was intentionally small:

- make the input placeholder reflect the selected language direction
- optionally show lightweight helper copy when a submitted query appears to
  use the wrong script for the selected direction

The prompt explicitly kept the work at the app tier. It prohibited:

- core changes
- ADR changes
- schema-literal changes
- warrant-review edits
- search or autocomplete work
- fuzzy or prefix matching
- romanized lookup
- cross-direction lookup
- automatic direction switching
- a second lookup attempt
- app-side canonicalization
- fabricated core diagnostics

Those prohibitions were not incidental prompt detail. They were the mechanism
that kept a small usability improvement from quietly becoming a search-system
redesign.

A wrong-direction hint can explain the current interface without claiming that
core diagnosed the problem. A direction-aware placeholder can make expected
input clearer without changing what lookup accepts. The application can guide
the learner while preserving the existing core contract.

The prompt therefore authorized presentation guidance, not new search
capability.

## Delivering The App-Tier Slice

Claude implemented the direction-guidance slice on:

```text
fix/usethai-direction-placeholder-hint
```

The reported implementation remained limited to two app-tier files:

```text
apps/usethai/src/lib/direction-chrome.ts
apps/usethai/src/pages/index.astro
```

The direction-chrome helper gained `placeholderForDirection`.

The page then imported that helper and `LexicalLanguageDirection`, updated
`syncDirectionChrome` so the placeholder changes with the selected direction,
added `scriptMismatchHint`, and threaded the optional hint into the no-result
rendering path.

That was the intended shape of the slice.

The existing lookup behavior remained the authority. The app gained clearer
guidance around that behavior without inventing new diagnostics, retrying in
another direction, or moving held capabilities into presentation code.

Validation was clean:

- `pnpm format:check`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`, covering 859 tests across 62 files
- `pnpm test:coverage`, reporting 92.79 percent statement coverage
- `pnpm validate`

The change merged through PR `#205` as:

```text
fix(usethai): add direction-aware placeholder and hint
```

This closed the authorized direction-guidance slice while keeping the larger
governance boundaries intact.

## Planning The UseThai State Handoff

After PR `#205` merged, the next task was not another feature.

It was planning a small `.claude/SESSION_STATE.md` update so the durable
handoff reflects the new application state.

Because the merged work was app-tier only, the core validation baseline should
remain unchanged at 859 tests, 62 files, and 92.79 percent statement coverage.
The completed core slices, schema-version literals, investigation log,
deferred scope, open doctrinal questions, and core baseline should also remain
unchanged.

The planned state update should record that:

- PR `#205` is the latest merged PR
- direction-aware placeholder guidance is now implemented
- submitted-query script-mismatch helper copy is now implemented
- user-facing error messages and URL-state persistence remain available
  second-triage app-tier presentation candidates, or the project may hold
- the application-tier current state now includes direction-aware input
  guidance
- the app-tier evidence record now includes the Cluster 1 residual and Cluster
  12 direction-guidance implementation
- the direction-aware chrome learning now covers the heading, document title,
  placeholder, and submitted-query mismatch helper copy

A follow-up prompt was prepared for a session-state-only documentation change.

That separation preserves a useful project habit:

```text
Implement the authorized slice.
Merge it.
Then make the durable state accurately describe what changed.
```

The state update remains documentation work, not permission to begin another
app-tier candidate or reopen held core-search ideas.

## Moving Terminal Run From Idea To Project

The second major effort began at a much earlier project stage.

`Terminal Run` started as a loose game idea with several possible directions:
an endless runner, a terminal-themed typing game, a Linux learning platform,
or a broader DevOps training experience.

The strongest concept emerged as a cyberpunk educational puzzle RPG.

Players would restore a fractured digital world by using Linux, Git, Docker,
CI/CD, and cloud-computing concepts through a fully simulated terminal
interface. The project would be game-first, with technical learning embedded
inside exploration and problem solving rather than presented as a sequence of
dry command lessons.

The narrative foundation centers on a global infrastructure AI that has
fractured and caused digital systems to fail. The player becomes an Operations
Apprentice traveling through corrupted environments:

- Linux Archive
- Git Repository Caverns
- Docker Foundry
- CI/CD Citadel
- Kubernetes Wastelands
- Cloud Nexus

A drone companion became the primary vehicle for onboarding, hints, feedback,
and narrative guidance.

This concept gave the project a world, a player role, and an educational
purpose. The next work was making sure the architecture could support those
ideas without creating unacceptable security or scope risk.

## Establishing The Simulated-Terminal Boundary

The most important technical boundary is simple:

```text
Terminal Run is a simulated educational environment, not a real shell.
```

The design prohibits:

- real command execution
- `eval`
- `Function()`
- `child_process`
- dynamic code execution

Player commands must be treated as untrusted text. All resulting output must
remain inert. Game content must remain data-only and may never contain
executable code.

This boundary is central to the product, not merely a later hardening task.

A terminal-shaped interface naturally invites assumptions about command
execution. Rejecting real shell behavior from the beginning makes the trust
model explicit. The game can teach command concepts and reward correct
reasoning without giving user input a path to the host environment.

Security joined accessibility, AI governance, and cost governance as a
first-class design concern from the start.

## Reducing Scope Before Building

The original concept included approximately 120 commands and concepts.

Architecture review challenged that scale and concluded that a much smaller
command set would create greater educational value while dramatically reducing
implementation complexity.

The initial release is now focused on three zones:

- Linux Archive
- Git Repository Caverns
- Docker Foundry

The later zones can remain visible in the world, but they should stay locked as
future content rather than becoming implied v1 commitments.

The most important delivery decision was to build a vertical slice before a
platform.

Instead of completing a broad game engine and content system before learning
whether the core experience is enjoyable, the first slice will target Levels
1 through 5 of the Linux Archive.

The question is not whether the project can model every future zone.

It is whether players enjoy the central loop enough to justify more project.

That decision was formalized alongside four other governance mechanisms:

- `ADR-15: Vertical Slice Before Platform`
- `ADR-16: Accessibility First`
- `ADR-17: Scope Discipline`
- `ADR-18: Named Moment content governance`
- `ADR-19: Cost-Constrained Architecture`

Together, these ADRs turn project restraint into an explicit operating model.

## Designing For Memorable Learning

The concept of a `Named Moment` emerged to keep Terminal Run from becoming a
technical tutorial wearing game visuals.

Each level should contain a memorable player-driven discovery or experience.
The design emphasis shifts from simply teaching commands toward creating
curiosity, mystery, exploration, and problem solving.

The mistake-classifier system became another core educational feature.

Rather than only labeling a submitted command correct or incorrect, the game
should recognize common mistake classes and provide targeted guidance. Failure
then becomes part of the learning loop instead of merely a penalty.

These two ideas work together.

Named Moments give a level something worth remembering. Mistake
classification gives the player a more useful path through uncertainty. The
drone companion can deliver guidance and narrative feedback without replacing
the player's own discovery.

The result is a more promising educational model than a command checklist.

## Governing Agents, Costs, And Repository Exposure

AI-assisted development was also brought under explicit governance.

The project plans to use an `AGENTS.md` contract for future Claude, Codex, and
other agent sessions. Agents should operate with strict repository contracts,
limited permissions, mandatory validation, and human-controlled trust
boundaries.

This mirrors the broader architecture posture. User commands are untrusted
inside the game, and agent actions are bounded during development. In both
cases, capability should follow explicit authorization.

Cost governance produced an equally strong constraint.

The planned architecture favors static export with:

- no backend
- no accounts
- no runtime AI APIs
- no hosted database
- no recurring infrastructure requirement

The guiding observation was:

```text
Revenue is optional. Recurring costs are mandatory.
```

The project should remain sustainable even if it never produces meaningful
revenue. A static architecture hosted through Cloudflare Pages could keep
operational costs near zero while preserving future monetization options.

Repository visibility received the same kind of deliberate treatment. The
recommendation is to keep the repository private through Gate `#1`
playtesting, then reconsider visibility after the vertical slice has been
tested.

The most valuable intellectual property may ultimately be the curriculum
design, mistake-classifier behavior, level progression, and drone-guidance
patterns rather than the engine alone. The project should gather evidence
before deciding how much of that work to expose.

## Transitioning Terminal Run Into Implementation

The day concluded by moving Terminal Run from architecture review into
implementation planning.

The resulting plan covers:

- Phase 0 repository setup
- security hardening
- AI governance controls
- monorepo structure
- a walking-skeleton development strategy
- session-by-session implementation sequencing
- vertical-slice milestones
- playtest gates

The plan front-loads a working terminal experience rather than engine
completeness.

The first meaningful milestone is intentionally small: type `pwd` in a browser
and receive output from the simulation. The first playable game moment is
expected around Session 9, with the first kitchen-table playtests shortly
afterward.

The next planned artifacts are:

- `AGENTS.md`
- the Style Bible
- a playtest observation template
- the Session 1 development charter

Architecture, governance, security, scope management, accessibility, AI
controls, and cost governance are now mature enough for the next effort to
focus on implementation.

## Why The Day Mattered

Day 40 showed governance working at two project stages.

`UseThai` already had a mature core, a completed phase, evidence-backed
friction observations, and a narrow app-tier candidate. Its challenge was to
improve the learner experience without allowing a presentation fix to drift
into core search behavior.

`Terminal Run` had a compelling concept but no implementation yet. Its
challenge was to define enough boundaries that implementation could begin
without building an unsafe shell, an oversized platform, or an expensive
service before proving the game loop.

The shared lesson was:

```text
Project maturity is not measured only by how much has been built.
It is also measured by how clearly the next work is bounded.
```

UseThai's direction-aware placeholder and mismatch hint were useful because
they stayed app-tier. Terminal Run's architecture became implementation-ready
because it rejected real command execution, reduced v1 scope, prioritized a
vertical slice, and made accessibility, AI, security, and recurring costs
governed concerns.

Both efforts ended with a smaller, clearer next action.

## Outcome

Day 40 advanced `UseThai` through a tightly controlled app-tier presentation
slice and advanced `Terminal Run` through a substantial project-definition
checkpoint.

For `UseThai`, the current state was confirmed before implementation: Phase 15
remains complete, no new core slice is authorized, and Phase 16 and Phase 17
remain behind their audit and authorization gates. The Claude prompt for
direction-aware input guidance was narrowed to prevent core, schema, ADR,
search-capability, romanized-lookup, cross-direction, and diagnostic scope
drift.

Claude implemented the authorized app-tier behavior in
`direction-chrome.ts` and `index.astro`. Validation passed, and PR `#205`
merged as `fix(usethai): add direction-aware placeholder and hint`. A separate
session-state-only follow-up was planned so the durable project handoff can
reflect the merged behavior without changing the core baseline or authorizing
new work.

For `Terminal Run`, the cyberpunk educational puzzle RPG concept became the
selected direction. The simulated-terminal trust boundary, reduced v1 zone
scope, five new ADRs, Linux Archive vertical slice, Named Moments,
mistake-classifier design, AI-agent contract, near-zero-cost static
architecture, private-repository posture, and playtest-gated implementation
plan moved the project from ideation toward execution.

The day closed with one small product slice merged and one new project ready
to begin building under explicit constraints.

## Definition Of Done

Day 40 reached an app-tier delivery and governed project-foundation
checkpoint:

- confirmed Phase 15 remains complete
- confirmed no new Lingua core slice is authorized
- kept Phase 16 and Phase 17 behind the HANDOFF section 9 audit and
  authorization gates
- continued from the second `UseThai` friction triage
- reviewed and tightened the Claude direction-guidance prompt
- authorized direction-aware placeholder text
- authorized optional submitted-query script-mismatch helper copy
- kept the implementation app-tier only
- prohibited core, ADR, schema, warrant-review, and search-capability changes
- kept romanized lookup, cross-direction lookup, automatic switching, and
  second-lookups out of scope
- prohibited app-side canonicalization and fabricated core diagnostics
- implemented the slice on `fix/usethai-direction-placeholder-hint`
- changed only `apps/usethai/src/lib/direction-chrome.ts` and
  `apps/usethai/src/pages/index.astro`
- passed format, lint, typecheck, test, coverage, and validation checks
- preserved the 859-test, 62-file, 92.79-percent core validation baseline
- merged PR `#205` as
  `fix(usethai): add direction-aware placeholder and hint`
- planned a separate `.claude/SESSION_STATE.md` follow-up
- kept remaining app-tier candidates separate and unauthorized
- selected a cyberpunk educational puzzle RPG direction for Terminal Run
- established the fractured-infrastructure-AI narrative
- established the Operations Apprentice player role
- defined the initial world zones and drone companion
- made Terminal Run a simulated terminal rather than a real shell
- prohibited real command execution, `eval`, `Function()`, `child_process`,
  and dynamic code execution
- required user commands to remain untrusted text
- required game content and output to remain inert and data-only
- reduced the initial scope to Linux Archive, Git Repository Caverns, and
  Docker Foundry
- kept later zones visible but locked as future content
- established ADRs 15 through 19
- prioritized Linux Archive Levels 1 through 5 as the vertical slice
- introduced Named Moments as a content-governance mechanism
- made mistake classification a core educational feature
- planned an `AGENTS.md` contract for governed AI-assisted development
- selected a static-export, near-zero recurring cost posture
- recommended keeping the repository private through Gate `#1` playtesting
- created a phased implementation and playtest plan
- identified `AGENTS.md`, the Style Bible, the playtest observation template,
  and the Session 1 development charter as the next artifacts

The day ended with governance doing its most practical job: making the next
implementation step smaller, clearer, and more trustworthy.
