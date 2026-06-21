---
title: "Day 50 - June 20, 2026: Paying the Security Cost Once"
description: "A Day 50 reflection on neibaur-labs governance audits, reusable docs templates, node-template CI hardening, and translating agent-security coursework into low-cost repository guardrails."
pubDate: "2026-06-20"
day: 50
dashboardSlug: "none"
dataSources:
  - "neibaur-labs governance audit notes"
  - "neibaur-labs/.github review notes"
  - "neibaur-labs/project-template-node review notes"
  - "neibaur-labs/org-governance review notes"
  - "Vibe Coding Agent Security and Evaluation whitepaper"
  - "Spec-Driven Production Grade Development in the Age of Vibe Coding whitepaper"
  - "project-template-docs scaffold notes"
  - "reviewing-pull-requests skill eval notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - github-governance
  - project-templates
  - security
  - ci
  - specs
  - semgrep
---

Day 50 was a template-hardening day.

Not in the satisfying sense where a user-facing feature appears at the end.
This was the quieter kind of work: governance, security, documentation, CI,
and agent-readiness. It was about taking the lessons from recent Google /
Kaggle agentic AI coursework and asking which of them should become reusable
organization-level defaults instead of one-off notes.

That framing mattered because the temptation with AI-security material is to
either overreact or underreact. The enterprise version of the problem can get
large fast: policy servers, complex agent identity models, centralized
authorization layers, dedicated evaluation infrastructure, and heavyweight
deployment gates.

Some of that is valuable in the right environment. Most of it does not fit my
actual operating model right now.

My setup is smaller and more practical: solo maintainer, GitHub-native,
static/template-first, CI as the trust boundary, human approval for protected
paths, and agents as scoped assistants rather than autonomous operators. The
right move was not to chase every enterprise control. It was to translate the
useful parts into low-cost defaults that future repositories can inherit.

That is the security cost I want to pay once.

## Three-Repo Governance Audit

The day started with a governance audit across the neibaur-labs template and
governance ecosystem:

- `neibaur-labs/.github`
- `neibaur-labs/project-template-node`
- `neibaur-labs/org-governance`

The goal was to compare the committed files against the governance model I
have been building: read, draft, and act separation; human-only protected
paths; consistent CI; dependency handling; security scanning; and reusable
template structure.

The good news was that the committed files were generally clean. The three
repositories showed the expected tiering model, and I did not find a major
"the whole system is pointing the wrong way" violation.

That was useful, but not an excuse to stop looking.

Governance drift is often small and boring. That is what makes it easy to miss.
The audit surfaced low and medium findings rather than dramatic failures, but
those findings matter because templates multiply whatever they contain.

One example was the organization `.github` repository. The docs CI appeared to
run `markdownlint-cli2`, but the README layout did not clearly list
`.markdownlint-cli2.yaml`. If that file was missing or unclear, markdownlint
could fall back to defaults that are too strict for long-form governance prose.
That is not a scary bug. It is a drift bug. The repo says "we lint docs," but
the exact linting contract is not visible enough from the docs surface.

Another finding came from `project-template-node`. The GitHub Actions were
pinned by SHA, which is the right direction for supply-chain hardening, but the
`gitleaks` image was still pinned by a mutable tag instead of a digest. Across
the organization there were also two different gitleaks image sources, which
made the recommendation clearer: standardize on the GHCR image and pin it by
digest.

There was also a stale comment problem. The docs CI action SHAs were verified
as real commits, but a workflow comment still described them as placeholders.
That kind of comment is small, but it creates distrust. A future reviewer
should not have to reverse-engineer whether the workflow is intentionally
pinned or halfway drafted.

The lesson was not that the repositories were broken. The lesson was that
governance gets stronger when the boring inconsistencies are removed before
they become copied defaults.

Templates compound. That is the point of them. So template drift compounds too.

## Reusable Docs Template

The next thread was turning the docs-governance pattern into something
repeatable.

I generated a reusable `project-template-docs` scaffold derived from
`org-governance`. The motivation was simple: `.github` and `org-governance`
had effectively been hand-built as docs-only repositories. That was fine once.
It should not become the standard way every future docs repo starts.

The generated template included the pieces I want a docs-only repository to
inherit by default:

- Docs CI for linting and security
- tuned `.markdownlint-cli2.yaml`
- docs-tier `AGENTS.md` and `CLAUDE.md`
- protected-surface awareness for `.claude/skills/**`
- `CODEOWNERS`
- actions-only Dependabot configuration
- hygiene files
- docs-specific `SETUP.md`
- a drills log

