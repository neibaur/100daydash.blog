---
title: "Day 65 - July 5, 2026: Bonks, Clones, and a Rule That Met Reality"
description: "A Day 65 reflection on bringing Boo-Boo Story's early quest prototype to life with kid-notebook graphics, bonk combat, clones, map-transition fixes, scratchpad validation, and an agent-governance rule that surfaced its own exception."
pubDate: "2026-07-05"
day: 65
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story visual-life prototype notes"
  - "Boo-Boo Quest transition-correctness bug notes"
  - "Boo-Boo Quest gameplay expansion notes"
  - "Boo-Boo Quest scratchpad validation notes"
  - "Boo-Boo Story PR #5 and PR #6 governance notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - prototyping
  - game-design
  - testing
  - code-review
  - developer-experience
---

Day 65 was the day Boo-Boo Story got bonks, clones, and a better reason to
care about map borders.

That makes it sound more finished than it is.

It is not finished.

It is still a small prototype, still rough, still full of placeholder choices,
and still trying to learn what kind of game it wants to become. But it moved
from a static walking map toward a little playable loop: explore, bump into
trouble, find a second tool, make silly copies of yourself, and discover
which parts of the map actually behave like a world.

The more serious story was underneath that.

This was another test of whether repository governance can make an agent
notice when the requested work and the standing rules disagree.

The answer was not perfect.

The first implementation still became too large.

But the useful part is that Fable surfaced the conflict, proposed a split,
performed the split, and escalated the remaining exception instead of quietly
pretending the contract had been satisfied.

That is not governance theater.

That is a feedback loop.

## Keeping The Notebook Alive

The first question was visual.

How could Boo-Boo Quest feel more alive without turning into a generic game?

That constraint mattered more than the specific effects.

The wrong answer would have been to upgrade the prototype into polished pixel
art, glossy gradients, commercial sprites, or a clean professional style that
erases the reason Boo-Boo Story is interesting in the first place.

The identity is the kid's notebook.

Paper. Pencil. Marker accents. Wobbly hand-drawn lines. Kai's existing
character sprites.

So the visual improvements had to be small signs of life inside that world:

- soft pencil-like shadows under characters
- drifting water squiggles
- occasional wiggling trees
- gently swaying flowers
- doodle variants for repeated tiles
- little walking dust puffs
- stronger impact feedback with a small screen shake and star-burst doodles

That is a different product standard from "make the graphics better."

"Better" can be a trap.

The goal was to make the world feel more alive without removing the visual
authorship of a child's notebook.

That is becoming one of the core Boo-Boo Story rules. The code can support
the drawing. It should not launder it into something more generic.

## The Bug Under The Adventure

Before the new gameplay could matter, there was a real prototype bug.

When Boo-Boo moved from one screen to another, the destination screen used a
fixed entry location. If a rock, tree, or other solid tile happened to occupy
that location, Boo-Boo could spawn inside the obstruction and become
permanently stuck.

At that point the practical recovery was to close the game.

That is funny once.

Then it is a correctness bug.

I asked Fable to fix that first, but not by moving one unlucky rock.

The requested fix was defensive:

- after every screen transition, check whether the player's collision box
  overlaps a solid tile
- if it does, use breadth-first search from the intended entry tile to find
  the nearest walkable tile
- apply the same relocation logic for transitions in all four directions
- add a runtime failsafe so that being stuck inside a solid tile for more than
  one second triggers the same recovery
- audit the full map for neighboring screens whose edge openings do not line
  up

That last item turned the bug into a better lesson.

The audit found nine real map-edge mismatches.

Forest Path opened into a tree in Wiggly Woods. Rocky Climb and Echo Cave had
misaligned openings. River Crossing was walled off from Quiet Grove along its
bottom border. Home Meadow, Flower Patch, and Boulder Garden had several
one-way exits hiding in the edges.

What looked like one unlucky spawn bug was partly a world-data consistency
problem.

That is exactly the kind of defect a prototype can conceal. Walking around
mostly works. One transition fails. The visible symptom looks local. But the
map itself has multiple broken contracts.

Fable aligned the map data, added the BFS `nearestWalkable()` recovery on
screen entry, and added the greater-than-one-second stuck failsafe.

That changed the feel of the prototype immediately.

Not because the feature was exciting, but because the world became less
fragile.

## Bonking, Not Combat Theater

Once Boo-Boo could move between screens more safely, the larger experiment was
to give the map a small gameplay loop.

I asked for kid-tuned combat, deliberately framed as bonking.

No blood. No death language. No grim feedback.

Enemies should pop into stars and doodles. If Boo-Boo runs out of hearts, he
should become dizzy and wake up back at Home Meadow with full hearts and this
message:

