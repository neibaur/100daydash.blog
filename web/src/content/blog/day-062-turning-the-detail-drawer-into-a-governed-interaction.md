---
title: "Day 62 - July 2, 2026: Turning the Detail Drawer Into a Governed Interaction"
description: "A Day 62 reflection on HaoMiantiao M8 detail-drawer implementation, source-grounded eval cleanup, spec ownership, B1/B2 scope boundaries, and calibrated PR review."
pubDate: "2026-07-02"
day: 62
dashboardSlug: "none"
dataSources:
  - "HaoMiantiao M7 closeout audit notes"
  - "reviewing-pull-requests eval case 0009 notes"
  - "HaoMiantiao M8 detail-drawer spec"
  - "HaoMiantiao M8 B1 implementation PR notes"
  - "HaoMiantiao M8 B1 PR review notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - haomiantiao
  - specs
  - code-review
  - evals
  - accessibility
  - testing
  - developer-experience
---

Day 62 was the day the detail drawer stopped being "just a drawer."

The visible product change was small enough to describe in one sentence:
HaoMiantiao needed Details buttons that open a native dialog for a selected
noodle.

But the real work was larger than that.

The day moved from M7 cleanup into M8 implementation through a more mature
agent workflow: audit first, spec second, implementation third, review last.
Each step put rails around the next one.

That made the drawer less like a loose UI addition and more like a governed
interaction.

## Starting With The M7 Trail

The day began as a checkpoint after M7 closeout and human-owned correction
work.

This was not a broad repository review. It was a tight closeout audit focused
on whether the M7 story was internally consistent across `PROJECT_STATE`, the
review-skill README, and the `0.2.0` eval results file.

The audit checked whether the M7 PR numbering correction had landed cleanly,
whether the eval documentation still matched the actual cases, whether the
new `0008` case was present, and whether stale "seven cases" language or old
fixture and provenance claims remained.

That would have been useful even if it only found bookkeeping drift.

It found something more important.

A prior B2b review had fabricated a governance citation. It claimed
`CLAUDE.md` required "one short line max" docstrings or comments. Neither
`CLAUDE.md` nor `AGENTS.md` contained that rule.

That changed the issue.

The underlying code observation may have been reasonable. Long or redundant
comments can be a legitimate style concern. But a real observation does not
become repository policy just because a review attaches it to a nonexistent
rule.

That became eval case `0009 fabricated-governance-citation`.

I think that is the right failure mode to preserve. It sits in the same
family as `0001`: a reviewer sees something real in the code, then overstates
the authority behind the finding.

The lesson is blunt but useful.

Accurate observations do not launder invented source authority.

If the source is a repo rule, cite the rule. If the source is code precedent,
say it is precedent. If the source is judgment, own it as judgment.

## Moving From Cleanup To M8

After the audit and eval loop, the work moved into M8 planning.

The spec-drafting session was intentionally seeded like a fresh Claude or
Fable handoff. The agent had to cold-read the repository instead of leaning
on memory from M7.

That mattered because M8 was not starting from a blank product surface.

M7 had deliberately deferred:

- blurb rendering
- style chips
- real image rendering
- buy links
- the detail drawer itself

The M8 planning pass also confirmed that `getNoodleById` already supported
detail-by-id access. That meant M8 did not need a new data package. The data
access path was already there.

The harder part was deciding what the first detail milestone was allowed to
own.

The reviewed spec was named `specs/m8-detail-drawer.md`. It was
agent-assisted in drafting, but maintainer-owned once reviewed and adopted.
That distinction mattered. Governance documents can use agent help, but they
cannot become binding project authority until the maintainer owns them.

M8 also had an empty dependency proposal. There was no PR A. Unlike earlier
app-tier milestones, the detail drawer did not need a dependency-adding
setup PR before implementation.

That was a useful simplification.

## The Drawer Was A Commerce Boundary Too

The M8 spec became more complicated than a simple UI drawer because it was
the first milestone touching real product images and commerce surfaces.

The live noodles dataset already had real names, blurbs, and styles for all
16 entries. But `nameZh`, `flag`, `image.*`, and `buy[]` were still uniformly
empty.

That created an important testing rule.

The populated image, buy-link, and disclosure paths should be tested with
test-local constructed `Noodle` fixtures. They should not be forced into the
production dataset just to make the new UI look complete.

