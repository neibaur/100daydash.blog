---
title: "Day 73 - July 13, 2026: Less Time, More Intentional"
description: "A Day 73 reflection on starting a new job, treating Kai's Boo-Boo Story feedback as product direction, and using a smaller block of time for honest triage instead of claiming implementation."
pubDate: "2026-07-13"
day: 73
dashboardSlug: "none"
dataSources:
  - "Kai Boo-Boo Quest bug reports and visual feedback"
  - "Kai house, bad-guy, and flamethrower artwork"
  - "Boo-Boo Story Claude planning-session notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - boo-boo-quest
  - product-feedback
  - scope-management
  - asset-pipeline
  - planning
---

July 13 was my first day at a new job.

That changed the operating conditions around this 100-day project. The work
now has to coexist with a full workday and a smaller block of personal
development time in the evening.

This is not a crisis, and it is not an excuse. It is simply a real constraint.
The question is no longer only what the project needs next. It is also what I
can responsibly finish in the time available without converting an unfinished
plan into a story about progress that did not happen.

Day 73 did not produce code for Boo-Boo Story.

I did not fix a bug, prepare an image, ask Fable to implement a feature, or
open an implementation pull request. I began a Claude chat to organize a new
set of bugs and visual feedback from Kai. The session was useful, but it
stopped at planning.

That is the honest boundary of the day.

The useful work was turning direct observations into smaller candidate
workstreams, identifying which changes depend on prepared artwork, and finding
one sentence whose meaning needs to be clarified before anyone should code
against it.

With less time available, those distinctions matter more.

## Kai Was Describing The Product

Kai reported that the newer Boo-Boo character faces the wrong direction while
moving. Its movement creates dust, but its legs do not alternate or shift the
way the original character's walking animation does.

He also pointed out that the house graphic is only a small corner or partial
snippet. He supplied the complete house drawing that should eventually replace
it.

The current circular enemies should become a new Boo-Boo-like bad-guy
character from his drawing. Those enemies should shuffle with the same
foot-wobbling motion used by the main character.

For the flamethrower, Kai supplied two fire drawings. He wants the game to
alternate between them so the flame looks active rather than behaving like a
single static image.

He also said that the main character needs to be called `Boo-Boo-1`.

It would be easy to reduce this to a list of visual corrections. That would
miss what the feedback says about the game.

A character facing the wrong direction does not merely have an incorrect
transform. It makes movement feel unresponsive because the character's pose
disagrees with the player's input. Dust moving while the legs remain fixed
creates a similar mismatch. The individual effects exist, but they do not
combine into coherent walking.

Replacing circular enemies with a character from Kai's drawing is not just an
asset swap. It moves the game away from abstract placeholders and closer to
the world he imagines. Reusing the existing foot wobble would give those
enemies a motion language that belongs to the same world without inventing a
new animation system for them.

Alternating two fire frames is technically small. Perceptually, it can be the
difference between displaying a picture of fire and making the weapon feel
alive.

The broken house crop is another useful lesson. An image can technically be
present in the game and still fail to communicate the intended object. The
complete drawing matters because the house is not a corner of an asset. It is
a place in Kai's world.

These are product decisions expressed through gameplay observations. Kai is
not decorating an implementation after the important work is complete. He is
showing what the implementation needs to become.

## The Plan Was A Sequence, Not A Batch

The Claude session did not turn the reports into one large fix request.

It proposed an initial grouping:

1. animate the flamethrower by alternating the two supplied fire frames
2. bring Boo-Boo-1's movement closer to the original character, including
   facing direction, leg shifting, and the unresolved naming question
3. replace the incomplete house asset
4. redesign the enemies with Kai's bad-guy art while reusing the existing
   foot-wobble behavior

That sequence is not a finalized engineering decision. It is a first attempt
to give each concern a reviewable boundary.

The fire change should not become a generic animation framework. The enemy
replacement should not become an enemy registry redesign. Movement parity
should reuse behavior the game already has where practical. A batch of bug
reports is not permission to rewrite the animation or entity systems.

This is the same repository-grounded discipline that has shaped the recent
Boo-Boo Story work: one concern at a time, evidence from the code before a
prompt is written, and no scope earned merely because adjacent improvements
are easy to imagine.

Smaller pull requests become more valuable when my available time becomes
smaller. A narrow change is easier to prepare, review, validate, and stop after
without leaving several unrelated systems half-finished. It creates a useful
checkpoint instead of demanding that an evening absorb an entire feature
batch.

The proposed sequence is valuable because it acknowledges dependencies too.
Several implementation tasks should not begin until the supplied artwork is
ready for production use.

## Attached Artwork Is Not A Production Asset

Kai's drawings cannot be treated as interchangeable image files that an agent
can simply drop into the game.

The bad-guy drawing and both fire images appear to be photographs of physical
artwork. They will likely need the repository's existing scan-processing
workflow: orientation correction, background removal or segmentation, and the
same kind of visual inspection previously used for marker or painted art.

The house appears closer to a clean drawing or scan. It may be a better fit for
the existing ink-extraction path.

Those are hypotheses from the planning session, not completed processing
results.

Before implementation, the images still need to be inspected at their real
dimensions and orientation. Background removal needs to preserve the marks
that belong to Kai's drawing. The outputs need to be checked visually rather
than accepted because a script completed. Archival files and game-sized
versions should remain distinct, following the existing art pipeline.

