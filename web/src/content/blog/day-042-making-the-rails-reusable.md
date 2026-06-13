---
title: "Day 42 - June 12, 2026: Making the Rails Reusable"
description: "Turning Terminal Run's Phase 0 security and governance lessons into a reusable project template, organization rulesets, and a clearer trust model."
pubDate: "2026-06-12"
day: 42
dashboardSlug: "none"
dataSources:
  - "Terminal Run repository"
  - "Project template repository"
  - "GitHub organization rulesets"
  - "GitHub Actions"
  - "Gitleaks"
  - "Dependabot"
  - "Claude"
  - "Codex"
status: "published"
tags:
  - terminal-run
  - project-template
  - repository-governance
  - ai-governance
  - security
  - github-actions
  - developer-experience
  - phase-0
---

Day 42 was the day the rails became reusable.

No Terminal Run gameplay was built. Session 1 still has not begun, and the
walking skeleton remains waiting for its first simulated command.

That was deliberate.

The previous day proved that Terminal Run could be started inside a governed
repository. Today asked the more valuable long-term question:

```text
How much of that hard-won Phase 0 setup can become the default for every
future project?
```

The answer was not a single configuration file or a perfect template. It was
a more mature system made from organization-level rules, a reusable project
scaffold, explicit setup sequencing, honest audit findings, and a clearer
model of what actually protects a repository when AI agents are involved.

The work moved from making one repository secure enough to begin toward
making future repositories easier to begin securely.

## Closing The Final Gitleaks Question

The day began by finishing the open Gitleaks follow-up from Terminal Run's
Phase 0.

The existing local pre-commit hook had already been corrected to scan the
staged diff through Gitleaks `stdin` mode. One important question remained:
was the custom `.gitleaks.toml` rule for standalone AWS access-key IDs
actually loading, or did the hook merely appear to use it?

The hook was tightened to fail closed. It uses `set -e`, resolves the
repository root through `git rev-parse --show-toplevel`, and passes the
configuration path explicitly when invoking Gitleaks.

The custom rule was then tested with a planted fake key and verbose scanner
output.

The important evidence was not that the command exited with an error. It was
the observed rule identifier:

```text
RuleID: aws-access-key-id-standalone
```

That result proved three separate things:

- the custom configuration loaded
- the standalone-key rule matched the intended input
- the pre-commit hook could block the planted secret before commit

The distinction matters because security controls are easy to trust based on
plausible configuration alone. Phase 0 had already demonstrated that a hook
can run, print reassuring output, and still fail its actual purpose.

This time, the conclusion was supported by direct rule-level evidence.

## Separating Organization Defaults From Project Scaffolding

With the final Terminal Run evidence wrapped, the focus shifted toward reuse.

The first architectural decision was to create two repositories with
different responsibilities:

- `.github` for minimal organization-wide community-health defaults
- `project-template` for the reusable governed-project scaffold

That separation prevents the organization community-health repository from
becoming a general-purpose configuration warehouse.

The `.github` repository should stay small and generic. It can provide
fallback files such as an organization-level `SECURITY.md`, pull request
templates, and perhaps an organization profile README.

The `project-template` repository serves a different purpose. It is where new
projects can inherit the prevention layer, development baseline, governance
documents, setup guidance, and Phase 0 verification structure needed to begin
work consistently.

Keeping those responsibilities distinct made the reusable model easier to
reason about:

```text
Organization defaults provide shared fallback behavior.
The project template provides a concrete starting repository.
Organization rulesets provide inherited enforcement.
Each new project still proves that the controls work.
```

The template can reduce repetition. It cannot replace project-specific
verification.

## Discovering The Bootstrap Problem In Strict Rulesets

Organization rulesets immediately exposed a practical initialization problem.

The organization expected five required checks:

- `build`
- `lint`
- `security`
- `test`
- `typecheck`

Applying that strict requirement to every repository can block the first
commit of a brand-new empty repository. GitHub's attempted README
initialization could not satisfy checks from a CI workflow that did not exist
yet.

The ruleset was doing exactly what it had been configured to do. The problem
was the setup sequence.

