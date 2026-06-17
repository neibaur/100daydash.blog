---
title: "Day 45 - June 15, 2026: From Vibe Coding to Harness Engineering"
description: "A Day 1 reflection on Kaggle's agentic AI course and the governance work that makes my local project templates safer, clearer, and more reviewable."
pubDate: "2026-06-15"
day: 45
dashboardSlug: "none"
dataSources:
  - "Kaggle whitepaper page"
  - "Day 1 whitepaper PDF"
  - "Google Antigravity codelab"
  - "AI Studio to Cloud Run codelab"
  - "local project-template governance notes"
  - "GitHub organization ruleset planning"
status: "published"
tags:
  - ai-agents
  - vibe-coding
  - agentic-engineering
  - harness-engineering
  - context-engineering
  - google-antigravity
  - cloud-run
  - github-governance
  - project-templates
---

Day 45 was yesterday's work from June 15, 2026, and it was really two
conversations that ended up reinforcing the same lesson.

One conversation was the first day of Kaggle's 5-Day Agentic AI course,
starting with the whitepaper [The New SDLC With Vibe Coding: From ad-hoc
prompting to Agentic Engineering](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment1-june-2026),
also available as the [Day 1 whitepaper PDF](https://drive.google.com/file/d/1IR7CddF_2FyQo_PdfBNTaEA50EGiVt2r/view),
the [Getting Started with Google Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity#0)
codelab, and the [Deploy from AI Studio to Cloud Run](https://codelabs.developers.google.com/deploy-from-aistudio-to-run?hl=en#0)
codelab.

The other conversation was my own ongoing work on project-template governance:
how to shape templates, rulesets, identity boundaries, and validation so
agent-assisted development stays safe enough to repeat.

The overlap between them was the real story. The course was not just about
"AI writes code now." It was about how much structure surrounds the model.

## The Whitepaper's Real Divide

The paper's big idea landed with me immediately: the shift is not from code
to no-code. It is from syntax to intent. I am spending less time spelling out
every line and more time making sure the system around the model can turn
intent into something reliable.

What mattered most was the distinction between three levels of AI-assisted
work:

- vibe coding, where prompts are loose and verification is basically "does it
  seem to work?"
- structured AI-assisted coding, where prompts are specific and I still review
  the result by hand
- agentic engineering, where the work is wrapped in specs, architecture docs,
  memory files, tests, CI/CD, evals, and human oversight

The dividing line that mattered most to me was verification. Tests tell me
whether deterministic behavior still works. Evals tell me whether a less
deterministic agent behavior, like tool choice or task trajectory, stayed
inside the quality bar I wanted.

That is a more useful way to think about the craft than simply asking whether
AI was involved.

The paper's context engineering section also matched the way I already work.
Good results depend less on clever prompts than on structured context:
instructions, knowledge, memory, examples, tools, and guardrails.

That maps cleanly to the static and dynamic context split:

- static context: always-loaded project rules like `AGENTS.md`, `CLAUDE.md`,
  and other persistent instructions
- dynamic context: task-specific skills, retrieved docs, tool output, session
  history, and whatever else only needs to be loaded when the work actually
  calls for it

I also liked the idea of agent skills because it gives a name to reusable
procedural knowledge. That is exactly the kind of thing I want future
templates and agents to carry without stuffing every rule into every prompt.

The factory model was another useful frame. The developer's output is no
longer just code. It is the system that produces code: specs, agents, tests,
quality gates, feedback loops, and guardrails.

That is where the phrase harness engineering stopped sounding abstract and
started sounding like my own work.

## Harness Engineering, Locally

The strongest connection between the course and my day was harness
engineering.

The paper uses that word for everything around the model: instructions and
rule files, tools, sandboxes, orchestration, guardrails and hooks,
observability, evals, and deployment configuration.

That is a very close description of the local patterns I have been tightening
in my own repo work. I was not just organizing repositories. I was designing
the scaffolding that makes agent-assisted work safer, more repeatable, and
easier to review.

That is why the current branch protection, bot identity isolation, validation
checks, and PR habits matter so much. They are not side chores. They are the
harness.

The economics piece clicked too. Casual vibe coding can look cheap up front,
but it can hide verification, security, and maintenance costs later. Agentic
engineering asks for more up-front CapEx in rules, tests, templates, and
context, but it pays that back as lower long-term OpEx because the work
becomes more repeatable and safer.

That is the tradeoff I want.

The developer role also feels like it is splitting into two useful modes:

- conductor mode: hands-on ideation, prompt hardening, and reviewing changes
- orchestrator mode: giving Codex a branch-safe task, requiring validation,
  and reviewing the result through a PR

I use Claude, Codex, and ChatGPT differently depending on which mode I need.
The course helped me name that instead of treating it like an informal habit.

The 80% problem was part of the same lesson. AI can generate a lot quickly,
but the edge cases, integration boundaries, correctness, and long-term
maintainability still need human judgment. The easier generation gets, the
more the human role shifts toward direction and verification.

## Antigravity As A Preview

The Google Antigravity codelab felt like a practical preview of that future
environment.

What stood out to me was not just the tool itself, but the model it implied:
projects with isolated settings, slash commands, scheduled work, MCP servers,
and artifacts. That is a much better mental model for agentic work than a bare
chat window.

The artifact idea matters a lot. If an agent is doing meaningful work, a human
needs evidence they can inspect: implementation plans, task lists, walkthroughs,
code diffs, screenshots, and other reviewable outputs.

That is already how I want my Codex and Claude workflow to behave. I expect
branch names, changed files, commit hashes, validation results, and PR
descriptions to exist as review artifacts, not as optional nice-to-haves.

The codelab did not invent that habit for me, but it reinforced that the habit
is correct.

It also made the case that the surrounding environment is part of the product.
A good agent experience is not just "the model can do the task." It is "the
task can be traced, reviewed, and resumed."

## Cloud Run Makes The Boundary Sharper

The [AI Studio to Cloud Run](https://codelabs.developers.google.com/deploy-from-aistudio-to-run?hl=en#0)
codelab was a reminder of how compressed the prototype-to-deploy path is
becoming.

A prompt-based prototype can now move to a deployed Cloud Run app very
quickly. That is powerful. It also means the governance question matters more,
not less.

The takeaway I wrote down for myself was simple: "can deploy quickly" is not
the same thing as "should be treated as production."

The production boundary still needs checks, ownership, rollback thinking, and
observability. Fast deployment does not remove the need for review. It
increases the need for review because the blast radius can show up sooner.

That is where the course and the governance work came back together for me.
The tooling is getting faster. The control plane has to get better with it.

## Template Governance Work

The second major thread of the day was me reasoning through how my GitHub
organization and project templates should support agent-assisted development
safely.

The first decision was about the current `project-template`. It probably should
become `project-template-node` rather than pretending to be universal. Future
templates should be stack-specific from the start:

- `project-template-node`
- `project-template-python`
- `project-template-dotnet`
- `project-template-ios`

I do not want to split into multiple GitHub organizations just to separate
tech stacks. One organization with custom properties and targeted rulesets
keeps the pay-once-govern-once model cleaner.

I also do not want to depend on repository names as policy boundaries. Names
are useful for humans, but they are brittle as enforcement. Policy should live
in rulesets and properties, not in a naming convention that can drift.

That is why the `lifecycle` custom property feels like the better control:

- `bootstrapping`
- `active`

New repositories should start in `bootstrapping` so the initial template setup
can happen without immediately getting trapped behind PR-only changes and
required checks. The final setup step would flip the repo to
`lifecycle:active`, which is what brings the stricter rulesets online.

I also want a `stack` custom property with values like:

- `unset`
- `node`
- `python`
- `dotnet`
- `ios`

`unset` should be the default. I do not want the org to assume every repo is
Node. If a repo becomes active while `stack` is still `unset`, I want that to
fail closed with a clear diagnostic instead of quietly letting a misconfigured
repo through.

That is the job of the trap ruleset. It should target
`props.lifecycle:active props.stack:unset` and require a phantom check like
`stack-not-configured`.

The rest of the ruleset model also makes more sense now that I am treating
policy as layers instead of one giant gate:

1. A baseline ruleset for all repositories that restricts deletions, blocks
   force pushes, and avoids broad bypass.
2. A push ruleset for `.github/**` so workflow and governance files can still
   be intentionally updated with a tightly scoped bypass.
3. A gate-common ruleset for `props.lifecycle:active` that requires pull
   requests, conversation resolution, linear history, and squash merge as the
   intended path.
4. Stack-specific check rulesets, like a Node ruleset for
   `props.lifecycle:active props.stack:node`, with required checks that match
   the actual job names in that stack's CI.
5. A stack-unset trap ruleset for `props.lifecycle:active props.stack:unset`
   that blocks activation until the repo is actually configured.

That layered model feels better than trying to make one policy do everything.

I also clarified the org `.github` repo versus per-template files distinction.
Some community-health files can live once in the organization repo. Others
have to physically exist in each template because they do not cascade:
`CODEOWNERS`, `README`, `LICENSE`, `.gitignore`, governance files like
`AGENTS.md` and `CLAUDE.md`, CI workflows, dependabot config, hooks, and
toolchain configs.

That distinction matters because GitHub's fallback UI can make it feel like a
repo is governed when the actual file is not there yet.

On the Python side, I decided that a venv reminder is useful, but it belongs in
a Python template, not in the current Node/TypeScript-oriented
`project-template`. A future Python template should probably include early
setup guidance like:

```bash
python -m venv .venv
```

with activation notes for Windows, macOS, and Linux, plus `.venv/` in
`.gitignore`, a pinned Python version, and explicit guidance that the local
virtual environment is for developer experience while CI creates its own
environment.

I also want to keep `uv` in mind as a future tool to evaluate, but I am not
treating it as already adopted in that template unless the repository files
support that decision.

Finally, I am not creating a `project-template-base` yet. GitHub templates do
not inherit from one another, so a base template would not automatically keep
stack templates in sync. For now, the Node template is the practical source to
clone and then swap the toolchain. A base-template-plus-sync-action only feels
worth the complexity once several stack templates exist and drift becomes
painful.

## Why The Day Mattered

The most important thing I took from Day 1 was not a feature or a launch
moment. It was the shape of the craft.

The course made the case that agentic development is less about raw generation
and more about the system around generation. The whitepaper, the Antigravity
codelab, and the Cloud Run codelab all pointed in the same direction: the
model is becoming more capable, but the surrounding harness is what decides
whether that capability is usable.

That validated the direction I was already moving in my own work. Branch
protection, template governance, bot identity isolation, validation checks,
and PR habits are not overhead. They are the reason agent-assisted development
can be trusted at all.

The ending I keep coming back to is this: generation is getting easier, but
verification, judgment, and direction are becoming the real work.

## Outcome

Day 45 tied the Kaggle/Google agentic AI material to my own governance work in
a way that felt unusually direct.

I completed the Day 1 course materials, including the whitepaper, the Google
Antigravity codelab, and the AI Studio to Cloud Run codelab. The whitepaper
clarified the shift from syntax to intent, the spectrum from vibe coding to
agentic engineering, the importance of verification, and the role of context
engineering, static context, dynamic context, agent skills, and harness
engineering.

The Antigravity codelab reinforced the idea that agentic environments need
projects, isolated settings, slash commands, scheduled work, MCP servers, and
artifacts that a human can review. The Cloud Run codelab reminded me that the
path from prototype to deployment is getting shorter, which makes governance
more important, not less.

On my own side, I reasoned through template and GitHub organization design:
splitting the current `project-template` into `project-template-node`, leaving
space for future stack-specific templates, avoiding a base template for now,
using `lifecycle` and `stack` custom properties instead of repository names as
policy boundaries, and layering rulesets so active repos fail closed when
they are not configured correctly.

The result was a stronger mental model for the whole 100-day arc. The tools
are getting easier to point at the work, but the real craft is in the
harness: context, checks, review artifacts, and governance.

## Definition Of Done

Day 45 reached a reflection-and-governance checkpoint:

- completed the Kaggle / Google 5-Day Agentic AI Day 1 materials
- reviewed the whitepaper [The New SDLC With Vibe Coding](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding?utm_medium=email&utm_source=gamma&utm_campaign=learn-intensive-assignment1-june-2026)
  and the [Day 1 whitepaper PDF](https://drive.google.com/file/d/1IR7CddF_2FyQo_PdfBNTaEA50EGiVt2r/view)
- worked through [Getting Started with Google Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity#0)
- worked through [Deploy from AI Studio to Cloud Run](https://codelabs.developers.google.com/deploy-from-aistudio-to-run?hl=en#0)
- connected the whitepaper's spectrum of vibe coding, structured AI-assisted
  coding, and agentic engineering to my own workflow
- treated verification as the important dividing line between tests and evals
- mapped context engineering to static and dynamic context
- recognized agent skills as reusable procedural knowledge
- framed my own repo and template work as harness engineering
- compared conductor mode and orchestrator mode in my use of Claude, Codex,
  and ChatGPT
- kept the 80% problem in view as a human-judgment issue, not a model
  marketing issue
- treated Cloud Run speed as a governance warning light, not just a launch
  convenience
- reasoned through `project-template-node` as the likely replacement for a
  generic `project-template`
- kept future Python template guidance separate from the current Node-oriented
  template
- preferred `lifecycle` and `stack` custom properties over repository names as
  enforcement boundaries
- kept the base-template question open until drift actually becomes painful
- ended the day with a clearer answer to what my 100-day dash is really
  building: not just dashboards, but the harness that makes AI-assisted work
  safe enough to repeat
