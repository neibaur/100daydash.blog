---
title: "Day 17 – May 18, 2026: Discoverability, Navigation, and Domain Strategy Governance"
description: "Improving journal discoverability with search and navigation while using domain portfolio review as a platform strategy and governance exercise."
pubDate: "2026-05-18"
day: 17
dashboardSlug: "none"
status: "published"
dataSources:
  - "Astro Content Layer"
  - "Vanilla JS"
  - "OpenAI ChatGPT"
  - "Google Gemini"
tags:
  - platform-engineering
  - developer-experience
  - search
  - domain-strategy
  - governance
---

Day 17 focused on discoverability, navigation, and portfolio strategy rather
than a new visual dashboard.

The work continued the pattern that has emerged across the project: small,
operationally grounded platform improvements that make the system easier to
maintain, easier to read, and easier to extend. As the number of journal entries
continues to grow, the site needs to behave less like a short chronological log
and more like a searchable operational knowledge base.

## Goal / Intent

The goal was to improve how readers and future maintainers move through the
100daydash.blog journal while also using domain portfolio planning as a
technical product strategy exercise.

The journal is still chronological by design. That is useful for showing the
sequence of work. But chronological order alone becomes less useful as the
archive grows. If a reader wants to find work related to Terraform, Cloudflare,
Kubernetes, CI/CD, or platform governance, they should not need to open entries
one by one and rely on browser search.

The intent was to preserve the static-site model while adding enough
discoverability to make the archive more usable. That meant build-time indexing,
published-only content filtering, and lightweight client-side keyword matching
instead of adding a search service, backend API, or single-page application
framework.

A secondary goal was career and portfolio calibration. The day included
reflection after an initial Cloud Engineer screening conversation and a
structured review of a personal domain portfolio. Both activities were treated
as platform governance exercises: mapping current technical assets and skills
against future operating requirements.

## Challenges Encountered

The main content platform challenge was scope control.

Search can become complicated quickly. Fuzzy matching, highlighting, ranking,
pagination, facets, tags, and external indexing services are all plausible
future improvements. None of them were required for the current site. The
immediate need was simpler: make published entries searchable by keyword without
changing the hosting model or increasing operational overhead.

The second challenge was information architecture. Previous and next navigation
helps readers move sequentially, but it does not solve topic discovery. Search
solves a different problem. The two features needed to work together: navigation
for reading flow, search for retrieval.

The career reflection also required careful framing. An initial screening
interview for a Cloud Engineer role at Children's Healthcare of Atlanta
indicated that the organization was seeking a more senior cloud engineering
profile, especially with deeper enterprise cloud infrastructure experience. The
useful response was not to treat that as a binary outcome. It was an operational
platform calibration exercise: compare enterprise cloud topology expectations
against current platform benchmarks and identify strategic technical backlog
items.

The domain review had a similar risk. A large domain portfolio can easily become
domain collecting rather than product strategy. The work needed to separate
active development candidates from names that may not justify future renewal
costs.

## Solutions / Work Performed

### Career And Technical Reflection

The Cloud Engineer screening conversation was used as a calibration point.

The strongest current signals remain platform engineering, automation,
governance, CI/CD, repository standards, and Infrastructure as Code. Those areas
show up repeatedly in the work behind this project and related Cloudflare
governance efforts.

The growth area is deeper enterprise cloud operations experience: larger cloud
topologies, production operational patterns, multi-environment governance,
networking depth, organizational controls, and cloud infrastructure ownership at
greater scale.

That gap was captured as a technical backlog rather than a personal judgment.
The practical next step is to keep strengthening the portfolio around cloud
architecture, IaC governance, operational runbooks, policy-as-code patterns,
observability, and cost-aware infrastructure design.

### Domain Portfolio Strategy And Prioritization

I used both ChatGPT and Gemini to evaluate and organize a large personal domain
portfolio from multiple angles.

