---
title: "Day 63 - July 3, 2026: Claims Are Pointers, Not Evidence"
description: "A Day 63 reflection on HaoMiantiao M9 planning, documentation truth, governed agent implementation, independent PR review, and a broken-button symptom that turned out to be missing hydration."
pubDate: "2026-07-03"
day: 63
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao PR-review skill documentation audit notes"
  - "HaoMiantiao M9 champion-and-share spec notes"
  - "HaoMiantiao M9 B1 implementation notes"
  - "HaoMiantiao M9 B1 PR review notes"
  - "HaoMiantiao M9 B1 manual browser investigation notes"
  - "BooBoo Story architecture and prototype notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - haomiantiao
  - specs
  - code-review
  - evals
  - testing
  - nextjs
  - developer-experience
---

Day 63 was the day a broken button became more useful than a working one.

That sounds backwards, but it is the right shape of the day.

The visible HaoMiantiao work was M9 B1: turn the minimal champion
acknowledgement into a fuller champion reveal, then add Play again behavior.

But the strongest story was not "I started M9."

The stronger story was the verification loop around it:

- documentation truth
- spec drafting
- maintainer decisions
- governed agent implementation
- independent PR review
- manual testing
- bounded investigation
- reproduced environmental failure

The day kept asking the same question in different forms.

What is the evidence?

A status board can be stale. A README can be plausible and wrong. A spec can
use a word too loosely. A PR body can report the wrong test count. A browser
can show a healthy-looking static shell while the application JavaScript never
hydrates.

Claims are pointers to verify, not evidence.

That was the useful lesson.

## Documentation Truth Can Drift

The first HaoMiantiao thread was a review of the PR-review skill and its eval
documentation after fixture capture for PRs #63 and #65.

The uncomfortable finding was that the correction had not propagated evenly.

The status board had been corrected, but the skill README and `0.2.0.md`
still contained stale claims. They were not wildly broken. That was part of
the problem. Each document could look individually plausible while disagreeing
with the others.

The drift showed up in small places:

- language still implying `pr-0047` was pending after it had already been
  captured
- promotion copy describing eight cases when case `0009` made the corpus nine
- wording that talked about cases `0005-0008` while omitting `0009`
- open-item text that still treated `pr-0047` fixture capture as outstanding
- no Run F or M8 section despite the M8 reviews and captured `pr-0063` and
  `pr-0065` fixtures

That is not glamorous work.

It is also exactly where governance systems get soft if nobody checks them.

A correction can drift when the same truth is duplicated in too many places.
The status board, README, and eval result file can each sound current enough
to pass a casual read while still disagreeing about what has actually
happened.

The decision was not to turn every observation from M8 into a new eval case
just to grow the corpus.

PR #63 mostly fit the existing faithful-findings and correctly-sized
discrepancy family. PR #65 had a coverage-metric labeling mistake that might
become a new reviewer-accuracy axis, but a single instance was not enough to
justify manufacturing a tenth seed.

Blind replay of existing origin-run seeds still felt more valuable than
adding a case for the sake of a larger number.

That restraint mattered later, because the M9 B1 review surfaced another test
count discrepancy. One instance is a note. A repeated pattern starts to look
like evidence.

## The Spec Needed Decisions, Not Just Detail

The next major thread was M9 planning.

I used a fresh Claude Opus session for spec drafting and required a cold read
of the committed HaoMiantiao surface before drafting.

That cold read was useful because it prevented M9 from starting from memory.
It established what M7 and M8 had actually shipped:

- `/play` already persisted the bracket
- a completed run restored as completed
- completion showed only a minimal Champion acknowledgement
- the M8 detail drawer was reachable from the champion card
- there was no full reveal, share flow, share hash, or play-again reset

That gave M9 a real starting line.

The most important clarification was around M4 serialization.

The M4 serialized format represents a full bracket run. It carries version,
contestants, and picks. The champion can be derived from that state, but it is
not stored as a direct champion field.

That meant a short URL design like this:

```text
#c=shin-ramyun
```

should not reuse the M4 full-run serialization.

The M9 share hash is a separate tiny champion-only encoding. It is not the
full bracket save format with fewer fields.

