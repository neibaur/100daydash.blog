---
title: "Day 85 - July 25, 2026: Removing Drift Without Removing Discipline"
description: "A Day 85 reflection on replacing Boo-Boo Story's duplicate title-screen weapon preview with real gameplay behavior and making CI governance precise enough for valid maintenance."
pubDate: "2026-07-25"
day: 85
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #90 through PR #101 implementation, maintenance, and validation notes"
  - "Boo-Boo Story Quest Kai title-screen and CI-governance repository history"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - game-development
  - testing
  - continuous-integration
  - repository-governance
  - dependency-management
  - security
---

Yesterday ended with a prompt.

Today the prompt became code.

Day 84 documented the remaining Quest Kai title-screen defects, connected
several visible weapon problems to one likely source, and arranged the work
into a sequence. It did not fix anything. On July 25, I used that diagnosis as
the starting point for implementation, tests, browser verification, and merged
pull requests.

The product work was only half of the day.

A group of routine dependency updates arrived at the same time. Most were
ordinary maintenance. One was not. A formatter upgrade changed both existing
tests and application files, and a CI safeguard treated the mixed pull request
as an unsafe batch change even though the work could be organized into a valid
tests-first sequence.

The rule protected a real principle. The check modeled that principle too
coarsely.

Those two threads looked unrelated at first. One involved weapons, sprites,
projectiles, and a title screen. The other involved Dependabot, lockfiles,
formatting, and commit inspection. Both eventually required the same kind of
correction: stop relying on a simplified copy of reality, preserve the intent,
and make the implementation represent what actually matters.

## From Yesterday's Prompt To Today's Code

The Day 84 plan divided the title-screen work into specific concerns. PRs #94,
#96, #97, #98, and #99 implemented them.

The first defect appeared only with the second selectable character.

Weapons were attached to the side opposite the character's direction of
travel. The initial symptom sounded like a bad offset, but PR #94 found a more
specific cause.

The title-screen container held both the character sprite and the weapon. The
whole container was flipped using logic that corrected each character's source
artwork. That correction was not the same thing as movement direction.

The two character drawings were created facing different native directions.
For the first character, the artwork correction happened to agree with travel
direction. Boo-Boo-1 needed the opposite artwork correction. Flipping the
container according to the artwork therefore moved every weapon behind that
character in both directions.

The fix separated the two meanings.

The container now follows movement direction, which keeps its weapon anchor in
front. The sprite receives its own character-specific correction so the art
still faces the direction of travel. Tests covered both characters facing both
ways.

This was related to the earlier hammer-grip repair, but Kai's artwork did not
need to change. The bug lived in how the code combined direction and
art-orientation correction.

A Boolean or flip value can look correct while carrying two different
concepts. It works until those concepts stop having the same answer. Separating
them made the intended rule visible.

## Small Fixes Needed Specific Diagnoses

The temporary scrollbar received an even smaller implementation.

PR #96 confirmed that the scrollbar belonged to the title overlay, not the
browser document. The overlay deliberately used `overflow-y: auto` because its
content can exceed the available height. Under CSS overflow computation,
leaving horizontal overflow visible while vertical overflow is automatic
effectively makes the horizontal axis scrollable too.

The weapon effect was a real child of that overlay. Near the boundary, its
swing extended past the container for a fraction of a second and raised a
horizontal scrollbar.

The fix added one horizontal containment rule. Vertical scrolling remained
available. The effect could still be activated at the edge and kept its normal
size. The portion outside the play area simply clipped at the boundary.

That one-line result depended on locating the correct overflow owner. Applying
rules to the page or the game wrapper would have answered a different problem.
Diagnosis was most of the work.

PR #97 completed two interface improvements from the plan.

Opening the map from the title screen had required pressing the Map button
again to return. The new back arrow appears only when the map originated from
the title screen. One Boolean records that origin. The normal in-game map and
the existing Map-button toggle keep their previous behavior.

