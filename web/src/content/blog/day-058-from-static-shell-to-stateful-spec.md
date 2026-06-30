---
title: "Day 58 - June 28, 2026: From Static Shell to Stateful Spec"
description: "A Day 58 reflection on HaoMiantiao M6 app-shell delivery, repo-grounded specification review, negative-path validation, governance refresh, and planning the M7 matchup screen."
pubDate: "2026-06-28"
day: 58
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao M6 app-shell spec"
  - "HaoMiantiao PR #47"
  - "HaoMiantiao commit bc5415d"
  - "HaoMiantiao M7 matchup-screen spec planning notes"
  - "Claude Project knowledge refresh notes"
  - "Sonnet PR review notes"
  - "Opus M6 implementation notes"
  - "reviewing-pull-requests skill eval notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - specs
  - haomiantiao
  - code-review
  - evals
  - nextjs
  - developer-experience
---

Day 58 was the day the app tier became real without letting the process get
loose.

That sounds like a UI milestone, but it was more than that.

HaoMiantiao moved from the M5 data package into M6, the app-shell milestone.
The visible result was a Next.js static-export shell. The more important
result was that the shell landed through the same governed loop the earlier
engine and data work had been teaching me to trust: repo-grounded spec
drafting, implementation handoff, independent review, negative-path
verification, documentation refresh, and then the next spec.

The day started with a question about Claude repository access.

It ended with M6 merged, governance refreshed, and M7 shaped into a much more
serious milestone: the first interactive screen that will import engine and
data, manage client state, persist bracket progress, and turn the M6 Start
affordance into a real `/play` route.

The useful part was not that each step was perfect.

The useful part was that each step left evidence.

## Clarifying The Context Layer

The first thread was not code at all.

I needed to clarify what kind of repository access Claude had in normal chat
and what that meant for the workflow.

The answer was practical. Chat-level GitHub access is mostly an attach-file
mechanism. It can help with spot checks, but it is not the same as live repo
traversal. Claude Projects, with their synced project knowledge, are the
better default for repo-wide context. Claude Code remains the right surface
for branch work, file traversal, implementation, and pull-request execution.

That clarification mattered because the project had been relying more and
more on durable context.

If the agent is drafting a spec, it should not be guessing from stale chat
memory. If the repo has changed after a merge, the project knowledge store
needs to be refreshed. If a file needs a spot check, attach it deliberately.
If the work requires live traversal, use Claude Code.

That became the practical rule:

- refresh the Project knowledge store after meaningful merges
- use attached files for narrow verification
- use Claude Code for live repo work
- keep spec drafting grounded in synced project context

That is not glamorous.

It is also the kind of boring clarity that prevents a workflow from quietly
splitting into several competing versions of the truth.

## Grounding M6 Before Implementation

The M6 app-shell spec started from repository evidence, not vibes.

The grounding set included `DESIGN.md`, `PROJECT_STATE.md`, ADRs, `AGENTS.md`,
package scripts, Vitest config, the workspace layout, and the dependency
policy.

That review surfaced several important constraints.

Before M6, `apps/web` did not exist. The workspace only covered `packages/*`.
That meant the app tier was not merely missing a page. It was not registered
as an application workspace yet.

At the same time, the existing CI build job already ran:

```bash
pnpm -r --if-present run build
```

That was a useful discovery. If `apps/web` had its own build script, the
existing recursive build check would pick it up without modifying `.github/**`.
The right implementation could strengthen the gate without touching protected
workflow files.

The dependency story also needed care.

The repo was intentionally ahead of stale model memory: TypeScript 6, ESLint
10, Vite 8, React 19, and Next 16. Those versions had to be verified live
before the spec could make confident claims. `eslint-plugin-jsx-a11y` was
deferred because its peer range did not declare ESLint 10 support. Manual
accessibility discipline stayed the M6 path instead of forcing a dependency
that did not yet match the repo's toolchain.

That is exactly where specs need to be living contracts.

A spec is not useful if it freezes assumptions from yesterday's package
ecosystem and then punishes implementation for reality changing.

## Correcting The Spec

The first M6 draft needed correction before it was ready.

The fixes were concrete.

Use vanilla CSS variables and CSS Modules, not Tailwind.

