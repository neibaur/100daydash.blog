---
title: "Day 84 - July 24, 2026: Testing Before Implementation"
description: "A Day 84 reflection on testing Boo-Boo Story before planning its next fixes, choosing AI tools by both capability and cost, and carrying repository practices into professional work."
pubDate: "2026-07-24"
day: 84
dashboardSlug: "none"
dataSources:
  - "Personal Boo-Boo Story title-screen testing and implementation-planning notes"
  - "Personal professional repository-governance notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - game-development
  - testing
  - implementation-planning
  - repository-governance
  - security
---

Day 84 did not produce another Boo-Boo Story pull request.

It produced the prompt for the next ones.

After the previous title-screen changes reached `main`, I returned to the
Quest Kai game and tested the current behavior manually. I focused on the
remaining edges rather than immediately asking an AI coding agent to modify
the repository.

That pass uncovered several concrete defects. I documented what I could see,
where it happened, and how the behavior differed between characters or between
the title screen and the game. Then I sent those observations to Claude Opus
and asked it to turn them into a more deliberate implementation plan.

Claude proposed likely causes, an implementation strategy, a four-PR sequence,
and testing expectations. It also identified questions that still required
repository investigation.

That is where the work stopped.

The defects had been observed, but they had not been fixed. The strategy had
been proposed, but it had not been confirmed against the code. No new
Boo-Boo Story tests were added, no implementation pull requests were opened,
and the behavior was not re-tested.

July 24 was primarily a testing and planning day. The useful artifact was a
more precise description of the work that should happen next.

## Testing The Remaining Edges

The title screen currently offers two default characters. The first new
problem appeared when I selected the second character and activated a weapon.

The weapon rendered on the opposite side from the direction the character was
facing. The first character did not show the same problem.

That comparison made the report more useful than simply saying that a weapon
looked wrong. Because the symptom followed the character rather than one
particular weapon, it suggested a problem involving facing state, sprite
flipping, or the weapon anchor.

It did not prove which explanation was correct. That still required inspecting
the implementation. But the contrast narrowed the investigation.

The first character exposed a different issue. Near the edge of the
title-screen play area, activating a weapon could briefly create a horizontal
scrollbar.

The expected rule is straightforward: a weapon effect should stay contained
inside the title-screen playground. It should never resize or shift the
surrounding page.

One diagnostic detail remained unresolved. I had not yet established whether
the scrollbar belonged to the play box or to the overall document. Claude's
plan preserved that uncertainty and instructed the future implementation pass
to identify the actual overflow owner before changing CSS.

That was an important restraint. Adding `overflow: hidden` to the first
plausible container might suppress the symptom while clipping the wrong
content or leaving the real geometry problem untouched.

## The Preview Had Drifted From The Game

The larger finding was that the title screen's weapon previews no longer
matched the artwork and behavior used during gameplay.

Fire still appeared as a generic fire emoji on the title screen even though
the game had moved to artwork supplied by Kai. The star appeared beside the
character instead of traveling toward the edge of the play area. Water did the
same.

Those could have been written as three separate bugs. Claude instead proposed
that they were likely one architectural problem: the title screen appeared to
contain a simplified copy of weapon behavior that had drifted away from the
game's real implementation.

Claude described the fire-art mismatch and the star-and-water behavior
mismatch as the same bug wearing two hats.

Its proposed direction was to remove that duplicate behavior inside Quest Kai
and allow the title screen to call the existing in-game weapon behavior,
constrained to the smaller preview box.

That was a proposal, not a repository-verified conclusion. The implementation
agent would still need to locate the real weapon code, understand its
dependencies, and prove that reuse could preserve the separation between
title-screen previews and earned gameplay inventory.

Still, the diagnosis connected the visible symptoms in a useful way. If the
title screen owns a second, simplified weapon system, correcting one emoji or
adding one local animation would only create another opportunity for the two
versions to diverge.

## A Reasonable Decision Can Develop A Cost

Claude's response also challenged an earlier design choice without pretending
that the original choice had been foolish.

An earlier prompt had explicitly discouraged introducing a weapon registry and
had encouraged a hardcoded title-screen lineup. At the time, that simpler
decision was defensible. There was not yet evidence that the duplication was
causing harmful drift, and a generalized system would have added complexity
for a hypothetical need.

The new defects supplied different evidence.

The answer was still not to build a plugin framework, a shared game engine, or
a speculative abstraction for every future weapon and game. Claude proposed
something smaller: remove the duplicate logic that exists today within Quest
Kai and reuse the behavior the game already owns.

That distinction matters.

Deduplication responds to a cost that can be observed. Premature abstraction
tries to solve a family of future problems that may never arrive. Both can
produce shared code, but they begin from different evidence.

