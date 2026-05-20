---
title: "Day 18 – May 19, 2026: Framework Modernization, Dependency Governance, and Platform Ideation"
description: "Documenting a platform engineering day focused on Databricks lakehouse learning, Tech Talent Pulse framework modernization, CI stabilization, and early product architecture ideation."
pubDate: "2026-05-19"
day: 18
status: "published"
dashboardSlug: "none"
dataSources:
  - "Spring Boot"
  - "Testcontainers"
  - "Flyway"
  - "PostgreSQL"
  - "Docker"
  - "GitHub Actions"
  - "Microsoft Databricks"
  - "Dependabot"
tags:
  - platform-engineering
  - dependency-governance
  - ci-cd
  - spring-boot
  - testcontainers
  - databricks
  - architecture
---

Day 18 blended hands-on platform engineering, cloud data platform learning,
dependency modernization governance, and early product architecture ideation.

The day started with a live Microsoft Databricks Lakehouse workshop and moved
into a deeper modernization pass on Tech Talent Pulse. The Databricks work
expanded the cloud-native analytics side of the platform learning backlog. The
Tech Talent Pulse work was the heavier engineering thread: stabilizing failing
Dependabot pull requests, treating major framework upgrades as controlled
migrations, and using CI as the final operational truth instead of relying on
local assumptions.

There was also future-facing architecture thinking around `booboostory.com`
and a group of Thai-learning and language-focused domains. Those ideas are not
implementation commitments yet. They are early platform strategy notes about
how creative and educational products could be structured with the same
engineering discipline as a production system.

## Goal / Intent

The goal was to keep learning and modernization connected.

The Databricks workshop provided a structured way to study modern lakehouse
architecture, workflow orchestration, and cloud analytics platform concepts.
The Tech Talent Pulse modernization work provided the practical counterweight:
real dependency upgrades, real CI failures, real framework compatibility
changes, and real integration-test behavior.

The intent was not to blindly merge automation-generated dependency pull
requests. The intent was to understand the migration surface, stabilize it on a
dedicated branch, preserve existing application behavior, and let Docker-backed
CI validation prove whether the system still worked.

## Databricks Technical Workshop

From approximately 9 AM to 3 PM, I participated in a live Microsoft Databricks
Lakehouse workshop.

The workshop included five hands-on Databricks labs. The work involved
creating and orchestrating lakehouses, workflows, and related data platform
components while moving through modern lakehouse architecture concepts in a
guided technical setting.

The useful part was not only seeing Databricks as a product surface. It was
seeing the operating model around it: governed data assets, repeatable
workflows, scalable data processing, and cloud-native analytics patterns that
sit between raw ingestion and business-facing insight.

That exposure expanded my understanding of scalable data engineering
ecosystems. Lakehouse platforms are not just storage plus notebooks. They are
an orchestration and governance layer around data products, compute, workflow
execution, and analytics delivery. The labs made that architecture more
concrete by requiring hands-on creation and coordination of the platform
pieces instead of only reading conceptual diagrams.

The Databricks work also fit the broader direction of this project. A journal
about dashboards eventually needs stronger intuition around the platforms that
feed dashboards: lakehouses, workflow schedulers, managed compute,
observability, data governance, and CI/CD-adjacent operational discipline.

## Dependency Governance & Framework Modernization

The primary technical focus of the day was Tech Talent Pulse dependency
modernization and CI stabilization.

Several Dependabot pull requests were failing or risky enough that they could
not be treated as routine package bumps. That distinction matters. A patch
upgrade can often be reviewed as a narrow dependency maintenance task. A major
framework upgrade is different. It can change package names, auto-configuration
contracts, test infrastructure, runtime behavior, and integration sequencing.

The resolution strategy was to create a stabilization branch and treat the
updates as a controlled engineering migration. That gave the work a safe place
to absorb incompatible changes, update tests, validate Docker-backed behavior,
and reason about migration risk before anything touched the trunk.

The modernization work covered several connected areas:

- Testcontainers 2.x migration
- Spring Boot 4 migration
- Flyway auto-configuration changes
- PostgreSQL integration parity
- Docker-backed CI validation
- GitHub Actions runtime validation
- Jackson compatibility management

The Testcontainers 2.x migration was a good example of why automated pull
requests need engineering review. The Maven artifacts changed names:
`junit-jupiter` became `testcontainers-junit-jupiter`, and `postgresql` became
`testcontainers-postgresql`. The PostgreSQL container package also moved from
`org.testcontainers.containers.PostgreSQLContainer` to
`org.testcontainers.postgresql.PostgreSQLContainer`.

That was not just a dependency coordinate update. The repository integration
tests needed to be modernized around the new package location and current API
usage. PostgreSQL container generic type usage was removed as part of that
cleanup, which brought the tests in line with the newer Testcontainers style.

Spring Boot 4 added its own migration surface. The MVC and auto-configuration
structure changed enough that the upgrade needed careful validation across
application startup, test contexts, data initialization, and integration
behavior. The work had to preserve existing Jackson 2 transformation behavior
while still accommodating Boot 4 changes. That compatibility strategy was
important because serialization behavior can be easy to break silently during a
framework migration.

Flyway was another key migration point. The work explicitly involved
`spring-boot-flyway`, Flyway schema initialization sequencing, and how database
bootstrap behavior interacts with Hibernate validation behavior. The
integration layer had to prove that Flyway migrations ran early enough for
Hibernate to validate the expected schema instead of failing during application
startup.

