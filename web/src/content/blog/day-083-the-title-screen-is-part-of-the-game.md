---
title: "Day 83 - July 23, 2026: The Title Screen Is Part of the Game"
description: "A Day 83 reflection on repairing Boo-Boo Quest's title-screen layout, interactions, and state boundaries without giving away the adventure."
pubDate: "2026-07-23"
day: 83
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #85 through PR #89 implementation and validation notes"
  - "Boo-Boo Quest title-screen layout, world-map, weapon-preview, and browser-verification notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - game-development
  - responsive-design
  - state-management
  - testing
  - scope-management
---

The first problems looked cosmetic.

The top of Kai's title logo was clipped. The Design Studio button was cut off
at the bottom of the game box. Boo-Boo appeared to hold a hammer by its head
instead of its handle.

Each one seemed like the kind of bug that should yield to a small CSS nudge.

Instead, they exposed a set of hidden contracts running through the Boo-Boo
Quest title screen: what a test was actually allowed to require, which
container owned overflow, how a browser-rendered emoji behaved under
animation, what the map could reveal before the adventure began, and whether
trying a weapon meant the player now owned it.

The title screen had gradually become more than a static splash image. Before
pressing START, a player can move Boo-Boo, try animations and sounds, inspect
the map, choose among Kai's character and art options, and now preview every
weapon.

That playfulness is valuable. It gives someone a low-pressure way to meet the
game before committing to the adventure.

It also means the title screen needs real layout rules, state boundaries, and
regression tests.