The review considered engineering portfolio potential, SaaS and dashboard
branding, global audience reach, Thai-language and Mandarin-language branding
possibilities, developer tooling concepts, gamified education ideas, long-term
monetization, and SEO.

The point was not simply to admire a list of domains. The work was portfolio
governance. Each domain was evaluated against naming quality, memorability,
radio-test clarity, international usability, product fit, and likely renewal
value.

Several strategic themes emerged:

- developer education
- dashboard and analytics platforms
- gamified scripting and terminal learning
- localized technical learning surfaces
- lightweight SaaS or tooling concepts
- long-term portfolio sites with clear brand intent

The result was a clearer distinction between domains that deserve active
development attention and domains that may not justify future renewal costs.
That is product strategy work: reducing option sprawl, preserving strong naming
assets, and aligning future build effort with realistic audience and technical
positioning.

### 100daydash.blog Platform Improvements

The site received three platform-oriented improvements.

First, previous and next entry navigation was added to published journal posts.
That makes the archive easier to read sequentially and improves movement across
daily entries without relying on the home page as the only way back into the
timeline.

Second, Markdown formatting in the Day 2 entry was cleaned up so repository
names render consistently. This was intentionally small and limited to content
presentation rather than historical metadata changes.

Third, keyword search was implemented for published journal entries. The new
search page uses Astro's Content Layer through `getCollection("blog")`, filters
entries to `status === "published"` at build time, and renders a small search
index into the static page. A vanilla JavaScript script then performs
case-insensitive keyword matching in the browser.

The searchable fields are intentionally practical: title, description, content
slug, dashboard slug, and stripped Markdown body text. This supports searches
for terms such as Terraform, Cloudflare, Kubernetes, and CI/CD while keeping the
implementation small.

The important architectural decision is that indexing happens during static
site generation, while filtering happens client-side against a prebuilt index.
That keeps the site compatible with static hosting and avoids external search
services, server-side infrastructure, or heavier client framework overhead.

## Technical Observations / Reflection

Day 17 was a reminder that publishing systems become knowledge systems over
time.

At the beginning of a project, a chronological journal is enough. There are only
a few posts, and the newest work is easy to find. By Day 17, the archive already
contains enough platform decisions, debugging notes, governance patterns, and
implementation details that discovery matters.

Search changes the archive from a read-only timeline into an operational
reference surface. It lets the site answer questions like: where did Terraform
come up, when did Cloudflare governance expand, which entries mention CI/CD,
and what work touched static-site infrastructure?

The implementation also fits the project philosophy. Static-site generation is
still doing the heavy lifting. Astro builds the content and emits a small index
from published entries only. The browser handles simple keyword filtering. That
combination improves usability while preserving the low-cost, local-first,
static delivery model.

The domain portfolio work followed the same pattern at a higher level. A domain
portfolio is only useful if it can be governed. The strategic value comes from
knowing which assets support future products, which names communicate clearly,
which concepts have international usability, and which assets should be allowed
to expire rather than carrying invisible maintenance cost.

The career reflection also became more concrete through this lens. Enterprise
cloud depth is not a vague aspiration. It can be decomposed into architecture,
operations, governance, networking, automation, observability, security, and
cost control. That turns a screening signal into an actionable platform
learning backlog.

## Definition of Done (DoD)

Day 17 was complete when:

- the journal had a dedicated keyword search page for published entries
- search indexing was generated from Astro content at build time
- draft and unpublished entries were excluded from the searchable index
- client-side matching worked without adding a framework or search service
- previous and next navigation improved sequential reading across journal posts
- the Day 2 Markdown formatting correction was kept small and content-only
- the domain portfolio review produced clearer development and renewal
  priorities
- the career screening reflection was translated into an enterprise cloud
  growth backlog
- repository validation, type checking, and static build checks remained clean

The work moved 100daydash.blog one step further from a simple chronological
engineering journal toward a searchable platform knowledge base.
