---
title: "Day 70 - July 10, 2026: The World Needs Edges and the Music Needs Shape"
description: "A Day 70 reflection on turning generated coverage into intentional game design through world-border invariants, structured procedural music, and tests-first agent development."
pubDate: "2026-07-10"
day: 70
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #47 border-sealing implementation and validation notes"
  - "Boo-Boo Story PR #48 structured overworld music implementation and validation notes"
  - "Boo-Boo Quest world-generation and music test notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - boo-boo-quest
  - game-design
  - procedural-generation
  - web-audio
  - testing
  - code-review
---

Day 70 started with two systems that already worked.

Boo-Boo Quest had a complete 6x5 world grid. Every coordinate had a screen,
including generated stubs that left room for Kai and me to add real locations
later.

The game also had overworld music. A lead and bass played through the existing
Web Audio system, respected the mute and volume controls, and looped while
Boo-boo explored.

Neither system was missing its primary function.

But the world had exits that led nowhere, and the music repeated before it had
time to develop.

Those problems looked like small pieces of polish. Close a few gaps with trees.
Replace one short tune with a longer one.

The engineering lesson was larger. Generation can provide coverage, but
constraints are what make the result feel designed.

For the map, that meant giving the world an explicit boundary invariant. For
the music, it meant giving a procedural score sections, phrases, fills, and
controlled variation. In both cases, the answer was not a larger system. It
was a clearer structure around the small system that already existed.

## An Open Edge Is A Promise

Yesterday's expansion turned the main overworld from a 4x3 map into a 6x5
grid. Eighteen new positions use a shared generated stub screen: an empty
meadow, bordered by trees but open on all four sides.

That is a useful default for an unfinished interior location. If a real screen
exists above, below, left, or right, the opening lets the player cross into it.
One generic template can therefore connect the scaffold without pretending
that every new location has already been designed.

The same default becomes false at the edge of the world.

A stub in the top row cannot have a normal northern neighbor. A stub in the
left column cannot have a normal western neighbor. Yet the generic screen
still exposed those passages. A player could walk toward what looked like a
valid exit and discover that the game had nowhere to take them.

This was more than a visual gap.

An opening in a game world is a promise. It says that movement can continue or
that something intentional will happen. If neither is true, the geometry is
lying to the player.

