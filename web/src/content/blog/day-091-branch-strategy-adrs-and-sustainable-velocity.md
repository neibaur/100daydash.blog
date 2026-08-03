---
title: "Day 91 - July 31, 2026: Branch Strategy, ADRs, and Sustainable Velocity"
description: "A Day 91 reflection on matching branch strategy to team needs, treating ADR acceptance as shared agreement, and balancing momentum with stability."
pubDate: "2026-07-31"
day: 91
dashboardSlug: "none"
dataSources:
  - "Professional repository-governance learning notes from July 31, 2026"
status: "published"
tags:
  - repository-governance
  - git
  - branching-strategy
  - architecture-decision-records
  - continuous-delivery
  - collaboration
  - sustainable-velocity
---

July 31 was more reflective than implementation-heavy.

I spent time thinking about two parts of repository governance that can look
simple when a project is small: how changes move between branches and how an
architectural decision moves from a proposal to an accepted standard.

In both cases, speed has real value. A short route from change to integration
keeps work moving. A written decision can give a new repository useful
direction. But speed is only sustainable when the people affected by a change
can understand it, validate it, and support it.

That was the central lesson of Day 91. Velocity is not only the rate at which
code reaches a branch or standards enter a document. It is the rate at which a
team can make progress while preserving stability, shared understanding, and
a trustworthy record of why decisions changed.

## Direct Pull Requests Have Worked Well For My Personal Repositories

Most of my recent personal repository work has used a relatively simple
branching model.

I create a short-lived branch for a feature or maintenance task, open a pull
request directly into `main`, complete the automated checks and review, merge
the change, and remove the branch.

A pull request is the reviewable proposal to combine one branch into another.
In this model, `main` is the latest integrated state, so there are few places a
developer needs to inspect to understand what the repository currently
contains.

That simplicity has several practical advantages:

- branches have less time to diverge
- stale branches are easier to avoid
- integration work is less likely to be repeated across several layers
- the Git history tends to remain more linear
- merges and reverts are easier to reason about
- there is less uncertainty about which branch contains the latest combined
  work

For a small personal project, those benefits are substantial. There are fewer
contributors to coordinate, fewer parallel release timelines, and usually one
current version to support. Adding permanent integration or release branches
would create maintenance responsibilities without necessarily solving a real
problem.

The success of that model does not make it universal.

It means the model fits the coordination and release needs of those
repositories.

## A Larger Team May Need Deliberate Promotion Points

A larger team can face a different problem.

Many developers may be working on features, fixes, and release preparation at
the same time. Some completed changes may need to be tested together before
they reach users. A release may require a stabilization period, formal
approval, or support for more than one production version.

In that environment, merging every approved change directly into the
production branch may not always produce the most stable user experience.

One possible response is a Gitflow-like model. Gitflow is a family of
branching practices that separates development, release preparation, and
production-ready code. A team might use:

- a stable `main` or `master` branch for production-ready releases
- a shared `develop` branch where completed work is integrated
- short-lived feature branches for focused changes
- release branches for final stabilization and testing
- hotfix branches for urgent production corrections

The important value is not the number of branches.

The value is the set of deliberate promotion points. Changes can be combined
in an integration branch, evaluated as a group, stabilized in a release
branch, and promoted to the production branch only after the required
evidence exists.

Those stages can give a team room to coordinate several workstreams without
making every completed pull request an immediate production candidate. They
can also make the distinction between ongoing development and a release being
prepared more explicit.

That may be useful when release management is a separate activity from daily
integration. It is not automatically useful merely because a repository has
many contributors or because the model sounds more formal.

## More Branches Create Their Own Risks

Additional branch layers are not free safeguards.

Every long-lived branch creates another state that the team must understand
and maintain. Integration branches can drift away from production. Release
branches can accumulate fixes that also need to move elsewhere. Developers
may be uncertain whether a correction belongs in a feature branch, the shared
integration branch, the current release branch, or several of them.

The result can include:

- more coordination overhead
- more merge conflicts as branches diverge
- uncertainty about where fixes should be applied
- disciplined back-merges after releases and hotfixes
- a more complicated history
- rollback procedures that must account for several promotion stages

A process intended to reduce production risk can introduce a different form
of operational risk if the team cannot maintain it consistently.

This is why I do not see Gitflow-like branching as the advanced answer and
direct pull requests as the beginner answer. They address different operating
conditions.

A small team with strong automated testing and continuous delivery may move
most effectively with trunk-based development or short-lived branches into
`main`. Another team may have scheduled releases, formal approvals, several
supported versions, or testing that must happen after multiple changes are
combined. Integration and release branches may earn their cost there.

The strategy should match the team's size, release frequency, testing
maturity, deployment process, approval or regulatory requirements, supported
versions, and tolerance for production risk.

Branching complexity should solve a demonstrated coordination or release
problem. It should not be added only to make a repository appear more
enterprise-ready.

## I Also Moved Some Decisions Too Quickly

The day's second lesson came from Architecture Decision Records, or ADRs.

An ADR records an important technical or governance decision together with
its context, alternatives, and consequences. Its value is not only the final
choice. It preserves enough reasoning for a future contributor to understand
why the repository took a particular direction.

While trying to establish a repository quickly, I moved some ADRs from
`Proposed` to `Accepted` before pausing long enough to collect as much feedback
from the wider team as I probably should have.

