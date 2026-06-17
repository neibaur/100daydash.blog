---
title: "Day 44 - June 14, 2026: Bot Identity Isolation for Local AI Work"
description: "Hardening local AI workflows with a bot-specific VS Code launch path, local secret loading, repo-local Git identity, and explicit GitHub CLI targeting."
pubDate: "2026-06-14"
day: 44
dashboardSlug: "none"
dataSources:
  - "Kaggle 5-Day AI Agents: Intensive Vibe Coding Course With Google"
  - "Claude local settings"
  - "Codex shell environment policy"
  - "VS Code bot profile"
  - "GitHub CLI"
  - "bot repository clone"
  - "local secret launcher script"
status: "published"
tags:
  - ai-governance
  - repository-governance
  - security
  - developer-experience
  - vscode
  - codex
  - claude
  - github-cli
---

Day 44 was about a simple idea that turned out not to be simple at all:
local AI tools need identity boundaries.

I started the day by beginning Kaggle's 5-Day AI Agents: Intensive Vibe
Coding Course With Google and listening to the opening 20-minute introduction.
That framing was useful before I wrote a single line of code. The course was
presented as something that needs structure, governance, and safety rails, not
just enthusiasm and experimentation. The capstone due during the first week of
July made the work feel concrete instead of abstract.

That tone matched the rest of the day. The main engineering task was not
building a feature. It was tightening the way I let coding agents operate
locally so that Claude and Codex can use a dedicated GitHub bot identity
instead of my main account.

## Course Kickoff

The first 20 minutes of the course did a good job of naming the thing I was
already feeling: agentic development is becoming normal fast, but normal does
not mean unstructured.

The course kickoff was relevant because it treated AI-assisted work as a
practice that needs process around it. That lined up with the real problem I
was working on today. I did not need another agent demo. I needed a safer local
operating model.

The near-term capstone mattered for the same reason. A time-bound project gives
the course a reason to stay practical, and practical pressure is good when
you are refining the way tools are allowed to act on your behalf.

## Why Profiles Were Not Enough

The starting point was my existing Claude setup.

Claude already supports a clean local pattern through
`.claude/settings.local.json`, where I can inject a `GH_TOKEN` tied to my
dedicated bot GitHub account, `neibaur-ai-bot-1`. Because that file is ignored
by Git, the token stays outside the repository. Claude-created issues, branches,
commits, and pull requests can then be attributed to the bot account instead of
my main `neibaur` identity.

That is a good governance pattern because it narrows the blast radius.
The bot can have tighter permissions, and agent activity stays visibly
separated from my personal GitHub account.

I wanted to know whether the Codex VS Code extension could fit into something
similar.

I explored several options:

- OpenAI API-key authentication for Codex
- VS Code's `Manage Extension Account Preferences`
- Separate VS Code Profiles
- Injecting `GH_TOKEN` through profile-specific terminal settings
- Launching VS Code itself with the bot token already loaded
- Configuring Codex's shell environment policy so subprocesses could see
  `GH_TOKEN`

The first few options did not solve the actual problem.

OpenAI API-key authentication controls Codex and OpenAI authentication. It does
not control the GitHub identity used by `gh`, `git push`, PR creation, or issue
operations.

`Manage Extension Account Preferences` did not expose the Codex extension in a
useful way.

Separate VS Code Profiles helped organize the work, but they did not isolate
GitHub CLI auth state. `gh auth login` is still global on the machine.

Profile-specific terminal settings were also not enough on their own. They can
shape a shell, but they do not automatically constrain the extension host
process or the way the editor itself was launched.

The lesson was becoming clearer:

> A profile is a convenience boundary, not an identity boundary.

The working pattern needed to be layered.

## Building The Bot Environment

The setup that finally made sense was a bot environment rather than a single
setting.

The layers were:

- a dedicated bot clone or folder
- a dedicated VS Code bot profile
- a bot profile terminal that starts PowerShell through a local startup script
- a local secret file stored outside the repo in a gitignored secrets folder
- a startup script that loads `GH_TOKEN` and `GITHUB_TOKEN` into the terminal
- repo-local Git identity configured for the bot account
- Codex shell environment forwarding for `GH_TOKEN` and `GITHUB_TOKEN`
- a separate launcher script that starts VS Code with the bot token already in
  the process environment

That stack is more work than "just use a profile," but it does the job the
profile cannot do by itself.

The bot-specific VS Code launch script was the critical missing piece. It means
the Codex extension host can inherit the bot identity instead of only the
integrated terminal session inside an already-open editor window.

I also hit a small setup bug along the way. The VS Code `settings.json` file
had a malformed JSON object after I accidentally nested a second top-level
block into the main settings structure. That was a good reminder that even the
governance around agent work still has ordinary editor failure modes. The fix
was simple once the problem was visible.

## Validating The Boundary

Once the bot environment was in place, I checked the identity from the
integrated terminal.

```text
gh api user --jq .login
neibaur-ai-bot-1
```

That was the first useful confirmation. It showed that the terminal session was
actually using the bot GitHub account.

I also verified the Git identity settings:

- `git config user.name` returned `neibaur-ai-bot-1`
- `git config user.email` returned the bot commit email
- `git config --show-origin user.email` showed the value coming from the
  repository's `.git/config`

That mattered because it meant the repository itself was carrying the right
identity, not just the shell session.

The next surprise came from Codex itself. It initially did not inherit the
terminal environment. When I asked Codex to run `gh api user --jq .login`, it
failed with a message that effectively pointed back to `gh auth login`. That
was the proof I needed that the integrated terminal and the extension host were
not the same environment.

The fix was to move the token loading one layer earlier.

