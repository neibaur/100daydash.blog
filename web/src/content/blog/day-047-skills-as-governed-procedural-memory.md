---
title: "Day 47 - June 17, 2026: Skills as Governed Procedural Memory"
description: "A Day 3 reflection on Cloudflare domain hardening, agent-skill template governance, and the Kaggle Google AI course material on Skills as portable procedural memory."
pubDate: "2026-06-17"
day: 47
dashboardSlug: "none"
dataSources:
  - "Agent Skills whitepaper"
  - "Agent Skills Day 3 PDF"
  - "Authoring Google Antigravity Skills codelab"
  - "Agents CLI ADK lifecycle codelab"
  - "DNS troubleshooting notes"
  - "Claude skill governance conversation"
status: "published"
tags:
  - ai-agents
  - agent-skills
  - google-antigravity
  - adk
  - cloudflare
  - dns
  - security
  - governance
  - project-templates
---

Day 47 moved between two kinds of infrastructure that do not look related at
first: DNS records for personal domains and Agent Skills for local AI-assisted
development.

The more I sat with it, the more they felt like the same problem in different
clothes. Both are easy to treat as background configuration. Both can quietly
shape whether the system is safe. Both become risky when they are implicit,
stale, copied around, or left without ownership.

That was the thread through the day: DNS should be explicit. Email posture
should be intentional. Skills should be reviewed, tested, and owned. Capability
does not become durable just because it is written down somewhere.

## Cloudflare Security Insights

The first thread was domain hygiene.

I spent part of the day investigating Cloudflare Security Insights warnings
across personal and project domains. The starting point was a dangling `A`
record or possible subdomain takeover warning on `isaacneibaur.com`.

The setup was the familiar GitHub Pages plus Cloudflare DNS shape: the domain
pointed at GitHub Pages IP addresses, but GitHub's Pages custom-domain and
certificate check appeared stuck. That turned a small alert into a useful
reminder that "the DNS record exists" is not the same thing as "the hosting
posture is correct."

The remediation path I explored was practical:

- verify the GitHub Pages custom domain from GitHub's side
- temporarily switch Cloudflare records from proxied to DNS-only so GitHub
  Pages can complete DNS and certificate checks
- re-enable HTTPS once GitHub issues the certificate
- decide whether the longer-term stable posture should be GitHub Pages with
  Cloudflare DNS-only, or a migration to Cloudflare Pages

That last question is the governance part. GitHub Pages and Cloudflare DNS can
work together, but the boundary has to be understood. If Cloudflare is proxying
too early, GitHub may not be able to see what it needs to issue the certificate.
If the record points somewhere that is no longer claimed, the domain can carry
a takeover-shaped risk even though the zone looks tidy at a glance.

I also reviewed DMARC and SPF posture. `isaacneibaur.com` had an MX-related
DMARC warning, and parked or lightly used domains such as `kpdeals.com` need a
clear decision: either intentional email routing, or explicit no-mail SPF and
DMARC lockdown records.

That is not glamorous engineering, but it matters. A parked domain with vague
mail posture is still a surface. It can be spoofed, misread by scanners, or
left in a half-configured state because nobody decided whether it sends mail.

The same pass included missing `security.txt` warnings across:

- `isaacneibaur.com`
- `kpdeals.com`
- `kamolwan.com`
- `100daydash.blog`
- `neibaur.me`

I do not think every personal domain needs enterprise ceremony. I do think
every domain benefits from an intentional posture. DNS records, email
authentication, certificate renewal, parked-domain defaults, and vulnerability
disclosure metadata are all part of the same domain portfolio surface.

The lesson was not "panic about every warning." It was "make the intended state
visible enough that warnings have somewhere to land."

## Skills In Templates

The second thread was a long governance conversation about whether my project
templates should include Agent Skills by default.

The initial question was tempting: should every template ship with a live skill
folder containing `SKILL.md`, `scripts/`, `references/`, and `assets/`?

The answer I landed on was no, or at least not as an empty default.

Empty live skills are not neutral. A vague `SKILL.md` can mis-trigger. A skill
folder in an agent discovery path can add context cost. A script-capable skill
can become part of the trusted surface before it has earned that trust. The
problem is not that skills are bad. The problem is that a fake capability can
look like a real one.