That is data honesty in a practical form.

M8 also clarified the affiliate disclosure boundary with M10. M8 owns
contextual per-drawer disclosure next to per-noodle affiliate links. M10 owns
the global or shop-strip disclosure surface.

The chosen sentence was:

```text
Some purchase links may earn us a commission at no extra cost to you.
```

The buy-link invariant was set uniformly:

```text
rel="nofollow sponsored noopener"
target="_blank"
```

Every rendered `buy[]` link should use that relationship and target,
regardless of the affiliate flag. The affiliate flag controls only whether
the per-drawer disclosure sentence renders.

The rationale was deliberately conservative. Under-attributing a compensated
link is the higher-risk failure mode, and one uniform invariant is easier to
test than a conditional one.

## Choosing Native Dialog Without Pretending It Solves Everything

The M8 spec chose native `<dialog>` as the preferred browser primitive.

That was not treated as a turnkey accessibility solution.

The split was explicit.

App-owned behavior had to be tested in jsdom:

- open and close wiring
- initial focus
- Escape and cancel handling
- focus restore
- scroll lock

Platform-delegated browser behavior had to be manually verified:

- top-layer rendering
- background inertness
- focus containment

That boundary was important because jsdom `29.1.1` does not implement
`showModal()` or `close()`. The spec required a small documented test setup
shim so the app-owned interaction contract could be tested without pretending
jsdom was a real browser.

That is the right kind of compromise.

Use automated tests where they prove the application's behavior. Use manual
browser checks where the platform is the thing being verified.

## Splitting M8 Before It Split Itself

M8 was intentionally split into B1 and B2 before implementation began.

That was a direct lesson from M7.

The point was to avoid a reactive split after the work had already started
to sprawl.

B1 was scoped to the drawer shell and mechanics only:

- Details buttons
- native dialog shell
- focus behavior
- close behavior
- scroll-lock behavior
- tests

B1's drawer body had a hard boundary: noodle-name heading plus close control
only.

B2 was reserved for full content:

- blurb
- style chips
- image
- buy links
- contextual affiliate disclosure

That boundary made the first PR easier to review. It also kept the product
story honest. B1 was not allowed to smuggle in B2 content just because the
empty drawer looked plain.

## Implementing B1

The B1 implementation prompt sent the agent to a fresh branch:
`feat/detail-drawer-shell`.

It required a cold read of the reviewed M8 spec, `AGENTS.md`, `CLAUDE.md`,
the play route, existing M7 pick tests, Vitest setup, `getNoodleById`, and
`next.config.ts`.

The prompt also set the implementation constraints:

- tests-first structure
- no new dependencies
- no B2 content
- no `localStorage` mutation
- preservation of existing M7 pick behavior

Opus completed M8 B1 as PR `#63`.

The reported result was compact and specific.

PR `#63` opened from `feat/detail-drawer-shell`, was labeled `ai-assisted`,
and stayed under the 400-line cap at 397 changed lines. `pnpm validate`
passed locally, and the static export still emitted `out/play/index.html`.

Commit 1 added failing interaction tests in `play-detail.test.tsx` plus the
documented `<dialog>` shim in `vitest.setup.ts`.

Commit 2 implemented `noodle-detail.tsx` using native `<dialog>` through
`showModal()`.

Details buttons were added to matchup cards and the champion card. The
drawer body stayed inside the B1 boundary: noodle-name heading plus close
control only.

The app-owned accessibility contract was tested:

- initial focus
- explicit Escape handler
- native cancel path
- focus restore
- scroll lock

The state boundary held too. `openNoodleId` remained ephemeral UI state, and
opening or closing the drawer did not write to `localStorage`.

The M7 pick tests passed unedited.

One small app-tier linting change was also included. `eslint.config.js` was
adjusted to include `apps/*/vitest.setup.ts` in the app-tier lint files so
the DOM-prototype shim was linted correctly.

That was additive lint coverage, not rule weakening.

The PR body also included a manual real-browser accessibility checklist for
the behavior jsdom cannot prove.

That last piece matters. It kept the automation boundary visible instead of
letting "tests passed" imply more than the tests could know.

## Reviewing The Review Surface

The review loop then ran through the PR-review skill in a fresh Sonnet
session.