There was no router, navigation stack, or browser-history system. One bit of
state represented the distinction the interface needed.

The same pull request centered the Design Studio link above the game box by
reusing its existing layout container and control styling. It did not create a
new component system to move one link.

The title fixes were small in line count and narrow in design. They were not
casual. Each one followed a specific explanation of the behavior it needed to
preserve.

## One Preview Instead Of Two Weapon Systems

PR #99 was the largest product change of the day.

Day 84 had recorded three visible symptoms. Fire used a generic emoji instead
of Kai's in-game artwork. The star appeared beside the character instead of
traveling. Water did the same.

The repository confirmed that these were not three independent defects. The
title screen owned a simplified DOM weapon mock separate from Quest Kai's real
combat behavior.

The inexpensive-looking copy had drifted.

PR #99 removed that duplicate preview and made the title area a live canvas.
It creates a temporary title-screen state, dispatches the hammer, star, water,
and flame thrower through the same functions used by the adventure, advances
their effects through the existing combat update loop, and draws them through
the existing rendering functions.

Fire now uses Kai's actual art. Star and water projectiles travel. Their
existing boundary behavior remains meaningful because the preview uses Quest
Kai's native 480-by-320 logical field and scales it visually with CSS.
Projectiles terminate at the preview boundary using the game's normal impact
behavior rather than a title-specific imitation.

The title state remains separate from the adventure state.

Trying a weapon before pressing Start does not grant it to the player. The
adventure still begins with its intended inventory, and the remaining weapons
still belong to its discovery progression. Shared behavior did not require
shared state.

The reuse decision stayed deliberately local.

The combat functions already accepted a state object, so they could operate on
the temporary preview state. Rendering was more awkward because the helpers
used Quest Kai's current canvas context. The implementation made the smallest
available change: during title rendering it temporarily pointed that context
at the preview canvas, rendered through the existing helpers, and then
restored the original context.

That is not a universal rendering adapter. It is not a weapon registry, plugin
architecture, cross-game engine, or new animation framework. It is direct
deduplication inside Quest Kai.

Future changes to those existing weapon behaviors can now appear in the title
preview without maintaining a second mock.

## Moving The Test Baseline First

Removing the DOM preview also meant removing `#tsbonk`, the old title-screen
hammer element.

An existing test required that element and pinned its CSS transform behavior.
If left untouched, the test would have defined an intentionally obsolete
implementation as permanent.

PR #98 retired that test before the implementation changed.

Deleting a test is not automatically an improvement. In this case, the subject
of the test was deliberately being replaced, and the replacement received new
coverage in PR #99. Moving the baseline in a tests-only pull request made the
decision independently reviewable instead of hiding it inside the larger
feature.

That sequence also preserved the repository's tests-first discipline.

PR #99 then added coverage that the title screen dispatches to the four real
weapon functions using the temporary title state, advances combat through the
existing loop, contains the preview canvas, and no longer carries the duplicate
weapon structures. Tests also covered star and water travel and termination at
the 480-by-320 boundary.

The final feature pull request reported a green `pnpm validate`, 401 tests at
that point in the sequence, a successful production build, and 342 changed
lines under the repository's 400-line cap. A headless browser run also showed
the preview canvas rendering successfully.

The validation mattered because reuse can fail in ways a code reading will not
show. A function can accept the right state and still draw to the wrong canvas.
A projectile can update and still disappear too quickly to be useful. The
browser check proved that the context swap, animation loop, and visible preview
worked together.

## Routine Updates Met Repository-Specific Policy

While that product work moved through focused pull requests, Dependabot opened
several maintenance proposals.

PR #90 updated `actions/checkout` from 7.0.0 to 7.0.1. PR #91 moved
`actions/setup-node` from 6.4.0 to 7.0.0. PR #92 updated
`typescript-eslint` from 8.63.0 to 8.64.0. I reviewed and merged those updates
after their validation completed.

That was the routine part.