That distinction matters because project documentation had blurred "M4
serialization" and the later "share hash" in a few places. If that wording
had gone into implementation unchallenged, the agent could have inferred an
architecture the maintainer had not actually chosen.

So the spec had to stop being broad and become specific.

Valid share hashes use the same kebab-case slug grammar as the data
validator. Shared-champion mode must be classified before the normal M7
persistence `load()` path. A visitor arriving through a valid shared hash must
not have their local saved bracket read into the shared view, written, or
cleared. Only after that visitor leaves shared mode should normal
restore-or-fresh behavior resume.

Other decisions were also made explicitly:

- exact share and shared-view copy was maintainer-approved
- celebration remains CSS-only with existing tokens and reduced-motion
  behavior
- no new dependency is needed
- M9 is intentionally split into two agent slices

The split was the important operational decision:

- B1: champion reveal and Play again only
- B2: share, champion hash, shared view, and cumulative M9 conformance

That boundary had to be hard. B1 must not include a share control, hash code,
shared-arrival mode, Web Share, or clipboard behavior.

The spec moved from `draft` to `reviewed` only after those decisions were
resolved.

That felt like the real work of spec-driven development. The value is not
writing a long instruction file. The value is identifying the decisions an
implementation agent must not be allowed to make accidentally.

## B1 Stayed Inside The Rails

Once the M9 spec was reviewed, I generated a bounded B1 handoff.

The implementation constraints were familiar by now:

- one concern
- at most 400 changed lines under the repository rule
- tests first
- no new dependency
- no protected-path changes
- no speculative engine or data APIs
- no B2 share behavior

B1 upgraded the minimal completion state into a champion reveal and added
Play again/reset behavior.

The work landed at 388 changed lines, under the cap.

That number matters because the cap is not decorative. It is a reviewability
constraint. M9 could have been tempting to merge into one larger slice:
champion reveal, celebration, Play again, share, clipboard, hash parsing,
shared arrival, local persistence boundary, and cumulative acceptance.

That would have made the review worse.

B1 stayed small enough that the reviewer could ask the right question: did
this slice improve completion and reset behavior without smuggling in B2?

That is what the boundary was for.

## The Review Re-Derived The Claims

I then ran the PR-review skill with Claude Sonnet.

The useful part was that the review did not simply trust the PR body.

It recalculated the changed-line count from the merge base. It checked the
tests-first commit in isolation. It ran the tests. It reproduced coverage. It
ran validation. It checked the static-export build.

That is the kind of review behavior I want to keep training toward.

The review found one small audit-trail discrepancy. The PR body reported 128
tests, while the reproduced result was 127.

That was not a code blocker.

It was not a reason to distrust the whole PR.

It was a correctly sized discrepancy: cosmetic, but worth noting.

The interesting part is that this echoed the M8 B1 review, where a PR body had
reported 110 tests while the actual result was 108.

That recurrence may become eval evidence later. I am not claiming it became a
new eval case that day. But the signal is getting more interesting:
optimistic PR-body test-count arithmetic may be a recurring reviewer-accuracy
axis.

Again, the pattern was the same.

The PR body was a pointer. The reproduced command output was evidence.

## The Broken Button Was Real

Then came the most important scene of the day.

During my own manual browser verification of the M9 B1 branch, I saw a scary
symptom.

The home page loaded.

"Start bracket" reached `/play`.

The Round of 16 rendered with two noodle choices.

The Pick controls looked like working buttons.

But clicking Pick did not advance the bracket.

At first glance, that looked like a severe M7 behavior regression introduced
by M9 B1. The most obvious prompt would have been:

```text
The Pick button is broken. Fix it.
```

I deliberately did not do that.

Instead, I generated a bounded investigation prompt. The agent had to
determine whether the symptom was a real PR regression, a browser or local
environment issue, a stale build/cache issue, or a misunderstanding of the
control.

The B1 scope boundary remained intact: no B2 share/hash work and no broad
refactor.

That distinction matters a lot with coding agents.

If I tell a capable agent that the click handler is broken, I strongly bias it
toward finding a click-handler fix. It may produce a plausible patch for a
problem that does not exist.

The harder discipline is giving the agent room to prove that my diagnosis is
wrong.