[PR #47](https://github.com/neibaur-labs/boo-boo-story/pull/47) fixed that
without changing the hand-designed screens or weakening the useful interior
connections. The change stayed inside the stub-fill logic in `world.ts`.

When the generator creates a stub, it now checks whether that coordinate sits
on the top, bottom, left, or right boundary. For each applicable side, it
replaces only the off-grid border with the stub's existing tree tile. A
reusable full-width tree row handles the horizontal edges, and the vertical
edges are sealed conditionally before the generated screen is stored.

Interior crossings remain open because they connect real neighboring screens.
Cave and den warp mouths remain valid because those tiles transport the player
instead of invoking ordinary edge scrolling. Hand-designed screens remain
untouched because they were already sealed correctly.

That precision matters. The fix was not "add trees around the map." It was
"remove only the openings whose implied destination does not exist."

## The Test Described The World, Not The Bug Report

The strongest part of the map fix was the specification that preceded it.

The new `quest-kai-border-seal.test.ts` test first demonstrated the failure.
It then became a permanent statement about the world's topology.

The test iterates across every screen on all four outer edges of the 6x5 grid.
Every outward-facing tile must be either solid or a valid cave or den warp
mouth. The existing adjacent-screen crossing test continues to protect the
opposite property: real neighbors inside the grid must retain valid crossings.

Together, those tests define both sides of the boundary:

- an apparent ordinary exit must lead to an adjacent screen
- an outward edge must stop movement unless it intentionally transports the
  player

That is more durable than testing the one screen where someone noticed the
problem. A single coordinate assertion would preserve a patch. The full-edge
iteration preserves a property of the generator.

This is one of the most useful forms of polish: turn the exception that exposed
the flaw into a rule that covers every equivalent case.

The PR changed two files, added 77 lines, removed one line, and preserved all
of the valid crossings already protected by the suite. `pnpm validate`, lint,
and typecheck passed, along with 116 site tests.

The world did not become more authored because its outer row gained tree
tiles. It became more intentional because its generator learned where its own
assumption stopped being true.

## The Music Worked Before It Had Shape

The overworld music had a similar problem in time rather than space.

Before Day 70, it was a short pair of hard-coded lead and bass arrays. The 32
steps advanced at roughly 210 milliseconds each, so the exact sequence returned
after about 6.7 seconds.

That was enough to establish that background music existed. It was not enough
time for the music to make a statement, answer itself, or create anticipation.
The loop restarted almost as soon as the listener recognized it.

The answer in [PR #48](https://github.com/neibaur-labs/boo-boo-story/pull/48)
was not a recorded soundtrack, an AI music service, a bundled audio asset, or
an external library. The game remained fully offline and continued to render
sound through its existing Web Audio setup.

Instead, the small procedural system gained compositional structure.

The new score follows an A/A/B/A form. Section A uses a relaxed C-Am-F-G
progression. Section B answers with a brighter, busier F-G-C-G progression.
Each section spans four bars, producing a 128-step cycle at 200 milliseconds
per step. One complete cycle now lasts about 25.6 seconds.

The arrangement still uses deliberately simple voices: a triangle-wave lead,
a sine-wave bass playing roots and fifths, and a soft high-pass-filtered noise
hat on the off-beats. The final bar chooses one of three rotating fills. On
alternating loops, Section B adds a quiet harmony a fifth above the melody.

The full variation pattern therefore takes six cycles, or roughly two and a
half minutes, to return exactly.

The important change is not just that the loop became longer. Repeating a
larger unstructured array would only postpone the same problem. The score now
has recognizable sections, a contrasting answer, phrase endings, and bounded
variation.

The music knows where it is going before it starts again.

## Making Composition Testable Without Testing Taste

The implementation separated composition from rendering.

The new `src/lib/quest-kai/music.ts` module is pure and deterministic. Its
basic contract is "absolute step in, musical event out." Calling
`musicStepAt(step)` returns the lead, harmony, bass, and hat information for
that position in the score.

`main.ts` remains responsible for time, Web Audio oscillators, the noise-hat
voice, and playback. All of those voices still route through the existing
master gain, so the mute button and volume dial remain authoritative. Muting
stops both tonal and percussion playback. The title-screen tune was
intentionally left unchanged.

This boundary made the musical structure testable without pretending that a
unit test can listen.

The tests-first `quest-kai-music.test.ts` specification checks that a cycle is
at least 20 seconds long, generation is deterministic, and the section order
is A/A/B/A. It verifies that Section B actually differs from Section A, that
melody, bass, and percussion events are present, and that consecutive loops
are not identical. It protects the three-fill rotation and ensures every
generated pitch remains within a safe 60-1600 Hz range.

Those assertions do not prove that the music is beautiful.

They protect the compositional scaffolding that human judgment selected: the
duration, form, contrast, instrumentation, variation, and technical bounds.
Whether the tune feels relaxed, whether the B section arrives at the right
moment, and whether the fills are pleasant still require listening.

That division is honest. The pure score makes intent inspectable and
repeatable. The renderer makes it audible. Tests guard the structure; ears
judge the result.

The PR added no dependency and no audio asset. Its three commits changed three
files, adding 197 lines and removing 14. `pnpm validate`, lint, typecheck, and
123 tests passed. The site build also passed, and the generated site was served
so `/play/quest-kai/` could be loaded in headless Edge. The game booted cleanly
with the new bundle.

## Two Kinds Of Boundary

The map and music changes were separate concerns in separate pull requests,
but they solved the same design problem.

The stub generator had a rule that was valid in the middle of the grid and
invalid at its boundary. The original music loop had enough events to keep
playing but not enough form to create a meaningful cycle.

One system needed spatial limits.

The other needed temporal shape.

Neither needed to be replaced. The map did not need 18 hand-designed screens
before it could become internally consistent. The soundtrack did not need a
studio recording or another runtime dependency before it could develop.

Both needed explicit rules about where generic behavior was allowed to stop.

For the map, a border coordinate changes which exits are valid. For the score,
a section and bar position change which notes, harmony, percussion, or fill
belong next. Those constraints reduce arbitrary output while preserving the
small system's flexibility.

That is what made the results feel more authored.

Procedural generation is sometimes described as the opposite of authored
design. This work made the relationship look different. Generation handles
repetition and coverage. Authorship establishes invariants, chooses form, and
decides which variations belong.

The useful unit of polish is often not a manual correction. It is a rule that
allows the generator to keep doing its job without making promises it cannot
keep.

## Narrow PRs Kept The Agent Inside The Lines

Claude Code performed both implementations, one concern at a time.

The border fix landed first. Only after it merged was the music feature based
on the updated `main`. Each PR began with a new failing specification, then
introduced the production code that satisfied it.

That ordering mattered because the recent Boo-Boo Quest work has expanded
quickly. Enemies, bosses, tools, maps, audio, and a larger overworld have all
arrived through agent-assisted changes. As those systems become richer, their
interactions create questions that were invisible when the game was smaller.

Expanding the grid exposed the false outer exits. Having an overworld loop
exposed the difference between audio that plays and a score that develops.
Refinement did not merely make existing work prettier. It revealed new
engineering properties worth protecting.

The narrow PR boundary helped keep those properties legible. The map PR did
not become a music refactor. The music PR did not revisit world generation.
Tests-first ordering made each change answer an executable contract, while
runtime browser evidence covered the integration that mattered for the audio
work.

That discipline is especially valuable when an agent is changing a playful
project. Fun ideas can still produce broad prompts, overlapping systems, and
difficult-to-review diffs. Keeping one concern per PR does not make the game
less creative. It makes the boundary around each experiment easier to see.

## Why The Day Mattered

Day 70 was not really about tree borders or a longer song.

It was about the point where a functional generated system starts needing a
grammar.

The 6x5 scaffold did its job: it created reachable space for future authored
locations. The border invariant now prevents that generic openness from
claiming that off-grid space exists.

The procedural audio system also did its job: it produced an offline
soundtrack with no asset pipeline or dependency. The pure score now gives
that stream of notes sections, contrast, endings, and variation without
abandoning the compact architecture.

A world does not feel complete merely because every coordinate contains a
screen. Music does not feel composed merely because notes continue to play.

The missing layer is structure: a rule for which exits are real, a form for
when a phrase should answer, and a boundary around which variations remain
coherent.

Generation provided the coverage.

Today, constraints gave it shape.

## Outcome

Day 70 refined two Boo-Boo Quest systems through small, tests-first pull
requests.

PR #47 corrected the boundary flaw exposed by the preceding 6x5 world
expansion. Generated stub screens now seal only their off-grid sides with the
existing tree tile while preserving interior crossings, valid cave and den
warp mouths, and all hand-designed screens. A new test checks every outward
tile on every edge of the world, converting a visual symptom into a durable
generator invariant. `pnpm validate`, lint, typecheck, and 116 site tests
passed.

PR #48 replaced the short overworld loop with a deterministic A/A/B/A score.
The 128-step, 25.6-second cycle contains lead, bass, off-beat hats, rotating
fills, and alternating Section B harmony. Its complete variation pattern
returns after roughly two and a half minutes. Composition now lives in the
pure `music.ts` module while `main.ts` retains Web Audio rendering, timing,
and integration with the existing master gain. The title tune and player
controls remain unchanged. `pnpm validate`, lint, typecheck, 123 tests, the
site build, and a headless Edge boot check passed.

Both PRs stayed dependency-free, followed tests-first ordering, and remained
focused on one concern. Together they showed the same principle in two forms:
generated systems become believable when their boundaries and rhythms are
explicit.

## Definition Of Done

Day 70 reached the intentional-structure checkpoint:

- followed Day 69 with the July 10, 2026 entry
- kept the narrative centered on one shared engineering lesson
- described PR #47 as a correction after the 6x5 expansion, not the expansion
  itself
- treated an apparent exit as a world invariant rather than a tree-placement
  symptom
- covered every outer coordinate and preserved valid interior crossings
- preserved cave and den warp mouths and left hand-designed screens untouched
- described PR #48 as a replacement for the short overworld loop, not the
  game's first music
- kept the music procedural, offline, dependency-free, and rendered through
  Web Audio
- explained the A/A/B/A form, voices, fills, harmony, and variation cycle
- distinguished the pure score module from the audio renderer
- avoided claiming that automated tests prove musical quality
- preserved the existing master gain, mute, volume, and title tune behavior
- recorded the reported repository, build, and browser validation evidence
- connected tests-first ordering and narrow PRs to safe agent development
- preserved the central lesson: generation provides coverage, while
  constraints make the result feel designed
