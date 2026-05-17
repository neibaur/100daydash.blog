---
title: "Day 15 - May 16, 2026: Operational Rollout and Dependency Governance"
description: "Scaling the domain placeholder rollout across approximately 50 owned domains while validating Cloudflare Pages, DNS, email routing, dependency upgrades, and future automation boundaries."
pubDate: "2026-05-16"
day: 15
dashboardSlug: "none"
status: "published"
tags:
  - cloudflare
  - cloudflare-pages
  - cloudflare-dns
  - email-routing
  - dependabot
  - dependency-governance
  - operational-validation
  - infrastructure-as-code
  - terraform
  - platform-operations
dataSources:
  - name: "Cloudflare Pages"
    url: "https://pages.cloudflare.com/"
  - name: "Cloudflare DNS"
    url: "https://www.cloudflare.com/application-services/products/dns/"
  - name: "Cloudflare Email Routing"
    url: "https://developers.cloudflare.com/email-routing/"
  - name: "Dependabot"
    url: "https://docs.github.com/en/code-security/dependabot"
  - name: "pnpm"
    url: "https://pnpm.io/"
  - name: "GitHub Actions"
    url: "https://github.com/features/actions"
  - name: "ChatGPT"
    url: "https://chatgpt.com/"
  - name: "Google NotebookLM"
    url: "https://notebooklm.google/"
  - name: "Manual operational validation"
    url: "https://developers.cloudflare.com/pages/configuration/custom-domains/"
---

Day 15 was an operations day at real portfolio scale.

No new dashboard was produced today. The work was about taking the domain
placeholder platform that had been validated over the previous few days and
applying it broadly across owned domains. That meant Cloudflare Pages projects,
custom domains, environment variables, DNS hygiene, email routing, smoke tests,
dependency maintenance, and a few careful decisions about what not to automate
yet.

The theme for the day was simple: manual first, automate later.

That is not a rejection of automation. It is a sequencing decision. Before
turning a workflow into Terraform, scripts, or a larger infrastructure system,
I wanted to feel the shape of the workflow by doing it by hand at enough scale
to expose the real repetition, friction, and risk.

## Goal / Intent

The goal was to roll the domain placeholder platform out across approximately
50 owned domains while keeping the operating model clear, observable, and
recoverable.

The placeholder platform already had the basic architecture: a reusable static
site, Cloudflare Pages deployments, deployment-specific public environment
variables, Cloudflare-managed DNS, custom domain attachment, and Cloudflare
Email Routing for simple contact aliases.

Day 15 tested whether that model could survive repetition.

The intent was not only to get pages online. It was to validate the full
operational loop for each domain: create the deployment, configure the settings,
connect the custom domain, add the DNS hygiene records, visit the deployed
site, send a test email to `hello@{domain}`, and confirm the message forwarded
to the monitoring Gmail account.

## Work Performed

The main rollout work was applying the domain placeholder repository to
approximately 50 owned domains.

For each placeholder deployment, I manually created the Cloudflare Pages
project, configured the required environment variables and settings, pointed
the project to the appropriate custom domain, and confirmed that the resulting
site loaded successfully.

I also added a TXT `_dmarc` DNS record for each domain. The goal was not to
claim complete mail deliverability hardening in one pass, but to improve basic
email-domain hygiene while the domains were already being touched for Pages
and Email Routing setup.

The contact path was validated manually as well. For each domain, I sent a
test email to `hello@{domain}` and confirmed that Cloudflare Email Routing
forwarded the message to the monitoring Gmail account. That made the rollout
more than a visual placeholder exercise. Each domain received a basic public
presence and a verified contact path.

In parallel, I handled active dependency governance work. I spun up a dedicated
spike branch to address several Dependabot-flagged updates, upgraded `astro`
to `6.3.3`, `eslint` to `10.4.0`, `vitest` to `4.1.6`, and `lint-staged` to
`17.0.5`, then ran local validation after the upgrades.

After the builds and checks succeeded, I merged the dependency update branch
back into `main`. That resolved the active Dependabot scan findings as part of
the same operational maintenance cycle.

## Challenges / Observations

Manual rollout across dozens of domains is repetitive, but that repetition is
useful when the system is still young.

The repeated Cloudflare Pages setup exposed the actual operating path more
clearly than a diagram would have. It made the required settings, environment
variables, DNS records, custom domain steps, and email-routing checks concrete.
It also made the cost of manual setup visible without immediately jumping to a
tooling answer.

That distinction matters. Automation created too early can preserve a workflow
before the workflow is fully understood. Today, the manual work served as a
learning mechanism. Each deployment was a small rehearsal of the same platform
operation, and the accumulation of those repetitions made the future automation
question more grounded.