The better template pattern is inert authoring material:

- documentation that explains when a skill is appropriate
- a copy-paste `SKILL.template.md`
- examples that live outside agent discovery paths
- guidance for review, versioning, evals, and CI gates

That distinction matters. A template can teach people how to author skills
without silently activating empty skills in every new repository.

The phrase that stuck with me was: skills are dependencies.

That means they need ownership. They need review. They need versioning. They
need tests and evals. A skill without tests is not a capability; it is a hope.

That also changes how I think about trust boundaries. A skill that can run
scripts belongs in the same mental category as `.github/**`, `AGENTS.md`, CI
configuration, and other governance files. It can shape what the agent sees,
what the agent believes it is allowed to do, and what commands it may delegate
to local code.

I also clarified which workflows are skill-worthy and which belong in
deterministic enforcement.

Conventional commit enforcement belongs in commitlint, hooks, or CI. License
headers belong in deterministic checks or fixers. Those are rules; they do not
need an agent to interpret them every time.

A validation-triage skill, though, could be valuable. That workflow is not just
"run a command." It is run the existing local validation suite, interpret the
failures, connect them back to likely files, and suggest a repair path before a
PR. That is procedural judgment around deterministic checks, which is exactly
where a skill can help.

Stack-specific scaffolding skills can also make sense at the template level
when they encode real, repeatable, multi-step conventions. A Python project
bootstrap skill, a Node package setup skill, or a docs-site release-prep skill
can be worth owning if it captures a pattern that would otherwise be repeated
badly by hand.

The multi-agent syncing question had a similarly practical answer. I do not
want to mentally keep separate skill copies in sync for Claude, Codex, and
Antigravity. The better model is one canonical skills source, then symlink or
install into tool-specific paths as needed. Always-on project conventions stay
in `AGENTS.md`. Tool-specific skills stay task-specific. ChatGPT web and Custom
GPT knowledge remain out-of-band because they do not share the same local
filesystem skill model.

That keeps the system honest. Project rules are not skills. Skills are not MCP.
MCP is not a repo governance file. Each piece should do the job it is actually
good at.

## Kaggle Day 3

The third thread was Day 3 of the Kaggle / Google AI vibe coding course.

