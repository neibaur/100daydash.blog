---
title: "Day 86 - July 26, 2026: Automation at the Wrong Scale"
description: "A Day 86 reflection on nine Dependabot pull requests, branch protection, 86 Cloudflare checks, package-manager drift, and knowing when infrastructure is not ready to become code."
pubDate: "2026-07-26"
day: 86
dashboardSlug: "none"
dataSources:
  - "Domain Placeholder Platform Dependabot PRs #52 through #60 and local maintenance notes"
  - "Domain Placeholder Platform branch-protection and Cloudflare Pages investigation notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - dependency-management
  - continuous-integration
  - branch-protection
  - cloudflare
  - terraform
  - infrastructure-as-code
  - repository-governance
---

Nine routine dependency pull requests turned into an infrastructure review.

Dependabot had opened PRs #52 through #60 in the Domain Placeholder Platform
repository. The updates covered application dependencies, development tools,
and GitHub Actions: Gitleaks, checkout, setup-node, Astro, Vite,
`@astrojs/sitemap`, ESLint, `@eslint/js`, `tsx`, and grouped npm changes.

The first question was how to process them.

Combining all nine into one dependency-refresh branch could reduce repeated
installation, validation, and deployment work. It could also make a failure
harder to isolate. A broken Astro update and a GitHub Actions runtime change
would share one result even though they affected different parts of the
system.

I considered several groupings, then chose the direct path: review, approve,
update, and run the Dependabot pull requests one at a time. I completed or
processed most of them individually.

That choice was less clever than a custom dependency campaign. It preserved
the isolation that Dependabot had already created, and it made each failure
easier to interpret.

The interesting part of the day was not the version numbers.

Routine maintenance exposed the difference between code validation, deployment
behavior, and infrastructure authority. Those systems all appeared as checks
on a pull request, but they did not mean the same thing and were not controlled
from the same place.

## Turning Branch Protection Back On

The repository already had branch-protection configuration, but the active
protection was not doing the intended work.

I enabled an active protection setup for `main` so changes must pass through
the expected pull-request and check process.

The difficult part was deciding what a required check should represent.

The repository owned a small set of meaningful checks, including validation,
CodeQL, Gitleaks, and Terraform validation. The pull-request interface showed
many more statuses than that.

It would have been easy to treat every visible status as an equally important
repository check. That would have confused the code's validation policy with
the behavior of an external deployment platform.

Today's change activated or updated branch protection. It did not redesign
every workflow or establish a final required-check policy for every external
status. Understanding the difference was part of the work.

## Why One Pull Request Had About 86 Checks

One sample dependency pull request showed roughly 86 checks.

The repository itself did not contain 86 distinct validation workflows. Most
of the additional statuses were Cloudflare Pages preview deployments.

The same placeholder application is connected to approximately 80 Pages
projects, one for each domain or placeholder site. When a pull request opens,
each connected project can independently build a preview and report another
GitHub check.

The result is technically consistent with the configuration.

Production deployments occur from `main`. Pull-request deployments are
previews, not production releases. A preview can be useful because it allows a
reviewer to inspect a branch before merging it.

One preview per pull request is useful.

Approximately 80 previews of the same placeholder platform are mostly
duplication, especially when the branch came from Dependabot and changes a
small dependency declaration or lockfile.

The checks were not evidence that the repository had an unusually deep
validation suite. They were evidence that one repository event was fanning out
across many separately connected deployment projects.

This distinction changes the response. The answer is not to remove code
validation because the check list is noisy. It is to decide where preview
deployment provides evidence and where it merely repeats the same work.

A future arrangement could keep one representative Pages project building
feature-branch previews while suppressing Dependabot previews or disabling
preview builds across most duplicate projects.

I did not change those Cloudflare settings today. The useful outcome was the
investigation and a clearer direction for later work.

## Configuration Was Not Yet Infrastructure Authority

With approximately 80 Pages projects, changing deployment settings by hand
would be slow and difficult to audit.

Terraform seemed like a natural answer. It could eventually express rules such
as:

- use `main` as the production branch
- keep production deployment enabled
- permit previews for normal feature branches
- exclude `dependabot/*` from preview deployment

