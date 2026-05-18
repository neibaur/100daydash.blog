---
title: "Day 4 - May 5, 2026: Reusing Platform Infrastructure to Launch a Production Portfolio Site"
description: "Documenting the platform engineering work behind adapting, hardening, and deploying a reusable Hugo portfolio architecture for a production client site."
pubDate: "2026-05-05"
day: 4
dashboardSlug: "day-004-portfolio-platform-reuse"
status: "published"
tags:
  - platform-engineering
  - ci-cd
  - cloudflare
  - github-pages
dataSources: []
---

Day 4 did not produce a dashboard.

The engineering work went into cloning, reworking, polishing, and deploying a
production portfolio site for a real end user. The site began as a reusable
Hugo-based portfolio architecture and was adapted into an accounting and
bookkeeping-focused professional portfolio for my wife.

That made the day less about portfolio content and more about platform reuse:
could an existing static-site deployment architecture be forked, governed,
themed, secured, and launched without turning into a one-off snowflake?

## Goal / Intent

The goal was to validate that a reusable portfolio platform could move from one
project context into another while preserving engineering rigor.

The work covered:

- Hugo Blox theming and configuration
- Hugo static site generation
- Markdown and YAML-driven content
- pnpm-based frontend dependency management
- Node runtime standardization
- GitHub Actions deployment workflows
- GitHub Pages hosting
- Cloudflare DNS and domain management
- secure deployment secret handling
- branded email routing

The result was a practical platform engineering exercise: reuse the architecture,
customize the product surface, harden deployment, troubleshoot production
infrastructure, and document what should be portable next time.

## Framework / Architecture

The portfolio used Hugo Blox, formerly Wowchemy, on top of Hugo static site
generation. Content remained mostly Markdown and YAML-driven, which kept the
site portable and easy to review in Git.

The deployment architecture separated source development from production
publishing:

```text
development repository
  -> GitHub Actions build workflow
  -> deployment repository
  -> GitHub Pages
  -> Cloudflare-managed custom domain
```

That separation matters because the source repository can retain development
history, branches, configuration, and authoring workflows while the deployment
repository remains a static publishing target.

## Standardized Tooling and Environment Parity

Part of the validation was making sure the portfolio architecture stayed
portable across projects.

The frontend workflow used pnpm for dependency management and a standardized
Node runtime so local development, CI, and deployment did not drift from each
other. That is especially important for reusable site templates because small
differences in package managers, lockfiles, or runtime versions can turn a
simple fork into a debugging session.

The objective was not just to make the site build once. The objective was to
make the development experience repeatable:

- dependencies install from a committed lockfile
- local builds match CI builds
- Node versions are explicit instead of implied
- reusable templates keep the same project ergonomics after cloning
- "works on my machine" drift is reduced before deployment

That same discipline applies to `100daydash.blog`. Rapid delivery depends on
boring, reproducible setup steps. A reusable platform is only reusable if the
next project can inherit the same working environment.

## Content and Theme Rework

The cloned portfolio was heavily reworked from a technical engineering portfolio
into an accounting and bookkeeping-focused professional site.

The homepage required the largest content shift. Hero and about sections were
rewritten around accounting, bookkeeping, tax-readiness, reliability, and
recruiter-oriented presentation. Calls to action were revised so the site felt
like a professional profile rather than a software engineering project archive.

The author profile was also rebuilt:

- biography updated for the intended end user
- accounting education represented accurately
- bookkeeping and tax preparation experience emphasized
- skills and metadata revised
- resume integration updated

The project sections were stripped of technical engineering examples and
repositioned around accounting, bookkeeping, and tax-readiness work. That
content change was important because reusable infrastructure should not leak the
old site's identity into the new one.

Metadata received the same treatment:

- branding updates
- SEO and social metadata
- base URL changes
- OpenGraph alignment
- CNAME handling

Those changes are operational, not cosmetic. Static sites are often deployed
through simple pipelines, but incorrect metadata, stale base URLs, or mismatched
CNAME settings can create broken previews, incorrect canonical URLs, and
confusing production behavior.

## Dark Mode Debugging

The most detailed frontend debugging work came from dark mode.

The cloned theme had light-mode overrides that were too broad. Some selectors
used `:not(.dark)` in a way that did not reliably scope styles to the root HTML
state. Those rules collided with dark-mode styling and caused heading contrast
issues. The result was a site that looked acceptable in light mode but had
inconsistent accessibility and readability in dark mode.

The problem came down to CSS specificity and theme-state targeting:

- light-mode overrides affected elements that should have inherited dark-mode
  colors
- `:not(.dark)` selectors did not consistently express the intended root state
- headings had contrast problems against dark backgrounds
- palette behavior varied between sections

The fix was to make the theme-state boundary explicit by refactoring selectors
toward `html:not(.dark)`. That kept light-mode overrides tied to the document
state instead of allowing them to leak into dark-mode surfaces.

The palette handling was also standardized so heading, body, and link colors
behaved consistently across both modes. This was less about choosing better
colors and more about making the theme predictable. Accessibility problems often
come from inconsistent state rules rather than a single bad color token.

## Deployment Architecture

Deployment used GitHub Actions to build the Hugo site and publish the static
output to a deployment repository served by GitHub Pages.

