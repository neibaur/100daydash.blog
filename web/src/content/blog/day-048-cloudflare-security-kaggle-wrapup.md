---
title: "Day 48 - June 18, 2026: Hardening the Edges While Finishing the Vibe Coding Course"
description: "A Day 48 reflection on Cloudflare edge hardening, Cloudflare Pages migration, pnpm security troubleshooting, and finishing Days 4 and 5 of the Kaggle Google vibe coding coursework."
pubDate: "2026-06-18"
day: 48
dashboardSlug: "none"
dataSources:
  - "Cloudflare Security Insights notes"
  - "Cloudflare Pages migration notes"
  - "pnpm troubleshooting notes"
  - "Vibe Coding Agent Security and Evaluation whitepaper"
  - "Spec-Driven Production Grade Development in the Age of Vibe Coding whitepaper"
  - "Kaggle Google vibe coding Day 4 codelabs"
  - "Kaggle Google vibe coding Day 5 codelabs"
status: "published"
tags:
  - ai-agents
  - vibe-coding
  - agentic-engineering
  - cloudflare
  - security
  - dependency-governance
  - pnpm
  - google-antigravity
  - production-readiness
---

Day 48 was about turning rough edges into governed surfaces.

That sounds cleaner than the day felt. In practice it meant bouncing between
Cloudflare Security Insights, `security.txt`, redirect rules, stale GitHub
Pages DNS records, a misleading pnpm lockfile failure, and the final two days
of the Kaggle / Google vibe coding coursework.

The common thread was not glamour. It was control.

Every warning, redirect, lockfile mismatch, and codelab pointed back to the
same lesson: agentic development only becomes useful when the surrounding
surfaces are explicit. Domains need disclosure paths. Preview environments
need different expectations than production domains. Package managers need
repo-local boundaries. Agents need specs, identity constraints, evaluation,
and review.

The day was not five disconnected chores. It was one long pass over the edges
where loose assumptions become operational risk.

## Cloudflare Security Insights

The first part of the day was a practical Cloudflare hardening pass across my
personal and portfolio domains.

I kept working through the remaining Security Insights warnings around
`security.txt`, AI bot protections, crawler controls, AI Labyrinth-style
recommendations, and the difference between production custom domains and the
Cloudflare-provided preview or system domains that sit behind them.

That distinction mattered more than I expected.

Production zones such as `foundegg.com` already had the intended bot
protections enabled. But `.workers.dev` and `.pages.dev` domains can still
surface their own Cloudflare warnings because they do not inherit every custom
zone setting. That makes the dashboard noisy unless the environment boundary
is understood.

Some warnings deserved remediation. Others were acceptable or dismissible once
the production hostname was already hardened and the warning applied to a
development or preview surface.

That is the quiet work of security dashboards: separate the real exposure from
the scanner-shaped residue.

The `security.txt` work had the same shape.

For `isaacneibaur.com`, I added or corrected
`/.well-known/security.txt`. The served file already carried the important
intent:

- `Contact`
- `Preferred-Languages`
- `Canonical`

Then validation made the missing part obvious. A strict `security.txt` file
also needs a future `Expires` field. Without that, the site can serve a file
that looks reasonable to a human but still fails validation.

There was also a Cloudflare-specific nuance. A dashboard insight may be
checking whether Cloudflare's native edge-managed `security.txt` feature is
enabled, not only whether the repository serves a valid file at the expected
path. That is a different question. The site can have a valid file and the
Cloudflare insight can still be pointing at an edge configuration feature.

The redirect side had its own version of the same lesson.

For `neibaur.me`, the domain redirects to `isaacneibaur.com`. That is fine,
but `security.txt` only works if the redirect preserves the path. The important
request is not just:

```text
https://neibaur.me
```

It is:

```text
https://neibaur.me/.well-known/security.txt
```

That needs to land at:

```text
https://isaacneibaur.com/.well-known/security.txt
```

So the redirect rule needs subpath matching and path suffix preservation. A
root-only redirect is not enough. The disclosure path is part of the contract.

None of this is exciting work in the launch-day sense. But it turned vague
dashboard warnings into concrete decisions about edge routing, bot posture,
preview-domain expectations, and vulnerability disclosure metadata.

## Cloudflare Pages Migration

The second infrastructure thread was moving more portfolio and static sites
away from GitHub Pages hosting and onto Cloudflare Pages.

