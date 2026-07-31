---
title: "Day 90 - July 30, 2026: Following the Dependency Graph to a Clean Security State"
description: "A Day 90 reflection on resolving automated dependency updates by tracing build failures, lockfile scope, transitive vulnerabilities, and tooling compatibility."
pubDate: "2026-07-30"
day: 90
dashboardSlug: "none"
dataSources:
  - "Public pull requests and security-maintenance results from neibaur/domain-placeholder-platform"
  - "Public pull requests and security-maintenance results from neibaur/tech-talent-pulse"
  - "Public pull requests and security-maintenance results from neibaur/lingua-core-platform"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - dependency-management
  - security
  - dependabot
  - continuous-integration
  - spring-boot
  - astro
  - pnpm
  - repository-governance
---

July 30 began with what looked like a queue of automated dependency updates.

It became an investigation of build compatibility, generated lockfiles,
package-manager scope, transitive dependencies, and the order in which related
pull requests needed to move.

I worked through security and dependency maintenance in
[Domain Placeholder Platform](https://github.com/neibaur/domain-placeholder-platform),
[Tech Talent Pulse](https://github.com/neibaur/tech-talent-pulse), and
[Lingua Core Platform](https://github.com/neibaur/lingua-core-platform). Some
Dependabot pull requests merged after ordinary review. Others needed their
branches refreshed, became obsolete after another change landed, or exposed a
repository problem that a version bump alone could not solve.

By the end of the day, the required builds and checks passed, the relevant
audits reported no known vulnerabilities, obsolete automated pull requests
were closed, and the repositories' security dashboards reflected a clean
state.

That result did not come from treating each notification as an isolated task.
It came from following the dependency graph until the repository as a whole
was healthy.

## An Automated Pull Request Is A Starting Point

Dependabot is good at identifying that a dependency can move.

It cannot always know whether the proposed branch still reflects the latest
base branch, whether another merged update has already replaced its work, or
whether a repository's build tools agree about the new dependency graph.

Domain Placeholder Platform provided the straightforward version of that
lesson.

[PR #64](https://github.com/neibaur/domain-placeholder-platform/pull/64)
merged and closed. PR #63 had previously been blocked by failing checks, but
updating its branch with the latest `main` changed the evidence: the checks
succeeded, and the pull request merged.

Dependabot then automatically closed PRs #65 and #66 because their proposed
updates were no longer necessary.

No separate manual repair was required for those two pull requests. The
repository had moved underneath them. Refreshing the dependency branches
showed which changes were now valid and which changes had become redundant.

This was a useful reminder that a red automated pull request does not always
mean its package needs a custom fix. Sometimes its branch is stale. Sometimes
another merged change has already established the required version. Updating
the proposal against the current base can resolve an outdated check or prove
that no proposal remains to merge.

## One Dependency Sequence Exposed Several Boundaries

Tech Talent Pulse was the main technical story of the day.

[PR #36](https://github.com/neibaur/tech-talent-pulse/pull/36) was a
straightforward Dependabot update. I reviewed and merged it, and the
repository's visible security-alert count fell from 17 to 8.

That was meaningful progress, but it was not the final state.

Dependabot PR #31 continued to fail its build and verification checks. PR #37
was created with Copilot assistance to address the remaining findings, but it
did not fully resolve the repository. PR #38 then supplied an additional
unblocking change and merged. After PR #31 was updated again, its checks
finally passed. PR #39 ultimately contained the changes required to clear the
remaining security issues.

The sequence matters.

No single pull request fixed everything. The successful result came from
reviewing the state after each change, using the next failure as diagnostic
information, and continuing until both application validation and security
evidence were clean.

## A Security Upgrade Met A JSON Compatibility Boundary

The Java build failure behind the dependency upgrade came from a real
compatibility boundary.

Spring Boot 4.1 changed its default JSON stack to Jackson 3. The application
still used Jackson 2 imports under `com.fasterxml.jackson.*`. The dependency
upgrade therefore changed more than a version number: it changed an assumption
below the application's source code.

A focused compatibility dependency allowed the existing application to keep
compiling without turning the security-maintenance task into an immediate,
large Jackson 3 migration.

That was a practical bridge, not a claim about the ideal permanent
architecture. Compatibility dependencies should remain visible and can be
removed when the application completes the larger migration or when upstream
support makes them unnecessary.

The backend validation command was:

```bash
mvn clean verify
```

There was also a smaller troubleshooting lesson inside that work. Maven first
failed because I ran the command from the `frontend` directory, where there
was no project `pom.xml`. Running the same command from the repository root
resolved that problem.

The command itself had not changed.

Its context had.

## A Clean Audit Was Looking At The Wrong Workspace

The remaining frontend findings were initially confusing.

These commands reported no changes and no known vulnerabilities:

```bash
pnpm --dir frontend install
pnpm --dir frontend audit
```

That looked reassuring, but it conflicted with the repository's visible
security state.

The discrepancy came from pnpm detecting an unrelated parent workspace outside
the repository. The commands were not treating the frontend as the independent
project I expected them to inspect. A successful command was therefore not
enough evidence. I also needed to verify which workspace and lockfile the
package manager was using.

Explicitly ignoring the unexpected parent workspace corrected the scope:

```bash
pnpm --dir frontend --ignore-workspace install --no-frozen-lockfile
```

The frontend lockfile could then be regenerated from the intended project
state.

This was one of the day's most reusable lessons. Tools can exit successfully
while operating in a context different from the one a developer has in mind.
A clean audit is only meaningful when it audits the dependency graph that will
actually be installed.

## Transitive Repairs Needed A Narrow Escape Hatch

Refreshing the lockfile removed much of the confusion, but a smaller set of
transitive vulnerabilities remained.

Transitive packages are installed because another dependency needs them, so
they may not appear as direct choices in the project's manifest. Temporary
pnpm overrides selected patched versions of:

- `fast-uri`
- `yaml`
- `@babel/core`

Overrides are useful when the direct dependency chain has not yet selected a
patched compatible release. They are also an exception that the repository
now owns.

I treated these as focused, practical fixes rather than permanent ideal
architecture. They should be revisited after the upstream dependency chain
naturally includes the patched versions. Until then, the lockfile and audits
provide evidence that the vulnerable resolutions are no longer installed.

After the changes, both the full audit and the production-only audit reported
no known vulnerabilities.

## Security Changes Also Test The Toolchain

The security upgrades exposed another compatibility boundary in the frontend.

TypeScript 7.0.2 was outside the supported peer range of the installed
`@astrojs/check` version. As a result, `astro check` crashed while accessing
the TypeScript configuration.

Pinning TypeScript to 5.9.3 restored compatibility with the Astro checking
toolchain.

Again, the important outcome was not choosing the highest available version.
It was choosing a secure, supported combination that left the project's
validation working. A dependency update that clears an audit while breaking
the typechecker is not a complete maintenance result.

Final frontend validation included:

```bash
pnpm --dir frontend --ignore-workspace install --frozen-lockfile
pnpm --dir frontend --ignore-workspace check
pnpm --dir frontend --ignore-workspace build
pnpm --dir frontend --ignore-workspace audit
pnpm --dir frontend --ignore-workspace audit --prod
```

The frozen installation, frontend check, and production build passed. The full
and production audits reported no known vulnerabilities.

## A Generated Lockfile Blocked Valid Updates

Lingua Core Platform demonstrated a different source of repeated dependency
failures.

Dependabot PRs #236, #237, and #238 were all failing for the same
non-security reason: Prettier was attempting to format `pnpm-lock.yaml`.

The lockfile is generated dependency data. Applying a source formatter to it
added noise and blocked otherwise valid updates without improving the quality
of the source code.

[PR #239](https://github.com/neibaur/lingua-core-platform/pull/239) added the
lockfile to `.prettierignore`. That small governance change removed the
repeated friction while preserving meaningful formatting checks for the files
the repository's authors maintain directly.

Afterward, PR #236 was updated with the latest `main` and merged successfully.
I added an `@dependabot rebase` comment to PR #237; after rebasing, Dependabot
determined that the proposed change was already present. PR #238 was similarly
refreshed and automatically closed because no update remained necessary.

Those closures were different from merges, and the distinction matters. The
repository did not need three additional dependency changes. It needed an
accurate view of which changes still existed after the base branch and
generated lockfile policy were corrected.

## An Empty Pull Request Queue Was Not A Clean Security State

Even after the pending dependency pull requests were resolved, Lingua Core
Platform's Security and quality tab still showed 16 alerts.

That was evidence that the pull request queue and the security state were two
different views of the repository.

I copied the public alert titles into Codex and used them as the starting point
for a repository dependency audit. Codex created a focused branch, inspected
the dependency graph, and updated the problematic dependencies. I reviewed the
result and merged it through a pull request.

The audit ran twice for a reason.

The first pass identified and corrected the problematic dependency state. The
second pass verified the result. After the merge, the Security and quality tab
showed no remaining flagged items.

That does not mean the repository can never receive another vulnerability.
Advisories and dependency graphs continue to change. It means the audit and
GitHub security dashboard were clean at the conclusion of July 30's work.

## Validate The Repository, Not The Notification

Across the three repositories, automated pull requests were valuable
instruments.

They identified available updates, prepared focused diffs, and made dependency
maintenance visible. Codex and Copilot also accelerated parts of the
investigation and implementation.

None of those tools defined the final state by itself.

The repository was the unit that needed to become healthy. That required
checking several connected forms of evidence:

- builds and required checks passed
- dependency audits reported no known vulnerabilities
- generated lockfiles represented the intended workspace
- compatibility fixes left application tooling operational
- obsolete Dependabot proposals closed without unnecessary replacements
- active dependency pull requests merged or were confirmed unnecessary
- GitHub's security dashboards reflected the completed dependency state

This is why security maintenance is more than merging Dependabot pull
requests.

A red check may point to stale branch state, a generated file in the wrong
validation path, a framework migration boundary, or a package manager using
an unexpected workspace. A green audit may be looking at the wrong lockfile.
An empty automated-update queue may coexist with unresolved security alerts.

The individual notification is a clue.

The complete repository state is the outcome.

## Outcome

Day 90 completed a multi-repository security and dependency-maintenance pass
using only public repository work.

In Domain Placeholder Platform, PR #64 merged, the previously blocked PR #63
passed after being updated with the latest `main`, and Dependabot automatically
closed PRs #65 and #66 after their proposed updates became unnecessary.

In Tech Talent Pulse, PR #36 provided the straightforward update and reduced
the visible security alerts from 17 to 8. PR #31 and PRs #37 through #39 formed
a connected troubleshooting sequence rather than one all-purpose fix. The
work addressed the Spring Boot 4.1 and Jackson compatibility boundary, rebuilt
the frontend lockfile in the correct pnpm scope, applied focused temporary
overrides for remaining transitive findings, and restored Astro checking by
pinning TypeScript to a supported version. PR #39 ultimately cleared the
remaining security issues.

In Lingua Core Platform, PR #239 stopped Prettier from treating the generated
pnpm lockfile as authored source. That unblocked the dependency sequence:
PR #236 merged, while refreshed PRs #237 and #238 were automatically closed
when their updates were no longer needed. A separate Codex-assisted dependency
audit then addressed the 16 alerts that remained after the automated pull
request queue was clear. A second audit and the GitHub dashboard confirmed the
clean result.

At the conclusion of the day's work, the required checks and builds passed,
the relevant audits reported no known vulnerabilities, and the security
dashboards showed no remaining flagged items. Those statements describe the
verified state on July 30, not a guarantee about future advisories.

## Definition Of Done

Day 90 reached the July 30 repository-security checkpoint:

- followed Day 89 with the July 30, 2026 entry
- focused exclusively on public repository information
- distinguished merged pull requests from automatically closed proposals
- treated Dependabot updates as starting points rather than complete solutions
- recorded the Domain Placeholder Platform branch refresh and obsolete updates
- described Tech Talent Pulse as a sequence involving PR #31 and PRs #36
  through #39
- avoided claiming that one Tech Talent Pulse pull request resolved everything
- explained the Spring Boot 4.1 and Jackson compatibility boundary
- presented the compatibility dependency as a focused bridge, not permanent
  ideal architecture
- recorded `mvn clean verify` and the repository-root working-directory lesson
- explained the unexpected pnpm parent workspace and corrected command scope
- described the lockfile regeneration and temporary transitive overrides
- recorded the TypeScript and Astro checking compatibility repair
- stated that backend and frontend validation passed
- stated that full and production frontend audits reported no known
  vulnerabilities
- explained why Lingua Core excluded the generated lockfile from Prettier
- preserved meaningful source formatting checks
- recorded the rebase and automatic-closure outcomes for obsolete proposals
- separated Lingua Core's Dependabot cleanup from its later security audit
- described Codex and Copilot as investigation and implementation aids
- ran the Lingua Core audit once to repair and again to verify
- validated the final repository states instead of stopping at individual
  pull-request outcomes
- limited clean-security claims to the conclusion of July 30's work
