---
title: "Day 0 - May 1, 2026: Building the Dashboard Factory"
description: "Setting up the foundation for 100 dashboards in 100 days."
pubDate: "2026-05-01"
day: 0
dashboardSlug: "day-000-introduction"
status: "draft"
tags:
  - dashboard
  - project-setup
  - astro
  - python
dataSources: []
heroImage: "/media/day-000-introduction/architecture-placeholder.svg"
---

Today is the foundation day for **100daydash.blog**, a public sprint to publish
100 dashboards in 100 days.

The goal is simple: each day should produce a useful data artifact and a short
writeup that explains the question, data source, method, and result. Some days
will be exploratory. Some will be polished. The important thing is that the
workflow stays repeatable enough to survive the full run.

![Architecture placeholder](/media/day-000-introduction/architecture-placeholder.svg)

The project is organized as a small monorepo:

- `web/` contains the Astro site, content collection, layouts, and public media.
- `dashboards/` contains Python dashboard code, tests, data folders, and outputs.
- `scripts/` contains local automation for creating and validating dashboard days.
- `docs/` captures architecture, security, and development notes.

## Hardening the CI/CD Pipeline

The first infrastructure pass focused on keeping the pipeline strict without
making it noisy. Gitleaks false positives were resolved so secret scanning can
stay enabled, CodeQL was upgraded to v4, and the security checks were tuned to
surface useful signals instead of routine lockfile and baseline churn.

## Security Baseline Improvements

The security baseline also now accounts for the UTF-8 encoding issue found
during local scans. Directory exclusions keep `.venv`, lockfiles, and generated
baselines out of repeated scan paths, which keeps feedback fast while preserving
reliable coverage for source, scripts, docs, and dashboard metadata.

## Environment Consistency Across Machines

The development workflow is built around `uv sync` for Python and
`pnpm install` for the Astro site. Running the same setup commands on both the
laptop and desktop keeps the toolchains aligned and helps preserve the current
87% coverage baseline across machines.

The Day 0 dashboard folder lives at
[`dashboards/day-000-introduction`](../../../dashboards/day-000-introduction/README.md).
It is intentionally lightweight: it proves the repo shape, test setup, and static
output flow before the first real data dashboard begins.
