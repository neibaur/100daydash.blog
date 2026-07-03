---
title: "Day 61 - July 1, 2026: Designing the Surface Before Building It"
description: "A Day 61 reflection on HaoMiantiao M8 detail-drawer planning, repo-grounded governance, eval evidence from a fabricated policy citation, and lightweight BooBoo Story prototype loops."
pubDate: "2026-07-01"
day: 61
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao M8 detail-drawer spec planning notes"
  - "HaoMiantiao M7 closeout and project-state audit notes"
  - "reviewing-pull-requests eval corpus notes"
  - "ChatGPT M8 review priming notes"
  - "BooBoo Story prototype ideation notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - haomiantiao
  - specs
  - code-review
  - evals
  - product-design
  - prototyping
  - developer-experience
---

Day 61 was about designing better decision surfaces before building the next
thing.

That sounds abstract, but the day had two very concrete shapes.

For HaoMiantiao, the shape was the M8 spec loop. M7 had closed the matchup
screen, so the next question was not "what can the agent implement next?" It
was "what contract does the next implementation need so it does not blur the
product, data, accessibility, and commerce boundaries all at once?"

For BooBoo Story, the shape was smaller and more playful: cheap prototype
concepts that could make a child's product feedback tangible before the idea
hardens into a direction.

Those look like different projects.

They used the same muscle.

Make the artifact early enough that feedback has somewhere to land.

## Opening M8 Without Treating It Like M7

The main HaoMiantiao work was not implementation.

It was the next governance and specification phase after M7.

I worked through a Claude and Fable M8 spec-drafting loop for the detail
drawer milestone. The core product behavior is simple to describe: tapping a
noodle card should open the full noodle detail.

But that simplicity is exactly why the spec needed care.

M8 is the first planned consumer of fields that were deliberately deferred
from M7:

- blurbs
- style chips
- real image rendering
- buy links
- the detail drawer itself

M7 could stay thin because noodle cards were mostly display surfaces for the
matchup flow. M8 changes that. It asks the product to expose more of the
noodle record, more of the visual identity, and the first real commerce
surface.

That makes it heavier than an ordinary UI slice.

It touches image licensing, empty-state honesty, focus management,
accessibility semantics, affiliate disclosure, and the boundary between a
single-noodle detail view and broader shop behavior.

That is not a reason to avoid M8.

It is a reason to specify it carefully.

## Cold-Reading The Repository

The most important instruction in the M8 loop was not a component name or a
visual detail.

It was the requirement to cold-read the repository.

The spec discussion emphasized that an agent should not trust prompt memory
when the repo can be inspected. That mattered because M8 sits on top of
several contracts that are easy to misremember:

- `AGENTS.md` remains the binding contract
- agents should not directly change protected or governance paths
- agent PRs should remain one concern and stay at or below 400 changed lines
- dependency additions require maintainer involvement
- affiliate links must remain plain anchors with
  `rel="nofollow sponsored noopener"`
- no tracker, pixel, or affiliate-library dependency should be introduced for
  M8
- M8 must render honestly against current data

That last point is the product hinge.

The current data shape has blurbs and styles available. Image fields and
`buy[]` entries are empty today.

So M8 cannot pretend the product already has a rich catalog. It needs to
render the real state of the data: useful detail where detail exists, honest
empty states where it does not, and no fake commerce behavior just to make the
screen feel more complete.

That kind of honesty is easy to lose in a spec because empty states feel less
exciting than screenshots.

But an implementation that gracefully shows "not available yet" is more
valuable than one that turns missing data into invented product certainty.

## Drawing The M8, M9, And M10 Lines

The M8 boundary also needed to be drawn against M9 and M10.

M8 is the per-noodle detail drawer and buy-link surface.

M9 is champion, share, clipboard, and share-hash behavior.

M10 is the broader shop strip or aggregated commerce surface.

Those boundaries matter because all three milestones are tempting to mix.

Once the detail drawer exists, it is easy to imagine a richer reveal moment.
Once a champion exists, it is easy to imagine sharing it. Once buy links are
visible on one noodle, it is easy to imagine a shop strip across the whole
experience.

None of those ideas are bad.

They are just not the same slice.

M8 should answer one question: when a user wants more information about a
specific noodle, can the app open a focused, accessible, honest detail surface
without crossing into later milestone behavior?

That is enough work.

The drawer needs to preserve matchup context. It needs a close path. It needs
keyboard and focus behavior. It needs to handle missing image and buy data
without embarrassment. It needs affiliate disclosure rules before there are
even real affiliate links to show.

That is the shape of a serious milestone.

Not big because it has lots of code.