This was the kind of review I want more of: faithful-positive, not credulous.

It independently checked the changed-line count. It ran build and validate
instead of trusting the PR self-report. It confirmed the tests-first commits.
It checked the hard B1 boundary. It confirmed that the champion-card valve
was not needed. It read the `eslint.config.js` change closely enough to
understand that it expanded lint coverage for the setup file.

The review also found a benign discrepancy in the PR self-report around test
counting.

It did not inflate that into a blocker.

That calibration matters. A good review should catch small self-report
errors without turning every mismatch into a governance emergency.

The actual merge prerequisites were more practical:

- maintainer verification of the real-browser accessibility checklist
- direct confirmation of green CI on the PR page, because the scoped PAT
  could not read check runs

That is a mature review stance. It distinguishes between evidence the agent
can verify, evidence the platform blocks it from reading, and evidence a
human still needs to check in a real browser.

## Why The Day Mattered

Day 62 was not just "added a drawer."

It showed the transition from M7 cleanup into M8 implementation with a much
clearer governance loop around the code.

The day started by auditing durable project state before opening the next
phase. It turned a fabricated governance citation into eval evidence. It
required the M8 spec to be repo-grounded and maintainer-owned. It split B1
and B2 before the implementation had a chance to blur them. It chose native
browser primitives while documenting what automation could and could not
prove.

Then the PR review caught real details without overreacting to a harmless
self-report mismatch.

That feels like the useful lesson.

More and more of agentic software work is not the code itself.

It is the rails around the code:

- source-grounded audits
- adopted specs
- testability contracts
- manual verification boundaries
- calibrated review

The drawer is useful.

The governed path to the drawer is the thing I want to keep repeating.

## Outcome

Day 62 moved HaoMiantiao from M7 cleanup into M8 B1 implementation.

The M7 closeout audit checked consistency across `PROJECT_STATE`, the
review-skill README, and the `0.2.0` eval results file. It verified the M7 PR
numbering correction, the presence of eval case `0008`, and the removal of
stale "seven cases" and stale fixture or provenance claims.

The audit also identified a fabricated governance citation from a prior B2b
review. The reviewer claimed `CLAUDE.md` required "one short line max"
docstrings or comments, but that rule did not exist in `CLAUDE.md` or
`AGENTS.md`. The issue became eval case `0009
fabricated-governance-citation`, framed as a real observation attached to a
nonexistent cited rule.

The M8 planning loop produced `specs/m8-detail-drawer.md`. The spec was
agent-assisted in drafting and maintainer-owned after review and adoption.
It confirmed that M7 had deferred blurb rendering, style chips, real image
rendering, buy links, and the drawer itself. It also confirmed
`getNoodleById` already supported detail-by-id access, so M8 did not need a
new data package.

M8 had no dependency proposal and no PR A. Native `<dialog>` was chosen as
the preferred browser primitive, with a documented jsdom `showModal()` and
`close()` shim for tests. App-owned behavior had to be tested in jsdom.
Platform-delegated browser behavior had to be manually verified in a real
browser.

The milestone was split into B1 and B2. B1 owned the drawer shell and
mechanics only: Details buttons, native dialog shell, focus and close
behavior, scroll lock, and tests. B1's drawer body was limited to the
noodle-name heading and close control. B2 was reserved for blurb, style
chips, image, buy links, and contextual affiliate disclosure.

The M8 and M10 disclosure boundary was resolved by splitting the surfaces.
M8 owns contextual per-drawer disclosure beside per-noodle affiliate links.
M10 owns the global or shop-strip disclosure surface. The selected disclosure
sentence was "Some purchase links may earn us a commission at no extra cost
to you." All rendered `buy[]` links use
`rel="nofollow sponsored noopener"` and `target="_blank"`. The affiliate flag
controls only whether the per-drawer disclosure sentence renders.

Opus implemented B1 as PR `#63` from `feat/detail-drawer-shell`. The PR was
labeled `ai-assisted`, reported 397 changed lines, passed `pnpm validate`
locally, and preserved the static export at `out/play/index.html`.

Commit 1 added failing interaction tests in `play-detail.test.tsx` and the
documented `<dialog>` shim in `vitest.setup.ts`. Commit 2 implemented
`noodle-detail.tsx` with native `<dialog>` and `showModal()`. Details
buttons were added to matchup cards and the champion card. The drawer body
remained inside the B1 boundary.