The dependency work also mattered because rollout days are exactly when
governance can quietly slip. It would have been easy to ignore Dependabot
alerts while focusing only on Cloudflare setup. Instead, the repository stayed
under active maintenance while the platform expanded. That is the kind of
infrastructure stewardship I want this project to practice: shipping and
maintenance happen together, not in separate worlds.

## Engineering Decisions

The most important engineering decision was to keep the rollout manual for now.

Terraform and broader Infrastructure as Code automation were considered
directly. I spent time ideating with ChatGPT about whether Terraform could
eventually automate Cloudflare Pages setup, DNS configuration, forwarding, and
email-routing setup. That exploration was useful because it clarified the
possible direction without forcing the current repository to absorb the whole
future platform.

The decision was not to expand the current placeholder repository into a
broader Cloudflare automation system right now.

That boundary is intentional. The placeholder repo should remain focused on
the placeholder application and its immediate deployment behavior. If the
Cloudflare setup burden becomes large enough, the better future shape may be a
dedicated Infrastructure-as-Code repository with a clear ownership model,
explicit state management, and stronger migration planning.

For now, operational simplicity wins. The rollout stayed manual so the workflow
could be understood before being abstracted. Terraform remains a possible
future tool, not an obligation created by today's discomfort.

I also decided against pursuing a `.th` or `.in.th` domain today. The domains
were interesting, but the registration path added trustee requirements, extra
cost, complexity, and operational overhead. That was a useful reminder that
experimentation still needs a maintenance budget.

## Operational Validation

The validation work was intentionally hands-on.

Every deployed placeholder site was manually visited to confirm that the page
loaded successfully. That smoke test was basic, but it was the right test for
this stage. The question was whether the domain resolved, Cloudflare Pages
served the deployment, and the placeholder rendered for a real user path.

Email validation followed the same pattern. For each domain, I sent a test
message to `hello@{domain}` and confirmed that Cloudflare Email Routing
forwarded it to the monitoring Gmail account. That verified the operational
contact path domain by domain instead of assuming a configuration pattern would
work everywhere.

The dependency spike also went through local validation before being merged
back into `main`. The point was not only to update package versions. The point
was to make sure the project still built and tested cleanly after the changes,
then close the loop on Dependabot findings with evidence.

## Lessons Learned

Manual work is not always technical debt. Sometimes it is research.

Today made the placeholder platform more real because it passed through the
same operational steps again and again. That repetition built a better mental
model of what the workflow actually requires. It also made the future
automation boundary clearer: automate when the pain is stable, understood, and
worth the additional system surface area.

Dependency governance is part of rollout discipline. A platform can be expanding
and still keep its dependencies current, its alerts resolved, and its local
validation habits intact. That combination is easy to undervalue, but it is
what keeps a small platform from gradually becoming fragile.

I also spent time listening to a Google NotebookLM-generated podcast about
Azure and Infrastructure as Code concepts. That learning fit the day well. The
practical Cloudflare rollout and the IaC concepts reinforced each other: tools
like Terraform are most valuable when they encode a workflow that has already
been made explicit.

The useful restraint today was avoiding premature abstraction. The domain
portfolio is growing, and automation will probably become attractive. But the
system is still better served by a clear manual operating model than by a
premature IaC layer that owns too much before the edges are understood.

## Definition of Done

Day 15 was complete when:

- placeholder pages were created across approximately 50 owned domains
- Cloudflare Pages projects were manually created for the placeholder
  deployments
- required environment variables and project settings were configured
- custom domains were connected to their appropriate deployments
- TXT `_dmarc` DNS records were added for the domains
- every deployed placeholder site was manually smoke-tested
- `hello@{domain}` forwarding was manually validated through Cloudflare Email
  Routing
- test messages were confirmed in the monitoring Gmail account
- operational smoke testing was completed across the deployed placeholder
  portfolio
- `astro` was updated to `6.3.3`
- `eslint` was updated to `10.4.0`
- `vitest` was updated to `4.1.6`
- `lint-staged` was updated to `17.0.5`
- dependency updates were tested and merged back into `main`
- active Dependabot findings were resolved
- Terraform and broader IaC automation were considered and intentionally
  deferred
- future automation was left pending clearer operational need

## Next Steps

The next step is to keep observing the manual operating model as the domain
portfolio evolves.

If the Cloudflare setup burden continues to grow, a dedicated
Infrastructure-as-Code repository may become the right answer. That future
work should start from the real workflow validated here: Pages projects, custom
domains, DNS hygiene, Email Routing, environment variables, smoke tests, and
governance checks.

For now, the platform is still healthier with a smaller surface area. The
manual rollout created the knowledge that future automation would need, and it
did so without expanding the placeholder application beyond its job.
