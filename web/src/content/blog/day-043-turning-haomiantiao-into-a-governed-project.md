---
title: "Day 43 - June 13, 2026: Turning Haomiantiao Into a Governed Project"
description: "Turning a noodle-content idea into a governed haomiantiao project with a narrowed MVP, scoped repo template, bot identity, and the first bracket-engine slice."
pubDate: "2026-06-13"
day: 43
dashboardSlug: "none"
dataSources:
  - "haomiantiao product ideation"
  - "haomiantiao repository"
  - "project template repository"
  - "Phase 0 drills"
  - "GitHub Actions"
  - "Codex"
  - "Claude"
status: "published"
tags:
  - haomiantiao
  - product-design
  - repository-governance
  - ai-governance
  - security
  - typescript
  - developer-experience
  - phase-0
---

Day 43 began with a loose noodle-and-food-content idea and ended with a
governed codebase pattern.

`haomiantiao` moved from a broad concept into a specific product direction,
a narrower MVP, a stricter repository contract, a separate bot identity, and
the first implementation slice of the bracket engine.

That was the real shape of the day: not "idea to app", but "idea to a
project that can actually be built safely and repeatedly."

## Choosing The Product

The first important decision was not technical. It was choosing what
`haomiantiao` actually is.

I started from a broader food-guessing-game idea for a Chinese or bilingual
audience, then compared several possible directions:

- noodle guessing game
- menu decoder
- noodle finder
- Chinese regional noodle guide
- personality quiz
- noodle passport
- recurring content

The `Instant Noodle World Cup` won because it had the best mix of product
clarity and implementation realism.

It is a real category with an existing fandom. It has obvious shareability.
It leaves room for affiliate potential without forcing that question into the
first release. Most importantly, it fits a clean static-site path.

The MVP narrowed to something much more disciplined:

```text
16-noodle bracket
evergreen first bracket
personal bracket only
static site
no backend
no database
no accounts
browser-local state via localStorage
compact clickable product cards
shareable champion/result
```

That scope cut removed a lot of future work on purpose. Live voting,
accounts, detailed product pages, heavy SEO, and gamified progression are all
possible later questions. They were not the right questions for day one.

The day needed a product that could become real without becoming large.

## Turning The Template Into A Contract

After the product shape was clearer, I created the new repository from my
`project-template`.

The important lesson was that the template is not just a starter skeleton.
It is a governance contract.

It brought along the parts that should be boring and dependable:

- pnpm workspace structure
- strict TypeScript
- Vitest and a coverage floor
- five-check CI
- `AGENTS.md` constraints
- human-only protected paths
- one concern per PR
- `<=400` changed lines
- tests-first where it matters
- no agent-added dependencies

I then added the project-specific pieces that make the contract real for
`haomiantiao`:

- a project-specific `AGENTS.md`
- a proprietary, all-rights-reserved license
- a license ADR
- ADRs for static export and client-only state
- `docs/DESIGN.md` for the architecture and milestone plan
- `docs/PROJECT_STATE.md` as the durable status and orientation doc

I also removed stale template leftovers so the repo would stop feeling like a
starter kit and start feeling like an actual project.

This was commercial groundwork, so the repo stayed private. The point was to
keep the first release path simple, governed, and local-first.

## Running Phase 0 Before Trusting The Rails

The day's security and governance drills did their job.

They were not there to make the repository look safe. They were there to see
whether the guardrails could be fooled.

One drill exposed a real fail-open bug in the forbidden-pattern CI check.
The workflow was scanning `apps` and `packages`, but `apps/` did not exist
yet. `grep` errored, and the `! grep ... || ...` structure treated that error
like success.

That is exactly the kind of bug Phase 0 should catch:

```text
the check ran, but it was not actually protecting anything yet
```

The fix was to scan only existing directories and fail closed when `grep`
hit an error.

That changed the result from "the workflow exists" to "the workflow really
means what it says."

I also confirmed the broader lesson that the most useful drills are the ones
that make the control fail before the project depends on it.

## Splitting Human And Bot Work

The workflow around AI-assisted development became more concrete too.

I set up a dedicated bot identity, `neibaur-ai-bot-1`, with write access but
not admin access, and added it to a `bots` team.

I also separated the work into two clones:

- a human clone for human-authored governance and protected-path changes
- a bot clone for AI-assisted implementation work

That split matters because it makes trust boundaries visible instead of
implied.

The GitHub CLI still wanted the maintainer's keyring credentials unless
`GH_TOKEN` was explicitly provided to the process, so the practical setup was
to keep the token in a gitignored bot-clone config or shell environment
instead of pretending the tooling would magically pick the right identity.