Keep the landing page pure static. The app shell should not import engine or
data yet.

Split M6 into a maintainer dependency/setup PR and an agent implementation PR.
Dependency and workspace registration changes are maintainer-owned setup, not
agent-owned implementation.

Prefer an explicit web build script that validates data first, then runs
`next build`.

Scope web coverage honestly so app smoke tests do not dilute engine and data
coverage.

Those changes made the spec smaller and more honest.

M6 was not the milestone where the product became interactive. It was the
milestone where the app tier became present, buildable, and governed.

That boundary matters.

If M6 had quietly imported engine and data, then M7 would inherit a blurry
contract. If M6 had taken on styling framework changes, dependency churn, and
interactive state all at once, the shell would stop being a shell and become
an excuse to overload the milestone.

The reviewed spec gave the handoff a clean shape.

## The M6 Handoff

After the maintainer dependency/setup PR prepared the app framework
dependencies, Opus implemented the M6 app shell in PR #47.

The implementation added the Next.js static-export app shell, design tokens,
the landing page, a web Vitest project, and a build hook that runs data
validation before `next build`.

Two implementation findings were worth recording because they changed the
shape of the spec in practice.

First, Next 16.2.9 no longer supports the `eslint.ignoreDuringBuilds` config
key. The spec had intended to avoid double linting during build, but the right
way to satisfy that intent was to omit the invalid key rather than force the
old config shape.

That is the good version of implementation deviation.

The acceptance criterion was no longer literally satisfiable with the pinned
framework version. The implementation did not fabricate a workaround. It
documented the mismatch and preserved the underlying intent.

Second, Vitest project roots needed to be anchored to `import.meta.dirname` so
filtered package commands resolved correctly from non-root working
directories.

That kind of detail is easy to lose in a summary, but it matters. Tooling that
only works when run from one directory is not really a repo-level tool yet.

M6 was supposed to make the app tier fit the existing governance model.

Those findings were part of proving that it did.

## Reviewing More Than The Happy Path

I ran the pull-request review skill against PR #47 using Sonnet.

The advisory review found no blocking issues.

That was useful, but I did not want the review loop to stop at "the reviewer
was happy" or "the table was green."

The important check was negative-path verification.

I intentionally broke `packages/data/noodles.json` on the branch and confirmed
that both commands failed as expected:

```bash
pnpm -r --if-present run build
pnpm validate
```

Then I fixed the data file and confirmed validation passed again.

That was the most reassuring part of the M6 merge.

The shell was static, but the gate was not decorative. A malformed data
package failed the app build path. That meant the new app tier did not sit
beside governance. It participated in it.

PR #47 merged to main at commit `bc5415d`.

The app shell existed.

The guardrails still held.

## Refreshing Governance After The Merge

After M6 merged, I refreshed the project knowledge store.

That was the direct consequence of the context-layer decision at the start of
the day. Meaningful merges should update the shared project context before the
next spec-drafting loop begins.

Then the M6 review itself turned into governance work.

I asked whether the PR review skill's eval corpus needed new cases or new
results after this run. The answer was yes for results, and optionally yes for
a new case around a fresh review axis.

The axis was subtle but important:

an acceptance criterion became unfulfillable because the pinned framework
version had moved on.

The correct review behavior is not to invent a defect. It is also not to
silently ignore the mismatch. The correct behavior is to accept a documented
implementation deviation when the implementation preserves the spec's
underlying intent.

That is exactly the kind of case a review skill needs.

The agent should be able to distinguish "the code failed the contract" from
"the literal contract named an obsolete config key, and the implementation
adapted responsibly."

I prepared and merged a human-only governance PR touching the appropriate
documentation and eval surfaces. Then I ran a scoped Sonnet reconciliation
audit focused on stale counts, stale docs, and cross-file consistency after
that governance pass.

The audit fixes were applied and merged to main.

Then the repository and project knowledge were refreshed again.

This is the part of agent-assisted work that still feels easy to underrate.
The merge is not the end of the loop. The loop ends when the durable project
state can guide the next fresh session without smuggling context through
memory.

## Opening M7

With M6 merged and governance refreshed, the next milestone planning loop
started.

M7 is the matchup screen.

That changes the project again.

