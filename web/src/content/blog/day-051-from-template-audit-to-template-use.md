---
title: "Day 51 - June 21, 2026: From Template Audit to Template Use"
description: "A Day 51 reflection on finishing the neibaur-labs governance template audit, resolving gitleaks and DESIGN.md conventions, and bringing haomiantiao closer to the current node-template standard."
pubDate: "2026-06-21"
day: 51
dashboardSlug: "none"
dataSources:
  - "neibaur-labs governance audit notes"
  - "neibaur-labs/.github review notes"
  - "neibaur-labs/project-template-node review notes"
  - "neibaur-labs/project-template-docs review notes"
  - "neibaur-labs/org-governance review notes"
  - "haomiantiao template sync notes"
  - "Opus read-only haomiantiao governance audit notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - github-governance
  - project-templates
  - security
  - ci
  - specs
  - haomiantiao
---

Day 51 was a transition day.

Not a dramatic one. More like the moment when the scaffolding has been checked
enough times that the next useful move is to start using it.

For the last several days, I have been working around the same center of
gravity: reusable governance templates, agent boundaries, protected paths,
security defaults, CI conventions, specs, and the difference between useful
automation and accidental authority expansion. June 21 was the day that work
started to feel less like an open-ended audit and more like a harness I can
carry forward.

There were two related tracks.

The first was finishing the current governance and template audit cycle across
the neibaur-labs organization. The second was using those standards on a real
repository by bringing `haomiantiao` closer to the current
`project-template-node` baseline.

That combination mattered. Templates are only trustworthy if they survive
contact with a real project. Real projects are only easier to govern if the
templates do not keep drifting underneath them.

## Finishing The Governance Pass

The governance pass centered on four repositories:

- `neibaur-labs/.github`
- `neibaur-labs/project-template-node`
- `neibaur-labs/project-template-docs`
- `neibaur-labs/org-governance`

The point was not to start another redesign. I was not trying to invent a
larger governance system because the previous one had suddenly become
insufficient. The work was more disciplined than that: review cross-repo drift,
finish the final cleanups, and make sure the standards I want to carry forward
actually agree with each other.

The review touched the familiar surfaces: CI, `AGENTS.md`, `CODEOWNERS`,
`SETUP.md`, skills-path conventions, security guidance, and template
documentation.

Those files are not glamorous, but they are the surfaces agents and humans
actually inherit. If they disagree, every future repo starts with a little
confusion baked in.

One useful correction came from the gitleaks digest question.

Earlier, I had been worried that the digest in the template might have been
fabricated. After verification, that concern turned out to be overstated. The
digest being used corresponded to the intended `gitleaks` `v8.30.1` image.

That was a relief, but it did not mean there was nothing to fix.

The real issue was a convention mismatch. One part of the system still talked
as if the digest were a placeholder until verified. Another part of the system
had already moved toward the better pattern: pay the verification cost once at
the template level, then let consuming repositories inherit a verified digest.

That is the direction I want.

Do not ask every downstream repository to rediscover the same security-tool
pinning decision. Do not leave stale language that makes a verified value look
suspect. Make the template and setup instructions tell the same story.

The Semgrep review had a similar shape. I looked again at the pinning pattern
in the node template and the difference between operating repositories and
template repositories. A live project and a template do not carry exactly the
same responsibilities. A live project optimizes for its own build and threat
model. A template also has to be honest about what it is giving future projects
by default.

That does not mean templates should be stuffed with every possible control. It
means the controls they do include should be documented, intentional, and easy
to update without creating drift across the organization.

## Avoiding Inert Artifacts

The other important governance decision was about `DESIGN.md`.

I considered whether template repositories should ship a live
`docs/DESIGN.md` skeleton by default. On paper, that sounds attractive. Every
project could start with a place for architecture intent, important system
shape, and design rationale.

In practice, an empty `DESIGN.md` in every new repository would probably become
another inert artifact.

That is one of the template risks I am trying to avoid. A file can look like
governance while quietly becoming evidence that no one is maintaining the
governance. Empty architecture files are especially prone to that. They imply
there is standing design documentation, but they do not actually help until a
project has enough design surface to justify one.

The better convention is conditional.

`SETUP.md` can mention `DESIGN.md` as something to create when a project
genuinely needs a standing architecture overview. Feature-level design should
live in `specs/`. Point-in-time decisions should live in ADRs. A broad
`DESIGN.md` should exist when there is real architecture to keep current, not
because the template wanted another tidy-looking file.

That led to a second boundary decision: `DESIGN.md` should not automatically
become an `AGENTS.md` protected trust-boundary file.

That distinction matters.

`AGENTS.md`, `CLAUDE.md`, `.github/**`, and `.claude/skills/**` can directly
shape agent behavior, CI behavior, ownership, or automation. They are
privilege-adjacent surfaces. A `DESIGN.md` is different. It is descriptive
design intent. It can be important. It can become stale. It can mislead if it
is wrong. But it is not the same kind of authority surface.

