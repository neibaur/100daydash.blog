---
title: "Day 16 – Portfolio-Scale Domain Rollout and Cloudflare Governance Expansion"
description: "Expanding the domain placeholder platform across the full owned domain portfolio while tightening Cloudflare governance, inventory, and compliance visibility."
pubDate: "2026-05-17"
day: 16
status: "published"
dashboardSlug: "none"
dataSources:
  - "Cloudflare API"
  - "GitHub Actions"
  - "PowerShell"
  - "Google Sheets"
tags:
  - Cloudflare
  - Terraform
  - Infrastructure-as-Code
  - DevOps
  - Governance
  - Automation
---

Day 16 was split between career preparation and operational platform work.

Part of the day went into interview preparation, which made the infrastructure
work feel especially useful. It was not abstract practice. The same themes that
show up in senior platform conversations showed up in the actual work:
repeatable systems, governed infrastructure, inventory clarity, validation
loops, and reducing the gap between "I own this" and "this is operated well."

The practical milestone was moving the domain portfolio from a loose collection
of mostly idle or parked domains into a managed lightweight surface. The
placeholder platform became useful at portfolio scale, and the Cloudflare IaC
governance project continued to serve as the compliance, inventory, and
observability layer around it.

## Goal / Intent

The goal was to finish the portfolio-scale rollout of the
domain-placeholder-platform and bring the full current domain inventory under a
more explicit governance model.

The placeholder platform has a deliberately small job. It gives undeveloped
domains a consistent landing page, a basic ownership signal, a contact path, and
domain-specific messaging without adding a backend, CMS, database, or paid
service.

Day 16 tested whether that simplicity still held when the scope expanded beyond
a few validation domains. The question was no longer whether the platform could
serve a single placeholder page. The question was whether it could become a
repeatable operating surface for a full portfolio of owned domains.

At the same time, the Cloudflare IaC governance workflow needed to keep doing
the larger job around the edges: tracking managed zones, checking Terraform
compliance settings, recording operational state, and making the domain
inventory visible enough to reason about.

## Work Completed

I spent part of the day preparing for interviews and part of the day expanding
the domain portfolio.

Roughly ten additional domains were picked up for future portfolio and project
use. That pushed the work from individual domain setup into portfolio
management. A domain by itself is just an option. A domain with DNS, a landing
page, email routing, inventory tracking, and governance checks becomes part of
an actual platform surface.

I finished setting up all owned domains to use the new
domain-placeholder-platform landing page. Each domain was checked live after
configuration to confirm that the placeholder page rendered correctly and that
the expected secondary language was configured for that specific domain.

I also verified email routing across the portfolio by sending mail to
`hello@{domain}` and confirming that it forwarded successfully into Gmail. That
kept the contact model lightweight while still making each domain reachable.
The result was a meaningful operational shift: the domains moved from idle or
parked assets into a governed set of lightweight landing pages with working
contact paths.

On the governance side, I ran the `cloudflare-iac-governance` workflow with the
variable flags enabled so the workflow could fix and log Terraform compliance
settings into Google Sheets.

Before running the workflow, I manually executed:

```powershell
python run_tools.py --list
```

That PowerShell run produced the JSON zone ID and domain mapping payloads for
the newly added domains. I copied the terminal payload directly into the
`REAL_TFVARS` GitHub secret so the workflow could operate against the expanded
inventory.

That step expanded the managed Cloudflare domain inventory from approximately
50 domains to the full current list of 71 domains.

## Challenges / Decisions

The main decision was to keep the operating model lightweight even while the
domain count grew.

It would be easy to overbuild at this stage: custom admin panels, databases,
domain lifecycle services, contact forms, analytics pipelines, or a heavier
deployment system. None of that was needed to solve the immediate problem. The
better decision was to make the smallest useful platform more complete:
consistent pages, verified routing, centralized email forwarding, and clearer
governance records.

The second decision was to use manual secret preparation as a controlled bridge
instead of pretending the workflow was fully self-discovering. Running
`python run_tools.py --list` locally, collecting the zone mappings, and placing
the JSON payload into `REAL_TFVARS` kept the workflow explicit. It also made the
current boundary clear: discovery and mapping are still partially manual, while
the compliance checks and logging behavior are automated through GitHub
Actions.

That is a reasonable tradeoff for this phase. The system is mature enough to
operate 71 domains consistently, but it is still transparent enough that the
inventory can be reviewed and corrected before automation acts on it.

## Validation / Definition of Done

Validation happened at the domain, email, and governance layers.

For the placeholder platform, each owned domain was checked after rollout to
confirm that the live placeholder page was available and displayed the expected
domain-specific secondary language.

For contact behavior, `hello@{domain}` was tested and confirmed to forward into
Gmail. That verified that the portfolio now has a simple, consistent contact
surface without needing a custom mail service or application backend.

For governance, the Cloudflare IaC workflow was run with the variable flags
enabled. The workflow updated and logged Terraform compliance settings to Google
Sheets using the expanded domain mapping data from `REAL_TFVARS`.

The day was done when the full current portfolio of 71 domains was represented
in the managed Cloudflare inventory, the placeholder landing pages were live,
email routing worked, and the governance workflow had a current set of inputs
for compliance and observability.

## Reflection / Learning

Day 16 made the placeholder platform feel real in a different way.

Earlier work proved that the pattern could function. This work proved that it
could scale across a portfolio without immediately needing a more complicated
architecture. That matters because operational maturity is not always about
adding bigger systems. Sometimes it is about making a small system repeatable,
observable, and boring enough to trust.

The Cloudflare IaC governance project also became more valuable as the domain
count grew. With a handful of domains, inventory can live in memory or in notes.
At 71 domains, governance becomes the thing that keeps the system legible. The
placeholder platform is the visible surface. The governance workflow is the
control layer that makes the surface manageable.

The larger lesson was that portfolio infrastructure needs both sides: a simple
user-facing default and a disciplined operational record behind it. Day 16
connected those pieces more tightly.