Across [PR #85](https://github.com/neibaur-labs/boo-boo-story/pull/85),
[PR #86](https://github.com/neibaur-labs/boo-boo-story/pull/86),
[PR #87](https://github.com/neibaur-labs/boo-boo-story/pull/87),
[PR #88](https://github.com/neibaur-labs/boo-boo-story/pull/88), and
[PR #89](https://github.com/neibaur-labs/boo-boo-story/pull/89), I treated the
space before START as part of the product rather than decoration around it.

## The First Constraint Was A Test

Before moving the clipped Design Studio link, I found a test that effectively
required it to remain inside the title overlay.

The stated product need was simple: the start screen should provide a working
link to `/design`. The test asserted something narrower. It searched the
source for the title-screen element followed by the link, pinning the link to
a particular location in the markup.

That location was part of the problem.

The title overlay lived inside a fixed-height, clipped game wrapper. Keeping a
page-level navigation link inside that wrapper made it vulnerable to the
wrapper's overflow behavior. A test intended to protect access to the Design
Studio had accidentally preserved an implementation detail that prevented the
link from rendering correctly.

I changed the baseline first in PR #85. The revised test identifies the link
through its own `designlink` ID and `/design` destination. It still fails if
the link disappears, is renamed, or points somewhere else. It no longer
dictates which container must enclose it.

Separating that test-only change mattered.

If I had rewritten the assertion while moving the production markup, the same
diff would have both changed the behavior and weakened the rule that judged
it. By making the test correction stand alone, I could show that the new
assertion passed against the existing implementation and preserved the real
requirement.

This was a useful reminder that tests are not automatically the truth. They
are executable descriptions of what someone believed should remain stable.
Sometimes they protect user-visible behavior. Sometimes they freeze an
accidental arrangement.

The work is to know which one I am looking at before I let the test constrain
the fix.

## The Clipped Elements Were Not The Root Cause

With the test baseline corrected, I could address both visible clipping
problems together in PR #86.

The logo and link sat at opposite ends of the title column, but they shared one
cause.

The overlay was absolutely positioned inside the game wrapper. Its available
height came from the canvas and HUD rather than from its own content. The
column was taller than that space, and vertical centering distributed the
overflow above and below the visible area. The parent then hid both ends with
`overflow:hidden`.

The natural instinct would have been to shrink the logo directly or pull the
button upward. Either adjustment might have repaired one screenshot while
leaving the underlying relationship intact.

Instead, I changed the column to start at the top and made vertical scrolling
the fallback. Content can now grow downward from a reachable origin. On short
screens, nothing is centered into negative space above `scrollTop: 0`.

The logo became the flexible item in the column. The controls beneath it have
useful fixed sizes, while the logo can give up height and preserve its aspect
ratio. That required clearing the replaced image's intrinsic minimum-height
behavior and using `object-fit: contain`, not editing or distorting Kai's
artwork.

The Design Studio link moved outside the clipped overlay into a page-level top
bar. The bar uses the same width as the game box and aligns with its edges, so
the navigation remains visually connected without pretending to be a game
object.

Headless browser measurements at desktop and phone widths confirmed that the
top bar and game box aligned and that the repaired title content no longer
overflowed its available height.

The measurements mattered because CSS explanations can sound convincing while
the browser still computes something different. Inspecting the live geometry
turned the layout theory into evidence.

That browser pass also found a separate mobile problem: the physical-control
row is wider than a phone viewport. I left it alone. It belongs to a different
container with different sizing rules, and folding it into the title-overlay
fix would have expanded the concern without improving the reasoning behind
either change.

Scope control was part of the repair.

## The Hammer Was Its Own Kind Of Asset

The next defect looked like an art-orientation problem.

On the title screen, Boo-Boo appeared to hold the hammer by its head. Because
the character can face either direction, the first suspects were the
character-facing flip and the source artwork.

Neither was responsible.

The title-screen hammer was not one of Kai's assets. It was the browser's
Unicode hammer emoji. Its built-in orientation placed the head against
Boo-Boo's body and the handle outward. Mirroring Boo-Boo and the hammer
together when the character faced left preserved the same bad relationship in
both directions.

The fix in PR #87 was to mirror the glyph itself.

That small transform had an animation consequence. CSS animation keyframes
replace a base `transform`; they do not automatically add their rotations to
it. Mirroring the resting hammer was therefore not enough. Every swing
keyframe also had to preserve the mirror.

Transform order mattered too. Rotation and mirroring are not interchangeable
operations. Applying them in the wrong order could make the swing travel in
the opposite direction even if the resting grip looked correct.

Regression tests now protect the base mirror, the mirror inside each swing
keyframe, and the intended order of rotation and reflection.

I also checked the other weapons rather than generalizing from the hammer.
They did not share the defect. Some were symmetrical, some were procedurally
drawn, and others already had controlled orientation.

The lesson was not that every weapon needed another transform. It was that a
browser-native glyph carries visual geometry of its own. An emoji may be
convenient, but it is not interchangeable with a deliberately controlled art
asset.

Kai's artwork was not wrong, and the fix did not change it.

## A Playground Should Not Spoil The Adventure

The title screen's growing interactivity raised a different kind of question:
how much of the game should be visible before START?

Players were intentionally allowed to open the world map from the playground.
Disabling that interaction would have reduced the sense that the controls were
real. But the initial game state already marked Home Meadow as seen, so the map
revealed its name, showed the current-location marker, and explained that the
player was there before the adventure had begun.

The map was available by design. The information leak was not.

PR #88 added a small pure `mapCellState` function in the existing world
module. Before START, every cell resolves to unseen. After START, the current,
seen, and unseen rules behave exactly as they did before.

The "you are here" portion of the legend is hidden during the pre-game state
as well. The explanation for unexplored cells remains visible, so the map is
still understandable without revealing a location.

This did not require a new game-phase architecture or a large component
extraction. One explicit boundary in a unit-testable function was enough.

The tests cover every pre-game cell remaining unrevealed, the absence of a
current-location marker, the hidden legend entry, the return of normal
discovery after START, and the marker following Boo-Boo as the player moves.

During the work, I noticed that the star marker may be clipped by a map cell's
overflow behavior after START. I preserved that established behavior. The PR
promised to prevent pre-game disclosure, not to redesign the post-START map.

Again, a nearby finding became a documented follow-up rather than an excuse to
make the current patch larger.

## Trying Is Not Owning

The repaired layout created room for one more useful interaction.

Until PR #89, the title playground demonstrated only the Bonk Hammer. I added
four weapon buttons so players can preview the Bonk Hammer, Star Thrower,
Water Gun, and Flame Thrower.

The picker reuses the game's existing inventory-slot button style. Selecting a
weapon changes the title-screen glyph, performs the swing animation, and plays
the sound already associated with that weapon. Number keys 1 through 4 choose
preview weapons before START and retain their normal inventory behavior after
START.

The difficult part was not drawing four buttons. It was preserving the
difference between previewing a system and progressing through it.

The selected preview weapon lives in a title-screen-only variable. It never
updates the real inventory slot or any weapon-ownership flag. After START, the
player still holds only the hammer. The other weapons remain unavailable until
they are discovered, and trying to equip one still produces the existing hint
about where it can be found.

Regression tests specifically pin that boundary. They verify the initial
hammer-only state, refusal and hints for undiscovered weapons, and normal
equipping after a weapon has actually been earned.

Browser verification then exercised keys 1 through 4, confirmed the selected
glyphs and sounds, and showed that the new row still fit. The flexible logo
from the layout repair could absorb the added controls without clipping START
or Kai's art credit.

That sequence made the earlier layout work more valuable. The title screen did
not merely fit today's content; it had a clear rule for how to respond when
the playful preview gained another row.

One inconsistency remains. The action button continues to display a hammer
while another title-screen weapon is selected. I attempted a direct update and
backed it out after finding that the preview label could survive into the real
game until the HUD refreshed.

A cosmetic fix that leaked preview state across START would have violated the
more important boundary. Correcting it belongs with the HUD transition, not as
an extra write from the picker.

Final validation for the weapon-preview work passed 382 tests across 52 files.

## Small Bugs Were Boundary Tests

The title screen now does more while giving away less.

Its content fits the game box instead of disappearing beyond it. Page
navigation sits in page chrome. Boo-Boo grips the browser-rendered hammer by
its handle. The map can be explored as an interface without revealing the
adventure's starting state. Every weapon can be tried without silently
entering the inventory.

None of those outcomes required treating the title screen as a separate game
or inventing a new architecture around it.

They required taking its existing interactions seriously.

The clipped logo revealed a container contract. The clipped link revealed a
test contract. The backwards hammer revealed a rendering and animation
contract. The world map revealed an information boundary. The weapon picker
revealed a state boundary between trying and earning.

The common pattern was that the visible defect sat at the edge of two systems.
Fixing only the visible element would have hidden the symptom without making
the boundary clearer.

Day 83 reinforced a lesson that keeps appearing throughout this 100-day
project: small bugs are often useful questions in disguise.

What behavior does the test really protect? Which container decides the
geometry? Which state owns this interaction? What can a player inspect without
receiving it? Which adjacent problem can wait for its own focused change?

The title screen is still the space before the game begins.

It is also part of the game experience, which means its promises deserve the
same care as everything that happens after START.

## Outcome

Day 83 completed the July 23 Boo-Boo Story title-screen work represented by
PRs #85 through #89.

PR #85 replaced a source-order assertion with a behavioral navigation
contract, allowing the Design Studio link to move without weakening its
coverage.

PR #86 fixed the shared cause of the clipped logo and controls by top-aligning
the title column, adding scroll fallback, making Kai's logo flex safely, and
moving page navigation into an aligned top bar. Desktop and phone browser
measurements confirmed the repaired geometry.

PR #87 corrected the Unicode hammer's grip by preserving its mirror through
every animation transform while leaving Kai's artwork unchanged.

PR #88 kept every map cell and the current-location legend unrevealed before
START, then restored the existing discovery behavior after play began.

PR #89 added four title-screen weapon previews with their existing sounds and
number-key controls while keeping preview selection completely separate from
inventory ownership. Final validation passed 382 tests across 52 files.

Across the five changes, the title screen became a more dependable interactive
playground without revealing discoveries, granting progression, or absorbing
unrelated fixes.

## Definition Of Done

Day 83 reached the Quest Kai title-screen checkpoint:

- followed Day 82 with the July 23, 2026 entry
- treated Boo-Boo Story PRs #85 through #89 as one connected engineering story
- linked every source pull request
- distinguished the user-facing navigation requirement from accidental DOM
  enclosure
- recorded the tests-first baseline change separately from the layout fix
- explained the fixed-height wrapper, centered overflow, and clipping root
  cause
- preserved Kai's logo artwork while allowing its rendered size to flex
- moved the Design Studio link into page chrome aligned with the game box
- recorded desktop and phone browser measurements
- left the separate mobile physical-control overflow issue out of scope
- identified the title-screen hammer as a Unicode glyph rather than Kai's art
- preserved mirroring and transform order through every swing keyframe
- verified that other weapons did not share the hammer's orientation defect
- kept the pre-START map available while hiding discovery and current-location
  information
- preserved the established post-START map behavior
- left the possible post-START star-marker clipping issue unchanged
- added all four weapon previews through existing slot styles and sounds
- preserved normal number-key inventory behavior after START
- kept title-screen preview state separate from inventory and ownership
- recorded the 382-test, 52-file final validation
- backed out an action-button label change that could leak preview state into
  play
- documented adjacent findings without expanding the five focused changes
