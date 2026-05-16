---
title: "Day 10 - May 11, 2026: Environment Stability, CI Reliability, and Workflow Hardening"
description: "Documenting an operational maturity day focused on Docker Desktop stability, Flyway migration reliability, CI parity, Git branch hygiene, and continued Java platform workflow hardening."
pubDate: "2026-05-11"
day: 10
dashboardSlug: "none"
status: "published"
tags:
  - docker
  - flyway
  - ci-cd
  - github-actions
  - developer-experience
  - infrastructure
  - java
  - devops
  - workflow-governance
dataSources:
  - name: "GitHub Actions"
    url: "https://docs.github.com/en/actions"
  - name: "Docker Desktop"
    url: "https://docs.docker.com/desktop/"
  - name: "Flyway"
    url: "https://documentation.red-gate.com/fd"
  - name: "Git"
    url: "https://git-scm.com/doc"
---

Day 10 did not produce a dashboard.

This was an operational maturity day. The work was less visible than a new
chart, dataset, or interface, but it mattered just as much to the long-term
health of the project. The focus was environment reliability, CI debugging,
repository hygiene, and continuing phased progress on the Java ETL/dashboard
platform.

Some days are about adding capability. This one was about making sure the
systems around that capability can be trusted.

## Goal / Intent

The goal was to stabilize the engineering foundation around the current Java
Architect E2E / Tech Talent Pulse style project while keeping the broader
`100daydash.blog` workflow disciplined and reviewable.

That meant continuing phased architecture implementation while also tightening
the operational surfaces that support the work:

- keep Java platform changes moving through feature branches and pull requests
- validate Flyway migrations in both local and CI environments
- investigate CI failures without assuming local success told the whole story
- restore Docker Desktop to a stable local development state
- clean up stale Git branches and reduce local repository noise
- keep branch protection expectations and workflow maturity moving in the right
  direction

The project is moving out of prototype setup and toward a repeatable engineering
workflow. That transition is not only about code structure. It is also about
trustworthy migrations, predictable CI, clean branches, and developer tooling
that behaves the same way tomorrow as it did today.

## Challenges Encountered

The first major challenge was a Flyway migration failure that only showed up in
CI.

Locally, the migrations appeared to pass. The application could see the expected
schema, and the migration sequence looked valid from the workstation. In GitHub
Actions, the same path failed. Hibernate schema validation reported missing
tables in the CI database, which meant the application was starting against an
incomplete schema even though the local migration state looked healthy.

The root cause was not Flyway itself. It was source control.

A broad `.gitignore` rule had accidentally excluded required migration `.sql`
files. Those scripts existed locally, so local validation could succeed. They
were not tracked in Git, so CI never received the full migration set. GitHub
Actions was not failing randomly. It was faithfully testing the repository as it
actually existed remotely, and the repository was missing part of the database
history.

That exposed a useful but uncomfortable distinction: local files are not the
deployment input. Tracked files are.

The second challenge was local Docker instability.

Docker Desktop initially failed or behaved inconsistently. Older Docker Machine
or Docker Toolbox style environment variables and stale context assumptions made
the situation harder to read. The shell could point at one Docker configuration
while Docker Desktop expected another. That kind of drift turns simple container
commands into environment archaeology.

The third challenge was Git workflow drift.

After several feature branches, PRs, dependency updates, and investigation
branches, the local repository had accumulated stale remote-tracking references
and obsolete merged branches. None of that blocked a build by itself, but it
increased cognitive load. A branch list full of dead paths makes it harder to
see what is active, what is already merged, and what still needs attention.

## Solutions / Work Performed

Work continued on the Java ETL/dashboard platform through phased architecture
implementation.

Feature branches were created, reviewed, and merged into `main` through pull
requests. The workflow is becoming more disciplined: small branches, reviewable
changes, CI validation, and stronger expectations around branch protection. The
platform is still evolving, but the operating model is becoming less ad hoc and
more repeatable.

The Flyway and CI failure investigation started by comparing local assumptions
against what CI could actually see.