Big because it decides what kind of product surface the app is allowed to
become.

## Cleaning Up The M7 Review Trail

There was also a secondary HaoMiantiao governance thread.

I worked through M7 closeout consistency and project-state cleanup. The point
was not to turn the day into a changelog of `PROJECT_STATE` edits. The point
was to make sure the durable repository story matched the milestone that had
actually closed.

That audit also touched the review-skill evidence from M7.

One finding mattered more than the cleanup itself: a prior review had cited a
supposed `CLAUDE.md` rule about one-line comments or docstrings.

That rule did not exist in `CLAUDE.md` or `AGENTS.md`.

The underlying observation was not absurd. Short comments are often better
than long ones, and over-documentation can be a real style smell. But that is
different from saying the repository has a binding one-line docstring rule.

The distinction became eval evidence:

```text
0009 fabricated-governance-citation
```

That is a good failure to capture.

An accurate style instinct does not justify inventing a governance citation.
If a reviewer wants to make a policy claim, it needs to be source-grounded.
If the source of authority is existing code precedent, say that. If it is a
preference, say that. If it is a repository rule, cite the actual rule.

This is where the review skill becomes more useful by recording failures, not
just successful behavior.

The goal is not to make the reviewer timid.

The goal is to make it precise.

## Priming A Second Review Loop

I also pulled ChatGPT into the M8 thread, but only lightly.

The work there was priming, not review completion.

I shared the Fable M8 prompt so ChatGPT could get grounded for a future
second-pass review. I had not yet sent the actual Fable response that needed
review.

That distinction matters because it keeps the activity honest.

The day did not complete a ChatGPT review of the M8 spec. It prepared the
review surface so the next pass could start from better context instead of a
cold summary.

That is still useful work.

It is just not the same as completing the review.

## Making BooBoo Feedback Playable

The second project thread was BooBoo Story ideation with Claude and Fable.

This was not repository work, and I do not want to overstate it as if a
shippable game milestone landed somewhere.

It was product thinking through prototypes.

Kai is eager to have something playable. He is especially interested in an
RPG-style world where his character can explore, move around, and discover
things.

That kind of feedback is hard to evaluate from words alone.

"An RPG world" can mean a dozen different things. A big production direction
would be premature. The better move is to make cheap, disposable demos that
let the user react to concrete interaction instead of a parent or developer
arguing from imagination.

Four demo concepts emerged:

1. a clickable world map with hotspots and comic-panel popups
2. a walkable character demo with keyboard and touch movement plus proximity
   dialogue
3. a branching choose-your-adventure or visual-novel style demo
4. a Zelda-like screen-by-screen exploration demo with a sprite, tile
   collisions, explored screens, and a map view

The useful part is that none of those needs to be the final direction.

They are probes.

A child can tell you very quickly whether clicking places on a map feels like
an adventure, whether walking a character around matters more than story
choices, whether dialogue is fun or boring, and whether screen-by-screen
exploration creates the right sense of discovery.

That feedback is much better than debating the genre in the abstract.

The prototype is not the product.

It is the question made playable.

## The Shared Pattern

HaoMiantiao and BooBoo Story are very different contexts, but Day 61 made the
shared pattern obvious.

HaoMiantiao needed specs, audits, and eval cases before M8 implementation.
BooBoo needed small demos before committing to a game direction.

Both are ways of reducing ambiguity before the expensive part starts.

For agents, the artifact is a spec that says what the next PR may touch, what
it must not touch, and what repository authority it needs to obey.

For reviewers, the artifact is an eval case that captures a failure mode
precisely enough to test for it later.

For users, the artifact is a prototype they can react to with their hands and
eyes instead of trying to grade a description.

That is the common thread.

Good artifacts create better feedback loops.

They do not remove judgment. They give judgment a place to stand.

## Why The Day Mattered

Day 61 mattered because it resisted the pressure to turn planning into fake
progress or implementation into premature certainty.

M8 is not implemented yet.

That is okay.

The detail drawer is now framed as a milestone with real product and
governance weight: current data honesty, image licensing, buy-link disclosure,
focus management, and clean boundaries from M9 share behavior and M10 shop
aggregation.

The review-skill work also became sharper. The fabricated governance citation
is exactly the kind of failure that should be preserved. A reviewer can be
helpful while still overstating the source of authority. Capturing that makes
future reviews more grounded.

And BooBoo Story got the right kind of early shape: not a production promise,
but a set of cheap playable questions.

That feels like the useful lesson for the day.

Before building, design the surface where decisions can happen.

For HaoMiantiao, that surface was the M8 spec and the eval case.

For BooBoo, it was tiny RPG-flavored demos.