Fable investigated with a real Chromium browser.

Because the repository did not include browser tooling and new dependencies
were forbidden, it drove headless Edge through Chromium's debugging protocol
using the existing Node environment instead of installing a new browser-test
dependency.

Against the actual B1 branch, the first Pick advanced normally. The bracket
saved. Progress updated.

The full 15-pick path also worked:

- the champion reveal appeared
- focus moved to the reveal on the completing pick
- reloading a completed bracket did not steal focus
- Play again cleared the intended bracket storage key while leaving a decoy
  key intact
- the fresh opener rendered
- the first Pick control received focus

That meant my symptom was real, but the first theory was wrong.

The branch itself was not failing the interaction path.

## The Static Shell Looked Alive

The investigation then reproduced my exact broken symptom under a controlled
condition.

Fable served the static export while making `/_next/*` assets return 404.

The result looked deceptively healthy.

The HTML rendered. Styling rendered. Pick buttons appeared.

But the application JavaScript never hydrated, so the buttons had no React
event handlers and did nothing.

That was the key technical moment.

The manual observation was valid.

The initial explanation was wrong.

This was not M9 breaking bracket advancement. It was an environment serving a
convincing static shell without the hydration JavaScript.

No application code change was made because the branch itself was not
defective. The investigation left the working tree clean and kept B1 at the
same 388 changed lines.

That outcome is easy to undervalue because it did not produce a patch.

But it produced something better than a patch for the wrong problem.

It classified the failure.

## The Verification Loop Is Becoming The Product

The repeated pattern across the day was not accidental.

The stale eval documentation was caught by reconciling multiple sources of
truth.

The M9 architecture was corrected by reading the actual M4 serialized shape
instead of trusting loose milestone wording.

The PR-review skill re-derived counts and test evidence instead of trusting a
PR body.

The browser investigation reproduced the symptom under a controlled missing
hydration condition instead of guessing at the click handler.

The common move was verification before action.

That is becoming the product of the workflow.

Earlier in this project, I might have seen an inert button and asked an agent
to patch the app. That would have felt decisive. It also might have produced a
change that made the code worse.

The better prompt was not "fix the broken Pick button."

The better prompt was "classify the failure."

Good agentic engineering increasingly means building ways to distinguish:

- a real code defect
- an inaccurate PR claim
- stale project documentation
- an unverified assumption
- an environmental failure that only looks like an application regression

That distinction is where the work is getting sharper.

The agent is not only a code generator. It is part of a verification loop. But
the loop has to be designed so that the agent can disagree with the premise.

That is the piece I want to keep.

## Boo-Boo Story Stayed Experimental

There was also a smaller Boo-Boo Story thread.

I continued shaping BooBooStory.com, a parent-managed site for my son's
hand-drawn stick-figure comic universe.

The architecture clarified as a mostly Node and TypeScript ecosystem:

- Astro and TypeScript
- static output
- Astro Content Collections with schema validation
- Markdown and YAML content
- Cloudflare Pages
- Vitest for the small amount of logic worth testing

The useful restraint was around four existing interactive prototypes.

Instead of immediately porting all four into Astro components, the decision
was to keep the self-contained vanilla HTML and JavaScript demos as separate
experimental modes under `public/play/`.

The rough modes are:

- map
- walk
- story or choose-your-adventure
- quest

Astro can serve those files untouched while the experiments remain cheap to
compare. The winner can later become a real Astro component or island.

That parallels the HaoMiantiao lesson in a smaller, more playful context.

Preserve the experiment boundary. Do not turn every promising idea into
permanent architecture too early.

## Why The Day Mattered

Day 63 mattered because it showed the verification loop getting more mature.

The scary manual symptom was not imaginary. I really did see a page where the
Pick buttons appeared and did nothing.

But the first explanation was wrong.

That is the kind of moment where an agent workflow can either become more
dangerous or more useful.

If the prompt overstates the diagnosis, the agent may produce a plausible fix
for a false premise. If the prompt asks for classification, the agent can
prove the premise wrong and preserve the code.

The same discipline applied before and after that browser investigation.

Documentation claims had to be reconciled. Serialization wording had to be
checked against the actual M4 shape. The PR body had to be verified against
commands. The browser symptom had to be reproduced under controlled
conditions.