M6 proved the app tier could exist as a static shell. M7 is where the app
starts touching the engine and data packages. It is the first real interactive
screen, the first client-state milestone, and the first place where
persistence belongs.

The fresh-chat prompt for `specs/m7-matchup-screen.md` emphasized that M7
needs live dependency verification again. It also emphasized the boundary
problem: M7, M8, and M9 need to be drawn carefully so the first interactive
screen does not absorb every future feature.

After review and revision, the M7 decisions became clear.

M7 uses `/play`, and the M6 Start affordance becomes a real link.

M7 adds interaction with the engine: two noodle cards, picking winners,
progress labels, and round labels.

Persistence lands in M7, not M9, using `serializeBracket` and
`deserializeBracket` with `localStorage` behind `try/catch`.

Malformed, stale, or unreadable storage falls back to a fresh bracket without
crashing.

No public `getContestants()` API is added to `packages/data`. The existing
`getNoodles()` shape structurally satisfies the engine's `{ id, seed }`
contestant contract.

`getTournament()` is the only new data accessor.

`@testing-library/user-event` is the explicit default interaction-test
dependency.

Implementation should likely happen as two agent PRs after the maintainer
dependency PR:

- `feat/matchup-screen-core`
- `feat/matchup-screen-advance`

The deferrals also mattered.

Random seeding, detail drawer, buy links, images, affiliate disclosure,
champion/share, play-again, `eslint-plugin-react`, `react/no-danger`, and
`jsx-a11y` stay out of M7.

That is the difference between a milestone and a wish list.

## Why The Day Mattered

Day 58 mattered because the workflow matured again.

Claude Project sync became the source-of-truth context layer for broad
repo-aware drafting. Claude Code stayed the live implementation surface.
Attached files stayed useful for spot checks, but not as a substitute for
project context.

The M6 spec became a living contract. It was corrected before implementation,
then corrected again by implementation reality when Next 16 had moved past an
old config key.

The PR review skill became more than an advisory reviewer. Its run produced
evidence for code quality and evidence for the review skill's own eval
surface.

The negative-path check mattered more than a green happy-path table. Breaking
`noodles.json` and seeing the build and validation fail proved that the app
tier was wired into the data gate.

The app shell itself was deliberately modest.

It did not make the product done.

It made the next product work possible without abandoning governance.

That is the real line Day 58 crossed.

HaoMiantiao now has an app tier. The matchup screen is specified, not
implemented. The next work will be more interactive, more stateful, and more
user-facing.

The process will need to get sharper as the product gets less abstract.

Today showed that the human and agent loop can tighten instead of loosen when
the surface area grows.

## Outcome

Day 58 moved HaoMiantiao through the M6 app-shell milestone and into reviewed
M7 matchup-screen planning.

The day started by clarifying Claude repository access. Chat-level GitHub
access is best treated as attach-file support for spot checks. Claude Projects
sync is the right default for broad repo context. Claude Code remains the
right surface for live traversal, branch work, and PR implementation. The
practical workflow is to refresh Project knowledge after meaningful merges,
attach files only for narrow checks, and keep spec drafting grounded in synced
project context.

The M6 app-shell spec was grounded against the repository before
implementation. The review confirmed that `apps/web` did not yet exist, the
workspace only covered `packages/*`, and the existing recursive build command
could pick up an app build script without changing `.github/**`.

The M6 spec was corrected before it was marked reviewed: vanilla CSS variables
and CSS Modules instead of Tailwind, a pure static landing page with no
engine/data import, a maintainer-owned dependency/setup PR before agent
implementation, an explicit build script that validates data before
`next build`, and honest web coverage that does not dilute engine/data
coverage.

Opus implemented M6 in PR #47 after the maintainer setup work. M6 added the
Next.js static-export app shell, design tokens, landing page, web Vitest
project, and a build hook that runs data validation before `next build`.

Two implementation findings were recorded. Next 16.2.9 no longer supports
`eslint.ignoreDuringBuilds`, so the implementation omitted the invalid config
key while preserving the spec's no-double-lint intent. Vitest project roots
needed `import.meta.dirname` so filtered package commands resolved correctly
from non-root working directories.