## CI/CD Validation and Root Cause Analysis

The most important discovery was that local validation was giving a false sense
of confidence.

Local Docker was not available, which meant some integration behavior could not
be exercised properly on the developer machine. That absence created a
false-positive local validation path: checks could appear acceptable locally
while Docker-backed PostgreSQL Testcontainers integration contexts still needed
to be proven somewhere else.

CI became the operational source of truth.

GitHub Actions had Docker available, so the repository integration tests could
run against real PostgreSQL Testcontainers contexts. That mattered because the
Flyway bootstrap failures only surfaced in CI. The failure mode was not visible
until the application had to initialize against the containerized database with
the updated framework and dependency stack.

The root cause analysis centered on startup sequencing and integration parity:
Spring Boot 4, Flyway auto-configuration behavior, Hibernate validation, and
PostgreSQL container startup all had to agree. Once the migration fixes were in
place, the CI run validated the full path with Docker-backed integration tests.

The stabilization outcome was clean:

- 53 tests passed
- 0 failures
- 0 errors
- 0 skipped
- Docker-backed integration validation completed successfully

That result was more meaningful than a local unit-only pass. It proved the
modernized dependency set under the same kind of runtime assumptions the
application needs for production-grade confidence: real container startup, real
database initialization, real schema migration, and real application context
loading.

The larger lesson is that CI/CD is not only a merge gate. It is an operational
diagnostic system. When local development lacks a dependency like Docker, CI
can become the first environment that tells the truth about integration
behavior. The right response is not to dismiss the failure as a pipeline quirk.
The right response is to treat CI as evidence.

## Platform Ideation and Domain Strategy

The day also included early architecture ideation for `booboostory.com`.

The concept is a story and comic-focused platform, likely more personal and
creative than the infrastructure-heavy work that usually appears in this
journal. Even so, it benefits from professional engineering structure. The
initial planning focused on how to organize development, how content might be
modeled, how publishing workflows could work, and what boundaries should exist
between creative assets, static pages, future interactive features, and any
backend services that might eventually become necessary.

The useful framing was that hobby and family creative platforms still deserve
good architecture. They may not need enterprise complexity, but they benefit
from source control, clear content organization, repeatable publishing,
portable assets, and enough governance to avoid turning a fun idea into an
unmaintainable pile of files.

I also spent time thinking about Thai-learning and language-focused domains.
The strategic question was how to organize multiple related domain ideas
without scattering execution across too many partially built surfaces.

That thinking included branding hierarchy, platform separation, language
learning product direction, and how different domains might map to different
audiences or experiments. Some domains may eventually serve as focused
educational platforms. Others may be better treated as redirects, placeholders,
or long-term options.

The important constraint is focused execution. Domain experimentation is useful
only if it produces clearer product direction. The platform strategy needs to
avoid letting domain inventory become a substitute for building. The better
pattern is to preserve the best names, clarify the hierarchy, and choose a
small number of execution paths with explicit ownership.

## Engineering Lessons Reinforced

Day 18 reinforced five engineering lessons.

First, governance-first dependency management matters. Dependabot is useful,
but automation should not be allowed to redefine architecture without review.
Major dependency updates need migration plans, stabilization branches, and
evidence.

Second, CI is a source of operational truth. Local checks are necessary, but
they are not sufficient when local dependencies are missing or incomplete.
Docker-backed CI validation can reveal failures that local development cannot.

Third, framework modernization is rarely one-dimensional. Testcontainers 2.x,
Spring Boot 4, Flyway, PostgreSQL, Jackson, Hibernate, Docker, and GitHub
Actions all interacted. Treating those as isolated package bumps would have
hidden the real migration risk.

Fourth, production-grade testing discipline depends on integration parity.
Repository tests that exercise PostgreSQL Testcontainers contexts provide a
different level of confidence than tests that only validate in-memory or mocked
paths.

Fifth, architecture ideation is more useful when it is constrained by
governance. `booboostory.com` and the Thai-learning domain ecosystem can remain
creative without becoming chaotic if content structure, publishing workflows,
and platform boundaries are considered early.

## Definition of Done

Day 18 was complete when:

- the Microsoft Databricks Lakehouse workshop was attended from approximately
  9 AM to 3 PM
- five hands-on Databricks labs were completed
- lakehouses, workflows, and data platform components were created and
  orchestrated during the workshop
- Dependabot modernization work was stabilized on a controlled branch
- Testcontainers 2.x Maven artifact renames were addressed
- PostgreSQL Testcontainers package relocation and generic type cleanup were
  handled
- Spring Boot 4 migration blockers were resolved
- `spring-boot-flyway` and Flyway schema initialization sequencing were
  validated
- Hibernate validation behavior was aligned with schema migration timing
- Jackson 2 transformation behavior was preserved alongside Boot 4 changes
- PostgreSQL Testcontainers integration contexts passed in Docker-backed CI
- GitHub Actions runtime validation completed successfully
- the CI result showed 53 tests passed, 0 failures, 0 errors, and 0 skipped
- early architecture ideation for `booboostory.com` was documented
- Thai-learning domain ecosystem strategy was clarified at an initial level
- Day 18 journal entry was published

The day connected modern data platform learning with dependency migration
discipline. That combination is the shape of the platform work I want to keep
practicing: learn the larger architecture, then prove the local system under
real validation pressure.