Claims are pointers to verify, not evidence.

That is the sentence I want from the day.

It is not anti-agent.

It is the opposite.

It is the work required to make agents useful in systems where plausible
answers are cheap and correct classification is expensive.

## Outcome

Day 63 moved HaoMiantiao from M8 closeout into M9 B1 implementation and
verification.

The day started with PR-review skill and eval documentation cleanup after
fixture capture for PRs #63 and #65. A cold read found stale or inconsistent
truth across the status board, skill README, and `0.2.0.md`. The status board
had been corrected, but the README and results file still contained stale
language around `pr-0047`, eight versus nine cases, `0005-0008` wording that
omitted `0009`, and missing Run F or M8 coverage for the captured `pr-0063`
and `pr-0065` fixtures.

The M8 observations were considered for a new eval case, but I did not add a
case merely to increase corpus size. PR #63 fit the existing faithful-review
family. PR #65's coverage-metric labeling mistake may become a new axis, but
it was still a single instance. Blind replay of existing seeds remained more
valuable than manufacturing a tenth seed.

The M9 planning loop used a fresh Claude Opus session and required a cold
read of the committed HaoMiantiao surface. That read confirmed that `/play`
already persisted brackets, completed runs restored as completed, the M8
detail drawer was reachable from the champion card, and the app still lacked
full champion reveal, share flow, share hash, and Play again behavior.

The M4 serialization distinction became a key maintainer decision. M4 stores a
full bracket run with version, contestants, and picks. The champion is
derivable but not stored as a direct field. Therefore the M9 share hash is a
separate champion-only encoding and should not reuse the M4 full-run
serialization.

The reviewed M9 spec defined valid share hashes using the same kebab-case slug
grammar as the data validator. It required shared-champion mode to be
classified before the normal M7 persistence `load()` path, and it prohibited a
valid shared arrival from reading, writing, or clearing the visitor's local
saved bracket. It also approved exact copy, kept celebration CSS-only with
existing tokens and reduced-motion behavior, added no dependency, and split
M9 into B1 and B2.

B1 covered champion reveal and Play again only. B2 was reserved for share,
champion hash, shared view, and cumulative M9 conformance. B1 was explicitly
barred from share controls, hash code, shared-arrival mode, Web Share, and
clipboard behavior.

The B1 handoff kept one concern, stayed under the 400 changed-line rule,
required tests first, added no dependency, avoided protected paths, avoided
speculative engine or data APIs, and preserved the B1/B2 boundary. The
implementation upgraded completion into a champion reveal and added Play
again/reset behavior at 388 changed lines.

The PR-review skill then ran with Claude Sonnet. The review recalculated the
changed-line count, checked the tests-first commit in isolation, ran tests,
reproduced coverage, ran validation, and checked the static-export build. It
found one cosmetic audit-trail discrepancy: the PR body reported 128 tests,
while the reproduced result was 127. That echoed the earlier M8 B1 pattern
where the PR body reported 110 tests while the reproduced result was 108.

Manual browser verification then surfaced a worrying symptom. The home page
loaded, Start bracket reached `/play`, the Round of 16 rendered, and Pick
controls appeared, but clicking Pick did not advance the bracket. Instead of
asking an agent to patch the click handler, I sent a bounded investigation
prompt that required classification of the failure as a possible PR
regression, browser or local-environment issue, stale build/cache issue, or
control misunderstanding.

Fable investigated with a real Chromium browser by driving headless Edge
through Chromium's debugging protocol using the existing Node environment.
Against the actual B1 branch, the first Pick advanced normally, saved the
bracket, and updated progress. The full 15-pick path worked, including the
champion reveal, focus movement on completion, completed reload behavior, Play
again clearing the intended storage key while preserving a decoy key, fresh
opener rendering, and first Pick focus.

Fable then reproduced my exact broken symptom by serving the static export
while making `/_next/*` assets return 404. The HTML and styling rendered, and
the Pick buttons appeared, but the app JavaScript never hydrated, so the
buttons had no React event handlers. No application code change was made
because B1 was not defective. The working tree stayed clean and the B1 change
remained at 388 changed lines.