Automated dependency proposals still operate inside repository-specific rules.
The package manager must produce a reproducible lockfile. A frozen install must
accept the committed result without modifying it. Audits, release-age policy,
the full validation suite, and local governance still decide whether a
version change is ready.

Dependabot can identify an update. It cannot always finish the reasoning around
that repository's constraints.

PR #95 demonstrated how several security controls can point in different
directions without actually disagreeing.

New high-severity advisories caused the security job to fail against versions
already present in an unchanged lockfile. `postcss` 8.5.15 arrived through the
Vitest, Vite, and coverage toolchain. `brace-expansion` 5.0.7 arrived through
ESLint and `minimatch`. Both were transitive development dependencies rather
than shipped game code.

The fix added targeted pnpm overrides. The regenerated lockfile resolved
`postcss` to 8.5.19 and `brace-expansion` to 5.0.8.

The repository also quarantined newly released packages for seven days.
`brace-expansion` 5.0.8 was still inside that window, so the update received a
narrow minimum-release-age exception. `postcss` 8.5.19 was old enough and did
not need one.

The audit policy said to move immediately. The release-age policy normally said
to wait. A specific exception allowed the patched version without disabling
either protection globally.

The pull request changed only `pnpm-workspace.yaml` and `pnpm-lock.yaml`.
Validation included installation, a high-severity audit, the full repository
suite, and dependency-path inspection. No game behavior changed. The
development and validation supply chain did.

## When The Guardrail Modeled The Wrong Thing

PR #93 was a grouped Dependabot proposal with seven updates:
`@commitlint/cli`, `@commitlint/config-conventional`,
`@vitest/coverage-v8`, `lint-staged`, Prettier, Vitest, and Astro.

The complication was Prettier.

Moving from Prettier 3.8.4 to 3.9.5 changed canonical formatting in existing
test and application files. A dependency-only update therefore produced
mechanical changes across both categories.

The repository's batch-discipline security check was intended to prevent an
agent from rewriting existing tests and implementation together. That is a
worthwhile rule. Existing-test changes should be visible and reviewable before
implementation begins.

The check evaluated the net pull request diff.

It saw tests and implementation. It did not see the difference between one
unsafe mixed commit and an ordered sequence in which the test baseline moved
first. The simplified model flattened away the evidence carried by commit
history.

This was not a reason to remove the safeguard.

It was evidence that automated safeguards are code too. They must be tested
against real situations, and their implementation has to evolve when it blocks
valid work that preserves the underlying policy.

## Making Tests-First Enforcement Commit-Aware

PR #100 changed the check from pull-request-wide classification to
commit-aware enforcement.

The revised policy evaluates each non-merge commit and its position in the
sequence.

| Commit history                                 | Result                |
| ---------------------------------------------- | --------------------- |
| Existing-test change, then implementation      | Pass                  |
| Existing test and implementation in one commit | Fail                  |
| Implementation, then existing-test change      | Fail                  |
| New test and implementation in one commit      | Pass                  |
| Merge `main` into the branch                   | Ignored by this check |

The principle remains intact.

An existing test cannot be changed in the same commit as implementation. Once
implementation has begun, a later commit cannot move the existing test
baseline. A newly added test may still arrive with its implementation where
the repository policy permits it.

Base-branch synchronization merges are excluded because their first-parent
diff can include files imported from `main` rather than authored by the pull
request. The stated tradeoff is that conflict-resolution edits committed
directly inside a merge commit are not evaluated in the same way. Reviewers
must inspect the resulting pull request diff carefully.

That limitation is more precise than pretending the automation proves
something it cannot prove.

The old check asked whether two categories appeared anywhere in one pull
request. The new check asks whether the commit sequence demonstrates the
discipline the policy was created to enforce.

The guardrail did not become less strict. It became more accurate.

## Commit Structure Became Evidence

With the CI rule representing commit order, PR #101 isolated the Prettier
migration from the grouped update.

It contained three commits:

1. Update Prettier to 3.9.5 and regenerate the lockfile.
2. Apply Prettier 3.9.5 formatting to existing tests.
3. Apply the formatter's mechanical changes to application code.