The point was not to make AI more powerful. It was to make the boundaries
around AI more legible.

## Landing The First Engine Slice

The first real implementation milestone was a framework-free TypeScript
package:

- `packages/engine`
- `@haomiantiao/engine`

The package introduces the first public types:

- `Contestant`
- `Matchup`
- `RoundOfSixteen`

It also adds `seedRoundOfSixteen()` for deterministic bracket pairing.

The bracket order is fixed:

```text
1 vs 16
8 vs 9
5 vs 12
4 vs 13
3 vs 14
6 vs 11
7 vs 10
2 vs 15
```

Validation keeps the input honest:

- exactly 16 contestants
- unique IDs
- seeds 1 through 16
- no duplicate seeds
- typed `SeedingError`

The implementation was tests-first and the validation came back green with
strong coverage.

I also removed the leftover `packages/example` scaffold once the engine
package existed, so the workspace would not carry an empty example that no
longer served a purpose.

That is a small cleanup, but it matters. Empty scaffolds can quietly become
CI noise later.

## Why The Day Mattered

Day 43 was not really about a bracket engine, even though the bracket engine
was the first code milestone.

It was about doing the unglamorous work that makes the rest of the project
possible:

- choose a product direction with enough real-world shape to matter
- cut the MVP down until it can actually ship
- treat the repo template as a contract instead of a starter kit
- run drills that are willing to expose a false sense of safety
- separate human and bot identities instead of blending them together
- land the first implementation slice under those constraints

The strongest outcome of the day was not the engine package by itself. It
was the fact that the project now has rails, governance, and a first
repeatable slice all pointing in the same direction.

## Outcome

Day 43 turned `haomiantiao` from a loose noodle idea into a governed
project start.

The product direction narrowed to the `Instant Noodle World Cup`, chosen over
other food-game concepts because it offered a real category, existing fandom,
shareability, affiliate potential, and a clean static-site path.

The MVP was cut down to a 16-noodle evergreen bracket with personal bracket
play, browser-local state, compact product cards, and a shareable
champion/result flow. Live voting, accounts, a backend, and more elaborate
product surfaces were deferred.

The new repository was created from the project template, but the template
was treated as governance infrastructure rather than a starter skeleton.
That brought in pnpm workspace structure, strict TypeScript, Vitest coverage,
five-check CI, `AGENTS.md` constraints, protected paths, one-concern PRs,
and limits on agent-added complexity. I then added project-specific
governance docs, ADRs, `docs/DESIGN.md`, and `docs/PROJECT_STATE.md`.

Phase 0 drills found a real CI bug: a forbidden-pattern check could fail open
when a directory in its scan path did not exist yet. The fix made the check
scan only existing directories and fail closed on `grep` errors.

A separate bot identity and dual-clone workflow split human-owned governance
work from AI-assisted implementation work. The important part was not the
convenience of that setup, but the fact that it makes trust boundaries
explicit.

The first implementation slice landed in `packages/engine` as a framework-
free TypeScript package with deterministic round-of-16 seeding, input
validation, typed seeding errors, and tests-first coverage.

The day ended with `haomiantiao` in a much better position than it started:
less vague, more governed, and finally moving toward something buildable.

## Definition Of Done

Day 43 reached a product-formation and governed-start checkpoint:

- chose `Instant Noodle World Cup` as the MVP direction
- compared the concept against several broader food-game directions
- narrowed the scope to a 16-noodle bracket
- kept the first release evergreen instead of seasonal
- kept the initial play experience personal rather than global
- kept the architecture static-site friendly
- deferred backend, database, account, and live-voting work
- created the `haomiantiao` repo from the project template
- treated the template as a governance contract
- preserved pnpm, strict TypeScript, Vitest, coverage, CI, and agent rules
- added project-specific governance docs and ADRs
- added `docs/DESIGN.md`
- added `docs/PROJECT_STATE.md`
- kept the repo private and proprietary
- ran Phase 0 drills before trusting the rails
- found a fail-open forbidden-pattern check
- fixed the CI check to fail closed
- set up a dedicated bot identity
- separated human and bot clones
- kept protected-path work and AI-assisted implementation distinct
- landed `packages/engine`
- added `@haomiantiao/engine`
- introduced `Contestant`, `Matchup`, and `RoundOfSixteen`
- implemented deterministic round-of-16 seeding
- validated exact contestant counts, unique IDs, and seed values
- added typed `SeedingError` handling
- wrote the work tests-first
- removed the stale `packages/example` scaffold

The day ended with a project that now has a narrower idea, a clearer
governance model, and a real first slice of code to build from.