A repository must exist before it can contain CI. CI must run before it can
produce status checks. Required-check enforcement must therefore account for
the bootstrap window between those states.

That led to a clearer setup doctrine for future repositories. Ruleset
targeting, repository properties, or a controlled setup window must allow the
initial scaffold to land before strict required checks become enforceable.

The lesson was not to weaken the organization rules permanently. It was to
design initialization as an explicit governed phase rather than assuming an
empty repository can satisfy mature-project controls immediately.

## Assembling The Reusable Project Template

The project template gathered the prevention and development baseline that
had previously been assembled directly inside Terminal Run.

The scaffold included:

- `.husky/pre-commit` and `.husky/commit-msg`
- `commitlint.config.js`
- `.gitleaks.toml`
- `.npmrc` with `ignore-scripts=true` and `engine-strict=true`
- `.gitattributes`, `.editorconfig`, `.nvmrc`, and `.gitignore`
- Prettier, ESLint, TypeScript, Vitest, and coverage configuration
- a minimal `packages/example` package with a passing test
- `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and `SECURITY.md`
- ADR templates and seed governance ADR drafts
- a blank Phase 0 drill template
- a scope-exception log
- a template plan
- a setup checklist

This was not intended to make every future repository identical.

The template establishes the parts that should be boring and dependable:
formatting, validation, security hooks, contribution expectations, agent
boundaries, setup order, and the first evidence that the repository can pass
its own checks.

Product architecture, runtime dependencies, domain rules, and project scope
still belong to the individual repository.

The template's value is that each new project should no longer need to
rediscover the same Phase 0 questions from scratch.

## Letting The Audit Say Not Clean

A Sonnet audit reviewed the scaffold that Codex had helped assemble.

The audit returned:

```text
NOT CLEAN
```

That verdict was useful precisely because it did not turn the existence of a
template into evidence that the template was trustworthy.

The most important finding concerned protected paths. Files under
`.github/**` had landed in an agent-assisted pull request. The maintainer had
manually reviewed and pasted the protected content, but the pull request still
combined human-owned and agent-assisted changes.

Squash merging then erased the intra-pull-request provenance. After the
merge, the final commit could no longer communicate which lines were
human-authored, manually pasted, or agent-assisted.

That produced a durable governance rule:

```text
When a repository contract requires human ownership of a protected path,
that path should land in a separate, fully human pull request.
```

Human review inside a mixed pull request is valuable, but it is not the same
as preserving human-only provenance.

The same principle applies beyond `.github/**`. Files such as `AGENTS.md`,
`CLAUDE.md`, and governance documents may need separate human-owned changes
when the repository contract assigns them special authority.

The audit also deserved a durable record rather than a quiet cleanup. A
written audit document and explicit dispositions for every finding were
planned so the repository can show what was found, what was accepted, what
was corrected, and what remains deferred.

An earlier scaffold pull request also received an `ai-assisted` label
retroactively. The label does not solve provenance by itself, but it makes the
development history more honest.

## Recognizing The Identity Agents Actually Use

The audit surfaced a second governance lesson that is easy to miss during
local development.

Local agent sessions use the maintainer's local Git credentials.

If the maintainer has administrator or ruleset-bypass rights, the local agent
effectively inherits those capabilities when it performs Git operations.
Organization push rulesets are therefore not a complete protection layer
against a local agent operating through an administrator's identity.

The ruleset may distinguish between organization roles and scoped external
identities. It cannot distinguish the maintainer typing a command from a
local agent invoking Git through the same credential context.

The updated doctrine became:

- use scoped agent identities by default
- give agent identities only the permissions needed for the task
- treat local-as-admin sessions as contract-only
- reserve local-as-admin agent work for lower-risk changes with extra review

This does not make local agents unusable.

It means the security model must describe the identity they actually possess,
not the identity the interface makes them feel like they possess.

## Documenting The Four Secret-Protection Layers

The day's security work converged into a four-layer secret-protection model.

### 1. Absence

Secrets should never exist in the repository or worktree.

This is the strongest layer because a tool cannot read, stage, commit, log, or
upload a secret that is not present.

### 2. Identity And Sandbox

Agents should run under scoped identities and least-privilege credentials.
Filesystem and process access should be limited where practical.

This reduces the damage possible when a task, prompt, or tool behaves
incorrectly.

### 3. Contract

`AGENTS.md` defines repository-wide rules that apply across tools such as
Claude, Codex, and future agents.

The contract makes expected behavior explicit, reviewable, and portable
between harnesses.

### 4. Harness Rules

Tool-specific controls such as `.claude/settings.json` and ignore-like
mechanisms can deny or discourage access to secret-file patterns.

These controls are useful, but they are not primary security boundaries.
Anything with shell access can still read files the operating system permits
unless stronger sandboxing prevents it.

That ordering corrected an intuitive but weak assumption.

Ignore files and harness deny rules can reduce accidental exposure. They do
not replace keeping secrets out of the repository, using scoped identities,
or limiting operating-system access.

The project template gained `.claude/settings.json` with harness-level deny
rules for secret-file patterns, and the same file was identified for
backporting to Terminal Run. The documentation explicitly treats that file as
layer four, not as a guarantee that secrets are inaccessible.

## Turning Audit Findings Into Concrete Remediation

The audit produced several smaller but meaningful corrections.

The planned or completed dispositions included:

- writing `docs/audits/2026-06-12-template-assembly.md`
- recording a disposition for every audit finding
- adding the `ai-assisted` label to the earlier scaffold pull request
- correcting a stale ADR reference in the scope-exception log
- adding an ESLint-family Dependabot group
- adding `.claude/settings.json` with harness-level deny rules
- documenting the limits of harness-level secret protection
- backporting Dependabot and Claude settings to Terminal Run

The Dependabot grouping is a modest example of why the template matters.

`eslint`, `@eslint/js`, and `typescript-eslint` move as a family. Grouping
their updates reduces fragmented dependency pull requests and makes
compatibility review easier. That is not a glamorous governance feature, but
it is exactly the kind of repeated maintenance friction a useful template
should remove.

The remediation work also preserved the value of the `NOT CLEAN` audit.

The goal was not to make the verdict disappear. The goal was to turn each
finding into a decision with visible evidence.

## Solving Organization-Level Required Checks

The longest debugging thread involved organization-level required checks.

The organization ruleset required:

- `build`
- `lint`
- `security`
- `test`
- `typecheck`

The repository's CI jobs ran successfully, but the ruleset continued to show
the required checks as `Expected`.

For a while, the behavior suggested that repository-level rulesets might be
necessary because the organization-level ruleset did not appear to recognize
the successful workflow.

The actual cause was in `ci.yml`.

Each job needed an explicit `name:` field matching the required check name.
Once the workflow jobs explicitly produced checks named `build`, `lint`,
`security`, `test`, and `typecheck`, the organization ruleset recognized them
correctly.

That clarified the division of responsibility:

```text
The workflow produces checks.
The ruleset gates merging based on check names.
The names must match exactly.
```

The organization ruleset does not run CI, infer intended jobs, or translate
internal job identifiers into the names the ruleset expects.

Reusable CI must therefore define stable, explicit job names when
organization-level required checks are part of the governance model.

Once the names matched, the repository-level ruleset was no longer needed. It
could remain disabled, leaving the organization-level ruleset as the single
source of truth.

That result was better than duplicating enforcement across every repository.
It preserved centralized governance while capturing the workflow convention
the template must follow.

## Why The Day Mattered

Day 42 did not advance Terminal Run's visible product.

It advanced the system that will support Terminal Run and future projects.

The final Gitleaks verification closed an open Phase 0 question with actual
`RuleID` evidence. The project-template scaffold captured the repeated setup
work. The organization bootstrap failure exposed the need for an explicit
initialization sequence. The required-check investigation established that
stable CI job names are part of the organization contract.

The audit made the governance model more honest.

It showed that squash merges can erase authorship provenance inside mixed
pull requests. It showed that a local agent using administrator credentials
inherits administrator power. It showed that harness deny rules are helpful
but sit behind absence, scoped identity, and repository contracts in the
secret-protection model.

These were not signs that the template effort failed.

They were the evidence needed to make it less naive.

The reusable foundation is now much more mature, but it is not permanently
solved. Each new repository will still need project-specific decisions,
controlled initialization, validation, review, and live drills. The template
should make those activities easier and more consistent without pretending
they can be skipped.

Terminal Run's Session 1 remains waiting.

That wait now buys something concrete: the next repository should begin with
fewer repeated mistakes, clearer ownership boundaries, stable required
checks, stronger prevention layers, and a setup process that already knows
where strict governance can create friction.

## Outcome

Day 42 turned Terminal Run's Phase 0 lessons into a more reusable governance
baseline.

The final local Gitleaks follow-up confirmed that the custom standalone AWS
access-key-ID rule loaded and blocked a planted fake key before commit. The
evidence included the expected `aws-access-key-id-standalone` rule identifier
rather than relying on configuration assumptions.

The organization model separated the minimal `.github` community-health
repository from the richer `project-template` scaffold. The template captured
security hooks, commitlint, Gitleaks, safer npm defaults, TypeScript, ESLint,
Vitest, coverage, an example package, governance documents, ADR templates,
setup guidance, and Phase 0 drill templates.

Strict organization rulesets exposed a repository-bootstrap problem, and the
required-check debugging established the durable fix for mature repositories:
CI jobs need explicit, stable names that match the organization ruleset's
required checks exactly. With those names present, the repository-level
ruleset was unnecessary.

The Sonnet audit returned `NOT CLEAN` and produced actionable governance
improvements. Protected human-only paths should use separate human-only pull
requests because squash merges erase intra-pull-request provenance. Local
agents inherit the maintainer's credentials, so local-as-admin sessions
require extra restraint and review. Secret protection was documented as four
layers, with absence from the repository as the strongest protection and
harness rules as a useful but limited final layer.

Terminal Run still has not begun its walking skeleton. The day instead made
the setup, security, and governance knowledge around that project easier to
reuse while the lessons were still fresh.

## Definition Of Done

Day 42 reached a reusable-template and organization-governance checkpoint:

- completed the final Terminal Run Gitleaks pre-commit verification
- made the hook fail closed with `set -e`
- resolved the configuration path from the Git repository root
- verified the custom standalone AWS access-key-ID rule through its `RuleID`
- confirmed the hook blocks the planted fake key before commit
- separated the `.github` community-health repository from `project-template`
- kept organization fallback files minimal and generic
- assigned reusable scaffolding and setup guidance to the project template
- identified the strict-ruleset bootstrap problem for empty repositories
- established initialization sequencing as an explicit governance concern
- assembled the reusable prevention and development scaffold
- included Husky, commitlint, Gitleaks, and safer npm defaults
- included Prettier, ESLint, TypeScript, Vitest, and coverage configuration
- included an example package with a passing test
- included agent contracts, contribution guidance, security guidance, ADR
  templates, Phase 0 drills, scope logging, and setup documentation
- used a Sonnet audit to challenge the assembled scaffold
- accepted and recorded the audit's `NOT CLEAN` verdict
- identified protected-path provenance loss in mixed squash-merged pull
  requests
- established separate human-only pull requests for human-only paths
- recognized that local agents inherit the maintainer's Git credentials
- established scoped agent identities as the default
- treated local-as-admin agent sessions as contract-only and higher-risk
- documented absence, identity and sandbox, contract, and harness rules as
  the four secret-protection layers
- kept secret absence as the strongest protection
- treated `.claude/settings.json` as a useful harness control rather than a
  primary security boundary
- planned or completed a durable written audit and finding dispositions
- retroactively labeled the earlier scaffold pull request as `ai-assisted`
- corrected a stale ADR reference
- grouped ESLint-family Dependabot updates
- identified Dependabot and Claude-settings backports for Terminal Run
- diagnosed why organization-level required checks remained `Expected`
- added explicit CI job names matching `build`, `lint`, `security`, `test`,
  and `typecheck`
- confirmed the organization ruleset recognizes the explicit check names
- kept the repository-level ruleset disabled
- preserved the organization-level ruleset as the single source of truth
- kept Terminal Run Session 1 waiting while the reusable foundation matured

The day ended with fewer assumptions hidden inside the setup process and more
of the governance baseline ready to travel to the next project.