```text
Boo-Boo went home for a snack. Adventure continues!
```

That tone boundary matters.

The prototype can have pressure and consequences without becoming mean. It
can have enemies without adopting the vocabulary or visual grammar of a more
violent game.

Fable added two placeholder enemy types:

- a grumpy blob-like Wanderer that drifts around and takes one bonk
- a spiky Chaser that notices Boo-Boo from several tiles away, pursues the
  player, and takes two bonks

The word "placeholder" is doing real work there.

Those enemies are pencil doodles that should eventually be replaced by Kai's
own drawings. The agent-generated shapes are not quietly becoming the
permanent monster art.

The prototype also gained a three-heart HUD with half-heart damage increments
and occasional heart pickups.

Two weapons created a basic inventory loop:

- the Bonk Hammer, available from the start as a short-range swing
- the Star Thrower, found in a treasure chest on Rocky Climb and limited to
  three active star projectiles

Weapons can be selected through inventory slots, number keys, or tapping.
Touch controls gained a round action button.

None of that makes a deep combat system.

That was not the goal.

The goal was to find out whether exploring, finding a tool, and encountering
different enemy behaviors gives the map more purpose.

It does, at least enough to keep testing.

## The Clone-O-Matic

The most playful mechanic of the day was the Clone-O-Matic.

I asked for a cloning box where Boo-Boo could make copies of himself.

That became a hand-drawn cardboard-box contraption on the Open Field screen.
Using the action control near it creates up to three blue-tinted Boo-Boo
clones.

The clones reuse Kai's existing Boo-Boo sprite frames and follow the player
with a delayed position trail.

That distinction matters.

This is not autonomous multi-agent game AI.

It is a position-trail prototype mechanic.

But it is a good prototype mechanic.

The clones can follow Boo-Boo through the current screen, interact with some
environmental behavior, bonk enemies they touch, absorb a nearby hit that
would otherwise hurt the player, and harmlessly pop into stars when left
behind during a screen transition.

That last behavior is the right kind of silly.

The mechanic makes the prototype feel less like a map viewer and more like a
small space for testing a child's game idea. What happens if the hero can make
three little copies? What should they do? Should they help? Should they get in
the way? Should they vanish dramatically when the screen changes?

Those are not architecture questions yet.

They are play questions.

The Clone-O-Matic gave the prototype a place to ask them.

## Validation Without Moving The Fence

There was a validation wrinkle.

The existing ADR-0005 keeps the `public/` demos outside the repository's
normal test perimeter.

Fable could have quietly changed that by adding permanent tests around the
demo. It did not.

Instead, it built a temporary headless DOM-stub harness in its scratchpad and
ran the real game loop in Node.

That matters because the harness respected the current architecture while
still checking the risky behavior.

The temporary checks covered 16 things, including:

- a programmatic audit of all 17 neighboring screen borders
- zero remaining border mismatches
- transition unstick behavior
- the one-second stuck failsafe
- hammer enemy interactions
- half-heart damage
- dizzy-to-respawn behavior
- clone cap, following, and hit absorption
- the initially locked second weapon slot

Those checks passed across repeated runs.

Fable also used headless Edge screenshots of the title screen, Home Meadow,
Open Field, and Rocky Climb to check that the notebook visual style still
held together.

`pnpm validate` passed. The site build passed.

The important part is not that a scratchpad harness is now a durable test
suite. It is not.

The important part is that the agent found a way to validate the work without
silently expanding the repository's permanent test perimeter.

That is the difference between useful verification and accidental
architecture.

## The 400-Line Rule Met The Prototype

The bigger process story came after implementation.

Fable reported that the initial change was 623 lines and exceeded the
400-line change cap in `AGENTS.md`.

That is exactly the moment I want governance rules to create.

The agent did not hide the violation. It did not treat my prompt as automatic
permission to ignore the repository contract. It reported the conflict and
suggested a natural split:

- one PR for the transition and map-correctness bug fix
- another PR for the larger gameplay expansion

I decided to take the split.

Fable reorganized the work into two stacked PRs.

PR #5, `fix/quest-transition-stuck`, targeted `main` and became a focused
81-line change. It contained the nine map-border alignment fixes, the BFS
nearest-walkable relocation on screen entry, and the greater-than-one-second
stuck failsafe.

A dedicated headless harness verified the border audit, transition landing,
forced-stuck recovery, and BFS behavior.

That PR was comfortably under the cap and represented one clear concern.

PR #6, `feat/quest-combat-and-clones`, stacked on the transition-fix branch.
It contained the notebook-style visual life improvements, enemies, hearts,
weapons, inventory behavior, the Clone-O-Matic, clone mechanics, the `/play`
description update, and ADR-0007 documenting the gameplay expansion decisions
and complexity ceiling.