That list is intentionally not glamorous. It is setup work. But setup work is
where a lot of repo safety either appears or vanishes.

The docs-tier agent files are especially important. A docs repository should
not pretend to be a code repository, but it still has protected surfaces:
workflow files, ownership files, instruction files, and skill material. A
docs-only repo can still influence agents, CI, and organization defaults.

That means a docs template needs its own version of the same boundary language:
what is read-only, what is draft-only, what requires human approval, and which
paths are too sensitive for autonomous changes.

All markdown files in the generated scaffold were linted successfully against
`markdownlint-cli2@0.22.0`. That mattered because the template should not begin
life with "fix the template's own docs formatting" as the first chore for every
consumer.

This was governance compounding in the good direction. Build the docs
repository shape once, validate it once, and make future docs repos start with
safer defaults.

## Node Template CI

After the docs scaffold, I asked for a PR-ready `project-template-node` CI
draft.

There was an important dependency-governance clarification before touching the
workflow: if some dependency versions looked newer than expected, that was
intentional. I had recently merged Dependabot PRs. The task was not to roll
versions back to match stale model knowledge.

That is a real agent-safety pattern.

An assistant can easily look at a dependency version, remember an older
ecosystem state, and "fix" the repo by downgrading something that was just
updated intentionally. That kind of change can look tidy while weakening the
actual system. The right behavior is to preserve current dependency state
unless there is verified evidence that a change is needed.

The CI draft focused on a few concrete improvements:

- keep existing dependency versions unchanged
- digest-pin the gitleaks GHCR image using durable `tag@sha256:` syntax
- leave a clearly marked digest placeholder rather than fabricating a digest
  when the registry could not be verified
- add explicit job names for build, lint, security, test, and typecheck

The named checks point matters more than it first appears. Branch protection
depends on stable required-check names. A workflow can be technically correct
and still create governance friction if its check names drift with every
rewrite. Stable names make GitHub rules easier to reason about and harder to
break accidentally.

The digest placeholder was the deeper lesson.

When verification is unavailable, the correct move is not to invent an
authoritative-looking value. It is to leave a safe placeholder with clear
instructions for how to verify and replace it.

That principle applies far beyond container digests. Agents should not
fabricate URLs, recipients, IDs, endpoints, action SHAs, package versions, or
security findings just because a complete-looking answer feels more helpful.

Incomplete but honest beats complete-looking and false.

## Day 4 Security Ideas

The next pass returned to the Day 4 whitepaper, "Vibe Coding Agent Security
and Evaluation," and mapped it against the current governance setup.

I did not try to adopt the whole enterprise model. That would be the wrong
fit. My repositories do not need a pretend enterprise security platform bolted
onto a solo-maintainer workflow. They need small, durable controls that line up
with GitHub, templates, CI, and human review.

Several ideas did translate cleanly.

The first was treating untrusted content as data, not instructions. That needs
to be explicit in `AGENTS.md`, not merely assumed. Diffs, issue text, PR
comments, dependency metadata, generated docs, and copied snippets can all
contain content that looks like instructions. Agents need a clear boundary
between repository rules and untrusted material they are inspecting.

That produced a drafted `agents-instruction-boundary.md`.

The second was replacing grep-style forbidden-pattern checks with real SAST.
Simple string checks are useful, but they are not a security program. For the
node template, Semgrep is a better fit as a lightweight, CI-friendly SAST
layer. It is not heavy infrastructure, and it gives future repositories a real
starting point for application-security scanning.

The third was invisible-payload scanning. Agent-facing repositories should care
about zero-width Unicode and bidi override characters because instruction
files, specs, prompt examples, and diffs are all text surfaces. A malicious or
accidental invisible payload can change how humans or agents interpret the
repository.

That check went through a correction. The initial Unicode-codepoint regex
approach was not reliable enough across runner locales. The better version
matched raw UTF-8 byte sequences under `LC_ALL=C`. That is a useful reminder
that security checks need to be boringly deterministic in CI, not just elegant
in a local shell.

The fourth idea was guarding against agent PRs that modify tests and
implementation together. That does not mean such changes are never valid. It
means the combination deserves attention because it is easier for an agent to
make a wrong implementation look correct when it also controls the tests in
the same pass.

