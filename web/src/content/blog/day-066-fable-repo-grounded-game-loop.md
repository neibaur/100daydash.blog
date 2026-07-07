---
title: "Day 66 - July 6, 2026: When the Workflow Itself Broke"
description: "A Day 66 reflection on using Fable in the Claude VS Code extension for repo-grounded Astro investigation, governance handoff, visual game debugging, playful Boo-Boo Quest mechanics, browser verification, and stacked-PR recovery."
pubDate: "2026-07-06"
day: 66
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story Astro dev-server investigation notes"
  - "Boo-Boo Quest visual-debugging notes"
  - "Boo-Boo Quest gameplay enhancement notes"
  - "Boo-Boo Story governance and CI notes"
  - "Boo-Boo Story stacked PR recovery notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - fable
  - claude
  - astro
  - game-design
  - testing
  - developer-experience
---

Day 66 started with a route that looked like it should work.

The Boo-Boo Quest demo lived under the public directory. In production, the
route was fine. In preview, the route was fine. The built site served both the
directory route and the explicit file route correctly.

But in development:

```text
/play/quest-kai/          -> 404
/play/quest-kai/index.html -> 200
```

That is the kind of bug that invites superstition.

Maybe Astro 7 changed something. Maybe the public directory was configured
wrong. Maybe the route needed a special setting. Maybe the answer was to move
the demo into the app router and stop serving it as a static public file.

The useful thing is that Fable did not start by guessing.

All of the day's repository work happened through Fable in the Claude VS Code
extension. I was directing the work, reporting bugs and feature ideas,
reviewing outcomes, and coordinating the PR flow. Fable was doing the
repo-grounded investigation and implementation loops.

That distinction matters because the strongest story of the day was not "an
agent added a few game features."

The stronger story was watching an agent work inside constraints: trace a
framework behavior, respect a governance boundary, debug visual state instead
of assuming logic was broken, build small verification loops, and then recover
when the delivery workflow itself went sideways.

That is the part I want to remember.

## The 404 Was Real, But Smaller Than It Looked

The Astro dev-server issue turned out not to be an Astro production routing
problem.

It was development-only behavior in Vite's public-file serving middleware.

Vite's `servePublicMiddleware` builds a set of exact public file paths. It
knows about files like:

```text
/play/quest-kai/index.html
```

It does not treat:

```text
/play/quest-kai/
```

as an equivalent directory request with an implicit `index.html`.

The underlying `sirv` setup also uses `extensions: []`, so there is no
extension or index fallback helping that trailing-slash request. The request
falls through Vite's public middleware, reaches Astro's router, and Astro
returns a development-only 404.

That is a very different conclusion from "Astro broke public routes."

The fix was correspondingly small.

Fable added a development-only Vite plugin at:

```text
packages/site/src/dev/public-dir-index.ts
```

The plugin rewrites trailing-slash public-directory requests to the matching
`public/<dir>/index.html` only when that file actually exists.

The details mattered:

- query strings are preserved
- percent-encoded paths are handled
- path traversal is blocked
- the plugin is typed structurally so the site package does not need a direct
  Vite dependency

That last point is not flashy, but it is the shape of the work I want.

The repository did not need a new dependency just because the fix happened to
live at a Vite extension point. It needed one small development-only adapter
around a specific mismatch between public-directory expectations and Vite's
dev middleware behavior.

That became PR #7 and was merged.

## The Tests Found A Second Governance Problem

The repository's agent contract requires tests-first commit structure.

Fable followed that rule explicitly:

- first commit: failing unit tests and Vitest wiring for the site package
- second commit: the implementation

That would have been enough for an ordinary bug fix.

But while making the test path real, Fable found another issue: Vitest 4 was
not applying the template's per-project coverage thresholds the way the
repository expected.

The intended 80/80 coverage guardrails were effectively not being enforced.

The fix moved coverage configuration to the root Vitest config while keeping
the thresholds unchanged.

That is one of the quiet benefits of investigation over patching.

The first visible defect was a route 404. The investigation went through the
actual framework behavior, then through the repository's test configuration,
and surfaced a second problem in the quality gate.

That is not code generation.

That is engineering work.

## When CI And The Agent Contract Disagreed

Then PR #7 failed CI.

Not because the tests failed.

Not because gitleaks found a secret.

It failed a workflow step called Batch discipline.