That second PR was still 644 changed lines.

Fable again did not self-waive the rule. It called out the remaining
violation in the PR description as a maintainer decision and offered a
stricter split into graphics, combat, and clones.

That is where the rule got interesting.

A compliant three-way split was possible.

But the 400-line cap is a proxy for reviewability and concern size. It is not
valuable because 399 is morally different from 401.

In this case, the implementation was a self-contained vanilla-JavaScript demo
file already outside the normal automated test perimeter. The work came from
one gameplay charter. The code was organized into explicit sections. Forcing
three more stacked review cycles might create more branching and rebase
overhead than review clarity.

That does not mean rules are optional.

It means a governance rule that repeatedly misrepresents the work should be
refined instead of silently ignored or obeyed into absurdity.

The possible refinement surfaced by the work was to apply the hard 400-line
cap primarily to `src/`, while treating self-contained demos under
`public/play/` as soft-capped at reviewer discretion, with waivers documented
in the PR.

I am not claiming that policy change landed.

The point is that the work surfaced the governance question.

That is useful.

## What Stayed Unfixed

There were honest loose ends.

Home Meadow still has a pre-existing rendering quirk where the larger house
body can be painted over by neighboring tile background fills, leaving mostly
the roof visible.

That appears to be a tile render-order issue. It predated this work and was
left untouched.

There are also questions the scratchpad harness cannot answer:

- whether the new action button is comfortable and thumb-reachable on a real
  phone
- whether the blue clone tint reads as blue instead of muddy gray over the
  yellow player sprite
- whether bonk feedback feels satisfying against both enemy types

That is the boundary between programmatic validation and playtesting.

The harness can prove that a clone cap holds. It cannot prove that the clones
feel funny in the right way.

The placeholder enemies also create a clear future handoff for Kai: draw one
grumpy monster and one spiky monster in pencil so the prototype can stop
using temporary agent doodles.

Fable also created and applied an `ai-assisted` GitHub label to both PRs.
That is small, but it may become useful provenance. Over time, those labels
could make it easier to look back at how much repository work was
agent-assisted and what kinds of changes needed extra governance attention.

## Why The Day Mattered

Day 65 mattered because Boo-Boo Story became more playable without becoming
less itself.

The visual work tried to preserve the kid-notebook identity. The bug fix made
the world safer to traverse. The enemies and hearts gave exploration a little
pressure. The Star Thrower added a reason to find the chest. The
Clone-O-Matic turned a funny idea into a concrete mechanic.

But the deeper lesson was about the system around the work.

I am increasingly using these projects to test not only whether an agent can
write code, but whether the surrounding repository can cause the agent to
notice when the requested work and the standing rules disagree.

In this case, `AGENTS.md` did not magically prevent an oversized diff.

What it did was make the conflict visible.

Fable reported the issue. It suggested a split. It performed the split. It
escalated the remaining exception instead of self-authorizing it.

That may be more valuable than a rule that blindly blocks all exceptions.

The point is not to worship the line count. The point is to make reviewability
visible enough that humans and agents can reason about it together.

That is the kind of governance I want more of.

Not a checklist that pretends every case is identical.

A contract that helps the work tell the truth about itself.

## Outcome

Day 65 moved Boo-Boo Story's Boo-Boo Quest prototype closer to a small game
while keeping it clearly in prototype territory.

The day started with a visual-life prompt: make the game feel more alive
without erasing its kid's-notebook identity. The requested effects stayed
inside that language: pencil-like shadows, drifting water squiggles, wiggling
trees, swaying flowers, doodle tile variants, walking dust puffs, and
stronger bonk feedback through small screen shake and star-burst doodles.

Before the new gameplay, Fable fixed a real transition bug. Boo-Boo could
spawn inside a solid tile after a screen transition and become stuck. The fix
added `nearestWalkable()` BFS recovery on screen entry, applied it for all
four transition directions, added a greater-than-one-second stuck failsafe,
and audited map-edge consistency.

The audit found nine real neighboring-screen border mismatches, including
Forest Path to Wiggly Woods, Rocky Climb to Echo Cave, River Crossing to Quiet
Grove, and several one-way edge openings around Home Meadow, Flower Patch,
and Boulder Garden. Those map data issues were corrected.

The prototype then gained kid-tuned bonk interactions. The placeholder
enemies were a one-bonk Wanderer and a two-bonk Chaser. The enemies pop into
stars and doodles rather than using death or violence framing. Boo-Boo gained
a three-heart HUD with half-heart damage, heart pickups, a starting Bonk
Hammer, and a Star Thrower found in a Rocky Climb chest.

