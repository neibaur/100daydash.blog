---
title: "Day 0 - May 1, 2026: Building the Dashboard Factory"
description: "Setting up the foundation for 100 dashboards in 100 days."
pubDate: "2026-05-01"
day: 0
dashboardSlug: "day-000-introduction"
status: "published"
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

Before building dashboards, the focus was on hardening the foundation to ensure
the system can scale across 100 consecutive days.

## Hardening the CI/CD Pipeline

The first infrastructure pass focused on keeping the pipeline strict without
introducing unnecessary noise. Gitleaks false positives were resolved so secret
scanning can stay enabled, CodeQL was upgraded to v4, and the security checks
were tuned to surface useful signals instead of routine lockfile and baseline
churn.

![GitHub Actions success](/media/day-000-introduction/github-actions-success.png)

_GitHub Actions quality gates are passing, including tests and linting, which
reinforces the project's coverage and CI goals._

## Security Baseline Improvements

The security baseline also now accounts for the UTF-8 encoding issue found
during local scans. Directory exclusions keep `.venv`, lockfiles, and generated
baselines out of scan paths, which keeps feedback fast while preserving reliable
coverage for source, scripts, docs, and dashboard metadata.

## Environment Consistency Across Machines

The development workflow is built around `uv sync` to manage the Python
environment and `pnpm install` to manage Astro and frontend dependencies.
Running the same setup commands on both the laptop and desktop prevents "works
on my machine" drift and helps preserve the current 87% coverage baseline
across machines.

![Cloudflare Pages deployment](/media/day-000-introduction/cloudflare-pages-deployment.png)

_The site is successfully deployed through Cloudflare Pages, matching the
local-first workflow with a static deployed target._

The Day 0 dashboard folder lives at
[`dashboards/day-000-introduction`](../../../dashboards/day-000-introduction/README.md).
It is intentionally lightweight: it proves the repo shape, test setup, and static
output flow before the first real data dashboard begins.

Coverage and reproducibility are treated as first-class constraints from Day 0.

### Definition of Done (Day 0)

- Daily dashboard creation is repeatable through local scaffolding and metadata
  validation.
- CI/CD quality gates cover formatting, linting, tests, security scans, and
  static site builds.
- Local laptop, desktop, and deployed environments remain reproducible from the
  same dependency files and setup commands.
