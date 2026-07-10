---
title: "Day 68 - July 8, 2026: Evidence Around the Artifact"
description: "A Day 68 reflection on shipping self-contained Boo-Boo Quest Canvas game changes with executable verification evidence, headless-browser screenshots, and stacked PR governance."
pubDate: "2026-07-08"
day: 68
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story ADR-0005 self-contained demo architecture notes"
  - "Boo-Boo Quest verification notes"
  - "Boo-Boo Quest stacked PR merge notes"
  - "Boo-Boo Story PR #24 through PR #30 landing notes"
  - "Boo-Boo Story pnpm validate results"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - boo-boo-quest
  - game-design
  - testing
  - code-review
  - developer-experience
---

Day 68 was about a single-file game that was not supposed to become anything
else.

That detail matters.

Boo-Boo Story has a set of self-contained HTML5 game demos. The main one
today was Boo-Boo Quest at:

```text
packages/site/public/play/quest-kai/index.html
```

It is roughly 1,400 lines of HTML, CSS, JavaScript, Canvas drawing, WebAudio,
and base64-embedded artwork.

That sounds like the opening paragraph of a refactor ticket.

It was not.

ADR-0005 says these demos are deliberately self-contained. They are meant to
be hand-edited as isolated artifacts, excluded from the normal Astro
component pipeline and formatting flow. The file is not a half-finished app
waiting to be turned into components. It is a portable browser artifact, and
the repository treats it that way on purpose.

That made the day's engineering question more interesting.

The repository contract normally wants tests-first commits, `pnpm validate`
before pull requests, and PRs under 400 changed lines. Those are good rules.
They protect real properties: reviewability, repeatability, and not letting
untested code become the foundation for more work.

But Boo-Boo Quest has no unit-test surface by design.

So the choice was not between "follow the rules" and "ignore the rules."

The real choice was whether I could preserve the property behind the rule
without forcing the artifact into an architecture it was deliberately designed
to avoid.

That became the lesson of the day.

Tests-first is a useful governance rule, but the deeper requirement is
trustworthy evidence.

When the artifact is intentionally outside the test harness, the answer is not
to abandon verification. It is also not to refactor the artifact merely so the
usual test shape becomes available.

The answer is to build the cheapest credible verification loop around the
artifact that actually exists.

## The Work Was Big Enough To Need Rails

The visible work was a large set of changes across Boo-Boo Story and
Boo-Boo Quest.

At the site level, the `/play` pages became easier to navigate. Every playable
demo page gained a back-to-Play link, so the browser back button was no
longer the only obvious way home. The Play landing page also started rendering
Kai's hand-drawn Boo-Boo artwork through `astro:assets`, matching the pattern
already used by the story pages.

Those were tidy site improvements, but they were not the hard part.

The hard part was the game stack.

Boo-Boo Quest gained an interactive title screen. Before START, the arrow keys
or d-pad can move Boo-Boo inside the title box. The hammer button triggers the
hammer animation. The dance button triggers the dance animation. MAP opens
the world map overlay, and the overlay was moved above the title screen with
a higher z-index. A 16-step synthesized chiptune loop plays through the
existing `tone()` helper.

Dropped hearts gained a lifecycle. After 15 seconds, they start blinking.
After 30 seconds, they despawn. For `prefers-reduced-motion`, the visual
fallback uses translucency instead of blinking.

The enemy system gained elemental variants. Uppercase entries in `ENEMY_DEFS`
now spawn "on fire" versions of existing enemies. Damage routing gained a
source parameter, such as `star`, so the game can distinguish what kind of
hit landed.

That let the rules become specific:

- hammer hits do no damage to burning enemies and show a hint toast
- clone hits do no damage to burning enemies and show a hint toast
- stars always land
- water-gun splashes start a `dousedT` countdown
- while doused, the enemy becomes vulnerable
- if the enemy survives the doused window, it reignites

Three world obstacles then turned tools into specific verbs. A burning bridge
plank requires the water gun. A star crystal in a cave corridor requires the
Star Thrower. A cracked boulder covering a heart container requires the
hammer. Each obstacle is represented as a solid tile type, and
`clearObstacle()` mutates the map array in place when the correct tool
connects.