The production path had several moving parts:

- source repository for development and review
- deployment repository for static output
- GitHub Actions CI/CD workflow
- deployment authentication through a GitHub secret
- personal access token management
- GitHub Pages hosting
- Cloudflare DNS management
- HTTPS enforcement
- CNAME alignment

The authentication boundary was important. Deployment credentials were handled
through GitHub Secrets rather than committed configuration. That kept the public
site repository clean and made the deployment workflow easier to rotate or
replace later.

## DNS and Infrastructure Troubleshooting

The production launch required the usual last-mile DNS work.

Cloudflare and GitHub Pages needed to agree on the custom domain target, CNAME
state, and HTTPS behavior. During deployment, the main issues were propagation
delay, incorrect DNS target troubleshooting, GitHub Pages custom-domain
verification, and SSL issuance timing.

This is where static hosting can look deceptively simple. The build may pass,
the repository may publish, and the domain may still fail until DNS, Pages, and
certificate state converge.

The operational lesson was to debug the path in layers:

- confirm the GitHub Actions build and publish step
- confirm the deployment repository received the generated site
- confirm GitHub Pages saw the expected custom domain
- confirm Cloudflare pointed at the correct target
- wait for DNS propagation where appropriate
- verify HTTPS once certificate issuance completed

That layered approach keeps DNS troubleshooting from becoming guesswork.

## Branded Email Routing

The site launch also included branded email routing through Cloudflare.

The route forwards `joy@kamolwan.com` to Gmail, giving the portfolio a branded
contact address without introducing a full mail-hosting stack. The setup still
required operational care around Cloudflare email routing, MX records, SPF and
DKIM considerations, and the Gmail verification workflow.

Email routing is easy to treat as a small finishing step, but it is part of the
production surface. A portfolio contact path needs to be trustworthy, routable,
and documented enough that it can be repaired later.

## Branching and Engineering Workflow

The implementation followed a safer development flow instead of editing
production directly.

Changes moved through a development branch, pull request review into `main`, and
production deployments tied to `main`. That kept experimentation away from the
production path and preserved a clear promotion boundary.

This is the same workflow expectation that supports `100daydash.blog`:

- short-lived branches for changes
- pull requests for reviewable diffs
- `main` as the production deployment source
- CI/CD checks before promotion
- repeatable rollback and redeploy paths

For a small portfolio, that may sound heavy. In practice, it keeps small sites
from accumulating hidden operational risk.

## Governance Portability

One of the more important lessons was that reusable projects should fork
governance alongside code.

The site architecture was not the only thing worth carrying forward. Operational
standards also needed to move with it:

- AGENTS.md reuse and adaptation
- preserved engineering conventions
- consistent CI/CD expectations
- repository safety rules
- branch and deployment discipline
- documentation expectations

Forking governance alongside infrastructure helps derivative projects inherit
the habits that made the original platform maintainable. Otherwise, the copied
site may keep the theme and deployment workflow but lose the rules that made
future changes safe.

## Security and Repository Safety

Cloned and repurposed repositories require deliberate secret hygiene.

Before treating the new site as public-facing production, the repository needed
to be checked for anything that should not survive the fork:

- legacy secrets
- personal metadata from the source project
- deployment credentials
- stale environment configuration
- old URLs and identity references

Deployment authentication was handled through GitHub Secrets and personal access
token management rather than static files. The repository history and working
tree were treated as part of the security surface, not just the final generated
site.

The mindset mirrors the Gitleaks and security scanning standards used here:
reusable workflows should make it harder to accidentally publish credentials,
old configuration, or private operational context.

## Transferable Engineering Concepts

Day 4 maps directly back to the dashboard platform.

The work reinforced several concepts that matter for any rapid delivery system:

- reusable deployment architecture reduces launch friction
- dev and deployment repo separation keeps source workflows clean
- CI/CD reliability is part of the product
- secrets management has to be designed before production
- branch discipline enables safer experimentation
- environment isolation prevents local tool drift
- Cloudflare infrastructure is portable when DNS, SSL, and routing are explicit
- frontend stability depends on testing stateful theme behavior
- operational debugging works best when each layer is verified independently

This was not a dashboard day, but it was a platform day. It validated that the
same infrastructure instincts behind `100daydash.blog` can support another
production static site.

## Definition of Done

Day 4 was complete when:

- production site deployed successfully
- custom domain resolved through Cloudflare
- GitHub Actions deployments functioned from the source workflow
- deployment repository received the generated static site
- dark mode contrast and selector issues were resolved
- resume and portfolio content aligned with the intended accounting profile
- SEO, social metadata, base URL, and CNAME settings were updated
- HTTPS was enabled
- branded email routing to Gmail was operational
- deployment credentials were handled through GitHub Secrets
- public-facing repository content was checked for stale secrets or source
  project metadata
- deployment workflow was documented and repeatable

## Reflection

Day 4 was a reminder that platform engineering is often invisible until it
fails.

A polished static site depends on more than theme edits. It depends on runtime
parity, clean repository boundaries, secure deployment credentials, DNS
correctness, accessible frontend states, and operational discipline.

That work is foundational to the 100-day project. Sustainable rapid delivery
does not come from moving fast once. It comes from building systems that can be
reused, debugged, and trusted on the next launch.