The security conventions draft also expanded the template language around
client-side trust failures, server-side authorization, default-deny behavior,
row-level security expectations, slopsquatting, and hallucinated package
risks.

The artifacts drafted from this pass were:

- `agents-instruction-boundary.md`
- updated `project-template-node-ci.yml`
- `security-conventions.md`

The through line was practical. Do not try to recreate an enterprise agent
security platform in a template. Do capture the durable lessons as repo-local
boundaries and CI checks.

## Day 5 Spec Discipline

The Day 5 whitepaper shifted the focus from pure security to workflow
discipline and spec-driven development.

That surfaced a gap in my current system.

I already have always-on rules through `AGENTS.md`. I have on-demand
procedures through skills. I have code and CI enforcement. But I did not yet
have a standard checked-in place for a human-reviewed, per-feature "what and
why" blueprint before an agent starts generating code.

That is what `specs/` is for.

The drafted Day 5 additions were:

- `specs/SPEC.template.md`
- `specs/README.md`
- `agents-additions-day5.md`
- updated `pull_request_template.md`
- `reviewing-pull-requests/SKILL.md`

A checked-in specs convention gives agents a source-of-truth feature
blueprint. It also gives humans something to review before implementation
momentum takes over.

The spec should answer the questions that are easiest to blur during
agent-assisted work:

- What is in scope?
- What is explicitly out of scope?
- What acceptance criteria define done?
- What data, API, or schema contracts must hold?
- What BDD or Gherkin-style scenarios describe expected behavior?
- What risks or protected paths require human attention?

That is not ceremony for ceremony's sake. It is a way to keep fast generation
tethered to reviewed intent.

The Day 5 pass also clarified dependency and authority rules. Agents must not
downgrade versions based on their training cutoff. They must not fabricate
URLs, recipients, IDs, endpoints, or other missing values. They must not take
autonomous real-world actions without human approval.

Those rules sound obvious until a model produces a confident-looking patch
with an invented endpoint or a "helpful" dependency rollback. Then they become
very practical.

The PR template additions moved in the same direction. PRs should include a
risk and impact summary: blast radius, likely breakage points, rollback plan,
and risk level. That is especially useful when agents are involved because the
human reviewer needs to understand not only what changed, but where the change
could fail.

The pull-request-review skill stayed draft-only. That was intentional. A skill
that reviews code can create a lot of false confidence if it is treated as
authoritative before it has a sufficient golden eval set.

Draft first. Evaluate before trusting. Then decide whether it graduates.

## Pull-Request Review Evals

The final thread followed naturally from that draft-only rule: seed a golden
eval set for the `reviewing-pull-requests` skill.

The seed set included seven labeled cases:

1. Clean pure utility change that should remain LGTM and avoid false positives.
2. Hardcoded secret.
3. SQL injection plus client-side trust issue.
4. XSS through `dangerouslySetInnerHTML`.
5. Governance violation involving dependency downgrade, direct dependency
   addition, and tests plus implementation in the same change.
6. Prompt injection hidden inside the diff.
7. Invisible payload using a real zero-width character.

That set is small, but it is pointed. It tests whether the reviewer can catch
classic security issues, agent-specific governance violations, prompt
injection, invisible text, and the equally important "do not cry wolf" case.

The eval package included diff fixtures, expected findings YAML, a
deterministic runner skeleton, and README documentation.

The placement recommendation was also part of the governance model:

- canonical home: `org-governance`
- sync into `project-template-node` if needed
- do not duplicate into `.github`
- do not put the TS/JS-focused reviewer into `project-template-docs`
- keep docs-specific review skills separate later if needed

That reinforces the larger principle: author once in the governance repo, then
sync or stamp into templates. Do not let every repository develop its own
slightly different reviewer, slightly different cases, and slightly different
definition of risk.

Drift is cheaper to prevent at the source than to repair across a dozen
copies.

## Why The Day Mattered

Day 50 mattered because it turned agent lessons into template defaults.

The work was not about shipping a dashboard or building a new app. It was about
making future agent-assisted work less fragile before there are more
repositories depending on it.

The three-repo audit showed that the core governance model was holding up, but
also that small inconsistencies still deserve attention: missing or unclear
markdownlint config, mutable security-tool image tags, multiple image sources,
and stale comments around pinned actions.

The docs template work converted hand-built documentation repository patterns
into a reusable scaffold.