Boo-Boo Story also moved forward as a secondary thread. The architecture
settled around Astro, TypeScript, static output, Astro Content Collections,
Markdown/YAML content, Cloudflare Pages, and Vitest for small logic tests. The
four existing interactive prototypes stayed as self-contained vanilla
HTML/JavaScript modes under `public/play/`: map, walk, story or
choose-your-adventure, and quest. The point was to preserve cheap
experimental comparison before rewriting a winner as an Astro component or
island.

## Definition Of Done

Day 63 reached the M9 B1 verification-loop checkpoint:

- corrected the requested sequence from Day 62 to Day 63 after confirming Day
  62 was already July 2, 2026
- kept the new post aligned to July 3, 2026
- reviewed recent HaoMiantiao post tone and sequence before writing
- audited PR-review skill documentation truth after PR #63 and PR #65 fixture
  capture
- identified stale `pr-0047` language in durable documentation
- identified stale eight-case promotion language after case `0009`
- identified stale `0005-0008` wording that omitted `0009`
- identified open-item text that still treated `pr-0047` capture as pending
- identified missing Run F or M8 documentation for `pr-0063` and `pr-0065`
- treated documentation drift as duplicated-truth governance risk
- chose not to manufacture a new eval case solely to increase corpus size
- treated PR #63 as largely within existing faithful-review eval families
- treated PR #65's coverage-metric issue as a possible but not finalized new
  reviewer-accuracy axis
- started M9 planning from a fresh repo-grounded cold read
- confirmed M7 persistence and completed-run restore behavior
- confirmed M8 detail-drawer reachability from the champion card
- confirmed the absence of full reveal, share flow, share hash, and Play again
  behavior before M9
- clarified that M4 serialization stores full bracket state
- clarified that the champion is derivable from M4 state but not stored as a
  direct champion field
- kept M9 share hash separate from M4 full-run serialization
- selected kebab-case slug grammar for valid share hashes
- required shared-champion mode to classify before normal persistence load
- prohibited valid shared arrivals from reading, writing, or clearing local
  saved bracket state
- kept normal restore-or-fresh behavior for after leaving shared mode
- approved exact share and shared-view copy before implementation
- kept celebration CSS-only with existing tokens and reduced-motion behavior
- added no M9 dependency
- split M9 into B1 and B2
- scoped B1 to champion reveal and Play again only
- reserved share, champion hash, shared view, and cumulative conformance for
  B2
- barred share control, hash code, shared-arrival mode, Web Share, and
  clipboard behavior from B1
- generated a bounded B1 implementation handoff
- preserved one-concern implementation scope
- stayed under the 400 changed-line rule at 388 changed lines
- required tests-first implementation
- avoided protected-path changes
- avoided speculative engine or data APIs
- upgraded the completion state into a champion reveal
- added Play again/reset behavior
- ran an independent PR-review skill pass with Claude Sonnet
- recalculated changed-line count from the merge base
- checked the tests-first commit in isolation
- ran tests, coverage, validation, and static-export build in review
- found the 128 versus 127 test-count discrepancy
- treated the discrepancy as cosmetic rather than a blocker
- noticed the recurrence with the earlier 110 versus 108 M8 B1 discrepancy
- manually observed Pick controls that appeared but did not advance
- avoided prompting the agent with a presumed click-handler bug
- used a bounded investigation prompt to classify the failure first
- preserved the B1/B2 boundary during investigation
- drove a real Chromium browser without adding browser-test dependencies
- reproduced normal first-pick advancement on the actual B1 branch
- reproduced the full 15-pick champion path
- confirmed focus movement on completing pick
- confirmed completed reload did not steal focus
- confirmed Play again cleared only the intended storage key
- confirmed fresh opener rendering and first Pick focus
- reproduced the inert-button symptom with missing `/_next/*` hydration assets
- concluded the manual symptom was real but environmental
- made no application code change for the environmental failure
- left the B1 working tree clean
- clarified Boo-Boo Story as an Astro and TypeScript static-content site
- kept four vanilla HTML/JavaScript interactive prototypes under `public/play/`
- deferred Astro component or island rewrites until a prototype direction wins
- preserved the core lesson: claims are pointers to verify, not evidence