Then Rumble Rex arrived.

The boss fight lives on a new off-grid arena screen, using the same broad
pattern as the cave interior. Rumble Rex is a dinosaur boss with 6 HP and a
small state machine:

```text
walk -> windup -> charge -> stun
```

When he charges into a wall, he becomes stunned. Hammer damage only lands
during that stun window. Stars can damage him at any time. Defeating him sets
a persistent flag so the den remains peaceful when Boo-Boo returns.

Finally, the audio path became more coherent. All synthesized tones now route
through one `GainNode`. A volume slider sits beside the existing mute button.
A calmer 32-step background loop starts after START and replaces the title
screen chiptune.

That is a lot of game change for one self-contained HTML file.

The fact that the file is intentionally self-contained did not make the work
less risky.

It made the verification problem more specific.

## Syntax First

The first verification layer was intentionally boring.

I extracted the inline `<script>` block from the HTML with a regular
expression and passed the extracted JavaScript to:

```text
node --check
```

This was not a grand test strategy.

It was a cheap gate.

Before asking a browser to run the game, before trying to simulate enemy
state, before taking screenshots, the code at least needed to parse.

That ordering matters. Cheap checks should run before expensive checks. A
syntax error does not need a headless browser screenshot. It needs the
fastest possible failure.

This layer did not prove gameplay correctness.

It prevented a class of waste.

## Then The Page Tested Itself

The second verification layer was more interesting.

For focused mechanics, I copied the game file into a scratch directory and
appended a temporary `<script>` block.

That script could call internal game functions directly:

```text
spawnEnemies()
damageEnemy(e, x, y, "star")
updateCombat(1 / 60, map)
```

The temporary script executed assertions, collected `PASS` and `FAIL`
messages, and rendered them into a fixed-position `<pre>` overlay inside the
page itself.

That changed the shape of the problem.

Boo-Boo Quest did not have a formal test API. It did not need one permanently
just to satisfy this round of work. But the browser artifact could still be
made to produce evidence while it ran.

The page became a temporary witness.

For the fire-enemy rules, that meant the verification could check whether
hammer damage bounced, whether clone hits bounced, whether stars landed,
whether water doused the enemy, whether the vulnerable window behaved
correctly, and whether the enemy reignited when it survived.

For the boss fight, it meant the script could walk Rumble Rex through the
parts of the state machine that mattered: charge, wall collision, stun,
damage, defeat, and the persistent peaceful state afterward.

This was not a new testing framework.

It was executable evidence wrapped around an artifact that already existed.

That distinction kept the architecture honest.

## Screenshots Were Evidence, Not Magic

The third layer was headless browser rendering.

The scratch copy loaded in Microsoft Edge with a command shaped like this:

```text
msedge --headless --disable-gpu --virtual-time-budget=N --screenshot=out.png
```

The screenshot mattered because it captured several things at once:

- the rendered `PASS` or `FAIL` assertion log
- sprite positions
- HUD state
- dialog and hint toasts
- the overall visual state of the Canvas game

That does not mean screenshots replaced tests.

That would be the wrong lesson.

The useful point is that Boo-Boo Quest already exists as an interactive
browser artifact. Running it in a browser, executing targeted assertions
inside the page, and capturing the resulting rendered state gave me more
credible evidence than reading the JavaScript and deciding it looked right.

For a normal module with a clean test surface, I would rather have ordinary
unit tests around the behavior.

For this artifact, browser execution was closer to the truth.

## The Cooldown Bug Was The Proof

The most valuable moment was a failed boss verification.

An early version of the Rumble Rex test simulated repeated warps. My mental
model was simple: advance combat time, repeat the action, watch the state
progress.

That was wrong.

The game has a `warpCd` cooldown. I assumed elapsed combat simulation would
be enough to move that cooldown forward.

But `warpCd` only decrements inside the normal `requestAnimationFrame` game
loop. A direct scripted function call into the combat logic did not reproduce
that part of runtime behavior.

So the verification script had to reset `warpCd` manually between simulated
warps.