Agents can help draft or update it when appropriate. Humans should review it
for drift and accuracy. That is a documentation-quality boundary, not an
automatic agent-authority boundary.

That may sound like a small categorization choice, but these choices compound.
If every descriptive file becomes protected by default, the governance model
gets noisy and harder to follow. If true authority surfaces are not protected,
the model gets unsafe. The useful path is to name the difference.

By the end of that pass, the org governance and template refresh felt done for
now.

I may still discover friction through real usage. That is normal. But this
round of auditing, reconciling, and final cleanup reached a stopping point.

## Applying The Harness To haomiantiao

The second track was `haomiantiao`.

That repository had been created from an older generation of my node project
template, so the question was practical: what has the revised template learned
since then, and which of those standards should be backported?

The comparison showed that the template had moved ahead in several areas:

- CI and security hardening
- the agent-governance contract
- PR template structure
- `CODEOWNERS`
- `specs/` scaffolding
- `.claude/skills/` support

That is exactly the kind of drift templates are supposed to reduce. But when a
real repository already exists, the work is not just "copy the new template
over it." A project has local history, local workflow, and local governance
choices. Backporting standards is a merge between the template's current
defaults and the repository's actual operating model.

I treated most protected-path changes as human-authored governance work. That
included `.github/**`, `AGENTS.md`, `CLAUDE.md`, and `.claude/skills/**`.

That boundary was intentional. These files influence automation, agent
behavior, repo ownership, and review procedures. They should not be casually
agent-authored as if they were ordinary implementation files.

The main exception was `specs/`. Specs are important, but the scaffolding
itself is not a protected path in the same way. It is a place for reviewed
feature intent, and it is reasonable for agents to help maintain the template
or examples there when the surrounding governance rules allow it.

The CI hardening backport included the pieces that now feel like part of the
standard harness:

- digest-pinned gitleaks
- Semgrep SAST
- invisible-payload and Trojan-Source scanning
- broader scan scope
- explicit job names
- refreshed action pins

That is the practical security posture I want for this class of repository.
Not enterprise ceremony. Not a fake platform. Just enough durable CI to catch
the kinds of problems agent-assisted development can amplify: secret leakage,
application security issues, invisible text payloads, stale action pins, and
unclear required-check names.

One template feature did not come over unchanged: the batch-discipline check
that fails PRs when tests and implementation change together.

That was a deliberate omission.

In `haomiantiao`, the current workflow is tests-first within a single PR:
failing test commit first, implementation commits after. A blanket check that
fails a PR for touching tests and implementation together would contradict
that workflow. It might be a good default in some template contexts, but here
it would create governance theater instead of governance value.

That is one of the more useful lessons from applying a template to a real repo:
defaults should be strong, but they still need to fit the operating model.

I also updated the PR template direction to include a Spec field and a Risk &
impact section while keeping the tests-first-same-PR workflow consistent. The
specs path gives future non-trivial changes a reviewed intent artifact. The
risk section makes reviewers look at blast radius, likely breakage points, and
rollback instead of only scanning for a green checkmark.

## Skills Need Governance Too

The `.claude/skills/` work made the same point from a different angle.

I added or prepared the `reviewing-pull-requests` skill path as a
human-maintained, draft-only review procedure, with evals documentation so it
is not treated as automatically production-grade.

That draft-only status is important.

A pull-request review skill can create a lot of confidence very quickly. That
does not mean the confidence is earned. Until a review skill has enough evals,
enough known cases, and enough demonstrated behavior, it should be treated as
a procedure under development rather than an authority.

This is the same pattern as the broader governance pass: avoid accidental
authority expansion.

It is easy to make an agent-facing file and then let the existence of the file
stand in for trust. A skill file is not trustworthy because it exists. It is
trustworthy when the procedure is scoped, reviewed, evaluated, and maintained.

That is especially true for review work because the failure modes are subtle.
A bad reviewer does not always break the build. Sometimes it simply misses the
important issue and says everything looks fine.

## The Opus Audit

After the backport work, I had Opus perform a final read-only governance and
CI consistency audit of `haomiantiao`.

That was the right ending for the day because the point was not to declare the
repository perfect. The point was to see whether the new template standards
had landed coherently and whether anything important still looked off before I
called the sync complete.

The audit found a few real cleanup items.

The most concrete one was that the PR review skill file appeared to have been
misnamed as `SKILLmd` instead of `SKILL.md`. That would make the skill
invisible to agents expecting the standard filename.

It also flagged that the skill's `allowed-tools` should be read-only scoped
rather than granting broad Bash access. That is exactly the kind of issue I
want this governance pass to catch. A review procedure should not accidentally
gain a wider tool surface than its job requires.

Other findings were consistency issues rather than total design failures:

- reconcile forbidden-pattern language between `AGENTS.md`, ESLint, CI grep,
  and the PR review skill
