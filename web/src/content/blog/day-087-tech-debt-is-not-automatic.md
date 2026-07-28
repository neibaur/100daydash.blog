---
title: "Day 87 - July 27, 2026: Tech Debt Is Not Automatic"
description: "A Day 87 reflection on reviewing routine dependency updates, repairing failed automation, and using engineering judgment to resolve transitive security findings and a Terraform provider migration."
pubDate: "2026-07-27"
day: 87
dashboardSlug: "none"
dataSources:
  - "Merged dependency, security, and infrastructure maintenance pull requests reviewed on July 27, 2026"
  - "GitHub Dependabot and security advisory evidence from the repositories discussed"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - dependency-management
  - security
  - dependabot
  - terraform
  - continuous-integration
  - repository-governance
  - technical-debt
---

The visible products did not change much on July 27.

The repositories did.

I spent most of Day 87 moving through dependency updates, security findings,
and maintenance pull requests across a collection of projects. Some changes
were exactly what dependency automation promises: a bot prepared a focused
version update, the repository's required checks passed, and I could review
the release scope and merge with meaningful evidence.

Other changes only looked automatic from a distance.

A failed dependency pull request could represent an incompatible constraint,
a stale lockfile, a formatting baseline, or a removed infrastructure
resource. A security alert could identify a vulnerable package without
providing a useful pull request at all. In those cases, the version number was
the easy part. The engineering work was understanding why the repository
could not accept the proposed change and finding the smallest compatible
repair.

By the end of the day, I had made substantial progress through the maintenance
queue. I also estimated that I was only about halfway through the broader
tech-debt pass.

Automation reduced the discovery work.

It did not remove the judgment.

## The Easy Path Was Trust, But Verify

Several pull requests followed the routine path.

The Astro update in Lingua Core Platform moved from 6.4.4 to 6.4.6. The patch
releases included ordinary fixes as well as security hardening around invalid
HTML attribute names and request-origin validation. In Tech Talent Pulse, the
day's reviewed updates included the JaCoCo Maven Plugin, Astro, the checkout
action, and the Spotless Maven Plugin. Cloudflare IaC Governance also had
straightforward GitHub Actions updates for Gitleaks, checkout, and Python
setup. The Gitleaks action's major update moved its runtime from Node 20 to
Node 24 without changing its documented inputs or behavior.

These were not reasons to click Merge without reading.

For a green Dependabot pull request, I still checked which dependency was
changing, whether the release crossed a major-version boundary, what files
changed, and whether the repository's defined checks had passed. A passing
suite did not prove that nothing could go wrong. It provided useful evidence
that the proposed update still satisfied the behaviors and policies that the
repository knew how to test.

Boo-Boo Story offered a good example of routine automation becoming routine
because of earlier maintenance. Its grouped update covered six minor and
patch changes across commitlint, Vitest coverage, lint-staged, Vitest, and
Astro. Earlier work had already repaired the repository's CI discipline and
established the new Prettier baseline. That groundwork meant the later
dependency group could be evaluated as a normal maintenance change instead
of reopening the governance problem from Day 85.

The bot prepared the changes.

I reviewed the scope, relied on the repository's evidence, and chose what to
merge.

## A Version Bump Became A Migration

The Cloudflare Terraform provider update was the clearest counterexample to
the idea that dependency maintenance is automatic.

Dependabot proposed moving the provider constraint from the v4.52 line to the
v5.22 line. The generated pull request could not be merged as a simple
constraint edit. The root configuration and a child module no longer agreed:
one asked Terraform for provider v5 while the other still required v4.
Terraform initialization could not select one version that satisfied both.

Resolving that conflict only exposed the next problem.

The v5 provider had removed `cloudflare_zone_settings_override`, a resource
used by the existing module. Updating the constraint without changing the
configuration would leave the infrastructure code referring to a resource
that no longer existed.

This was a migration, not a typo in a version string.

I used prompt engineering and coding agents to investigate the failed update
and formulate a focused repair. The completed change aligned the child module
with Cloudflare provider `~> 5.22` and replaced the removed aggregate resource
with individual `cloudflare_zone_setting` resources. The migration preserved
the existing intent for SSL mode, security level, HTTPS behavior, minimum TLS,
browser integrity, and bot management, then validated the resulting Terraform
configuration.

The failed check was doing useful work. It showed that the provider graph was
internally inconsistent. The removed-resource error then showed that the new
provider represented an API change in the infrastructure code.

Weakening the check would not have made the migration safe. It would only have
hidden the evidence that the migration was incomplete.

## Security Lived Below `package.json`

The security work exposed another boundary of automation: the vulnerable
package was often transitive.

A transitive dependency is a package installed because another dependency
needs it. It may appear in the lockfile even though the project never lists it
directly in `package.json`. That makes remediation less obvious than changing
one direct version.

This repository's `fast-uri` repair was one example. The vulnerable 3.1.2
resolution entered through `ajv@8.20.0`. The correct repair was not to select
the largest version number available. It was to move to `fast-uri` 3.1.4, the
patched release that still satisfied AJV's declared `^3.0.1` constraint.

The lockfile was regenerated, the dependency path was traced, the audit ran,
and the repository validation passed. The result removed the vulnerable
resolution without pretending that AJV had declared compatibility with a new
major version.

Domain Placeholder Platform required the same kind of reasoning at a wider
scale. One focused pull request used pnpm overrides for vulnerable transitive
versions of `ws`, `brace-expansion`, `js-yaml`, `fast-uri`, `linkify-it`,
`markdown-it`, and `esbuild`. For each override, the work included inspecting
why the package was installed, regenerating the lockfile, running the audit,
validating the repository, building the project, and reviewing the final diff.