That migration is easy to summarize badly as "the site deploys." The real
work is more specific than that:

- Cloudflare Pages project setup
- GitHub repository connection
- build command and output directory configuration
- environment variables
- custom domains
- DNS cleanup
- canonical hostname decisions
- redirects from legacy hostnames

For Hugo-based sites, Cloudflare Pages needed explicit runtime configuration,
including `HUGO_VERSION` and `GO_VERSION`. That is the kind of small platform
assumption that only becomes visible when a site moves from one host to
another.

I got `isaacneibaur.com` successfully running on Cloudflare Pages. Then the
DNS review surfaced the next bit of hidden legacy state: the apex domain
pointed at the Cloudflare Pages deployment, while `www.isaacneibaur.com` still
pointed at the old `neibaur.github.io` GitHub Pages target.

That forced a canonical-host decision.

The two reasonable options were:

- let Cloudflare Pages handle both apex and `www`
- use a cleaner `www` to apex redirect

I leaned into the redirect model. Cloudflare has a "Redirect from www to root"
template that fits this well, and a single wildcard-style redirect rule can
cover both:

- `www.isaacneibaur.com` to `isaacneibaur.com`
- `www.kamolwan.com` to `kamolwan.com`

The DNS detail matters: redirect rules only work if the `www` records are
proxied through Cloudflare. If the stale `www` CNAME is still DNS-only or still
pointing directly at GitHub Pages, the rule will not get a chance to run.

That was the bigger migration lesson. Moving hosting is not just a successful
deployment. It is stale DNS records, canonical hostnames, redirect behavior,
preview domains, edge settings, and old assumptions that continue to exist
until they are actively removed.

## pnpm And Dependabot

The dependency thread started as a Dependabot or security scan failure in Hugo
and pnpm-based portfolio repositories, including:

- `isaacneibaur-portfolio-platform`
- `kamolwan-portfolio-platform`

The first failure looked direct:

```text
ERR_PNPM_LOCKFILE_MISSING_DEPENDENCY
Broken lockfile: no entry for 'markdown-it@14.2.0' in pnpm-lock.yaml
```

The tricky part was that the lockfile appeared to include
`markdown-it@14.2.0`.

The missing piece was not the package entry. It was the matching `snapshots:`
entry. That is a wonderfully annoying kind of failure because a quick text
search can make the file look correct while the lockfile is still structurally
broken for pnpm's frozen install mode.

Local debugging made it worse.

On my machine, pnpm was resolving against a parent workspace rooted at:

```text
C:\Users\found
```

That meant local installs could appear to succeed while GitHub Actions still
failed. CI was not being inconsistent. My local environment was carrying an
extra workspace boundary that the clean checkout did not have.

The fix was to move to a clean clone outside that parent workspace under
`/c/tmp`, regenerate the lockfile with pnpm `10.14.0`, and confirm that the
dependency appeared in both the package section and the snapshot section.

Then the next layer appeared. The scans still found vulnerable transitives
through:

```text
markdownlint-cli2@0.22.1 -> markdown-it@14.1.1
markdownlint-cli2@0.22.1 -> js-yaml@4.1.1
```

Because `markdownlint-cli2@0.22.1` was still the latest published version, the
practical fix was not to wait for an upstream release. It was to use
`pnpm.overrides` to force:

```text
markdown-it@14.2.0
js-yaml@4.2.0
```

I also added `pnpm-workspace.yaml` in the affected repositories so pnpm would
anchor inside each repository instead of accidentally walking up into a parent
workspace.

The validation signal was the boring one I wanted:

```bash
pnpm install --frozen-lockfile
pnpm validate
```

That was the dependency lesson for the day. Security fixes are not always just
"bump the vulnerable package." Sometimes the real bug is the package manager's
workspace boundary, the lockfile's internal structure, and the mismatch
between local convenience and CI reality.

## Kaggle Day 4

The course side of the day started with Day 4 of the Kaggle / Google vibe
coding coursework: security and evaluation.

