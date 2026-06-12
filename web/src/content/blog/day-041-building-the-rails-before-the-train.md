---
title: "Day 41 - June 11, 2026: Building the Rails Before the Train"
description: "Bootstrapping Terminal Run into a governed AI-assisted repository, testing its safety controls, and learning why prevention layers must be challenged before they are trusted."
pubDate: "2026-06-11"
day: 41
dashboardSlug: "none"
dataSources:
  - "Terminal Run repository"
  - "Terminal Run governance documents"
  - "Terminal Run Phase 0 drills"
  - "GitHub Actions"
  - "Gitleaks"
  - "pnpm"
status: "published"
tags:
  - terminal-run
  - ai-governance
  - repository-governance
  - security
  - ci-cd
  - phase-0
  - cost-governance
  - developer-experience
---

Day 41 was boring on purpose.

`Terminal Run` still does not have gameplay. It cannot answer `pwd`, restore a
fractured system, or introduce the player to Patch. What it has now is a
governed repository foundation designed to make those future changes safer.

The day focused on the work that is easiest to dismiss when a new project is
exciting:

- defining what AI agents may and may not do
- establishing human-only repository boundaries
- creating the workspace and validation scaffold
- enabling branch protection and organization rulesets
- installing CI and local prevention layers
- deciding how cost constraints shape the architecture
- running drills intended to prove that the controls actually work

The most important outcome was not that every control worked immediately.

One did not.

The first local Gitleaks hook looked installed, emitted reassuring output, and
allowed a planted secret through. The negative test exposed a real false-pass
before that false confidence could become part of the normal workflow.

That failure clarified the real purpose of Phase 0:

```text
Do not merely install controls.
Try to falsify them before trusting them.
```

## Defining The AI-Assisted Development Contract

The work began by clarifying the role of chat, code sessions, and credentials.

Chat is for planning, reviewing outputs, and writing bounded charters. Code
and agent sessions are for executing those charters inside the repository.
That separation keeps broad reasoning and implementation authority from
quietly collapsing into one unrestricted workflow.

The security model followed the same principle.

GitHub tokens should not be stored in project-level chat context. Chat is not
a secret store. If direct repository verification is ever necessary from
chat, the credential should be short-lived, read-only, fine-grained,
restricted to one repository, and revoked afterward.

The broader rule is simple:

```text
Credentials should be scoped, ephemeral, and revocable.
```

That rule is not specific to one agent or one tool. It is the trust model for
any future automation that needs repository access.

The initial `AGENTS.md` became the binding contract for AI agents working on
Terminal Run. `CLAUDE.md` remained intentionally thin and pointed back to
that shared authority rather than creating a competing set of rules.

The contract established several non-negotiable technical boundaries:

- Terminal Run is a fully simulated terminal, never a real shell.
- Agents may not introduce `eval`, the `Function` constructor, dynamic
  execution, command forwarding, or user-provided code execution.
- Terminal output must remain inert text rather than being rendered through
  `innerHTML` or `dangerouslySetInnerHTML`.
- `packages/engine` must have zero runtime dependencies.
- Dependency changes require an explicit proposal and approval.

It also established repository and workflow boundaries:

- agents must not modify `.github/**`, `AGENTS.md`, `CLAUDE.md`, `LICENSE`,
  repository settings, branch protection, or the scope-exception log
- one task should address one concern through one pull request
- validation must run before a pull request
- tests should come first where they provide meaningful evidence
- human authors retain player-facing fiction and governance documents
- agents may write plumbing, tests, schemas, fixtures, and tooling

The goal was not to make agents passive.

The goal was to make their authority legible.

## Turning Cost Anxiety Into Architecture

Cost governance also became explicit.

A personal-project budget of roughly `$2,000` per year is acceptable. That
does not mean the project should casually spend until it reaches the limit.
It means the project can pay for tools that create real governance or
delivery value while preserving an operating-cost target near `$0` per
month.

The resulting model is:

- keep ongoing operating costs near `$0` indefinitely
- allow deliberate project and tooling spend inside the annual envelope
- avoid uncapped usage-based billing
- require hard spend caps or an explicit exception for usage-based services
- prefer flat-rate tools when they solve the problem well

GitHub Pro and the organization setup were immediately justified because they
enabled enforceable branch protection. A paid CodeQL add-on remained deferred
because Terminal Run is currently static, local-first, and already covered by
cheaper or free safeguards.

The same cost rule influenced hosting and automation.

Static hosting on Cloudflare Pages reduces exposure to usage-driven hosting
and DDoS billing risk. GitHub Actions spending limits should be set at the
organization level. Recurring services should not become architectural
defaults merely because they are convenient during setup.

Cost discipline is therefore part of the safety model.

An architecture that cannot surprise the project with an unbounded bill is
easier to sustain and easier to trust.

## Bootstrapping The Repository And Testing The First Boundary

The first bounded agent charter was Session 0 repository boilerplate.

The session created the initial documentation and configuration scaffold:

- `.gitignore`
- `.editorconfig`
- `.npmrc`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/README.md`
- `docs/event-taxonomy.md`
- `docs/fidelity-exceptions.md`
- `docs/phase-0-drills.md`
- `docs/playtest-observation-template.md`
- 19 ADR stubs

The task also requested `docs/scope-exception-log.md`.

The agent refused to create it because `AGENTS.md` classified the file as
human-only.

That refusal was an early success.

The task prompt and the repository contract conflicted. Instead of silently
choosing the most convenient instruction, the agent followed the higher-level
contract and surfaced the conflict.

This was an accidental preview of the later Boundary Drill. It demonstrated
that the governance document was not merely descriptive text. It could
actually constrain a bounded implementation session.

The next charter created the Phase 0 workspace scaffold.

The scaffold included:

- a pnpm workspace structure
- root scripts for lint, typecheck, test, and validate
- strict TypeScript configuration
- ESLint flat configuration
- Vitest coverage configuration
- `packages/engine` with a trivial `engineVersion` function and a
  no-runtime-dependencies test
- `packages/content` with a placeholder Zod `levelIdSchema`
- `packages/events` with an initial `GameEvent` union and `LocalJournalSink`
- `apps/web` as a minimal Next.js static-export application

This was wiring, not gameplay.

Its purpose was to give the repository enough real structure for CI,
validation, dependency boundaries, and future charters to operate against
something concrete.

## Moving Into An Organization And Enforcing The Rules

The repository moved into the `neibaur-labs` organization:

```text
https://github.com/neibaur-labs/terminal-run.git
```

The move required updating local remotes and confirming that the Code and
Claude GitHub App was authorized for the organization repository.

It also exposed an important branch-protection detail: required status checks
do not appear as choices until those checks have run at least once.

That made the order of operations clearer.

The workspace scaffold and CI checks had to exist and run before the
required-check ruleset could be completed.

Because `.github/**` is human-only, the CI workflow was drafted for manual
entry rather than assigned to an agent. The workflow defined five required
jobs:

- `lint`
- `typecheck`
- `test`
- `build`
- `security`

The workflow used least-privilege permissions, concurrency cancellation, and
SHA-pinned action versions.

SHA pinning initially needed clarification. A pinned SHA points to a specific
commit in the action publisher's repository. It does not refer to a Terminal
Run commit and does not need to change whenever Terminal Run changes.
Dependabot can later propose controlled updates when upstream actions release
new versions.

The security job included:

- Gitleaks scanning
- forbidden-pattern checks for `eval`, `new Function`, `child_process`, and
  `dangerouslySetInnerHTML`
- `pnpm audit`

The first Gitleaks approach used the Gitleaks GitHub Action wrapper. After the
repository moved into an organization, that wrapper required a paid
`GITLEAKS_LICENSE` for an organization-owned private repository.

The project did not buy the license.

The workflow moved to the free MIT-licensed Gitleaks CLI through Docker. That
decision followed the cost rule already captured in ADR 19: prefer free or
hard-capped tooling when it provides the necessary protection.

The security job then failed for a different reason. It attempted to run
`pnpm audit` without installing pnpm in that job.

The fix reinforced a fundamental GitHub Actions rule:

```text
Every job starts on a fresh virtual machine.
Nothing installed in another job is available automatically.
```

The security job gained `pnpm/action-setup` and `actions/setup-node` before
the audit step.

Once the checks had run, branch protection and the main ruleset could be
completed.

The repository now requires pull requests before merging and requires all
five checks. Branches must be up to date before merge. Force pushes and branch
deletions are blocked. Signed commits remain off for now. The repository is
moving toward squash-only merge for a clean conventional history, and
conversation resolution is part of the review posture.

An organization push ruleset also restricts `.github/**` so write-role actors
cannot modify workflows while an administrator can still perform the required
human-only maintenance.

Tag rulesets remain deferred until tag-triggered release workflows exist.

## Choosing Patch's Voice Without Delegating The Fiction

Governance work also reached the style bible.

The companion drone is named Patch.

Patch's default voice is warm, curious, supportive, and peer-like. Patch also
carries a corrupted `Fragment` of the old Weave documentation system. That
Fragment may occasionally surface through formal record-style notation.

The blended voice creates room for warmth and mystery without turning error
feedback into performance.

Several style rules became explicit:

- never joke in error explanations
- keep hints and mistake responses short and supportive
- use the Fragment voice sparingly
- never use the Fragment voice while the player is struggling
- Patch never says `tutorial`, `level`, `XP`, `player`, or `game`
- Named Moments must be caused by the player rather than delivered as
  exposition
- player-facing fiction remains human-authored

That final rule matters in an AI-assisted project.

Agents can help construct the systems that deliver dialogue, validate content
schemas, and exercise fixtures. They do not become the default author of the
voice the player experiences.

The project can use agents heavily without delegating its creative identity.

## Running The Phase 0 Governance Drills

The initial `phase-0-drills.md` focused on application-runtime behavior that
does not exist yet.

It was revised to focus on the governance controls that Phase 0 can actually
test. The original runtime drills were preserved in a deferred appendix for
later, when the game has a runtime worth challenging.

The governance drills then moved from documentation into live tests.

### Secret Drill

A fake AWS-style credential was planted on a branch.

The pull request security check failed at Gitleaks, and merge was blocked.

That proved CI could prevent the credential from reaching `main`. It also
revealed the limit of that protection: CI runs after the secret has already
been pushed into branch history.

A real secret that reaches a remote branch is burned. It must be rotated even
if branch protection keeps it out of `main`.

CI secret scanning is therefore containment, not complete prevention.

### Gauntlet Drill

An `eval(...)` call was added inside `packages/engine`.

Lint failed through `no-restricted-syntax`, and the security forbidden-pattern
check was later confirmed to fail independently as well. Merge was blocked.

The drill proved that two different layers recognize one of Terminal Run's
most important prohibited patterns.

The second run mattered because a layered control is only useful when the
layers have actually been shown to operate independently.

### Direct-Push Drill

A direct push to `main` was attempted.

GitHub rejected it through the ruleset with `GH013`.

That transformed the branch policy from a written expectation into an
enforced repository behavior.

### Boundary Drill

An agent was asked to modify `.github/workflows/ci.yml`.

The agent refused and cited `AGENTS.md` section 3.

That verified the contract layer deliberately, after the Session 0 refusal
had already provided an accidental preview.

A platform-boundary live-fire test remains deferred. As a solo administrator,
testing a separate write-role identity would require additional credential
ceremony that was not justified for this stage.

The drill record was updated with the actual results and follow-up work.

## Learning That Installed Does Not Mean Effective

The Phase 0 drills made one gap especially clear.

CI Gitleaks scanning catches secrets after they reach a remote branch. A local
prevention layer is needed to block staged secrets before the commit and push.

A bounded setup charter added:

- Husky
- lint-staged
- commitlint
- a Gitleaks pre-commit check

Because `.npmrc` sets `ignore-scripts=true`, the setup requires `pnpm prepare`
to run manually after installation. Commitlint correctly rejected a
non-conventional commit message. Lint-staged provided formatting and linting
for staged files. The Gitleaks hook was designed to fail closed so a missing
Gitleaks installation would block the commit rather than quietly pass.

Windows added two local setup lessons.

Gitleaks installed through `winget` was not immediately visible on the
existing PATH, so VS Code and terminal sessions needed to be fully restarted.
Corepack also encountered an `EPERM` error until `corepack enable` ran in an
elevated shell.

The workspace itself needed pnpm rather than npm. The reliable setup path is
to run `pnpm install --frozen-lockfile` from the repository root and let
Corepack enforce the package-manager-pinned pnpm version.

The repository was also moved out of a path containing spaces to reduce
Windows and Git Bash path friction. Prettier warnings appeared likely to be
line-ending related, leading to the addition or consideration of
`.gitattributes` for LF normalization.

Those issues were inconvenient, but they were visible.

The more dangerous problem was a control that looked successful.

A planted-key test was run against the pre-commit Gitleaks hook. The commit
succeeded.

The hook output reported:

```text
0 commits scanned
```

The local prevention layer was installed, active, and ineffective at its main
job.

Investigation identified several causes:

- `gitleaks protect` is removed in Gitleaks `v8.30.1` and no longer provides
  the intended staged-change behavior
- well-known AWS example keys are allowlisted by default and are poor scanner
  acceptance-test inputs
- a standalone `AKIA` access-key ID without a nearby secret is not matched by
  the default rules

The hook was changed to scan the staged diff explicitly:

```text
git diff --cached | gitleaks stdin --redact --no-banner
```

That command gives Gitleaks exactly the content the commit is about to
introduce.

The negative and positive tests then behaved correctly:

- staged fake key pair: blocked
- staged clean file: passed

This was the most valuable lesson of the day.

The first implementation looked plausible. The tool ran. The hook printed
output. The commit workflow continued. Without a planted-secret test, the
project could have treated that appearance as evidence.

Good governance requires trying to disprove the control.

One question remains open: whether Terminal Run should add a custom
`.gitleaks.toml` rule for standalone AWS access-key IDs. If that configuration
is added, it must include:

```text
[extend]
useDefault = true
```

Without that extension, a custom configuration would replace the default
rules rather than supplement them. Both CI Git scanning and the local stdin
hook would then need verification against the configuration.

Phase 0 should not be declared fully finished by quietly ignoring that
decision.

## Handling Dependency Risk As A Separate Concern

Dependabot also reported a PostCSS cross-site-scripting vulnerability.

The fixed version sat outside the transitive range available through the
current dependency graph. The immediate exposure was assessed as low because
PostCSS runs at build time against trusted CSS in a static-export
application.

The recommended correction is a small, atomic dependency pull request using a
top-level pnpm override for PostCSS `>= 8.5.10`, followed by installation,
validation, and a build.

That work should remain separate from the Husky and pre-commit changes.

The alert matters, but combining unrelated dependency and prevention-layer
work would make both harder to review and harder to reverse.

## Recognizing The Reusable Pattern

By the end of the day, the Terminal Run setup had started to look less like
one project's boilerplate and more like a reusable governance pattern.

The reusable pieces divide naturally into two layers.

A template repository could provide:

- GitHub workflows
- Dependabot configuration
- pull request templates
- `CODEOWNERS`
- a generic `AGENTS.md` and thin `CLAUDE.md`
- `.npmrc`, `.editorconfig`, `.gitattributes`, and `.nvmrc`
- shared ESLint, Prettier, TypeScript, and Vitest configuration
- a documentation skeleton
- an ADR template
- empty scope and fidelity logs
- Phase 0 drill templates
- root validation scripts

Organization-level rulesets could provide inherited branch protection and
push restrictions without repeating every setting for every repository.

Some setup remains intentionally repository-specific:

- enable private vulnerability reporting
- confirm Actions permissions are read-only
- disable Actions permission to create or approve pull requests
- set Actions spending limits
- connect the Code app
- run the drills

Templates can make the expected controls easier to install.

They cannot replace proving that those controls work in the new repository.

## Why The Day Mattered

Day 41 did not produce the first Terminal Run command.

It produced the conditions under which the first command can be built with
more confidence.

The agent contract refused a conflicting request. Branch protection rejected a
direct push. CI blocked unsafe code and a planted secret. Organization
rulesets protected human-only workflow files. The style bible preserved a
human-authored player voice. The cost model rejected an unnecessary recurring
license. The local prevention layer failed its first meaningful negative test,
and the failure led to a better implementation.

That last result is the clearest measure of progress.

A weak governance process tries to make the controls look complete.

A useful governance process creates situations where the controls can fail
early, visibly, and safely.

The day moved Terminal Run from an implementation plan into a governed
repository foundation. Phase 0 is close to complete, with the standalone-key
Gitleaks decision still open and the walking skeleton waiting next.

The likely next product milestone remains intentionally small:

```text
Make Terminal Run answer its first simulated command, likely pwd.
```

The setup work was not a detour from building the game.

It established the trust boundary that should let future AI-assisted work move
faster without asking the project to rely on optimism.

## Outcome

Day 41 bootstrapped Terminal Run into a governed, AI-assisted development
environment.

The project clarified the division between chat planning and bounded code
sessions, rejected project-chat token storage, and established scoped,
ephemeral, revocable credentials as the access model. Cost governance became
explicit through a roughly `$2,000` annual envelope, a near-`$0` monthly
operating target, and a prohibition on uncapped usage-based billing.

`AGENTS.md` and `CLAUDE.md` established the binding agent contract. Session 0
created the repository boilerplate and demonstrated the contract when the
agent refused to create a human-only scope-exception log. The workspace
scaffold gave CI meaningful lint, typecheck, test, build, security, engine,
content, event, and web surfaces without beginning gameplay.

The repository moved into `neibaur-labs`, gained five required status checks,
branch protection, and an organization push ruleset for `.github/**`. The CI
workflow used least privilege and SHA-pinned actions. Gitleaks moved from a
paid organization-repository wrapper to the free CLI, and the security job
was corrected after revealing that every GitHub Actions job needs its own
tool setup.

Patch's blended warm and Fragment voice direction was accepted while keeping
player-facing fiction human-authored.

The Phase 0 governance drills proved that CI blocks planted credentials,
prohibited dynamic execution, and unsafe merges; GitHub rejects direct pushes
to `main`; and agents respect protected-file boundaries. The local Gitleaks
pre-commit layer then failed its first planted-key test, exposing a false-pass
before it could become trusted workflow. The hook was corrected to pipe the
staged diff into `gitleaks stdin`, after which a fake key pair was blocked and
a clean staged file passed.

The standalone AWS access-key-ID rule remains an open decision. Phase 0 is
therefore close to complete rather than overstated as finished.

## Definition Of Done

Day 41 reached a governed repository-foundation checkpoint:

- clarified chat as the planning, review, and charter-writing surface
- clarified code and agent sessions as bounded charter-execution surfaces
- rejected storing GitHub tokens in project-level chat context
- established short-lived, read-only, single-repository, fine-grained tokens
  as the model for any future chat-side verification
- established scoped, ephemeral, and revocable credentials as the security
  principle
- accepted a roughly `$2,000` annual personal-project budget
- kept the operating-cost target near `$0` per month
- prohibited uncapped usage-based billing without caps or an explicit
  exception
- approved GitHub Pro and organization setup for enforceable branch
  protection
- deferred a paid CodeQL add-on
- identified static Cloudflare Pages hosting and Actions spending limits as
  cost controls
- drafted `AGENTS.md` as the binding AI-agent contract
- drafted `CLAUDE.md` as a thin pointer to the shared contract
- established Terminal Run as a fully simulated terminal
- prohibited real command execution, dynamic execution, `eval`, the
  `Function` constructor, command forwarding, and user-provided code
  execution
- required terminal output to remain inert text
- required `packages/engine` to have zero runtime dependencies
- established human-only protected repository areas
- required explicit dependency proposals and approvals
- established one-task, one-concern, one-pull-request discipline
- required validation before pull requests
- preserved player-facing fiction and governance documents as human-authored
- completed the Session 0 repository boilerplate scaffold
- created the documentation skeleton and 19 ADR stubs
- confirmed the agent refused to create the human-only scope-exception log
- treated the refusal as evidence that the contract can override a conflicting
  task prompt
- moved the repository into the `neibaur-labs` organization
- updated local remote and application-access expectations after the move
- clarified that required checks must run before they appear in branch
  protection settings
- created the pnpm workspace and strict TypeScript scaffold
- created initial engine, content, event, and static web surfaces
- kept the workspace scaffold focused on wiring rather than gameplay
- manually added CI because `.github/**` is human-only
- established required lint, typecheck, test, build, and security jobs
- used least-privilege permissions and concurrency cancellation
- SHA-pinned GitHub Actions
- clarified how pinned action SHAs and Dependabot updates work
- included Gitleaks, forbidden-pattern checks, and `pnpm audit` in security CI
- replaced the paid Gitleaks Action wrapper with the free Gitleaks CLI
- fixed the security job by installing pnpm and Node inside that job
- enabled branch protection and the main ruleset
- required pull requests and five status checks
- required branches to be current before merge
- blocked force pushes and branch deletion
- kept signed commits off for now
- moved toward squash-only conventional history
- enabled the conversation-resolution recommendation
- restricted `.github/**` through an organization push ruleset
- deferred tag rulesets until tag-triggered releases exist
- selected Patch as the companion drone
- accepted Patch's warm peer voice and sparing Fragment record-notation
- prohibited jokes in error explanations
- kept hints and mistake responses short and supportive
- kept Fragment voice away from player struggle
- kept Named Moments player-caused
- kept player-facing fiction human-authored
- replaced premature runtime drills with governance-focused Phase 0 drills
- preserved runtime drills in a deferred appendix
- confirmed CI Gitleaks blocks a planted credential from merging
- documented that CI does not prevent remote branch-history exposure
- confirmed lint and security grep independently block `eval`
- confirmed direct pushes to `main` are rejected with `GH013`
- confirmed an agent refuses to modify a protected workflow
- deferred the platform-boundary live-fire test
- installed Husky, lint-staged, commitlint, and local Gitleaks prevention
- documented the manual `pnpm prepare` requirement caused by
  `ignore-scripts=true`
- confirmed commitlint rejects a non-conventional message
- resolved Windows Corepack and Gitleaks PATH issues
- established pnpm and `pnpm install --frozen-lockfile` as the workspace setup
  path
- reduced Windows path friction by moving the repository out of a path with
  spaces
- identified LF normalization as the likely correction for Prettier
  line-ending warnings
- ran a planted-key negative test against the local Gitleaks hook
- discovered that the initial hook falsely passed
- identified the removed `gitleaks protect` behavior and unsuitable test-key
  assumptions
- changed the hook to scan `git diff --cached` through `gitleaks stdin`
- confirmed a staged fake key pair is blocked
- confirmed a staged clean file passes
- kept the custom standalone AWS access-key-ID rule as an open decision
- documented that any custom Gitleaks configuration must extend default rules
- identified both CI Git mode and local stdin mode as required verification
  surfaces
- kept the PostCSS advisory correction as a separate atomic dependency change
- identified a template repository and organization rulesets as the reusable
  governance model
- preserved per-repository security settings and drill execution as explicit
  setup work

The day ended with Terminal Run ready to approach its walking skeleton from a
foundation that has already been challenged, corrected, and made more
trustworthy.
