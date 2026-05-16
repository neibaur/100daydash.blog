---
title: "Day 11 - May 12, 2026: Full-Stack Analytics Platform and Runtime Hardening"
description: "Documenting the day Tech Talent Pulse evolved from backend analytics APIs into an early full-stack analytics platform with orchestration, advanced analytics, Astro dashboard visualization, and local runtime hardening."
pubDate: "2026-05-12"
day: 11
dashboardSlug: "day-011-full-stack-analytics-platform-runtime-hardening"
status: "published"
tags:
  - analytics-platform
  - astro
  - spring-boot
  - java
  - postgres
  - react
  - recharts
  - runtime-debugging
  - dashboard
dataSources:
  - name: "Spring Boot"
    url: "https://spring.io/projects/spring-boot"
  - name: "Astro"
    url: "https://astro.build/"
  - name: "React"
    url: "https://react.dev/"
  - name: "Recharts"
    url: "https://recharts.org/"
  - name: "PostgreSQL"
    url: "https://www.postgresql.org/"
---

Day 11 produced an early working dashboard.

The important shift was that Tech Talent Pulse no longer felt like only a
backend analytics service. By the end of the day, the project had a Java 21 and
Spring Boot backend ingesting public technology ecosystem signals, persisting
analytics-ready metrics in PostgreSQL, exposing recruiter-friendly APIs, and a
working Astro dashboard on localhost that could summarize and visualize those
backend responses.

It is still early phase, but it is a real dashboard artifact. The frontend now
captures backend analytics data, handles runtime states, and turns the API
responses into metric cards and charts. The project feels more like a small
internal engineering analytics platform than a tutorial CRUD application.

## Goal / Intent

The goal was to close out the next major platform arc for Tech Talent Pulse by
moving through Phases 6, 7, 8, and 9:

- make local demo startup reproducible
- add operational orchestration around ingestion and transformation workflows
- expose advanced analytics that are useful to recruiters and portfolio viewers
- build the first Astro frontend dashboard layer
- debug the real runtime issues that appear when backend APIs and browser
  dashboards finally meet

This was not just about adding endpoints or charts. The intent was to make the
system more operable, observable, explainable, and demo-ready.

## What I Built

Phase 6 focused on demo workflow and operational stabilization.

I added demo profile support, demo data seeding, and a more reproducible local
runtime path. That included hardening datasource configuration, resolving
invalid JDBC URL startup failures, and fixing nested Spring datasource
placeholders that were resolving literally instead of falling back to usable
defaults.

The lesson was direct: environment defaults and fallback handling are critical
for reproducible local onboarding. A demo profile is only useful if someone can
start the project without understanding every internal configuration trap first.

Phase 7 added operational orchestration and observability.

The backend gained orchestration workflows, ingestion and transformation
pipeline endpoints, operational history APIs, orchestration DTOs and services,
and structured workflow statuses. A `smoke-local-demo.sh` validation script
helped turn local startup into a repeatable operational check instead of a
memory exercise.

That phase also clarified a key product behavior: empty-but-valid data states
must be distinguished from application failures. A system with no new public
signals is not the same thing as a broken pipeline. The API and operational
history need to make that distinction visible.

Phase 8 added advanced analytics.

The analytics layer now supports trend delta analytics, rising technology
analytics, tag comparison analytics, bounded historical comparison APIs,
deterministic sorting, and rank movement calculations. The responses are shaped
for recruiter-friendly charting rather than raw backend inspection.

The main analytics concepts were signal deltas, percent change, rank movement,
rising technologies, bounded 30-point comparison history, and UTC-normalized
analytics snapshots. Those details matter because analytics APIs need to be
stable enough for a dashboard to render, explain, and compare consistently.

Phase 9 turned the platform toward frontend visualization and runtime
hardening.

I added an Astro 6 frontend foundation with TypeScript support, React island
architecture, Recharts visualizations, environment-based API configuration,
loading states, error states, empty states, formatted metric cards, explanatory
analytics help text, semantic accessibility improvements, and friendlier
backend-offline handling.

The dashboard layout also improved: better hierarchy, clearer recruiter/demo
UX, more readable charts, and stronger separation between summary metrics,
trend movement, and comparison history.

## Technologies Used

The main stack for the day was:

- Java 21
- Spring Boot
- PostgreSQL
- Docker Compose
- Maven
- Astro 6
- TypeScript
- React islands
- Recharts
- browser DevTools

The broader work combined backend platform engineering, analytics API design,
frontend dashboard implementation, local environment debugging, and operational
validation.

## Challenges / Blockers

The first major blocker was a React and Astro hydration failure.

The frontend shell loaded, but the dashboard stayed stuck on "Loading
analytics." At first glance, that looked like a backend availability problem.
The surprising clue was in DevTools: no Fetch or XHR requests appeared at all.

That changed the investigation. If no network requests appear, the frontend
runtime may be failing before the API fetch logic ever executes.

The console exposed the root problem:

```text
react-dom/client.js did not provide createRoot
```