The motivation was reasonable. I wanted to avoid becoming stuck in planning,
and I wanted the repository to begin with clear standards instead of a long
list of unresolved questions.

Still, an accepted ADR communicates more than personal confidence in an idea.
In a team setting, it can signal that the relevant people have reviewed the
decision and are prepared to work within its consequences.

Moving the status too quickly can create an appearance of agreement before
that agreement fully exists. The immediate setup may move faster, but later
discussion can turn the early decision into cleanup work.

I am now considering additional standards, including feature-naming
conventions. Introducing them responsibly requires feedback and agreement,
not only a well-written rule.

The lesson is not that initiative was wrong.

It is that governance velocity needs to include the time required for shared
understanding.

## Editing History And Evolving History Are Different

That realization creates a practical question for the ADRs that already exist.

Because the repository is still early, should I revise the accepted records?
Or should I preserve them and write new ADRs that amend, clarify, or supersede
the earlier decisions?

Quietly rewriting an accepted ADR can produce a cleaner document, but it can
weaken the historical record. Once a decision has influenced implementation
or team behavior, future readers benefit from seeing both the original
reasoning and the information that caused the standard to evolve.

In many cases, a new ADR is the clearer route. It can:

- reference the earlier decision
- explain what new information or team feedback emerged
- identify exactly what is changing
- mark the previous ADR as amended or superseded when appropriate
- preserve a traceable history of the repository's standards

That approach treats changed judgment as part of the architecture rather than
as an error to erase. It also gives reviewers a focused proposal instead of
asking them to infer the meaning of edits inside a record that was already
accepted.

I do not think that guidance needs to become absolute.

In a very new repository, an ADR may not yet have affected meaningful code,
workflow, or team behavior. A small factual correction or clarification may be
reasonable, especially when the change is transparent and the people involved
are aware of it.

The important requirements are visibility and context. Whether the team edits
an early record or creates a new one, future contributors should be able to
understand what changed, why it changed, and whether the earlier decision
still applies.

## Sustainable Velocity Includes Agreement

Branching and ADRs appear to be different governance topics.

One controls how code moves. The other records how consequential choices are
made. On July 31, they pointed to the same underlying principle.

Practices that work well in a personal repository may not scale directly to a
larger team. Fewer branches reduce complexity, but coordinated testing and
release stability can justify more promotion stages. More process is not
automatically safer, because poorly maintained process creates its own
ambiguity and failure modes.

The same balance applies to decisions. Writing standards quickly can create
momentum, but an `Accepted` label should represent real agreement rather than
the desire to finish setup. Early feedback may feel slower than moving a
document forward alone, yet it can prevent avoidable rework and produce a
standard the team can actually support.

Good repository governance is not the fastest possible creation of rules.

It is the deliberate selection of enough structure to help people coordinate,
validate changes, and recover when assumptions change. Policies should be
allowed to evolve, but that evolution should remain visible. Decisions should
move, but at a pace that preserves both momentum and trust.

That is the kind of velocity I want to optimize: progress that remains stable,
understandable, and supportable after the immediate task is complete.

## Outcome

Day 91 did not represent the implementation of a full Gitflow process or a
large repository milestone.

It was a governance reflection grounded in recent experience. I compared the
short-lived branch model that has worked well in my personal repositories with
the additional integration and release needs a larger team may encounter. I
treated a Gitflow-like structure as one possible response, with deliberate
promotion points as its real value and ongoing coordination as its real cost.

I also recognized that I had moved some early ADRs from `Proposed` to
`Accepted` before gathering as much team feedback as the decisions deserved.
That experience clarified the difference between moving setup forward and
establishing genuine agreement.

For decisions that need to evolve, a new ADR that amends or supersedes an
earlier record will often preserve the clearest history. A transparent small
edit may still be reasonable when a repository is new and the original
decision has not influenced meaningful work.

The right answer depends on context in both cases. Branch strategy should
match the team's release and coordination needs. ADR maintenance should match
the decision's maturity and impact. Sustainable velocity comes from moving
quickly enough to make progress without outrunning stability, feedback, or the
shared record that lets a team understand its own system.

## Definition Of Done

Day 91 reached the July 31 repository-governance reflection checkpoint:

- followed Day 90 with the July 31, 2026 entry
- kept the professional setting, organization, team, repositories,
  applications, business domain, and implementation details private
- described short-lived branches and direct pull requests into `main` as a
  model that has worked for personal repositories
- connected fewer branches to reduced drift, stale state, duplicated
  integration, and ambiguity
- avoided presenting one branching strategy as universally correct
- described a Gitflow-like model as one possible structure for larger-team
  integration and release management
- identified deliberate promotion and validation points as the value of added
  branch layers
- acknowledged coordination, conflict, back-merge, history, and rollback costs
- connected branch choice to team size, release frequency, testing maturity,
  deployment, approvals, supported versions, and production risk
- acknowledged moving some ADRs from `Proposed` to `Accepted` too quickly
- framed the ADR lesson as balancing initiative with wider team feedback
- treated accepted status as a signal of agreement, not merely setup progress
- compared revising early ADRs with amending or superseding them through new
  records
- preserved room for transparent small corrections in very new repositories
- connected visible decision history to future understanding
- framed sustainable velocity as progress that preserves stability, shared
  understanding, and traceable decisions