The tests covered initial focus, explicit Escape handling, native cancel
handling, focus restore, scroll lock, and preservation of M7 pick behavior.
`openNoodleId` remained ephemeral state, and opening or closing the drawer
did not write to `localStorage`.

The app-tier lint config was expanded so `apps/*/vitest.setup.ts` would be
linted. The PR body included a manual real-browser accessibility checklist
for top-layer rendering, background inertness, and focus containment.

The PR-review skill then ran in a fresh Sonnet session. The review
independently checked changed-line count, ran build and validate, confirmed
the tests-first commits, checked the B1 boundary, confirmed the champion-card
valve was not needed, and read the lint config change. It found a benign
self-report and test-count discrepancy without treating it as a blocker.

The remaining merge prerequisites were maintainer verification of the
real-browser accessibility checklist and direct confirmation of green CI on
the PR page, because the scoped PAT could not read check runs.

## Definition Of Done

Day 62 reached the M8 B1 implementation and review checkpoint:

- completed a tight M7 closeout audit instead of a broad repo review
- checked `PROJECT_STATE`, the review-skill README, and the `0.2.0` results
  file
- verified the M7 PR numbering correction
- verified eval case `0008`
- removed or checked for stale "seven cases" language
- removed or checked for stale fixture and provenance claims
- identified a fabricated `CLAUDE.md` governance citation
- confirmed the cited one-line docstring rule did not exist in `CLAUDE.md`
  or `AGENTS.md`
- captured the issue as `0009 fabricated-governance-citation`
- framed the eval case as a real observation attached to invented authority
- moved from M7 cleanup into M8 planning
- required a fresh repo cold-read before spec conclusions
- named the spec `specs/m8-detail-drawer.md`
- treated the spec as agent-assisted but maintainer-owned
- confirmed M7 had deferred blurbs, style chips, real images, buy links, and
  the drawer
- confirmed `getNoodleById` already supported detail-by-id access
- avoided a new M8 data package
- kept M8 dependency proposal empty
- skipped PR A because no dependency addition was needed
- chose native `<dialog>` as the preferred primitive
- documented that native `<dialog>` is not a complete accessibility solution
- required a jsdom shim for `showModal()` and `close()`
- required jsdom tests for app-owned open, close, focus, cancel, restore, and
  scroll-lock behavior
- reserved browser manual verification for top-layer rendering, background
  inertness, and focus containment
- split M8 into B1 and B2 before implementation
- scoped B1 to shell and mechanics only
- limited the B1 drawer body to noodle-name heading plus close control
- reserved B2 for blurb, style chips, image, buy links, and contextual
  disclosure
- resolved the M8 and M10 disclosure boundary
- assigned contextual per-drawer disclosure to M8
- assigned global or shop-strip disclosure to M10
- selected the disclosure sentence for per-drawer affiliate links
- set the uniform buy-link invariant to `rel="nofollow sponsored noopener"`
  and `target="_blank"`
- kept the affiliate flag responsible only for disclosure rendering
- prompted B1 implementation on `feat/detail-drawer-shell`
- required tests-first implementation
- added no new dependencies
- avoided B2 content
- avoided `localStorage` mutation
- preserved M7 pick behavior
- opened PR `#63`
- labeled the PR `ai-assisted`
- stayed under the 400-line cap at 397 changed lines
- passed `pnpm validate` locally in the implementation report
- preserved static export output at `out/play/index.html`
- added failing detail interaction tests before implementation
- added the documented `<dialog>` shim in Vitest setup
- implemented `noodle-detail.tsx` with native `<dialog>` and `showModal()`
- added Details buttons to matchup cards and the champion card
- tested initial focus, Escape, cancel, focus restore, and scroll lock
- kept `openNoodleId` ephemeral
- kept M7 pick tests passing unedited
- expanded lint coverage for `apps/*/vitest.setup.ts`
- included a manual real-browser accessibility checklist in the PR body
- ran a fresh PR-review skill session
- independently checked changed-line count, build, validate, commits, scope,
  and lint config
- found a benign self-report discrepancy without overreacting
- left maintainer browser verification and PR-page CI confirmation as merge
  prerequisites
- preserved the core lesson: governed agent work is the rails around the code