A decision can be reasonable when it is made and still accumulate a cost that
becomes visible later. Good engineering does not require defending the old
choice forever or condemning it in hindsight. It requires noticing when the
conditions have changed.

The title-screen drift was that evidence.

## Turning Findings Into A Sequence

Claude separated the proposed work into four pull requests:

1. Correct the second character's weapon-facing or anchor behavior.
2. Contain weapon effects so activation cannot create a scrollbar.
3. Unify title-screen and in-game weapon behavior.
4. Improve title-screen navigation and center the Design Studio button.

These pull requests had not been created. The list was a sequencing plan for a
future implementation pass.

The order contained useful reasoning. Claude placed the overflow repair before
weapon unification because real traveling projectiles could make the existing
containment problem more visible. Reusing gameplay behavior before knowing
which box owned overflow could turn a temporary scrollbar into a more frequent
one.

The unification work also remained dependent on repository investigation and
behavior decisions.

The future agent would need to find where the in-game weapon behavior actually
lives. It would need to decide whether a projectile should disappear at the
title-screen boundary or show an impact. It would also need to determine
whether gameplay projectile speed should be scaled for the much smaller
preview area.

That last question was especially practical. A speed that reads clearly
across a full game level might cross the title-screen box so quickly that the
projectile looks like a flicker.

Reusing behavior does not necessarily mean blindly reusing every dimension,
distance, or timing value. The shared part should preserve the weapon's
identity and rules while the preview context still supplies a meaningful
boundary.

The fourth proposed PR covered two smaller interface findings.

When the world map is opened from the title screen, returning to the main
title interface is not intuitive. The player currently has to press the Map
button again. Claude proposed a visible return arrow that would appear only
when the map was opened from the title screen, leaving active-gameplay map
behavior unchanged.

The Design Studio button also remained aligned toward the right above the main
interactive area. Because nothing competes with it in that space, the preferred
layout was to center it horizontally above the title-screen play box.

Again, these were intended outcomes, not completed changes.

## The Prompt Defined The Next Checkpoint

The implementation prompt called for focused pull requests, tests-first
commits where appropriate, validation after each concern, root-cause reporting,
and re-testing of the final browser behavior.

Writing those expectations down did not satisfy them.

That boundary is easy to blur in AI-assisted work because a detailed plan can
sound like a completion report. A diagnosis can be written confidently. A PR
sequence can have exact scopes. Test expectations can name the behavior they
would protect.

None of that changes the repository.

The plan reduced ambiguity for the next implementation pass. It turned a loose
set of visual complaints into hypotheses, dependencies, ordering constraints,
and explicit unknowns. That is real progress because it can reduce the amount
of exploration performed while code is already being changed.

It is not the same kind of progress as a verified fix.

The behavior still needed to be implemented and tested. The prompt was the
handoff, not the result.

## Capability Was Only One Tool Constraint

Tool economics shaped the day as well.

During the previous day's work, the available Fable usage consumed
approximately $40 of promotional credit very quickly. No Fable credits were
available for this session, so I used Claude Opus to analyze the observations
and structure the next implementation prompt.

Claude was sufficient for that job. The task required synthesis, sequencing,
and careful language about uncertainty. It did not yet require an agent to
execute code, run tests, or inspect a repository.

I plan to use the next batch of promotional Fable credits when they become
available in August. Fable may still be useful, particularly when a task
benefits from its coding workflow. Based on the current consumption rate,
however, I do not expect to purchase it for ongoing personal side-project use.

That is a practical constraint rather than an attack on the product.

The right tool depends on more than capability. Cost matters. The value of the
project matters. The shape of the task matters. Planning and code execution
do not always need the same system.

A highly capable tool can still be difficult to justify if a personal project
consumes its available credit faster than the work can support. A reasoning
tool can be enough when the immediate deliverable is a better implementation
plan.

July 24 made that division unusually clear.

## Side-Project Practice Became Professional Instinct

The second part of the day involved helping establish a new repository for a
professional project.

I am intentionally keeping the context general. The employer, project,
repository, product, internal architecture, and business details are not part
of this story.

What I can share is that it was rewarding to reuse practices I had been
learning and repeating through recent personal projects: branch protection,
linting, Git hooks with Husky, secret scanning, automated quality gates, and
safer repository defaults.

Earlier in my learning, each of those topics required deliberate research.
They felt like separate systems to remember after the main code existed. With
repetition, they were beginning to feel more like a coherent starting point.

That changed when the questions appeared.

Instead of treating governance and validation as cleanup for later, I could
help raise them while the repository was still new. What should be protected
before normal development begins? Which checks should run automatically?
Which mistakes can a local hook catch quickly? Which defaults make the safe
path the ordinary path?