Sonnet reviewed PR #47 and found no blocking issues. I also performed the
negative-path check manually by breaking `packages/data/noodles.json` and
confirming that both `pnpm -r --if-present run build` and `pnpm validate`
failed as expected. After restoring the data file, validation passed again.
PR #47 merged to main as `bc5415d`.

After the merge, I refreshed the project knowledge store, updated governance
and eval surfaces, and ran a scoped Sonnet reconciliation audit for stale
counts, stale docs, and cross-file consistency. Those audit fixes were merged,
and the project knowledge was refreshed again.

M7 planning then started. The reviewed M7 direction is `/play`, real Start
linking from the M6 shell, two noodle cards, winner selection, progress and
round labels, engine interaction, and localStorage persistence using
`serializeBracket` and `deserializeBracket` behind `try/catch`. Malformed,
stale, or unreadable storage falls back to a fresh bracket without crashing.

M7 will not add a public `getContestants()` API. `getNoodles()` structurally
satisfies the engine's `{ id, seed }` contestant shape, and `getTournament()`
is the only new data accessor. `@testing-library/user-event` is the explicit
default interaction-test dependency. Implementation should likely split into
`feat/matchup-screen-core` and `feat/matchup-screen-advance` after the
maintainer dependency PR.

## Definition Of Done

Day 58 reached the M6-to-M7 governance checkpoint:

- clarified Claude chat, Project, and Claude Code repository-access roles
- treated Project sync as the broad source-of-truth context layer
- kept attached files for spot checks
- kept Claude Code as the live repo traversal and implementation surface
- grounded the M6 spec in `DESIGN.md`, `PROJECT_STATE.md`, ADRs, `AGENTS.md`,
  package scripts, Vitest config, workspace layout, and dependency policy
- verified that `apps/web` did not exist before M6
- verified that `pnpm-workspace.yaml` only covered `packages/*`
- identified that the existing recursive build job could activate an app
  build script without touching `.github/**`
- kept workspace registration and lockfile changes as maintainer-owned setup
- live-checked dependency reality around TypeScript 6, ESLint 10, Vite 8,
  React 19, and Next 16
- deferred `eslint-plugin-jsx-a11y` because its peer range did not declare
  ESLint 10 support
- corrected the M6 spec to use vanilla CSS variables and CSS Modules
- kept the M6 landing page pure static
- split M6 into maintainer setup and agent implementation
- required web build to validate data before `next build`
- scoped web coverage so smoke tests did not dilute engine/data coverage
- used the reviewed M6 spec to drive implementation
- landed the M6 app shell in PR #47
- recorded that Next 16.2.9 no longer supports `eslint.ignoreDuringBuilds`
- accepted omission of the invalid config key as the correct implementation
  deviation
- anchored Vitest project roots with `import.meta.dirname`
- ran a Sonnet advisory review on PR #47
- confirmed the review found no blocking issues
- intentionally broke `packages/data/noodles.json` to verify failure paths
- confirmed `pnpm -r --if-present run build` failed on malformed data
- confirmed `pnpm validate` failed on malformed data
- restored the data file and confirmed validation passed again
- merged PR #47 to main at `bc5415d`
- refreshed the Project knowledge store after merge
- updated governance and eval surfaces after M6
- captured the review-axis case for documented implementation deviation
- ran a scoped Sonnet reconciliation audit after the governance pass
- applied and merged stale-count, stale-doc, and consistency fixes
- refreshed repository/project knowledge again
- generated the M7 matchup-screen spec prompt
- reviewed and revised the M7 spec direction
- selected `/play` as the M7 route
- made the M6 Start affordance a real link
- scoped M7 to two noodle cards, winner selection, progress labels, and round
  labels
- placed persistence in M7 using `serializeBracket`, `deserializeBracket`, and
  `localStorage` behind `try/catch`
- required malformed, stale, or unreadable storage to fall back safely
- avoided adding a public `getContestants()` API
- kept `getTournament()` as the only new data accessor
- chose `@testing-library/user-event` as the default interaction-test
  dependency
- planned likely follow-up implementation PRs for matchup core and matchup
  advance
- deferred random seeding, detail drawer, buy links, images, affiliate
  disclosure, champion/share, play-again, `eslint-plugin-react`,
  `react/no-danger`, and `jsx-a11y`
- kept the product status honest: the app shell exists, and the matchup
  screen is specified but not implemented yet