I read the Agent Skills whitepaper from the
[Kaggle whitepaper page](https://www.kaggle.com/whitepaper-agent-skills?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment3-june-2026)
and the
[Google Drive PDF](https://drive.google.com/file/d/1Wso-CM4aAvTxFZa5wjBntKM3IVSg7PWW/view).
I also completed the
[Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills?hl=en#4)
codelab and the
[Agents CLI / ADK lifecycle](https://codelabs.developers.google.com/agents-cli-adk-lifecycle?utm_source=reg&utm_medium=email&utm_campaign=learn-intensive-assignment3-june-2026&utm_content#9)
codelab.

The strongest idea from the day was that Agent Skills are a lightweight,
portable primitive for procedural memory.

A skill is usually just a folder anchored by `SKILL.md`, with optional
`scripts/`, `references/`, and `assets/`. That small shape matters because it
makes skills feel less like magic and more like repo-native artifacts. They can
be reviewed. They can be versioned. They can be tested. They can be moved
between compatible agents and environments.

The progressive-disclosure model is the part that feels most important.
Metadata is always visible. The skill body loads only when triggered.
Supporting resources load only when needed.

That gives a better answer to context rot than stuffing everything into one
giant always-loaded prompt. The agent does not need every migration rule, docs
release checklist, design pattern, and incident playbook in memory for every
task. It needs the right procedural memory at the moment the work calls for it.

That also clarified the relationship between skills, MCP, and `AGENTS.md`:

- MCP gives the agent reach into tools and systems
- `AGENTS.md` carries always-on project conventions
- Skills carry task-specific know-how

Mixing those together is where systems get mushy. If a convention should
always apply in a repo, it belongs in `AGENTS.md` or deterministic tooling. If
the agent needs a repeatable task procedure, that is skill territory. If the
agent needs to query or act through an external capability, that is MCP or a
tool boundary.

The whitepaper's read, draft, and act ladder mapped cleanly onto the way I
already think about governance.

Read-only skills can retrieve, inspect, or summarize. Draft-only skills can
produce artifacts for human review. Action-allowed skills need the strictest
review, tests, evals, and human approval boundaries because they can change the
workspace or touch real systems.

That framing is useful because not every skill has the same risk. A style-guide
lookup skill is not the same thing as a deployment skill. A validation triage
skill is not the same thing as a credential rotation skill. Capability needs a
permission model, not just enthusiasm.

The codelabs made that concrete. Antigravity Skills use the same small folder
shape, introduce examples like commit formatting, license headers, schema
validation, and model scaffolding, and show how skills can be installed at
global or project scope. The interesting part was not just "skills can exist."
It was the question underneath: which of these should be deterministic checks,
which should be agent procedures, and which should not be automated at all?

That is the question I want my templates to answer over time.

## Why The Day Mattered

Day 47 was another governance day, but it was not abstract.

Cloudflare Security Insights turned domain configuration into visible work.
DMARC and SPF warnings forced an email posture decision. Missing
`security.txt` warnings made disclosure metadata part of the same surface.
GitHub Pages plus Cloudflare DNS reminded me that certificate issuance,
proxying, and record ownership have to line up in a real system, not just in a
diagram.

The Agent Skills work did the same thing for AI-assisted development.

It is easy to say "we should add skills to templates" and feel like that is
progress. The harder and better answer is to ask what the skill owns, what
triggers it, what it may execute, how it is evaluated, where it is installed,
and whether a deterministic check would be safer.

That is the practical lesson I want to keep: avoid magical thinking.

DNS records should point at claimed resources. Email authentication should say
what the domain actually does. `security.txt` should make disclosure channels
explicit. Skills should be governed procedural assets, not scattered prompt
lore.

## Outcome

Day 47 connected domain security hygiene and agent-skill architecture under
one theme: surfaces need governance before they can be trusted.

On the domain side, I investigated Cloudflare Security Insights warnings around
GitHub Pages DNS, possible dangling records, DMARC and SPF posture, parked
domains, and missing `security.txt` metadata across my domain portfolio.

On the agent side, I clarified that live skills should not be shipped empty in
every repo template. Templates should include inert authoring documentation and
copy-paste skill templates, while real skills need ownership, review,
versioning, evals, CI gates, and clear trust boundaries.

For Kaggle / Google Day 3, I read the Agent Skills whitepaper, completed the
Antigravity Skills codelab, and completed the Agents CLI / ADK lifecycle
codelab. The main takeaway was that skills are not "more prompts." They are
versioned, governed, testable procedural assets that let agents load the right
know-how at the right time.

That feels like the right direction for the next layer of my project
governance: fewer invisible assumptions, more explicit ownership, and
capability treated as something that has to be earned.

## Definition Of Done

Day 47 reached a security-and-skills governance checkpoint:

- investigated Cloudflare Security Insights warnings across personal and
  project domains
- reviewed a possible dangling `A` record or subdomain takeover warning on
  `isaacneibaur.com`
- explored the GitHub Pages plus Cloudflare DNS remediation path around custom
  domain verification, DNS-only checks, HTTPS certificate issuance, and future
  Cloudflare Pages migration
- reviewed DMARC and SPF posture for active, parked, and lightly used domains
- identified missing `security.txt` warnings across `isaacneibaur.com`,
  `kpdeals.com`, `kamolwan.com`, `100daydash.blog`, and `neibaur.me`
- clarified that project templates should not ship empty live skills by
  default
- preferred inert skill-authoring documentation and `SKILL.template.md`
  examples outside agent discovery paths
- treated skills as dependencies that need ownership, review, versioning,
  evals, and CI gates
- separated deterministic enforcement from skill-worthy workflows
- identified validation triage and stack-specific scaffolding as better skill
  candidates than conventional commit or license-header enforcement
- decided to keep one canonical skills source and install or symlink into
  tool-specific paths for Claude, Codex, and Antigravity
- completed Kaggle / Google AI vibe coding course Day 3 activities
- read the Agent Skills whitepaper from the Kaggle and Google Drive source
  material
- completed the Antigravity Skills codelab
- completed the Agents CLI / ADK lifecycle codelab
- ended with a clearer model of skills as governed procedural memory rather
  than scattered prompt lore