In both cases, the work was not to make the final thing.

The work was to make the next conversation more concrete.

## Outcome

Day 61 moved HaoMiantiao from M7 closeout into M8 detail-drawer planning
without starting implementation.

The main M8 loop was a Claude and Fable spec-drafting pass focused on the
detail drawer. M8 is the milestone where tapping a noodle card should open a
full noodle detail surface. It is also the first planned consumer of fields
deferred from M7: blurb, style chips, real image rendering, buy links, and
the detail drawer itself.

The M8 discussion emphasized cold-reading the repository rather than trusting
prompt memory. The binding constraints included `AGENTS.md`, protected-path
discipline, one-concern agent PRs, the 400 changed-line cap, maintainer-owned
dependency additions, plain affiliate anchors with
`rel="nofollow sponsored noopener"`, no tracking dependencies, and honest
rendering against today's data.

That data honesty matters because blurbs and styles exist today, but image
fields and `buy[]` entries are empty. M8 must show useful detail where the
data supports it and clear empty states where it does not.

The milestone boundaries were clarified. M8 owns the per-noodle detail drawer
and buy-link surface. M9 owns champion, share, clipboard, and share-hash
behavior. M10 owns the broader shop strip or aggregated commerce surface.

M7 governance cleanup also continued. A project-state and eval-focused audit
identified a prior review problem: a supposed `CLAUDE.md` rule about one-line
comments or docstrings did not exist in `CLAUDE.md` or `AGENTS.md`. That
became eval case `0009 fabricated-governance-citation`, a reminder that
source-grounded review matters even when the underlying style instinct is
reasonable.

ChatGPT was only primed for a future M8 review by sharing the Fable prompt.
The actual Fable response had not yet been sent to ChatGPT for review, so no
completed second-pass ChatGPT review happened on this day.

The BooBoo Story thread stayed in ideation and prototype territory. Kai wants
something playable, especially an RPG-style exploration world. The discussion
favored cheap, disposable demos over committing to production direction:
clickable map hotspots with comic-panel popups, a walkable character demo
with proximity dialogue, a branching visual-novel demo, and a Zelda-like
screen-by-screen exploration demo with sprite movement, tile collisions,
explored screens, and a map view.

## Definition Of Done

Day 61 reached the M8 planning and prototype-loop checkpoint:

- kept M8 as planning, not implementation
- treated M8 as the post-M7 governance and specification phase
- focused M8 on the detail drawer milestone
- defined the user behavior as tapping a noodle card to open full noodle
  detail
- identified M8 as the first planned consumer of deferred M7 fields
- included blurb as an M8 surface
- included style chips as an M8 surface
- included real image rendering as an M8 surface
- included buy links as an M8 surface
- included the drawer itself as an M8 surface
- required cold-reading the repository before spec conclusions
- kept `AGENTS.md` as the binding contract
- preserved protected-path discipline for agents
- preserved one-concern agent PRs
- preserved the 400 changed-line cap
- kept dependency additions maintainer-owned
- required affiliate links to stay plain anchors
- required `rel="nofollow sponsored noopener"` on affiliate links
- rejected tracker, pixel, or affiliate-library dependencies for M8
- required honest rendering against current data
- noted that blurbs and styles exist today
- noted that image fields are empty today
- noted that `buy[]` entries are empty today
- scoped M8 to per-noodle detail drawer and buy-link surface
- kept champion, share, clipboard, and share-hash behavior in M9
- kept the broader shop strip and aggregated commerce surface in M10
- treated image licensing as an M8 product decision
- treated empty-state honesty as an M8 product decision
- treated accessibility and focus management as M8 requirements
- treated affiliate disclosure as an M8 requirement
- continued M7 closeout consistency work without turning it into the whole
  post
- identified the fabricated one-line docstring rule as a review failure
- confirmed the cited rule was not present in `CLAUDE.md` or `AGENTS.md`
- captured the issue as `0009 fabricated-governance-citation`
- framed the eval case as source-grounded review evidence
- primed ChatGPT with the Fable M8 prompt for a future review
- did not claim ChatGPT completed the Fable response review
- resumed BooBoo Story ideation with Claude and Fable
- kept BooBoo as ideation and prototype practice, not committed repo work
- centered Kai's desire for a playable RPG-style world
- preferred disposable demos over early production commitment
- identified a clickable map prototype
- identified a walkable character prototype
- identified a branching visual-novel prototype
- identified a Zelda-like screen-by-screen exploration prototype
- connected both projects through lightweight artifacts and feedback loops
- preserved the core lesson: specs, demos, and eval cases reduce ambiguity
  before implementation hardens