The repository already contains Terraform, but its current role is
validation-oriented. It does not yet safely manage the existing Cloudflare
Pages estate through complete resource definitions, imported state, and a
controlled lifecycle.

That difference matters.

Having Terraform files is not the same as Terraform having authority over
existing infrastructure. Giving it authority before the resources are fully
modeled and imported could turn a cleanup task into unexpected updates,
replacements, or configuration drift across approximately 80 projects.

Infrastructure as code is valuable partly because it makes authority explicit.
That value disappears if the code describes only part of the real resource and
the state does not establish which existing object it owns.

Two safer future paths emerged.

The first is a narrow, audited Cloudflare API script. It would inventory the
projects, select only those connected to this repository, back up current
settings, show a dry run, update one pilot, verify the result, and proceed only
through an explicit allowlist. Its final report would identify both successes
and failures.

The second is deliberate Terraform adoption. That work would establish secure
state, model all significant project properties, import one pilot project, and
require a plan with zero destroys and zero replacements. Lifecycle protection
and controlled batches would follow before the remaining projects moved under
management.

Neither path was implemented today.

That restraint was part of the engineering decision. Terraform may be the
right long-term authority, but prematurely claiming authority over 80 existing
projects would be riskier than leaving the settings manual until inventory,
state, backup, pilot, and rollback controls exist.

## The Lockfile Repair Started With The Wrong pnpm

One Dependabot pull request failed validation, so I checked out its branch
locally and tried to repair the installation and lockfile.

My local environment used pnpm 11.17.0. The repository selected pnpm 10.11.0.

That difference produced changes unrelated to the dependency under review.
Package-manager metadata moved, and invalid placeholder-style entries appeared
in `pnpm-workspace.yaml`. A small repair was becoming a package-manager
migration without anyone choosing one.

The recovery process began by restoring `package.json`, `pnpm-lock.yaml`, and
`pnpm-workspace.yaml`, then confirming that the working tree was clean.

I used Corepack to honor the repository-selected pnpm version, confirmed that
10.11.0 was active, regenerated only the lockfile, verified a frozen
installation, ran repository validation, and inspected the final diff before
considering a commit.

The approximate sequence was:

```bash
git restore -- package.json pnpm-lock.yaml pnpm-workspace.yaml
git status --short
corepack pnpm --version
corepack pnpm install --lockfile-only
corepack pnpm install --frozen-lockfile
corepack pnpm validate
git status --short
git diff -- pnpm-lock.yaml
```

The lesson was larger than the lockfile command.

A package manager is part of the repository's toolchain. A newer local version
can interpret metadata differently, rewrite files, and obscure the narrow
change under review. Restoring first and using the pinned version separated the
intended dependency update from accidental toolchain drift.

This was local troubleshooting on the failing Dependabot branch. I am not
claiming that the repair was merged.

## Rebase And Recreate Preserve Different Things

I also learned two useful Dependabot commands.

The first response after `main` changes is usually:

```text
@dependabot rebase
```

That asks Dependabot to move its pull request onto the latest base, regenerate
the update where possible, and rerun checks.

The stronger option is:

```text
@dependabot recreate
```

Recreate discards manual commits on the Dependabot branch and rebuilds the
dependency proposal from the latest base.

That destructive difference is the point.

Rebase is appropriate when branch work should be preserved. Recreate is useful
when a generated branch is conflicted or polluted and its manual changes have
no value. In that situation, asking Dependabot to reproduce its own update can
be safer than manually resolving a lockfile conflict without confidence about
which side represents the intended dependency graph.

Automation still required a human decision about what deserved preservation.

## Three Systems Behind One Green Check List

By the end of the investigation, the pull-request page represented at least
three different systems.

Repository validation answered whether the code, dependency graph, Terraform
syntax, and security checks met the project's rules.

Cloudflare preview deployments answered whether each connected Pages project
could produce a branch preview.

Infrastructure authority answered who could safely change the configuration of
those Pages projects at scale.

All three involved automation. Only the first two currently executed from pull
requests, and only the repository checks belonged naturally in the required
validation policy.