That step rejected any pull request that touched tests and implementation in
the same PR.

The problem was that `AGENTS.md` required tests-first commits inside the same
PR.

So the repository had a contradiction:

- the written agent contract required tests and implementation together
- CI rejected PRs that contained both tests and implementation
- `.github/**` was treated as human-only

That is exactly the kind of moment where an agent can become dangerous if its
only goal is to make the check green.

The convenient move would have been to edit the workflow.

Fable did not do that.

It respected the human-only boundary around the GitHub Actions file. Instead,
it documented the contradiction on the PR, explained why the two rules could
not both be satisfied, gave the maintainer step-by-step instructions, and
supplied a full replacement YAML block.

The proposed fix scoped Batch discipline to modified or deleted existing test
files using:

```text
git diff --diff-filter=a
```

That allows newly added tests to land with their implementation while still
protecting against broad rewrites of existing tests.

I made the protected workflow change as a human-authored PR #8.

That was the best governance moment of the day.

Good agent behavior did not mean silently editing whatever file was necessary
to unblock itself. It meant stopping at the boundary, making the conflict
legible, and handing the protected change back to the human maintainer with
enough precision that the maintainer could act.

That is not less capable.

That is more useful.

## The Half Heart Was Not A Health Bug

After the development-route and CI work, the day turned back toward the
Boo-Boo Quest game itself.

The next visible symptom looked like broken game state.

After Boo-Boo took one hit, the heart HUD appeared unchanged. Hearts only
visibly changed every two hits. Half-heart pickups also seemed to do nothing.

The tempting diagnosis was that health was being tracked in full-heart units,
or that half-heart pickups were not updating state.

That diagnosis was wrong.

The health model was already tracking half-heart units correctly.

The defect lived in CSS.

Each `.hp` span had a fixed `1em` box, but the heart glyph only occupied
roughly half of that box. The overlay intended to show a half heart was clipped
to about 55 percent of the span. Because the glyph itself sat inside only part
of the span, that 55 percent still covered the entire visible heart.

The state changed.

The visible glyph did not.

The fix was to shrink-wrap the heart span to the glyph and clip the overlay at
a true 50 percent.

Fable verified the change at the pixel level by rendering every heart state in
headless Edge before and after the fix.

That became PR #9 and was merged.

I like this bug because it is a small version of a larger product lesson. A
user can report "health changes every two hits" and be accurately describing
the experience while still naming the wrong layer of the system.

The symptom was game-state shaped.

The cause was presentation.

## A Gap Became An Invariant

The next issue was a map-design problem.

Forest Path, the second screen on the top row, had an opening in the tree line
at the top edge of the world.

That opening looked like an exit.

It was not an exit.

Travel in that direction was impossible.

Instead of sealing only the reported gap, Fable wrote a scripted audit for the
outer edges of all 12 screens. That audit found the reported Forest Path issue
and one more: Quiet Grove, at the bottom-right corner of the map, had three
right-edge openings that mirrored intentional exits on its left side.

Both accidental openings were sealed.

The same audit verified that intentional inter-screen exits still aligned.

That became PR #10 and was merged.

This is another pattern I want to keep.

A human report can identify one visible defect. An agent can turn that report
into a repeatable invariant check across the system.

The point is not to over-engineer every visual issue.

The point is to notice when a single defect implies a broader rule:

```text
World edges should not imply exits that do not exist.
Intentional neighboring exits should still line up.
```

Once the rule is that clear, a small audit is better than a one-tile patch.

## Exploration Rewards, Not Just More Hearts

The larger feature work started with heart containers.

Boo-Boo Quest gained three hidden containers:

- one at the Sandy Shore beach tip
- one in the Echo Cave corridor
- one inside Echo Cave

Each one increases Boo-Boo's maximum health by one full heart, capped at six
hearts. The HUD row grows dynamically with max health.

That sounds like a standard game mechanic, and it is.

But in this prototype it had a specific job.

The map needed reasons to explore that were not only enemies, obstacles, and
blocked paths. A heart container is a small promise that poking around the
world can make Boo-Boo more capable.

The containers also use a pulsing hand-drawn heart doodle rather than a
polished imported icon.

That matters for the same reason yesterday's art work mattered. The
mechanic can be familiar, but the object still has to belong to Kai's
notebook-shaped world.

This work was eventually recreated as PR #16 after the stacked-branch recovery
later in the day.