The important clue was that migrations worked locally but failed in GitHub
Actions. That pointed away from purely application-level logic and toward
repository state, environment state, or CI database setup. The missing tables in
Hibernate validation made the failure concrete: the CI database did not receive
all required schema changes.

The fix was straightforward once the source control problem was identified:

- update `.gitignore` so migration SQL files are allowed
- add the missing Flyway migration scripts to Git
- rerun validation pipelines
- confirm local and CI behavior aligned again

The lesson was larger than the patch. CI does not validate the developer's
working directory. It validates the committed repository. If required files
exist only locally, the project has already drifted. That makes `git status`,
tracked-file inspection, and CI parity part of the migration workflow, not
optional cleanup after the fact.

Docker Desktop remediation took a different kind of patience.

The work involved inspecting Docker-related environment variables, clearing
stale references from older Docker Machine / Docker Toolbox style setups,
validating Docker contexts, and manually reinstalling or reconfiguring Docker
Desktop until the local engine and UI agreed again. Eventually the Docker
Desktop UI functionality returned, and the default Docker engine context worked
again.

That mattered because containerized development depends on boring local
reliability. If Docker is unstable, every database-backed test, migration run,
and local service check becomes suspect. Restoring a clean Docker Desktop state
reduced future troubleshooting uncertainty and made the local environment a
better match for the workflows the project is trying to standardize.

Git cleanup closed the loop on repository hygiene.

Stale remote-tracking branches were pruned, merged local branches were deleted,
obsolete feature branches were cleaned up, and local state was synced with the
remote. The goal was not tidiness for its own sake. It was to make the active
work easier to see.

Keeping only active branches locally reduces friction. It makes the repository
easier to navigate, lowers the chance of building from the wrong base, and
supports the same branch discipline that the PR workflow is trying to enforce.

## Definition of Done (DoD)

Day 10 was complete when:

- Java ETL/dashboard platform work continued through phased architecture
  implementation
- feature branches were created, reviewed, and merged into `main` through PRs
- repository hygiene and workflow discipline improved
- migrations and CI pipelines were validated
- branch protection expectations and workflow maturity became stronger
- the Flyway CI migration issue was diagnosed and resolved
- missing SQL migrations were tracked correctly in Git
- `.gitignore` was updated to allow required migration scripts
- validation pipelines were rerun successfully
- local and CI migration behavior aligned again
- Docker Desktop was restored to a stable working state
- stale Docker environment references and context confusion were removed
- the default Docker engine context worked again
- stale remote-tracking branches and obsolete local branches were cleaned up
- local repository state was synced with the remote
- the Day 10 post passed existing Astro and metadata validation

## Key Lessons / Reflections

Local success is useful evidence, but it is not proof of CI parity.

The migration failure was a clear reminder that source control is the true
deployment input. If a file is required for the system to run, it must be
tracked, reviewed, and validated through the same path CI uses. A local database
can hide missing migration files because it has already seen them. A clean CI
database will not be so forgiving.

Repository assumptions are infrastructure.

A broad ignore rule can be just as disruptive as a broken test or bad
configuration value. It changes what the system is allowed to know about itself.
That makes `.gitignore` part of the operational surface, especially in projects
where migrations, generated assets, fixtures, and local data all need different
tracking rules.

Developer environment stability is also part of architecture.

Docker Desktop problems can feel separate from application design, but they
directly affect whether engineers can run the system, validate migrations, debug
services, and trust local feedback. Infrastructure issues can consume more time
than visible feature work, and pretending otherwise does not make the project
move faster.

Git hygiene reduces cognitive load.

Pruning stale branches and deleting merged local work does not change product
behavior, but it changes the working environment. A clean branch list makes the
current state easier to understand and supports better decisions about where new
work should start.

The broader lesson from Day 10 is that invisible infrastructure work is still
real progress. Stable environments, tracked migrations, reliable CI, disciplined
branches, and repeatable PR workflows are what let visible dashboard work happen
without constantly fighting the foundation underneath it.