The order was not ceremony.

It showed the tool change, then exposed the changed test baseline on its own,
then applied the same mechanical rule to production files. The source and test
edits were formatter output, not intended behavior changes.

Validation included `pnpm install --frozen-lockfile`, `pnpm validate`, and the
updated batch-discipline check. The frozen install was important: regenerating
a lockfile shows what the package manager produced once; installing from it
without modification shows that the committed result can reproduce the
dependency graph.

PR #93 was closed without merging after PR #101 established the Prettier 3.9.5
baseline. At the end of the July 25 work, no recreated grouped Dependabot pull
request existed yet. Recreating or replacing it against the updated `main`
branch remained follow-up work.

That distinction matters. The formatter migration and governance repair were
complete. The other grouped dependency updates were not silently converted
into merged work.

## Preserving The Principle

The title-screen preview and the CI safeguard failed in similar ways.

The duplicate weapon preview looked simpler than using the real gameplay path.
It eventually stopped representing the weapons it claimed to preview.

The pull-request-wide CI rule looked simpler than interpreting commit history.
It eventually stopped distinguishing an unsafe batch rewrite from a valid
tests-first migration.

Neither fix required abandoning the original goal.

The title screen still lets a player experiment before beginning the adventure,
but it no longer maintains fake weapon behavior. The repository still requires
existing test changes to precede implementation, but it no longer treats every
mixed net diff as equivalent. Security auditing still requires patched
dependencies, while release-age protection still applies except for a narrow,
documented case. Lockfiles still change when dependencies move, and frozen
installation verifies that the resulting state is reproducible.

In each case, the useful move was to preserve the principle while replacing a
representation that had drifted away from it.

Automation does not eliminate maintenance. It creates another maintained
system.

Dependabot was useful because it surfaced routine updates. The audit was useful
because newly disclosed vulnerabilities could make yesterday's lockfile unsafe
without any source change. The release-age policy was useful because freshness
can carry supply-chain risk. The batch-discipline check was useful because test
changes can be used to conceal regressions.

None of those tools could supply all of the judgment.

Human review still had to distinguish a normal version bump from a transitive
security repair, a quarantine exception, a formatter baseline migration, and a
CI false positive. The answer was not to make the repository permissive. It
was to make each exception and sequence narrow enough to explain.

## What I Learned

Day 85 reinforced that strictness is not measured by how many valid changes a
system rejects.

A strong rule encodes its intent closely enough to reject the unsafe behavior
while allowing safe work to remain inspectable. When a rule blocks the wrong
thing, refining its implementation is governance work, not a retreat from
governance.

The day also gave commit structure a more concrete role.

The three Prettier commits communicated facts that a final diff could not:
first the tool moved, then the existing test baseline moved independently, then
application formatting followed. Commit order became part of the review
evidence.

The title-screen work made the same point through code paths. Fire, star, and
water were not three defects requiring three title-specific patches. They were
evidence that a copied preview had stopped representing the game. Reusing the
real behavior solved the observed drift without inventing a generalized engine.

Small changes unlocked the larger sequence. One overflow rule worked because
the correct container had been identified. One Boolean clarified title-only
navigation. One tests-only pull request made removal of obsolete behavior
reviewable. One CI-only pull request allowed a formatter migration without
discarding test discipline.

Yesterday's prompt was valuable because it organized the evidence.

Today's work was valuable because the repository tested the plan against
reality.

## Outcome

Day 85 completed the July 25 Boo-Boo Story work represented by PRs #90 through
#101, with PR #93 explicitly excluded from the merged result.

PR #94 separated movement direction from per-character artwork correction so
weapons stay on the forward side for both skins in both directions. Kai's art
and the earlier hammer-grip behavior did not need to change.

PR #96 confirmed that temporary horizontal scrolling belonged to the title
overlay and hid only that axis while preserving required vertical scrolling.
PR #97 added a title-origin-only map return arrow using one Boolean and centered
the existing Design Studio link without adding navigation or UI frameworks.