I worked through the whitepaper
[_Vibe Coding Agent Security and Evaluation_](https://www.kaggle.com/whitepaper-vibe-coding-agent-security-and-evaluation?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment4-june-2026),
also available as the
[Google Drive PDF](https://drive.google.com/file/d/1kEtWZmFMTGYqe12jMiZPOi9zYcyFXfHF/view).
I also completed the
[ambient expense agent](https://codelabs.developers.google.com/vibecode-ambient-expense-agent?hl=en#4)
codelab and the
[secure agentic coding](https://codelabs.developers.google.com/secure-agentic-coding?utm_source=reg&utm_medium=email&utm_campaign=learn-intensive-assignment4-june-2026&utm_content#12)
codelab.

The whitepaper framed the shift from casual vibe coding toward disciplined
agentic engineering. That was exactly the right phrase for the day.

Security gets harder once agents can execute tools, modify code, access APIs,
and act with delegated authority. The risk is not just that an agent might
write a bad function. The risk is that the agent may act across multiple
systems with partial context and borrowed authority.

The themes in the paper mapped directly onto the work I was already doing:

- sandboxing
- supply-chain defense
- hallucinated package mitigation
- egress governance
- non-interactive access controls
- application logic vulnerabilities
- MCP spoofing and contextual authorization
- confused deputy risk
- delegated versus agentic identity
- zero ambient authority
- just-in-time downscoping
- red, blue, and green security teaming
- repository poisoning and invisible payloads
- tracing the agent's "vibe trajectory"
- intent drift and trust decay
- checkpoints and circuit breakers

That list sounds broad, but the center is simple: an agent should not inherit
ambient trust just because it is useful.

That connected directly to my own recent work. Bot identity isolation,
Cloudflare hardening, repo-scoped validation, dependency scans, and branch-safe
agent workflows are all versions of the same idea. Give the system enough
authority to do useful work, but make the authority visible, constrained,
reviewable, and reversible.

The evaluation section was just as important. Vibe coding agents cannot be
evaluated only like deterministic code because they translate intent into
action over time. The path matters. Tool choices matter. Intermediate state
matters. The same final diff can be more or less trustworthy depending on how
it was produced and what controls surrounded it.

The labs reinforced that point in a practical way. Building agentic workflows
is not just about making the agent do more. It is about permissions, controls,
review, secure execution, and knowing where a human needs to stay in the loop.

## Kaggle Day 5

Day 5 was the production-grade and spec-driven capstone of the coursework.

I read
[_Spec-Driven Production Grade Development in the Age of Vibe Coding_](https://www.kaggle.com/whitepaper-spec-driven-production-grade-development-in-the-age-of-vibe-coding?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment5-june-2026),
also available as the
[Google Drive PDF](https://drive.google.com/file/d/1lCx0Lh06sK6j59nTNc_pYRdnoxgDtJcn/view).
I also completed the
[enterprise cloud scale deployment to Agent Runtime](https://codelabs.developers.google.com/enterprise-cloud-scale-deploying-the-expense-agent-to-agent-runtime-on-google-cloud?utm_source=reg&utm_medium=email&utm_campaign=learn-intensive-assignment5-june-2026&utm_content#11)
codelab and the
[frontend with Antigravity](https://codelabs.developers.google.com/vibecode-frontend-with-antigravity?utm_source=reg&utm_medium=email&utm_campaign=learn-intensive-assignment5-june-2026&utm_content#9)
codelab.

The core message landed cleanly: vibe coding can accelerate implementation,
but "vibe coding" is not the same thing as "vibe in production."

That is the sentence I want pinned to the inside of every agent-assisted
workflow.

As implementation gets faster, specifications matter more. A good spec gives
the agent a target that is explicit, reviewable, testable, and reusable. It
reduces the distance between human intent and machine action without pretending
that intent alone is enough.

The paper covered the production side of that shift:

- spec-driven development
- what makes a good specification
- behavior-driven formats
- where instructions live
- different prompts for different use cases
- MCP as a reusable integration layer
- team process evolution
- code reviews in an agentic workflow
- sustainability
- zero-trust development
- guardrails
- sandboxing
- human-in-the-loop review
- AI-generated test coverage
- evaluation
- policy servers
- context hygiene and prompt sanitization

That is not just course theory for me anymore. The blog itself is a spec and
artifact trail. Codex prompts are becoming operational inputs. PR validation,
branch protection, pnpm frozen installs, Cloudflare redirects, and
`security.txt` all become parts of a governed production workflow.

The Day 5 labs made the capstone mindset concrete. It is one thing to get an
agent to build something. It is another thing to specify, deploy, secure,
evaluate, and review the thing it builds.

That is the shift I wanted from the course, and Days 4 and 5 delivered it.

## Why The Day Mattered

Day 48 made the course material feel less like a separate learning track and
more like a name for the work already in front of me.

Cloudflare Security Insights were about surfacing edge assumptions.
`security.txt` was about making vulnerability disclosure explicit. Redirect
rules were about preserving security-relevant paths through hostname changes.
Cloudflare Pages migration was about removing stale hosting assumptions.
Dependabot and pnpm troubleshooting were about making dependency state
reproducible across local and CI environments.

The Kaggle / Google material gave that work the larger frame.

Day 4 said: once agents can act, security and evaluation have to follow the
action path, not just the final output.

Day 5 said: once implementation gets fast, specs, reviews, guardrails, and
production discipline matter more, not less.

That is the through line I want to keep: governed surfaces beat vague trust.

## Outcome

Day 48 combined practical infrastructure hardening, dependency-security
debugging, and the completion of Days 4 and 5 of the Kaggle / Google vibe
coding coursework.

On the Cloudflare side, I worked through remaining Security Insights warnings,
separated production-zone posture from preview-domain noise, corrected
`security.txt` expectations, accounted for the required `Expires` field, and
clarified redirect behavior for `neibaur.me` so `/.well-known/security.txt`
can preserve its path through to `isaacneibaur.com`.

On the hosting side, I moved more portfolio/static sites toward Cloudflare
Pages, including `isaacneibaur.com`, and treated the migration as more than a
successful deploy: build settings, Hugo and Go versions, custom domains, stale
GitHub Pages DNS records, `www` cleanup, proxied records, and canonical
redirects all had to line up.

On the dependency side, I debugged a pnpm frozen-lockfile failure where
`markdown-it@14.2.0` appeared to exist but lacked the needed lockfile snapshot,
then traced the local/CI mismatch back to a parent workspace. The fix was a
clean clone, regenerated lockfile state, `pnpm.overrides` for vulnerable
transitives, and repo-local `pnpm-workspace.yaml` files to anchor resolution.

On the course side, I completed Day 4 and Day 5 coursework. Day 4 focused on
agent security and evaluation. Day 5 focused on spec-driven,
production-grade development. Together they made the same argument as the
day's infrastructure work: agents become useful when they operate inside
specs, constraints, identity boundaries, validation, deployment discipline,
and reviewable security posture.

## Definition Of Done

Day 48 reached an edge-hardening and course-completion checkpoint:

- investigated remaining Cloudflare Security Insights warnings across
  personal and portfolio domains
- distinguished production custom-domain protections from `.workers.dev` and
  `.pages.dev` preview or system-domain warnings
- treated acceptable preview-domain warnings as dismissible where production
  posture was already hardened
- added or corrected `/.well-known/security.txt` for `isaacneibaur.com`
- identified the need for a future `Expires` field in strict `security.txt`
  validation
- clarified that Cloudflare's dashboard insight may refer to the native
  edge-managed `security.txt` feature rather than only a repository-served file
- planned or fixed `neibaur.me` redirect behavior so
  `/.well-known/security.txt` preserves the path through to
  `isaacneibaur.com`
- moved portfolio/static sites from GitHub Pages toward Cloudflare Pages
- brought `isaacneibaur.com` up on Cloudflare Pages
- reviewed Hugo-specific Cloudflare Pages configuration, including
  `HUGO_VERSION` and `GO_VERSION`
- cleaned up or planned `www` to apex redirect behavior for portfolio domains
- noted that Cloudflare redirect rules require proxied DNS records to run
- debugged pnpm frozen-lockfile failures in portfolio repositories
- traced the local/CI mismatch to an accidental parent pnpm workspace rooted at
  `C:\Users\found`
- regenerated lockfile state from a clean clone under `/c/tmp`
- used `pnpm.overrides` for `markdown-it@14.2.0` and `js-yaml@4.2.0`
- added repo-local `pnpm-workspace.yaml` files in affected repositories
- validated the affected repositories with `pnpm install --frozen-lockfile`
  and `pnpm validate`
- completed Kaggle / Google vibe coding Day 4 materials on agent security and
  evaluation
- completed the Day 4 ambient expense agent and secure agentic coding codelabs
- completed Kaggle / Google vibe coding Day 5 materials on spec-driven,
  production-grade development
- completed the Day 5 Agent Runtime deployment and Antigravity frontend
  codelabs
- ended with a sharper production lesson: fast agent output is only useful
  when surrounded by explicit specs, constrained authority, validation, and
  review