That was not an annoying test adjustment.

That was the test paying rent.

It exposed a mismatch between my model of the game and the way the game
actually executes. Code inspection alone can miss that kind of difference
because the pieces are all visible. The cooldown exists. The update path
exists. The combat helpers exist. Nothing looks mysterious.

The mistake appears when the code runs under the same assumptions as the
verification.

That is why executable evidence mattered.

It did not merely confirm the story I already believed.

It corrected it.

## The Stack Kept Review Possible

The second major engineering problem was Git.

All of the game features touched the same single HTML file, so the work was
stacked. Each feature branch was created from its predecessor instead of
directly from `main`.

That was intentional.

If every branch had started from `main`, each later pull request would have
shown all earlier game changes again. Stacking let each PR initially show its
own incremental delta against the preceding feature branch.

That kept review possible and helped preserve the repository's 400-line PR
limit.

The complication arrived at merge time.

GitHub squash-merge collapses a pull request's branch history into one new
commit on `main`. The next stacked branch, however, was created from the
previous branch's original unsquashed history.

After PR N was squash-merged, PR N+1 no longer shared the same ancestry with
`main`, even though its file contents logically included the predecessor's
work.

That made the remaining stack require deliberate base advancement.

The fix was sequential. For PR #24 through PR #30, the process was:

1. retarget the PR base to `main` with `gh pr edit N --base main`
2. merge the newly updated `main` branch into the feature branch
3. push the merge commit
4. verify the resulting diff and mergeability with `gh pr view --json mergeable`

Once the predecessor's squash-merged contents existed on `main`, merging
`main` into the next branch let Git compare against a base that already had
the equivalent file state. The branch still contained its original history,
but the merge base and resulting content comparison changed. The visible PR
diff collapsed back to the feature's actual incremental change.

That avoided force-pushing.

It avoided rebasing or rewriting the shared branch history.

It avoided recreating the PRs.

It also required patience. The stack had to be advanced one PR at a time
because every branch physically contained the unsquashed commits of its
predecessors until those features were represented on `main`.

Stacked PRs optimized review.

Squash merging changed the ancestry assumptions behind the stack.

Neither fact made the other wrong. They just needed an explicit landing
procedure.

## What The Rule Was Really Protecting

The more I use these repositories as agentic engineering laboratories, the
more I care about the property behind a rule.

"Tests first" is a good rule because it prevents unverified code from
becoming the basis for later work. It forces implementation to answer to some
external check.

But a rule is not the property itself.

For Boo-Boo Quest, conventional unit tests were structurally unavailable
without changing the artifact boundary. That did not make verification
optional. It made the evidence design more important.

The verification stack became:

1. parse the extracted inline script with `node --check`
2. run targeted functional assertions inside a scratch browser copy
3. capture headless Edge screenshots of the rendered result

That loop was cheap enough to use repeatedly and credible enough to catch a
real false assumption.

It was not exhaustive.

It was not a permanent game-testing platform.

It was a workable substitute for the repository's normal tests-first workflow
for one artifact that is deliberately outside the normal test harness.

That honesty matters.

The goal is not to win an argument that screenshots are tests.

The goal is to avoid making "this seems to work in my browser" the acceptance
criterion.

## Why The Day Mattered

The day's visible output was fun: title-screen movement, chiptune music,
blinking hearts, fire enemies, tool-specific obstacles, Rumble Rex, and a
proper master volume path.

But that is not what I want to carry forward.

The useful lesson is that an unusual artifact can still be surrounded by
discipline.

The self-contained game file stayed self-contained. The PRs stayed small
enough to review. `pnpm validate` passed. The game PRs carried explicit
verification evidence. The screenshots and rendered PASS/FAIL logs made the
claim visible. The stack landed without force-pushing or rewriting shared
history.

That combination is the part I care about.

The point was not to make Boo-Boo Quest more conventional.

The point was to build enough rails around an intentionally unconventional
artifact that ten separate changes could move through the repository without
turning trust into the test plan.

## Outcome

Day 68 focused on shipping a large set of Boo-Boo Story changes while
preserving the intentional self-contained architecture of Boo-Boo Quest.