PostCSS needed a separate repair. The dependency graph contained vulnerable
PostCSS 8.5.14, while 8.5.18 was the first patched release. The repository
already resolved 8.5.23 elsewhere through Vite, so the override reused 8.5.23
instead of introducing an unnecessary additional resolution. Dependency
tracing then confirmed that no installed PostCSS version remained below the
patched line.

GitHub security alerts were valuable discovery mechanisms. They identified
that a vulnerable version was present.

They did not always decide which patched version was compatible, which parent
introduced it, or whether the lockfile actually stopped installing the
vulnerable resolution. That still required investigation and validation.

## Checks Were Diagnostic Information

Across the day, green and red checks meant different kinds of work.

A green dependency pull request made review efficient. I could inspect the
release scope, changed files, and evidence, then decide whether the update was
appropriate. The Astro, GitHub Actions, JaCoCo, and Spotless changes largely
fit this path.

A red pull request was not merely an obstacle between me and the Merge button.
It was a report about the interaction between the update and the repository.

Sometimes that interaction was a provider constraint. Sometimes it was a
removed Terraform resource. In other repositories, it could be a lockfile
that no longer represented the manifest, a formatter that changed the
baseline, or a package whose compatible patched version needed to be selected
deliberately.

Coding agents helped inspect those failures, trace dependency graphs, and
prepare focused solutions. They did not independently approve or merge the
work. I reviewed the proposed changes, used the repository's checks as
evidence, and retained responsibility for the merge decision.

That distinction matters because an agent can make investigation faster
without becoming the owner of the decision.

The same is true of Dependabot. It can notice an available release and prepare
a change. It cannot guarantee that an infrastructure provider removed no
resources the repository uses, that every indirect package is compatible with
an override, or that a passing test suite covers every risk.

Automation is strongest when it makes evidence easier to produce and review.
It becomes dangerous when its output is mistaken for judgment.

## Maintenance Made Future Maintenance Easier

The grouped Boo-Boo Story update also showed why tech-debt work compounds in a
useful direction.

Day 85's formatter and CI-governance repairs were not repeated on July 27.
They did not need to be. Because the repository already had a valid formatting
baseline and more precise quality gates, the next minor-and-patch dependency
group could travel the easy path.

That is one of the quieter returns on maintenance.

A repaired lockfile makes the next dependency diff easier to understand. A
precise CI rule distinguishes a real policy violation from a valid change. A
known formatting baseline prevents unrelated noise from being mixed into a
future update. A documented provider migration leaves the module internally
consistent for the next Terraform initialization.

The value is not only the vulnerability removed or the version updated today.
It is the reduction in ambiguity when the next update arrives.

## Halfway Through Was Still Progress

The day did not end with every repository current and every alert closed.

It ended with a meaningful portion of the queue reviewed, several routine
updates merged, multiple transitive security findings repaired, and one
substantial Terraform provider migration completed. It also ended with more
maintenance still visible.

I estimated that I was approximately halfway through the broader tech-debt
pass. Another maintenance session was planned, but that future work was not
part of July 27 and was not yet complete.

That boundary is important in maintenance writing. A long list of merged pull
requests can create the impression that the queue reached zero. It did not.
Repositories continue to accumulate releases, advisories, runtime changes,
and assumptions that eventually meet a new dependency.

The goal was not to claim that tech debt had been eliminated.

The goal was to keep paying it down with enough care that today's fix did not
become tomorrow's unexplained exception.

## Outcome

Day 87 was primarily a multi-repository maintenance day.

I reviewed and merged routine Dependabot updates when their scope was
understandable and the repositories' required checks provided appropriate
evidence. Those changes included framework, Maven plugin, and GitHub Actions
updates across several projects.

I also used prompt engineering and coding agents to investigate updates that
could not safely be merged as generated. The largest example was the
Cloudflare Terraform provider v5 migration, which required aligning root and
child-module constraints and replacing a removed aggregate zone-settings
resource with individual resources while preserving the existing
configuration intent.

Security findings below the direct dependency layer required targeted pnpm
overrides, regenerated lockfiles, dependency tracing, audits, repository
validation, builds, and final diff review. The `fast-uri` repair selected
3.1.4 because it was patched and remained inside AJV's declared compatible
range. The PostCSS repair reused an already-present patched resolution rather
than adding another version unnecessarily.

The maintenance sweep was not complete. By the end of July 27, I estimated
that the broader effort was approximately halfway finished.

## Definition Of Done

Day 87 reached the July 27 maintenance checkpoint:

- followed Day 86 with the July 27, 2026 entry
- framed the day as tech-debt work rather than visible product development
- distinguished routine Dependabot review from failed-update repair
- preserved human responsibility for approval and merge decisions
- treated passing CI as meaningful evidence rather than proof of absolute safety
- used the Cloudflare provider v5 change as the primary migration example
- explained the incompatible root and child-module provider constraints
- explained that `cloudflare_zone_settings_override` was removed in provider v5
- recorded the replacement with individual zone-setting resources
- described transitive dependencies in plain language
- recorded the compatible `fast-uri` 3.1.4 remediation through AJV
- summarized the broader pnpm override work without becoming a package changelog
- recorded the PostCSS 8.5.23 override and removal of vulnerable resolutions
- treated failed checks as diagnostic information instead of bureaucracy
- connected earlier repository governance work to easier routine maintenance
- made no unsupported claims about inaccessible repository pull requests
- claimed no work from July 28 as completed on July 27
- stated that the broader tech-debt pass remained approximately halfway complete