The expected destination discussed in the session was the established Kai
asset area under `packages/site/src/assets/kai/`. That path was part of the
plan. No files were added there on July 13.

This ordering matters. If I ask an implementation agent to wire unprepared
photos into the game, the prompt silently delegates asset judgment along with
code changes. The agent may crop, rotate, segment, resize, or rename the files
in whatever way makes the immediate implementation work. Even if the game
builds, that can create inconsistent archival handling and lose details from
the original art.

Asset preparation is not administrative work before the implementation. It is
part of the implementation.

## One Name Hid A Product Decision

Kai's statement that the main character "needs to be called Boo-Boo-1" sounds
specific. It is also ambiguous.

He may mean that `Boo-Boo-1` should be the internal or conceptual name for the
newer character or skin. He may instead mean that the player should visibly
see the name in the game, perhaps in the HUD, on the title screen, or in a
character selector.

Those interpretations produce different acceptance criteria.

The first might be resolved through naming in data, code, or documentation.
The second introduces a user-interface decision: where the label appears,
when it appears, and whether other characters need the same treatment.

The planning session identified the ambiguity. It did not resolve it.

This is a good example of a small sentence hiding meaningful scope. Asking for
clarification before implementation is not slowing the project down. It is
preventing an agent from choosing a product behavior simply because one
interpretation is easier to code.

## Planning And Implementation Need Different Discipline

The Claude session also briefly considered whether one model family should
continue from bug triage into implementation-prompt preparation.

The useful takeaway was not that one commercial model is objectively best.
Planning and implementation ask for different kinds of discipline.

Planning requires judgment about boundaries, dependencies, ambiguity, and
scope. It needs to distinguish what the repository already supports from what
a short piece of feedback merely suggests.

Implementation requires disciplined execution against those boundaries. It
needs to inspect the code, preserve existing behavior, add appropriate
evidence, and stop when the acceptance criteria are met.

Using the same model family across those stages may make the handoff more
predictable because the vocabulary and context remain familiar. But the model
name matters less than the written constraints and the repository evidence
carried into the task. A vague plan handed to a capable coding agent remains a
vague plan.

Today only reached the planning side of that handoff.

## A Planning Session Still Has A Stopping Point

It is tempting during a daily project to treat the existence of a plan as
evidence that the work described by the plan is underway.

That is how activity begins to sound like completion.

On July 13, Kai's feedback was gathered. The reports were grouped into
possible workstreams. The need for asset processing was identified. The
`Boo-Boo-1` naming question remained open.

No artwork was processed. No archival or game-sized assets were created. No
code changed in Boo-Boo Story. Fable did not implement anything. No
implementation pull request was opened.

That stopping point does not make the planning meaningless. It makes the next
step clearer.

The artwork should be prepared and visually verified first. Then one tightly
bounded concern can be passed to the implementation agent with the relevant
repository evidence and explicit non-goals. The other reports can remain in
the queue without being smuggled into the same change.

Starting a new job changed the number of hours available to this project. It
did not change the standard for describing what happened during them.

The project can continue at a pace that fits the new constraint. That will
require smaller pieces, clearer stopping points, and more deliberate choices
about what earns an implementation session.

Less time does not make planning count as shipped code.

It makes intentional scoping count for more.

## Outcome

Day 73 was the first day of my new job and the first day this project operated
within a meaningfully smaller block of personal development time.

The only Boo-Boo Story activity was an initial Claude planning session around
Kai's latest bug reports and artwork. The session grouped the work into
possible flamethrower animation, Boo-Boo-1 movement parity, house replacement,
and enemy-redesign concerns. It also identified that the photographed bad-guy
and fire artwork will likely need orientation and segmentation work, while the
house may fit the existing ink-extraction path. Archival and game-sized assets
should remain separate under the established Kai asset pipeline.

The plan remains preliminary. The meaning of "needs to be called Boo-Boo-1"
is unresolved, and no implementation choice was made on Kai's behalf.

No assets were processed, no code was changed, Fable performed no
implementation, and no Boo-Boo Story pull request was opened. The next useful
step is to prepare and verify the supplied artwork, then hand off one bounded
task at a time at a pace that fits the new constraint.

## Definition Of Done

Day 73 reached the intentional-triage checkpoint:

- followed the existing Day 72 post with the July 13, 2026 entry
- stated that July 13 was my first day at a new job
- treated reduced evening availability as an operating constraint
- stated plainly that the day produced no Boo-Boo Story code
- recorded all seven issues and requested changes from Kai's feedback
- treated Kai's observations as product direction rather than cosmetic notes
- separated the initial work into reviewable candidate concerns
- kept the proposed sequence explicitly preliminary
- avoided turning fire animation into an animation-framework proposal
- avoided turning enemy art into an entity-system redesign
- identified asset preparation as a prerequisite to implementation
- distinguished photographed artwork from production-ready game assets
- recorded the likely segmentation and ink-extraction paths as hypotheses
- preserved the expected archival and game-sized asset distinction
- mentioned the expected Kai asset area without claiming files were added
- recorded the unresolved meaning of the `Boo-Boo-1` name request
- distinguished planning judgment from implementation discipline
- made no unsupported model-ranking or release-status claim
- claimed no asset processing, code changes, Fable work, or implementation PRs
- set the next step as verified asset preparation followed by one bounded task