The node CI draft sharpened the dependency and verification rule: preserve
intentional versions, pin what can be verified, and leave honest placeholders
when verification is unavailable.

The Day 4 and Day 5 whitepaper passes gave names to the next layer of controls:
instruction-source boundaries, real SAST, invisible-payload scanning, agent PR
guardrails, specs before implementation, no fabricated operational values, no
autonomous real-world actions, and explicit risk summaries.

The eval seed set made the PR-review skill accountable before it becomes
trusted.

That is governance compounding. Pay the cost at the template level so the next
repository starts safer by default.

## Outcome

Day 50 continued the neibaur-labs governance and template-hardening arc.

I audited `neibaur-labs/.github`, `neibaur-labs/project-template-node`, and
`neibaur-labs/org-governance` against the read, draft, and act model;
human-only protected paths; CI consistency; dependency handling; security
scanning; and template reuse. The repositories were generally aligned, with
low and medium findings around docs lint visibility, mutable gitleaks image
pinning, image-source standardization, and stale workflow comments.

I generated a reusable `project-template-docs` scaffold from `org-governance`
so future docs-only repositories do not have to be assembled by hand. The
template included docs CI, tuned markdownlint configuration, docs-tier agent
instructions, protected-surface awareness, CODEOWNERS, actions-only Dependabot,
hygiene files, setup documentation, and a drills log. Its markdown passed
`markdownlint-cli2@0.22.0`.

I drafted a PR-ready `project-template-node` CI update focused on preserving
current dependency versions, digest-pinning the gitleaks GHCR image with a
safe placeholder when the digest could not be verified, and stabilizing
required-check names for build, lint, security, test, and typecheck.

I mapped Day 4 agent-security ideas into lightweight template controls:
instruction-source boundaries, Semgrep SAST, invisible-payload scanning, agent
PR test/implementation guardrails, client-side trust warnings, server-side
authorization expectations, default-deny posture, row-level security language,
slopsquatting awareness, hallucinated package risk, and plain-language
summaries before high-impact actions.

I mapped Day 5 spec-driven development ideas into a future `specs/` convention,
PR template additions, dependency and authority rules, and a draft-only
pull-request-review skill.

Finally, I seeded a golden eval package for that PR-review skill with seven
labeled cases covering clean changes, secrets, SQL injection, client-side
trust, XSS, governance violations, prompt injection, and invisible payloads.

## Definition Of Done

Day 50 reached a template-hardening checkpoint:

- audited `neibaur-labs/.github`, `neibaur-labs/project-template-node`, and
  `neibaur-labs/org-governance`
- confirmed the committed files were generally clean and aligned with the
  governance model
- verified consistent read, draft, and act tiering across the three repos
- identified low and medium governance findings rather than major violations
- noted the `.github` docs CI and `.markdownlint-cli2.yaml` visibility issue
- identified mutable-tag gitleaks image pinning in `project-template-node`
- recommended standardizing on the GHCR gitleaks image by digest
- confirmed docs CI action SHAs were real commits despite stale placeholder
  comments
- generated a reusable `project-template-docs` scaffold from `org-governance`
- included docs CI, tuned markdownlint, docs-tier agent instructions,
  CODEOWNERS, Dependabot, hygiene files, setup docs, and a drills log
- linted the docs template markdown with `markdownlint-cli2@0.22.0`
- drafted PR-ready `project-template-node` CI updates
- preserved current dependency versions instead of rolling back recent
  Dependabot updates
- used a safe digest placeholder rather than fabricating an unverified value
- added stable explicit check names for build, lint, security, test, and
  typecheck
- mapped Day 4 agent-security ideas into lightweight template controls
- drafted `agents-instruction-boundary.md`,
  `project-template-node-ci.yml`, and `security-conventions.md`
- corrected the invisible-payload scan from a locale-sensitive regex approach
  to raw UTF-8 byte matching under `LC_ALL=C`
- mapped Day 5 spec-driven development ideas into a `specs/` convention and
  PR-review workflow
- drafted `specs/SPEC.template.md`, `specs/README.md`,
  `agents-additions-day5.md`, an updated `pull_request_template.md`, and
  `reviewing-pull-requests/SKILL.md`
- kept the pull-request-review skill draft-only until it has enough golden
  eval coverage
- seeded seven labeled golden eval cases for the pull-request-review skill
- chose `org-governance` as the canonical home for the eval package
- avoided duplicating TS/JS review skill material into `.github` or
  `project-template-docs`
