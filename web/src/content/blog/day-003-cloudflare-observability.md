---
title: "Day 3 - May 4, 2026: From Automation to Observability"
description: "Resolving repository connection hurdles and transitioning infrastructure data into actionable BI insights via Looker Studio."
pubDate: 2026-05-04
day: 3
dashboardSlug: "day-003-cloudflare-observability"
status: "draft"
tags:
  - dashboard
  - platform-engineering
  - cloudflare
  - observability
dataSources: []
---

Day 3 marked a shift from building systems to making them measurable.

The work centered on resolving last-mile deployment friction, restoring a
healthy deployment pipeline, and moving the Cloudflare automation work toward an
observable BI-driven platform. The system had already started to automate and
repair infrastructure drift. The next step was proving what it was doing,
surfacing where it was working, and making the results visible outside the CI
logs.

## Goal / Intent

The goal was to transition the Cloudflare Infrastructure as Code workflow from
automated and self-healing to measurable and observable.

That meant pushing infrastructure audit results into Google Sheets, shaping the
data for Looker Studio, and beginning the first operational dashboard components
for tracking Cloudflare fleet health.

## Platform & Deployment Fixes

Before the observability work could be trusted, the deployment path needed to be
clean again.

Scan and CI issues were creating workflow reliability friction, so the first
step was to troubleshoot the failing checks and confirm which failures were
quality-gate problems versus deployment connectivity problems.

The key deployment issue was that Cloudflare Pages was still tied to an old
GitHub repository that had been deleted. That stale association left the site in
an unclear state: the project existed in Cloudflare, but the deployment source
was no longer a valid repository target.

The fix was to re-establish a clean GitHub connection in Cloudflare and reconnect
Pages to the current `100daydash.blog` repository. Once the repo ownership path
was clear again, the deployment pipeline was restored.

This reinforced three platform requirements:

- Deployment traceability matters. A deployed site needs an obvious source repo,
  branch, and build path.
- Repository ownership must stay unambiguous. Deleted or renamed repositories
  should not remain hidden dependencies in deployment systems.
- CI/CD observability is part of reliability. A passing workflow is useful, but
  knowing what is connected, when it ran, and what it deployed is what makes the
  platform operable.

## Work Completed

#### CI/CD & Automation

The automation controls were tightened around explicit remediation.

Manual remediation now requires dual gating:

- `run_remediation=Y`
- `FIX_DETECTED_GAPS=Y`

That keeps write-enabled repair paths intentional while allowing read-only audit
workflows to run safely on a schedule.

The audit workflow now supports weekly scheduled checks on Sunday UTC, while
Google Sheets synchronization can be triggered on demand with `workflow_dispatch`.
The split is deliberate:

- read-only audit workflows identify current state and drift
- write-enabled remediation workflows require explicit operator intent

#### Data Pipeline & Architecture

The Google Sheets integration moved to a dual-table design:

- `recent` stores the latest snapshot and is overwritten on sync
- `history` stores append-only records for time series analysis

This data shape is intentionally simple. The `recent` sheet supports current
operational views without requiring Looker Studio to calculate the latest record
per domain. The `history` sheet preserves the time series needed for trend
analysis.

Pre-shaping the data upstream avoids complex "latest timestamp" logic in BI and
lets the dashboard support both real-time and historical analytics from the same
pipeline.

#### BI Integration

Looker Studio was connected to both Google Sheets datasets:

- `recent` powers scorecards and the operational domain view
- `history` powers trends and time series analysis

The first calculated fields were added:

- `Compliance Level`, mapping domain state to Pass or Fail
- `Security Configuration`, combining SSL and bot protection signals

The first dashboard components are intentionally basic but useful:

- Fleet Health Scorecard
- domain-level status table

Some early BI friction also surfaced. ISO 8601 timestamps needed careful parsing,
and UTC timestamps had to be treated consistently against local viewing context.
Those issues are manageable, but they confirmed that timestamp modeling should
be solved upstream where possible instead of hidden inside chart configuration.

#### Documentation

Documentation was updated to match the current system behavior.

The README now clarifies workflow triggers, documents the Sheets integration,
and explains the remediation safety controls. That improves onboarding for this
project and makes the Cloudflare workflow easier to reuse across related
projects without rediscovering the same operational rules.

## Key Insights

Pre-shaped data is better than complex BI logic.

Separating snapshot data from historical data simplifies the dashboard model.
The operational view can ask, "What is true now?" while the historical view can
ask, "How is the fleet changing over time?"

Looker Studio's limitations are useful feedback. They reinforce the need to
model data upstream in a way that is easy to query, chart, and explain.

The system is now evolving through a clear platform arc:

```text
Infrastructure as Code -> Self-Healing -> Observable Data Platform
```

## Definition of Done

Day 3 was complete when:

- Cloudflare and GitHub were reconnected through a stable Pages deployment path
- CI/CD workflows were functioning for manual and scheduled execution
- Google Sheets sync was working correctly
- Looker Studio was connected to both `recent` and `history`
- the initial scorecard and domain table were working accurately
- documentation reflected the current workflow behavior

## Next Steps

- Add a time series compliance visualization for the "Hero's Journey" view.
- Track fleet and domain growth over time.
- Add compliance distribution charts.
- Improve dashboard layout, labeling, and visual hierarchy.
- Introduce compliance recovery rate across pre-remediation and
  post-remediation states.
- Start aligning the dashboard narrative with portfolio storytelling.

## Reflection

Day 3 was about moving from building systems to proving they work.

Automation creates leverage, but visibility turns that leverage into something
communicable. The Cloudflare workflow is still early, and the Looker Studio
dashboard is not yet mature, but the shape is now clear: infrastructure state can
be audited, repaired, synced, measured, and explained.
