---
title: "Day 46 - June 16, 2026: From Agent Tools to Organization Guardrails"
description: "A Day 2 reflection on agent interoperability, grounded tool access, and the GitHub organization ruleset model that keeps agent-assisted development fail-closed."
pubDate: "2026-06-16"
day: 46
dashboardSlug: "none"
dataSources:
  - "Agent Tools & Interoperability whitepaper"
  - "Day 2 whitepaper PDF"
  - "Hands-on with Antigravity CLI codelab"
  - "Google Developer Knowledge MCP server codelab"
  - "GitHub organization ruleset test notes"
status: "published"
tags:
  - ai-agents
  - agent-tools
  - mcp
  - google-antigravity
  - github-governance
  - rulesets
  - protocols
  - security
---

Yesterday was about taking the Day 1 idea one layer deeper. Day 1 was about
moving from vibe coding to harness engineering. Day 2 was about the standards
that let the harness safely connect to the outside world.

That is the frame that held everything together for me. The whitepaper, the
codelabs, and my own organization ruleset work all pointed at the same idea:
protocols are not just plumbing. They are governance boundaries.

## The Whitepaper Backbone

The [Day 2 whitepaper PDF, _Agent Tools & Interoperability_](https://drive.google.com/file/d/1_emw2Pj1aecYZe4LKFcL8-zMDeBBRgQF/view)
gave me the clearest mental model for the day.

Its main point is that the next stage of software is not just humans writing
code directly. It is orchestration by interoperable agents. That is a useful
shift in language because it moves the focus from "how do I prompt this model?"
to "what system of tools, boundaries, and trust lets the model actually do
work?"

The simplest version of that idea is the one I keep coming back to:

`Agent = Model + Harness`

The model provides capability. The harness provides context, access, safety,
and review. That harness includes the tools, permissions, transport, memory,
observability, and human checkpoints that make the system trustworthy enough
to use repeatedly.

The paper also treats several protocols as the industry standards that keep
agent systems from becoming one-off custom machines:

- `MCP` for tools and context
- `A2A` for agent-to-agent collaboration
- `A2UI` for safer generative UI
- `AP2` and `UCP` for agentic commerce and action

`MCP` matters first because it sits at the tool/context layer. It helps avoid
writing custom wrappers for every model-tool pair and reduces the N x M
integration problem that shows up as soon as more than one model and more than
one tool are in the picture.

The paper's distinction between discovery, configuration, and connection was
especially useful:

- discovery of public, third-party, or internal MCP servers
- configuration of scope, credentials, and permissions
- connection and validation through tool listing and schema checks

That is a more disciplined mental model than "point the agent at some tools and
hope for the best."

The MCP best practices that stuck with me were equally practical:

- audit public servers before connecting them
- avoid public or unverified MCPs in production
- do not hardcode credentials
- prefer environment variables and scoped access
- use development projects and read-only access when real data is involved
- include human-in-the-loop review for tool inputs
- debug transport directly with MCP Inspector or browser and dev tools instead
  of only tweaking prompts

`A2A` is the agent-to-agent collaboration layer. That matters when the caller
does not just need a result, but needs another participant to take
responsibility for a task.

The bounded-versus-unbounded distinction was one of the most useful ideas in
the paper. Tools are structured and fire-and-forget. Agents may need multi-turn
clarification, negotiation, pause and resume behavior, and stateful
collaboration.

`A2UI` extends the same thinking into interfaces. The safer pattern is not to
let agents ship arbitrary executable UI code. Instead, they should declare UI
intent through a trusted component catalog so the client can render safe native
UI.

`AP2` and `UCP` carry the model further into commerce and action. `UCP` covers
catalog and order-style interactions. `AP2` covers payment authorization,
mandates, auditability, and guardrails. That is a good reminder that once an
agent can act, the boundary between "tool use" and "real-world consequence"
starts to matter very quickly.

The personal takeaway for me was simple: protocols define where an agent may
read, act, delegate, render, or transact.

## Antigravity CLI As Practice

The [Hands-on with Antigravity CLI](https://codelabs.developers.google.com/antigravity-cli-hands-on#7)
codelab felt like hands-on practice with the terminal surface of Antigravity.

The CLI/TUI surface matters because it gives agentic development a place to
work that is still legible to a human. It supports multi-step reasoning,
multi-file editing, tool calling, and conversation history from the command
line. That is a lot closer to the way real engineering work happens than a
single chat response with no visible trail.

The lab covered the pieces I would expect from a practical setup:

- install and configuration
- initial login
- trusted workspace setup
- `/help`
- `/config` or `/settings`
- tool permission modes
- command parameters
- model selection
- shell mode
- example use cases

The permission-mode discussion connected directly to my governance thinking.
`request-review` keeps the human in the loop. Sandboxed execution can improve
safety. Fully autonomous or permission-skipping modes are powerful, but they
should be treated carefully.

That theme showed up in the vibe-coding example too. The real value was not the
demo itself. It was the evidence model around the demo: plans, task lists,
implementation evidence, and verifiable outputs. If the artifact trail is
missing, the work is much harder to trust.

That is also why this whole phase feels more like learning how to inspect the
factory than building the factory floor itself.

## Grounded Docs Through MCP

The second codelab, [Google Developer Knowledge MCP server in Google
Antigravity 2.0, IDE, and/or CLI](https://codelabs.developers.google.com/developer-knowledge-mcp-antigravity?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment2-june-2026#0),
was a concrete example of grounded tool access.

Google Developer Knowledge is positioned as a canonical, machine-readable
source of Google public developer documentation. That matters because it gives
an agent a current, structured source of truth instead of forcing it to rely on
stale model training data or web scraping.

The lab walked through the practical setup:

- enable the Developer Knowledge API
- create an API key
- configure Antigravity's MCP config
- validate the `google-developer-knowledge` MCP server

That process lined up almost exactly with the paper's MCP model:

- discover the server
- configure credentials and scope
- connect and validate available tools
- approve tool use when the agent first invokes it

The real win here is not just convenience. It is reduced hallucination risk.
An agent that can query current developer documentation through MCP is much
better grounded than one that is guessing from memory.

## Governance As Protocol Design

In parallel with the AI Agents Intensive, I kept hardening my GitHub
organization setup for governed AI-assisted development.

The practical problem was that repo templates and branch protections can fail
open during bootstrapping if custom properties are left at defaults. I wanted
the system to fail closed instead of fail open, but still allow the initial
template or bootstrap stamp to land.

The model I ended up testing centered on two custom properties:

- `lifecycle`
- `stack`

The intended state machine was straightforward once I wrote it down:

- `lifecycle:bootstrapping` should allow only the initial stamp or creation
  behavior, then block further default-branch progress with a phantom required
  check named `set-lifecycle-to-active`
- `lifecycle:active` plus `stack:unset` should block with a phantom check
  named `stack-not-configured`
- `lifecycle:active` plus a real stack, such as `stack:node` or `stack:docs`,
  should activate the real stack-specific checks

The ruleset names I ended up with were:

- `org-baseline-ruleset`
- `org-active-lifecycle-ruleset`
- `org-stack-node-ruleset`
- `org-block-unset-stack-ruleset`
- `org-block-bootstrapping-lifecycle-ruleset`
- `org-push-ruleset`
- `org-stack-docs-ruleset`

`org-push-ruleset` is the one that matters most for human control of the
governance surface. It restricts `.github/**` paths so workflow and governance
edits stay intentionally human-controlled.

I validated the model with real test repos instead of trusting the policy
design on paper.

`foundegg` was created from `project-template-node` with `lifecycle` still set
to `bootstrapping` and `stack` still set to `unset`.

- initial creation succeeded
- a direct edit to `main` was blocked
- a PR could not merge because `set-lifecycle-to-active` was required
- after setting `lifecycle` to `active` but leaving `stack` as `unset`, the PR
  was still blocked by `stack-not-configured`
- after setting `stack` to `node`, the PR became mergeable

`wodezhongguo` was created with `lifecycle` still `bootstrapping`, but `stack`
already set to `node`.

- creation succeeded
- direct changes to the default branch were blocked
- PR merge was still blocked by `set-lifecycle-to-active`

That second repo mattered because it validated that the bootstrapping blocker
targeted lifecycle alone and closed the partial-set seam.

I also created and started an `org-governance` repo and ran into a genesis
commit and default-branch wrinkle. An empty repo without README, LICENSE, or
gitignore does not really have a branch yet. The first pushed branch can become
the default branch. That is not a major ruleset failure, but it is a repo
creation and training issue. The cleanup was to rename the accidental default
branch to `main` and prefer template-created or initialized repos going
forward.

That led me to one more design choice: the decision log belongs in a dedicated
governance or ops repo, not in each project template.

I also added a docs stack concept:

- `org-stack-docs-ruleset`
- target: `props.lifecycle:active props.stack:docs`
- required checks: `lint` and `security`
- no fake `typecheck` check for docs-only repos

I discussed moving org-wide `CONTRIBUTING.md` and `SECURITY.md` into the
public `neibaur-labs/.github` repo so they cascade as community-health
defaults. The `.github` repo is special because it must be public for those
defaults to cascade, but it should still be treated as `lifecycle:active` and
`stack:docs` with `lint` plus `security` checks.

That all sounds like repository plumbing, but it is really policy design.
The same idea from the whitepaper showed up in my own work: the tools are only
safe when the harness and boundaries are explicit.

## Why The Day Mattered

This was less about producing application code and more about tightening the
harness around agent-assisted development.

The whitepaper explains protocol boundaries for agents. The codelabs show
those boundaries in Antigravity and MCP. The org-ruleset work applies the same
principle to GitHub: explicit lifecycle states, stack-specific checks, blocked
unsafe defaults, and human-only governance paths.

That made the day feel like building guardrails for the factory rather than
building the product itself. I think that is the right thing to be doing right
now.

## Outcome

Day 46 tied the AI Agents Intensive and my own governance work together in a
way that felt unusually direct.

I read _Agent Tools & Interoperability_ as the backbone for the day and kept
coming back to the same model: `Agent = Model + Harness`. The paper's
discussion of MCP, A2A, A2UI, AP2, and UCP gave me a much clearer picture of
where an agent may read, act, delegate, render, or transact.

The Antigravity CLI codelab reinforced the terminal-side workflow: install and
configuration, login, trusted workspaces, slash commands, permission modes,
model selection, shell mode, and the artifact trail that makes agent work
reviewable.

The Google Developer Knowledge MCP codelab showed what grounded tool access
looks like in practice. Instead of relying on stale memory or ad hoc web
scraping, the agent can query current docs through MCP after discovery,
configuration, connection, and validation.

On my side, I hardened an org-level ruleset model around `lifecycle` and
`stack`, validated it in real repos, closed a bootstrapping seam, and clarified
where `.github` governance files and docs-only defaults should live.

The day ended with the same conclusion in three different contexts: protocols
are only safe when the harness and boundaries are explicit.