## The Cave Stopped Being A Sign

Echo Cave had previously been a promise, not a place.

Entering the cave mouth produced a "To be continued!" toast.

That is fine for a prototype. It is also a little sad, because a cave is
exactly the kind of object that asks to be entered.

Fable turned it into a real interior.

The cave lives at an off-grid world slot, `4,0`, and includes:

- a boulder maze
- two Chaser enemies
- the third heart container
- a lantern-glow darkness vignette
- an exit door back to the outside world

The important part is that the prototype did not need to abandon its current
self-contained shape to make the cave real.

It stayed a static single-file demo.

It simply gained one more playable space.

That became PR #17.

The cave is not a finished dungeon. It is not trying to be. It is the right
amount of real for this stage: enough to make the placeholder stop being only
a sign.

## The Water Gun Pushes Instead Of Hurts

The next feature was the Water Gun.

A new chest at Giggle Lake's beach now contains it. To support that, the
chest system was generalized from one hard-coded chest into per-screen chest
definitions.

The Water Gun fires droplets.

It does not damage enemies.

Instead, it pushes enemies backward and makes flowers bloom larger.

That choice is more interesting than the implementation.

It would have been easy to make the Water Gun a ranged attack with water
damage. That would have made it mechanically legible, but it would also have
pushed the prototype toward the same combat vocabulary as every other small
adventure game.

This is a children's game demo built around a silly, hand-drawn character.

A tool that pushes trouble away and makes flowers grow says something better
about the world.

It gives the player agency without making damage the answer to every
interaction.

That became PR #18.

## Dancing As A Design Mechanic

Then came the Wiggle Dance.

Boo-Boo can now dance with:

- the `Q` key
- a music-button control

The animation is a hoppy wiggle with music notes.

Nearby enemies become confused. They stop chasing, stumble around, and show
stars over their heads. The confusion lasts 4.5 seconds, and the dance has an
8-second cooldown.

There are also joke toasts.

Again, the product choice matters more than the mechanic name.

The game needed another way to handle pressure. One answer would be a stronger
weapon. Another would be a shield. Another would be damage upgrades.

Instead, Boo-Boo dances.

That is more specific.

It fits the character better.

It also keeps the prototype asking a useful design question: what if solving
trouble in this world is sometimes playful, embarrassing, musical, and
nonviolent?

That became PR #19.

## Sound Without Files

The final game feature added sound.

There are synthesized WebAudio cues for:

- bonks
- pops
- player damage
- pickups
- chests
- Water Gun squirts
- the Wiggle Dance tune
- warps
- going home

There are no audio files.

The demo remains one self-contained HTML file.

The `AudioContext` unlocks from the Start button click, and the game has a
speaker mute control.

That became PR #20.

The self-contained part is important. At this stage, the prototype benefits
from being portable and easy to reason about. Adding a folder of sound assets
may happen someday, but synthesized cues were enough to make the world feel
more alive without changing the artifact shape.

The sound is not the final audio direction.

It is a working signal.

That is all it needed to be.

## Verification Became A Habit

The bigger game work used a repeatable browser-verification technique.

Because the demo is currently a large self-contained HTML file with an inline
script, Fable built small temporary checks around that shape instead of
pretending it was already a full application with a mature E2E suite.

The loop was practical:

1. extract the inline game script
2. run `node --check`
3. create a patched scratchpad copy
4. click Start automatically
5. dispatch keyboard events
6. override game state when necessary
7. run the game in headless Edge
8. inspect screenshots

That is not a permanent test framework.

It is not product-level E2E coverage.

But it is much better than manually clicking around and trusting memory after
every change.

The half-heart pixel comparison and the map-edge audit were the same kind of
thing: focused verification tools shaped around the actual risk of the change.

I keep coming back to that because it is one of the places where agentic
development becomes meaningfully different from just asking for code.

The useful agent is not only the one that can make a patch.

It is the one that can build the smallest credible way to check whether the
patch worked.

## The PR Stack Collapsed

The last technical challenge of the day was not in the game.

It was in Git.

The original feature PRs #11 through #15 were stacked on top of one another.
They were not each based directly on `main`.

Then they were closed and their remote branches were deleted before merging.

That sounds worse than it was, because the local branch tips still existed.

But it still required understanding the branch topology rather than blindly
recreating work from memory.

Fable recovered the chain by:

- rebasing all five single-commit branches onto the updated `main`, which
  already contained PRs #9 and #10
- rebuilding the features as a clean stack
- encountering zero conflicts
- re-verifying the final tip with the map-edge audit, syntax check, and
  `pnpm validate`
- pushing fresh branches
- deleting one stale remote branch named `feat/quest-kai-sound-effects` before
  recreating it
- reopening the five PRs as #16 through #20

All five PRs had green CI checks.

The merge instructions were explicit:

```text
#16 -> #17 -> #18 -> #19 -> #20
```

Each merge reduces the next PR's diff to only the feature introduced by that
branch.

This recovery matters because it is a reminder that agentic workflows do not
remove the need to understand Git history.

They may increase it.

When a stack is closed in the wrong order, or branches disappear remotely,
the answer is not panic and not blind copying. The answer is to reason from
the commits that still exist, rebuild the intended graph, and verify the new
tip.

That is old-fashioned engineering discipline in a very modern workflow.

## What The Day Was Really Testing

Looking back, Day 66 was not really about any one feature.

The Astro dev-server fix mattered.

The CI governance handoff mattered.

The heart HUD and map-edge fixes mattered.

The heart containers, Echo Cave, Water Gun, Wiggle Dance, and synthesized
sound made Boo-Boo Quest more playful and complete.

The PR recovery mattered a lot.

But the through-line was the same in every case.

Can the agent operate inside a real repository contract?

Can it investigate unfamiliar behavior instead of guessing?

Can it separate a symptom from its cause?

Can it respect a human-only boundary even when editing that file would be the
fastest way to unblock itself?

Can it create verification shaped to the risk?

Can it recover when the delivery process itself breaks?

That is the interesting frontier for me now.

The question is no longer only whether an agent can write code. It can.

The more important question is whether the agent can work in the system around
the code: the framework behavior, the tests, the CI rules, the protected
paths, the review flow, the visual checks, the Git topology, and the human
decisions that should remain human.

Fable was useful on Day 66 because it acted less like a code generator and
more like an engineering collaborator inside a governed repo.

Not autonomous.

Directed.

Bounded.

Repo-grounded.

Able to stop when stopping was the correct action.

That last part may be the most important one.

## Outcome

Day 66 used Fable in the Claude VS Code extension for a full repo-grounded
engineering loop in Boo-Boo Story's Boo-Boo Quest demo.

The day began with a development-only Astro route problem. In `astro dev`,
`/play/quest-kai/` returned 404 while `/play/quest-kai/index.html` returned
200, even though build, preview, and production served both routes correctly.
Fable traced the behavior to Vite's `servePublicMiddleware`: it tracks exact
public file paths and uses `sirv` with `extensions: []`, so trailing-slash
public-directory requests do not automatically fall back to `index.html`.

The fix was a small development-only Vite plugin at
`packages/site/src/dev/public-dir-index.ts`, registered through
`astro.config.mjs`. It rewrites trailing-slash public-directory requests to a
matching `public/<dir>/index.html` only when that file exists. The
implementation preserves query strings, handles percent-encoded paths, blocks
path traversal, and avoids adding a direct Vite dependency by using structural
typing.

Fable followed the repository's tests-first commit rule for PR #7 by first
adding failing tests and Vitest wiring, then adding the implementation. During
that work, it found that Vitest 4 was ignoring the template's per-project
coverage configuration. Coverage thresholds were moved to the root Vitest
config while keeping the intended 80/80 thresholds.

PR #7 then exposed a governance contradiction. The written `AGENTS.md`
contract required tests-first commits in one PR, but the Batch discipline CI
step rejected any PR touching both tests and implementation. Because
`.github/**` was human-only, Fable did not edit the workflow. It documented
the contradiction, explained why both rules could not be satisfied, and
provided a replacement YAML block. I made the protected workflow change as a
human-authored PR #8.

The game-debugging work fixed two visual correctness issues. The half-heart
HUD bug looked like health state changing only every two hits, but the state
was already correct. The defect was CSS: the `.hp` span was wider than the
heart glyph, so the half-heart overlay still covered the visible glyph. The
fix shrink-wrapped the glyph and clipped the overlay at 50 percent, verified
with pixel-level headless Edge renders. A separate map-edge audit turned one
reported Forest Path tree-line gap into a check across all 12 screens, found
an additional Quiet Grove right-edge issue, sealed both accidental openings,
and verified intentional exits still aligned.