The issue was not that the backend was offline. The React island was not
hydrating correctly, so the dashboard code never reached the point where it
could call the API.

The second major blocker was local CORS behavior.

The dashboard worked on `localhost`, then failed on `127.0.0.1`. The browser
returned `403 Forbidden` with a missing `Access-Control-Allow-Origin` header.
That looked inconsistent until the origin model became the center of the
debugging session.

`localhost` and `127.0.0.1` are separate browser origins. Local development can
look broken even when both addresses reach the same machine because the browser
does not treat them as the same trusted caller.

## Solutions / Work Performed

For the hydration issue, I investigated the Astro and React island runtime path
instead of staying focused only on backend availability. Once the missing
network traffic made sense as a frontend runtime failure, the fix was to correct
the frontend hydration and runtime integration, verify the React island mounted
correctly, and confirm that API requests began executing.

The lesson was useful: missing network activity can indicate frontend hydration
failure, not backend downtime.

For the CORS issue, I hardened the local-development CORS configuration without
weakening production assumptions.

The relaxed behavior was scoped to demo and development Spring profiles. The
configuration now supports `localhost` and `127.0.0.1` on ports `4321` and
`4322`, preserves environment variable override support, and avoids wildcard
production CORS.

That balance matters. Local dashboards should be easy to run, but production
configuration should not become permissive just because development needed a
more flexible origin list.

The operational work also included repeated validation through:

- `mvn clean verify`
- `docker compose config`
- `pnpm astro check`
- `pnpm run build`
- runtime API verification
- browser DevTools validation
- CORS preflight verification
- React hydration validation

The validation loop was intentionally layered. Build success alone would not
prove the browser could hydrate. API success alone would not prove the frontend
could fetch. CORS preflight success alone would not prove charts rendered.
Putting those checks together gave a more realistic view of whether the system
actually worked as a full-stack local demo.

## Key Discoveries

Environment fallback behavior is product behavior.

If a local demo profile fails because placeholders resolve literally or a JDBC
URL is invalid, the project has an onboarding problem, not just a configuration
problem. Reproducibility begins at startup.

Operational APIs need to explain the difference between no data and broken
systems.

An empty ingestion result can be valid. A failed ingestion result is different.
The orchestration layer needs statuses, history, and workflow visibility so
users can tell whether the system is quiet, complete, partial, or failing.

Analytics APIs become easier to visualize when they are chart-ready by design.

Deterministic sorting, bounded history, UTC-normalized snapshots, rank movement,
signal deltas, and percent change are not frontend details. They are API design
decisions that make the frontend more trustworthy and easier to explain.

Frontend silence can be misleading.

When a dashboard is stuck loading and no network requests appear, the backend
may not be involved yet. Hydration can fail before fetch logic runs. Browser
DevTools are useful because they show both halves of that story: console runtime
errors and network activity.

Localhost is not one origin.

`localhost` and `127.0.0.1` feel interchangeable to a developer, but they are
not interchangeable to the browser. Local CORS configuration needs to reflect
the way people actually run and test the project.

## Definition of Done

Day 11 was complete when:

- demo profile support existed for the backend
- demo data seeding supported reproducible local startup
- datasource configuration handled local defaults more reliably
- invalid JDBC URL startup failures were resolved
- nested Spring datasource fallback placeholders behaved correctly
- orchestration workflows and pipeline endpoints were available
- operational history APIs exposed workflow state
- orchestration DTOs and services supported structured responses
- `smoke-local-demo.sh` provided a repeatable local validation path
- empty-but-valid data states were separated from application failures
- trend delta analytics were available
- rising technology analytics were available
- tag comparison analytics were available
- bounded historical comparison APIs were available
- analytics responses supported recruiter-friendly charting
- deterministic analytics sorting and rank movement calculations were added
- Astro 6, TypeScript, React islands, and Recharts formed the frontend base
- loading, error, empty, and backend-offline states were handled in the UI
- metric cards, chart readability, hierarchy, and accessibility improved
- React island hydration was fixed and verified
- API requests executed from the dashboard
- local CORS supported expected development origins without wildcard production
  behavior
- backend APIs and frontend dashboard behavior were validated together

## Current State

Tech Talent Pulse now has an operational backend analytics platform, a
functional frontend visualization layer, a recruiter/demo workflow,
orchestration tooling, advanced analytics APIs, frontend/backend runtime
integration, and a reproducible local operational workflow.

The project has crossed an important line. It is no longer only a service that
can compute interesting metrics. It is becoming a platform that can run,
explain itself, surface operational state, and present analytics through a
dashboard someone can actually inspect.

## What Comes Next

The likely next phase is Phase 10: deployment preparation.

That probably means hosted deployment strategy, production profiles, deployment
documentation, hosted PostgreSQL planning, environment separation,
production-safe configuration, architecture diagrams, portfolio screenshots,
and hosted frontend/backend integration.

The next challenge is to preserve the local reliability gained today while
introducing hosted runtime complexity carefully. The dashboard now exists. The
next step is making it presentable, portable, and safe outside localhost.