The third system did not become safe merely because Terraform existed in the
repository.

This was the larger theme behind nine dependency updates. Automation is useful
only when its scope is understood.

Dependabot automated version proposals, but it could not decide whether nine
updates should be grouped, whether a failed lockfile was caused by toolchain
drift, or whether a branch should be rebased or recreated.

Cloudflare correctly created previews from connected projects, but the
configuration that was reasonable for one project no longer fit approximately
80 copies of the same platform.

Terraform could eventually make that fleet manageable, but adopting it
carelessly would give incomplete code too much authority.

Good maintenance is not measured by how many systems change in one day.
Sometimes it means activating the protection that is ready, repairing the
branch with the toolchain the repository actually selected, and declining to
change infrastructure until the controls around that change are credible.

## What I Learned

A small dependency update can reveal a much larger operating model.

Nine routine pull requests surfaced inactive branch protection, dozens of
duplicated previews, local package-manager drift, and the current limits of
Terraform ownership.

None of those findings made the automation useless.

Dependabot reduced the work required to identify updates. Branch protection
made the intended review path enforceable. Cloudflare previews proved that
branch builds were possible. Corepack made the selected package-manager
version reproducible. Terraform validation still protected the code that
exists today.

The problem was treating every automated result as if it had the same purpose
or authority.

Approximately 86 checks did not mean 86 independent quality signals. A
Terraform directory did not mean 80 existing projects were safely managed.
pnpm installed on my machine did not mean I was using the repository's pnpm.
A generated Dependabot branch did not mean every manual conflict resolution
was worth preserving.

The day became more productive when those boundaries became explicit.

## Outcome

Day 86 processed most of the nine open Domain Placeholder Platform Dependabot
PRs, #52 through #60, through individual review and validation rather than a
single combined refresh branch.

I activated or updated branch protection for `main` without claiming that
every workflow or required-check policy was redesigned.

I traced roughly 86 checks on a sample pull request to the repository's normal
checks plus preview deployments from approximately 80 connected Cloudflare
Pages projects. Production remained associated with `main`; the additional
pull-request deployments were previews. No Cloudflare deployment settings were
changed.

I considered both an audited API script and a controlled Terraform adoption
project for future preview-policy changes. No Terraform or Cloudflare resources
were changed. The current Terraform setup remains validation-oriented rather
than a complete, imported, state-backed management layer for the Pages
projects.

On one failing Dependabot branch, I restored unintended package files, used
Corepack to honor the repository-pinned pnpm 10.11.0 instead of local pnpm
11.17.0, regenerated only the lockfile, checked frozen installation and
validation, and reviewed the resulting diff. That work was local
troubleshooting, not a claim that the repair merged.

I also learned when to ask Dependabot to `rebase` and when a branch is better
discarded and recreated.

## Definition Of Done

Day 86 reached the dependency-maintenance and infrastructure-investigation
checkpoint:

- followed Day 85 with the July 26, 2026 entry
- identified PRs #52 through #60 as nine Dependabot proposals
- described most updates as individually reviewed or processed without
  claiming that all nine merged
- explained why grouping could reduce repeated work but obscure failures
- recorded that branch protection for `main` was activated or updated
- did not claim a complete workflow or required-check-policy redesign
- distinguished repository validation from Cloudflare preview statuses
- explained approximately 86 checks as a small validation set plus previews
  from approximately 80 connected Pages projects
- distinguished pull-request previews from production deployment on `main`
- proposed representative preview and Dependabot-suppression options as future
  work only
- made no claim that Cloudflare settings changed
- described the current Terraform setup as validation-oriented
- made no claim that Terraform resources, imports, or state changed
- documented safe API-script and Terraform-adoption directions without
  presenting either as implemented
- recorded the pnpm 11.17.0 and repository-pinned 10.11.0 mismatch
- separated unintended package-manager rewrites from the intended lockfile
  repair
- described the repair as local troubleshooting without claiming it merged
- explained the preservation difference between Dependabot rebase and recreate
- connected dependency maintenance to validation, deployment behavior, and
  infrastructure authority