I created a separate launcher script in the local secrets folder. The launcher
reads the bot token from the local secret file, exports `GH_TOKEN` and
`GITHUB_TOKEN`, and then launches VS Code into the bot profile and bot
repository.

That made the token available to the VS Code process itself, which in turn made
it available to Codex.

After that, Codex could authenticate GitHub CLI operations as
`neibaur-ai-bot-1`.

## Codex Environment Forwarding

I also reviewed the global Codex config at a high level.

The pieces that mattered were:

- Windows sandbox configuration
- `workspace-write` sandbox mode
- network access enabled for the workspace-write sandbox
- the bot repository marked as a trusted project
- `GH_TOKEN` and `GITHUB_TOKEN` explicitly allowed through Codex's shell
  environment policy

Those settings do not replace the launcher script. They complement it. The
launcher gets the right identity into the process tree, and the Codex shell
policy lets that identity survive into the subprocesses that need it.

There was a little network noise while I was validating the setup. `curl.exe`
and `Test-NetConnection api.github.com -Port 443` sometimes behaved oddly
inside Codex's environment even when GitHub CLI worked correctly.

That was useful as a reminder not to overread transport diagnostics when the
real target is application-level authentication. The important success signal
was still the GitHub CLI result:

```text
gh api user --jq .login
neibaur-ai-bot-1
```

## The SSH Alias Trap

One other detail mattered more than I expected.

`gh repo view` failed because the repository remote is configured with the SSH
alias:

```text
git@github.com-agent:neibaur-labs/haomiantiao.git
```

That alias is useful for keeping Git SSH identity separate, but GitHub CLI does
not automatically infer that `github.com-agent` maps to GitHub.

The fix is to be explicit with GitHub CLI commands:

```bash
gh repo view neibaur-labs/haomiantiao --json nameWithOwner --jq .nameWithOwner
```

or to pass `--repo neibaur-labs/haomiantiao` when creating PRs, listing issues,
or using other repository-scoped GitHub CLI operations.

That is a small command-line detail, but it is exactly the kind of detail that
can make an identity-isolation workflow feel flaky if it is not documented and
remembered.

## Why The Day Mattered

The biggest lesson of the day was not about one config file or one launcher
script.

It was about the difference between organizing work and actually isolating
identity.

VS Code Profiles are useful, but they are not sufficient on their own. They do
not cleanly separate GitHub CLI state, they do not automatically define the
extension host environment, and they do not replace repo-local Git identity.

The safer pattern needed all of the following at once:

- a bot-specific VS Code launch environment
- local secret loading outside the repo
- Codex environment forwarding
- repo-local Git identity
- explicit `gh --repo` usage because of the SSH alias

That is a much better story for agentic development than "I switched profiles
and hoped for the best."

It is also a better fit for the course I started today. If the capstone is
going to push me deeper into agentic workflows, then the local operating model
needs to be explicit enough to survive that pressure.

## Outcome

Day 44 turned a vague desire for safer local AI work into a practical identity
boundary.

The day began with the opening session of Kaggle's 5-Day AI Agents: Intensive
Vibe Coding Course With Google. The introduction framed agentic development as
something that needs structure, governance, and practical safety rails, which
fit the rest of the day's work well.

On the technical side, I confirmed that Claude can already use a bot-specific
GitHub token through `.claude/settings.local.json`, keeping the bot identity
isolated from my main account.

I then explored several possible Codex and VS Code identity approaches and
found that neither OpenAI auth nor VS Code Profiles alone solved the problem.
The real solution required a layered bot environment: a dedicated bot clone, a
bot VS Code profile, a local startup script, a local secret file outside the
repo, repo-local Git identity, Codex shell environment forwarding, and a bot
launcher script that starts VS Code with the bot token already loaded.

I fixed a malformed `settings.json` during the setup work, verified the bot
identity through `gh api user --jq .login`, and confirmed the repository-local
Git identity came from `.git/config`.

I also learned that Codex itself needed process-level environment inheritance,
not just terminal-level setup, and that GitHub CLI operations need explicit
`--repo neibaur-labs/haomiantiao` targeting because the SSH remote uses the
`github.com-agent` alias.

The result is a more disciplined local workflow: human identity for human work,
bot identity for agent work, and enough explicit wiring that the boundaries are
visible instead of implied.

## Definition Of Done

Day 44 reached a local identity-isolation checkpoint:

- started Kaggle's 5-Day AI Agents: Intensive Vibe Coding Course With Google
- listened to the opening 20-minute introduction
- treated agentic development as a governance and safety problem, not just an
  experimentation problem
- confirmed the course capstone gives the work a near-term reason to stay
  practical
- verified that Claude can use a bot-specific GitHub token through
  `.claude/settings.local.json`
- kept the Claude bot token outside the repository through a gitignored local
  secret file
- explored OpenAI auth, extension account preferences, VS Code Profiles,
  profile terminal settings, launcher scripts, and Codex shell policy as
  possible identity controls
- confirmed that VS Code Profiles alone do not isolate GitHub identity
- built a layered bot environment around a dedicated clone, bot profile,
  startup script, local secret loading, repo-local Git identity, Codex env
  forwarding, and a bot launcher script
- fixed a malformed `settings.json` during the setup process
- verified `gh api user --jq .login` as `neibaur-ai-bot-1`
- verified repo-local Git identity from `.git/config`
- confirmed that Codex needed process-level environment inheritance
- learned that `gh repo view` needs explicit repo targeting when the remote
  uses the `github.com-agent` SSH alias
- established `gh --repo neibaur-labs/haomiantiao` as the reliable GitHub CLI
  pattern for this repository

The day ended with a clearer local trust model: the editor, the shell, the
agent, and GitHub all need to agree on who is acting, and that agreement has to
be built on purpose.