PR #98 retired the obsolete `#tsbonk` test in a dedicated tests-only baseline
change. PR #99 then removed the duplicate DOM weapon preview and rendered a
separate temporary title state through Quest Kai's real combat and rendering
functions. The title preview does not change the adventure inventory. The
feature validated with 401 tests at that point, a green `pnpm validate`, a
successful production build, boundary-behavior coverage, headless browser
verification, and 342 changed lines.

Dependabot PRs #90, #91, and #92 merged routine updates to checkout,
setup-node, and `typescript-eslint`.

PR #95 repaired two newly disclosed high-severity transitive development
dependency issues with targeted overrides: `postcss` 8.5.19 and
`brace-expansion` 5.0.8. Only `brace-expansion` needed a narrow exception to
the seven-day minimum-release-age policy. No product behavior changed.

Grouped Dependabot PR #93 proposed seven updates but closed without merging
after the Prettier 3.9.5 formatting changes triggered the repository's
pull-request-wide batch-discipline rule.

PR #100 refined that rule to inspect non-merge commits and their order. It
continues to reject existing-test and implementation changes in the same
commit, and it rejects existing-test changes after implementation begins. It
allows an independently reviewable tests-first sequence, new tests with their
implementation where permitted, and base-branch synchronization merges.

PR #101 established the Prettier 3.9.5 baseline in three ordered commits:
dependency and lockfile, existing tests, then application code. The formatting
changes were mechanical, with no intended behavioral change. Frozen
installation, full validation, and the updated governance check passed.

At the end of the requested scope, recreating or replacing grouped Dependabot
PR #93 remained follow-up work. The formatter baseline and CI rule were merged;
the remaining grouped updates were not.

## Definition Of Done

Day 85 reached the title-screen implementation and governance-refinement
checkpoint:

- followed Day 84 with the July 25, 2026 entry
- treated Day 84's diagnosis and prompt as the starting point, not completed
  implementation
- covered Boo-Boo Story PRs #90 through #101 without presenting twelve equal
  changelog entries
- distinguished merged PRs from closed-unmerged PR #93
- kept UTC timestamps on the July 25 Eastern Time workday
- separated movement direction from artwork-orientation correction
- stated that Kai's character art did not need editing
- identified the title overlay as the temporary scrollbar owner
- preserved vertical scrolling while clipping only horizontal overflow
- limited the map return arrow to title-origin navigation
- reused the existing Design Studio layout and styling
- justified the tests-only retirement of the obsolete `#tsbonk` baseline
- connected replacement coverage to the real weapon-preview implementation
- described the temporary preview state as separate from adventure state
- stated that title-screen experimentation does not grant adventure weapons
- recorded the native 480-by-320 logical preview boundary
- described the temporary canvas-context swap without claiming a new adapter
  or engine
- claimed no weapon registry, plugin system, cross-game engine, or animation
  framework
- recorded PR #99's 401-test checkpoint, passing validation and build,
  headless rendering verification, and 342 changed lines
- grouped the three routine Dependabot merges concisely
- recorded the exact `postcss` and `brace-expansion` patched versions
- limited the release-age exception to `brace-expansion` 5.0.8
- distinguished development supply-chain repair from product behavior
- listed the seven grouped updates in PR #93
- explained why Prettier 3.9.5 produced mechanical test and source changes
- treated the original CI principle as valid and its implementation as coarse
- recorded the commit-aware pass and fail cases from PR #100
- preserved the merge-commit conflict-resolution tradeoff
- recorded PR #101's three-commit sequence
- distinguished formatter output from intentional behavior changes
- included frozen-lockfile reproduction and full validation
- stated that PR #93 closed without merging
- left recreation of the grouped update as explicit follow-up
- connected duplicate product behavior and flattened governance through drift
- preserved security, release-age, tests-first, and reproducibility principles
  while describing their more precise implementations