The work included 10 PRs in total. The first site-level changes added
back-to-Play navigation across five playable demo pages and rendered Kai's
hand-drawn Boo-Boo artwork on the Play landing page through `astro:assets`.

The game changes all converged on
`packages/site/public/play/quest-kai/index.html`, the intentionally
self-contained Canvas game documented by ADR-0005. The feature work included
an interactive title screen, a 16-step title chiptune, timed heart pickup
despawning, fire enemy variants, source-aware damage routing, three
single-tool obstacles, the Rumble Rex boss fight, a shared audio `GainNode`,
a volume slider, and a calmer 32-step in-game background loop.

Because the game is intentionally outside the normal unit-test harness,
verification used a three-layer executable evidence loop. First, the inline
script was extracted and checked with `node --check`. Second, scratch copies
of the game received temporary assertion scripts that called internal
functions such as `spawnEnemies()`, `damageEnemy(e, x, y, "star")`, and
`updateCombat(1 / 60, map)`. Those scripts rendered `PASS` and `FAIL` logs
inside the page. Third, headless Microsoft Edge captured screenshots of the
assertion output and rendered game state.

The verification loop caught a real boss-test assumption. The simulated
Rumble Rex warps initially failed because `warpCd` only decrements in the
normal `requestAnimationFrame` loop, not in the direct combat helper calls the
scratch script was using. The script had to reset `warpCd` manually between
simulated warps, which exposed a real difference between code inspection and
runtime behavior.

The game PRs were stacked because every feature touched the same HTML file.
Stacking preserved incremental review and helped keep each PR under the
400-line limit. After squash merges landed predecessors on `main`, PR #24
through PR #30 needed sequential base advancement: retarget the PR to `main`,
merge updated `main` into the branch, push the merge commit, and verify
mergeability with `gh pr view --json mergeable`. This changed the merge base
and content comparison without force-pushing, rebasing, rewriting shared
history, or recreating the PRs.

The net result was 10 PRs, each under the 400-line limit, with `pnpm validate`
passing, explicit verification evidence on the game PRs, and the
self-contained game architecture left intact.

## Definition Of Done

Day 68 reached the executable-evidence checkpoint:

- confirmed the post follows Day 67 for July 7, 2026
- assigned the next sequence slot to Day 68 for July 8, 2026
- kept the central lesson on verification evidence rather than release notes
- treated ADR-0005's self-contained game file as intentional architecture
- avoided framing the lack of components as technical debt
- avoided framing the lack of unit coverage as permission to skip verification
- explained the property behind the tests-first rule
- described the site-level back-to-Play navigation work
- described the Play landing page `astro:assets` artwork change
- summarized the game changes without making ten equal release-note entries
- included title-screen movement, hammer, dance, map, z-index, and chiptune behavior
- included timed heart blinking, despawn, and reduced-motion fallback
- included uppercase `ENEMY_DEFS` fire variants
- included source-aware damage routing
- included hammer, clone, star, water-gun, doused, vulnerable, and reignite rules
- included the water-gun bridge plank
- included the Star Thrower crystal
- included the hammer boulder
- included `clearObstacle()` mutating the map in place
- included the Rumble Rex arena, HP, state machine, stun, hammer, star, and peaceful-den behavior
- included the shared `GainNode`, volume slider, and background-loop change
- described the inline script extraction and `node --check`
- described scratch-copy temporary scripts and in-page `PASS`/`FAIL` logs
- described headless Edge screenshot evidence
- avoided claiming screenshots replace tests
- included the `warpCd` verification failure as the concrete evidence story
- explained why direct helper calls did not reproduce the normal animation-loop cooldown
- described the stacked PR strategy for one self-contained HTML file
- explained the squash-merge ancestry problem precisely
- described the sequential PR #24 through PR #30 base-advancement procedure
- avoided saying Git magically removed commits
- noted that no force-push, rebase, history rewrite, or PR recreation was needed
- preserved the final lesson: when the artifact sits outside the normal test harness, build the cheapest credible verification loop around the artifact that actually exists