The larger feature work made Boo-Boo Quest more playful without changing the
prototype into a generic combat game. Heart containers became hidden max-health
exploration rewards. Echo Cave stopped being only a "To be continued!" toast
and became an explorable interior with a boulder maze, Chasers, lantern-glow
darkness, an exit door, and the third container. The Water Gun was placed in a
Giggle Lake beach chest and designed to push enemies and grow flowers instead
of damaging enemies. Wiggle Dance let Boo-Boo confuse nearby enemies through a
hoppy music-note animation. WebAudio added synthesized cues for bonks, pops,
damage, pickups, chests, Water Gun squirts, dance, warps, and going home while
keeping the demo self-contained.

Verification stayed practical and repeatable. Fable extracted the inline game
script, ran `node --check`, patched scratchpad copies, clicked Start
automatically, dispatched keyboard events, overrode state when needed, ran
headless Edge, inspected screenshots, compared HUD pixels, and used scripted
map-edge audits. These were not permanent product-level E2E tests, but they
were focused checks around the real risks of a self-contained HTML prototype.

The day ended with Git recovery. The original feature PRs #11 through #15 had
been stacked, then accidentally closed with their remote branches deleted.
Because the local branch tips still existed, Fable rebased the five
single-commit branches onto updated `main`, rebuilt the stack cleanly,
re-verified the final tip with the map-edge audit, syntax check, and
`pnpm validate`, pushed fresh branches, recreated one stale remote branch, and
opened replacement PRs #16 through #20. The intended merge order was documented
as `#16 -> #17 -> #18 -> #19 -> #20`, with each merge reducing the next PR's
diff.

## Definition Of Done

Day 66 reached the Fable repo-grounded game-loop checkpoint:

- confirmed Day 66 follows Day 65 for July 6, 2026
- explicitly recorded that all repository work happened through Fable in the
  Claude VS Code extension
- avoided claiming that Fable autonomously built the game
- framed my role as directing work, reporting bugs, reviewing outcomes, and
  coordinating PR flow
- opened with the Astro development-only public-directory 404
- distinguished `astro dev` behavior from build, preview, and production
- traced the route issue to Vite's public-file middleware behavior
- avoided inventing an Astro configuration workaround
- implemented the fix as a small development-only Vite plugin
- preserved query strings in the route rewrite
- handled percent-encoded paths
- blocked path traversal
- avoided adding a direct Vite dependency
- followed the repository's tests-first commit rule
- found the Vitest 4 coverage-threshold configuration problem
- moved coverage thresholds to the root Vitest config
- surfaced the CI Batch discipline contradiction
- respected the human-only `.github/**` boundary
- handed the workflow fix back to the human maintainer
- described the `git diff --diff-filter=a` proposal
- treated the half-heart bug as a state-versus-presentation debugging lesson
- identified CSS clipping as the real HUD defect
- verified heart rendering with headless Edge pixel checks
- turned the reported Forest Path gap into a map-edge audit
- found and sealed the Quiet Grove right-edge issue
- preserved intentional inter-screen exits
- added hidden heart containers as exploration rewards
- capped max health at six hearts
- grew the HUD dynamically with max health
- turned Echo Cave from a placeholder into a real interior
- kept the cave inside the self-contained demo shape
- generalized chests enough to support the Water Gun
- made the Water Gun push enemies instead of damage them
- let Water Gun droplets grow flowers
- added Wiggle Dance as a playful pressure-management mechanic
- made confused enemies stop chasing and stumble temporarily
- added synthesized WebAudio cues without audio files
- kept audio unlocked through a Start-button user gesture
- added a mute control
- used repeatable browser-driven verification for the game work
- extracted and syntax-checked the inline game script
- used patched scratchpad copies for focused checks
- drove headless Edge for interaction and screenshots
- treated scratchpad checks as bounded verification, not a full E2E suite
- recovered accidentally closed stacked PRs from local branch tips
- rebased five single-commit branches onto updated `main`
- rebuilt the feature chain as replacement PRs #16 through #20
- verified the final stack tip before recreating the PRs
- documented strict merge order for the rebuilt stack
- preserved the core lesson: a capable agent is most useful when it can work
  inside constraints, verify behavior, respect governance boundaries, and
  recover cleanly when the workflow itself breaks