I am not claiming a particular provider, vendor, coverage threshold, approval
policy, or final configuration. The meaningful outcome was the transfer of
practice.

Side projects had provided a place to research these ideas, apply them, make
mistakes, and repeat the setup. That repetition made the professional
conversation more natural.

The tools had not changed into instincts on their own. The sequence had:
protect important branches, catch basic problems early, scan for secrets, and
make quality checks visible before the repository accumulates years of
exceptions.

Good defaults are easiest to establish near the beginning. Later, every new
gate has to negotiate with existing habits, legacy failures, and workflows
that already depend on the absence of the rule.

Starting early does not guarantee perfect governance. It makes the intended
baseline explicit while change is still inexpensive.

## Investigation Is Engineering Work

The two parts of Day 84 looked different.

One involved a game title screen, character direction, projectiles, overflow,
navigation, and duplicated weapon behavior. The other involved the early
defaults around a professional repository.

They were connected by work that happens before implementation accelerates.

Testing the title screen created evidence before another coding pass. Turning
the findings into a sequence exposed dependencies before they became tangled
inside a large pull request. Establishing repository protections early made
expectations visible before contributors had to retrofit them around existing
work.

In both cases, preparation reduced the chance that speed would become rework.

A precise bug report can make a future agent more effective because it defines
the observed behavior without pretending to know the cause. A focused plan can
separate what is known from what still requires investigation. A repository
baseline can make recurring quality work automatic rather than dependent on
memory.

None of those artifacts is the finished product.

They are part of creating conditions where the finished product can be built
with less ambiguity and fewer avoidable mistakes.

Day 84 did not end with the title-screen defects repaired. It ended with a
clearer account of what was wrong, why several symptoms might share one cause,
which work should come first, and what the next implementation pass still had
to discover.

It also showed that recent learning was becoming portable. Practices repeated
in personal repositories were available when a professional project needed
them.

Testing and planning were not substitutes for implementation.

They were the work required before implementing responsibly.

## Outcome

Day 84 completed the July 24 investigation and planning checkpoint.

I manually tested the current Quest Kai title screen and documented problems
with the second character's weapon direction, temporary horizontal overflow,
weapon previews that had drifted from gameplay, unclear return navigation from
the title-screen map, and the alignment of the Design Studio button.

Claude Opus grouped those observations into a proposed four-PR sequence. Its
central hypothesis was that the outdated fire artwork and the stationary star
and water previews were likely consequences of duplicate title-screen weapon
logic. It recommended repository investigation followed by focused reuse of
Quest Kai's existing gameplay behavior, not a speculative registry or shared
game framework.

The plan intentionally placed overflow containment before traveling-projectile
reuse and preserved open questions about code location, boundary impact
behavior, and projectile speed.

No Boo-Boo Story fixes, tests, or pull requests were completed for these
findings on July 24. Implementation and re-testing remained the next step.

Claude was used because the previous session had consumed approximately $40 of
promotional Fable credit and no Fable credits were available that day. The
choice reflected the planning nature of the task and the economics of a
personal project.

Separately, I reused recent learning about branch protection, linting, Husky
Git hooks, secret scanning, automated quality gates, and safer defaults while
helping with a new professional repository. The details remain confidential;
the shareable lesson was that repeated side-project practice had begun to
transfer into professional instinct.

## Definition Of Done

Day 84 reached the testing, planning, and repository-practice checkpoint:

- followed Day 83 with the July 24, 2026 entry
- described manual title-screen testing without claiming implementation
- recorded the second character's weapon-direction symptom
- recorded the temporary scrollbar without assuming which container owned it
- distinguished Kai's current fire artwork from the title-screen emoji
- recorded the star and water preview drift from gameplay behavior
- framed duplicate title-screen weapon logic as Claude's unverified hypothesis
- distinguished evidence-based deduplication from speculative abstraction
- acknowledged that the earlier hardcoded choice was defensible at the time
- summarized the proposed four-PR sequence without claiming the PRs existed
- placed overflow containment before traveling-projectile reuse
- preserved open questions about code location, boundary behavior, and speed
- described the proposed title-screen-only map return control
- described the preferred centered Design Studio alignment
- treated the implementation prompt as a handoff rather than a completed fix
- claimed no new Boo-Boo Story code, tests, validation, or re-testing
- recorded approximately $40 of consumed promotional Fable credit
- made no claim that Fable was purchased with personal funds
- treated capability, cost, project value, and task shape as tool constraints
- kept the professional repository, employer, product, and architecture private
- limited the professional practices to branch protection, linting, Husky Git
  hooks, secret scanning, automated quality gates, and safer defaults
- made no unsupported claim about vendors, providers, policies, or coverage
- connected repeated side-project learning to professional practice
