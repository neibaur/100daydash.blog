---
title: "Day 0: Building 100daydash.blog"
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

The Day 0 dashboard folder lives at
[`dashboards/day-000-introduction`](../../../dashboards/day-000-introduction/README.md).
It is intentionally lightweight: it proves the repo shape, test setup, and static
output flow before the first real data dashboard begins.