- remove leftover decision-point comments around the omitted batch-discipline
  CI step
- decide how to handle `CODEOWNERS` entries for tool folders that may not exist
  yet

Those findings are useful, but they are today's cleanup list, not yesterday's
completed work.

That boundary matters for the blog record. June 21 got `haomiantiao` nearly
caught up to the current template standard and surfaced the remaining
governance cleanup through a final read-only audit. Applying those final fixes
belongs to the next work session.

## Why The Day Mattered

Day 51 mattered because it moved the work from auditing the harness to using
the harness.

The governance/template pass finished the current round of reconciliation
across `.github`, `project-template-node`, `project-template-docs`, and
`org-governance`. The gitleaks digest concern turned into a clearer standard:
verify once at the template level, then make the docs and setup path reflect
that verified state. The `DESIGN.md` decision sharpened the distinction
between useful documentation and protected authority surfaces.

Then `haomiantiao` tested the template work against a real repository. Most of
the updated standards transferred cleanly: CI hardening, SAST, invisible text
scanning, agent governance, specs, PR template structure, and skill support.
One standard did not fit unchanged, and that was useful too. Governance should
not fight a repo's intended tests-first workflow just because the template has
a generic guardrail.

The larger lesson was restraint.

Avoid template drift. Avoid inert artifacts. Avoid giving agents authority just
because a file sits in an agent-facing path. Avoid pretending a template can be
applied without judgment.

This is the part of agent-assisted development that feels slow until it starts
making everything else faster. The harness is only useful if it is boring,
consistent, and honest about where humans still own the decision.

## Outcome

Day 51 closed the current neibaur-labs governance/template audit cycle and
used `haomiantiao` as the first serious application of the refreshed node
template standards.

Across the template repositories, I reviewed drift in CI, agent instructions,
ownership, setup docs, skills-path conventions, security guidance, and
template documentation. I verified that the gitleaks digest concern was not a
fabricated-digest problem, then corrected the framing toward a consistent
"verified once at the template" convention. I also decided not to ship an empty
`docs/DESIGN.md` skeleton by default and not to treat `DESIGN.md` as an
automatic protected trust-boundary file.

In `haomiantiao`, I compared the repository against the newer
`project-template-node` baseline and backported the standards that fit:
stronger CI/security checks, agent-governance files, PR template direction,
`CODEOWNERS`, `specs/` scaffolding, and `.claude/skills/` support. I kept the
tests-first-same-PR workflow intact instead of adopting the template's
batch-discipline failure check unchanged.

Finally, I sent the nearly synced repo through a read-only Opus governance and
CI audit. That audit surfaced the next cleanup list, including a likely
`SKILLmd` versus `SKILL.md` filename issue, overly broad review-skill
`allowed-tools`, forbidden-pattern language drift, leftover CI comments around
the omitted batch-discipline step, and open `CODEOWNERS` questions for tool
folders that may not exist yet.

Those audit fixes are the next work, not something I completed on June 21.

## Definition Of Done

Day 51 reached a governance-transition checkpoint:

- completed the current governance/template audit pass for
  `neibaur-labs/.github`, `project-template-node`, `project-template-docs`, and
  `org-governance`
- reviewed cross-repo drift in CI, `AGENTS.md`, `CODEOWNERS`, `SETUP.md`,
  skills-path conventions, security guidance, and template docs
- verified that the gitleaks `v8.30.1` digest concern was overstated
- reframed the gitleaks issue as a documentation and convention mismatch
  rather than a fabricated-digest problem
- reinforced the "pay once at the template with a verified digest" pattern
- reviewed Semgrep pinning and the difference between operating repos and
  template repos
- decided not to ship an empty `docs/DESIGN.md` skeleton by default
- decided `DESIGN.md` should be conditional documentation, not an automatic
  protected agent trust-boundary file
- treated the org governance/template refresh as done for now
- compared `haomiantiao` against the current `project-template-node` standards
- identified template drift in CI, agent governance, PR template structure,
  ownership, specs, and skill support
- treated `.github/**`, `AGENTS.md`, `CLAUDE.md`, and `.claude/skills/**` as
  human-authored protected governance work
- kept `specs/` as the main safely agent-assisted scaffolding exception
- brought over or prepared CI hardening for digest-pinned gitleaks, Semgrep,
  invisible-payload and Trojan-Source scanning, broader scan scope, explicit
  job names, and refreshed action pins
- intentionally did not adopt the template batch-discipline failure check
  unchanged because it conflicted with `haomiantiao`'s tests-first-same-PR
  workflow
- updated the PR template direction around specs plus risk and impact
- added or prepared `specs/` workflow scaffolding for future non-trivial
  changes
- added or prepared the draft-only `reviewing-pull-requests` skill path with
  evals documentation
- had Opus perform a final read-only haomiantiao governance and CI audit
- captured the Opus audit findings as today's follow-up list rather than
  yesterday's completed work