The Clone-O-Matic was added to Open Field as a hand-drawn cardboard-box
contraption. It can create up to three blue-tinted Boo-Boo clones using Kai's
existing sprite frames. The clones follow by delayed position trail, can bonk
enemies they touch, can absorb a nearby hit for the player, and pop into
stars when left behind on a screen transition.

Validation stayed temporary and bounded. Because ADR-0005 keeps `public/`
demos outside the normal test perimeter, Fable used a scratchpad headless
DOM-stub harness rather than silently adding permanent tests. The harness ran
the real game loop in Node and passed 16 checks, including all 17 neighboring
screen borders, transition recovery, stuck recovery, combat interactions,
damage, respawn, clones, and locked weapon-slot behavior. Headless Edge
screenshots also checked title, Home Meadow, Open Field, and Rocky Climb
presentation. `pnpm validate` and the site build passed.

The first implementation exceeded the 400-line cap at 623 lines. Fable
reported the violation and proposed a split. The work became two stacked PRs:
PR #5, `fix/quest-transition-stuck`, with an 81-line transition-correctness
fix against `main`; and PR #6, `feat/quest-combat-and-clones`, with the
larger gameplay round stacked on top.

PR #6 still exceeded the cap at 644 changed lines. Fable documented the
exception as a maintainer decision and offered a stricter split into graphics,
combat, and clones. That surfaced a governance refinement question: whether
self-contained `public/play/` demos should be soft-capped differently from
core `src/` work, with any waiver documented in the PR. That policy was not
completed in this day's repository history; it was the question the work
exposed.

The pre-existing Home Meadow house render-order quirk remained unfixed. The
scratchpad harness also could not answer real playtesting questions around
phone ergonomics, clone tint readability, or bonk feedback feel. The
placeholder enemy art remains a future handoff for Kai.

## Definition Of Done

Day 65 reached the Boo-Boo Quest bug-fix and gameplay-prototype checkpoint:

- confirmed the post follows Day 64 for July 4, 2026
- assigned the July 5, 2026 work to Day 65
- kept Boo-Boo Story as the primary subject
- framed the work as prototype progress rather than a polished game launch
- preserved the kid's-notebook visual identity as the product constraint
- avoided describing the visual direction as generic graphical improvement
- added visual-life ideas inside the paper, pencil, marker, and doodle style
- started from the real transition-stuck bug before adding gameplay features
- described the fixed-entry spawn failure mode
- required defensive recovery rather than moving one obstruction
- used BFS nearest-walkable recovery after screen transitions
- applied the recovery to transitions in all four directions
- added the greater-than-one-second stuck failsafe
- audited neighboring map edges
- found nine real map-border mismatches
- aligned the broken map openings
- separated the urgent transition-correctness fix from the gameplay round
- introduced kid-tuned bonking without blood or death language
- preserved the snack-and-respawn framing for running out of hearts
- added Wanderer and Chaser placeholders without treating them as final art
- marked the enemy doodles as future Kai-art replacements
- added hearts, half-heart damage, pickups, and inventory selection
- added the Bonk Hammer as the starting weapon
- added the Star Thrower as a Rocky Climb chest reward
- limited active star projectiles to three
- added a touch action button
- implemented the Clone-O-Matic as a cardboard-box contraption
- capped clones at three
- reused Kai's Boo-Boo sprite frames for clones
- kept clone following as delayed position-trail behavior
- avoided overstating clone behavior as autonomous game AI
- let clones bonk enemies and absorb nearby hits
- made left-behind clones pop into stars on screen transition
- validated risky behavior with a temporary scratchpad harness
- respected ADR-0005 by not silently expanding the permanent test perimeter
- checked all 17 neighboring screen borders
- reached zero remaining border mismatches in the harness
- checked transition unstick and forced-stuck recovery
- checked hammer interactions, half-heart damage, and respawn
- checked clone cap, following, and hit absorption
- checked the initially locked second weapon slot
- used headless Edge screenshots for notebook-style visual review
- passed `pnpm validate` and the site build in the implementation report
- reported the initial 623-line cap violation
- split the work into PR #5 and PR #6
- kept PR #5 focused on transition correctness at 81 lines
- left PR #6 as the larger gameplay round
- documented the remaining 644-line exception as a maintainer decision
- surfaced a possible future refinement to the 400-line rule
- did not claim that the policy refinement was completed
- left the pre-existing Home Meadow render-order quirk untouched
- identified phone ergonomics, clone tint, and bonk feel as playtesting
  questions
- preserved the core lesson: the repository rule made the conflict visible,
  and the agent escalated the judgment instead of self-authorizing it
