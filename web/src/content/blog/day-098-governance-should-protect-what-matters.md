---
title: "Day 98 - August 7, 2026: Governance Should Protect What Matters"
description: "A Day 98 reflection on AI-assisted security remediation, proportional controls, and putting repository governance at the right boundary."
pubDate: "2026-08-07"
day: 98
dashboardSlug: "none"
dataSources:
  - name: "lingua-core-platform PR 242"
    url: "https://github.com/neibaur/lingua-core-platform/pull/242"
  - name: "100daydash.blog PR 187"
    url: "https://github.com/neibaur/100daydash.blog/pull/187"
  - name: "100daydash.blog PR 188"
    url: "https://github.com/neibaur/100daydash.blog/pull/188"
status: "published"
tags:
  - repository-governance
  - security
  - dependency-management
  - ai-assisted-development
  - developer-experience
  - ci-cd
---

August 7 was mostly a modest tech-debt day. I did not spend a large block of
time building something new. I closed a handful of security findings, thought
more carefully about some repository rules, and came away with a better idea
of what useful governance should accomplish.

The two parts of the day initially looked different. In my personal
repositories, governance limited what an AI agent could change while helping
me investigate dependency vulnerabilities. At work, I reconsidered rules I
had introduced and decided that some of them should become less restrictive.

Both experiences pointed toward the same lesson: governance should reduce
meaningful risk, not simply maximize the number or strictness of rules.

## Detection Did Not Include A Ready-Made Fix

Several GitHub security alerts did not have matching Dependabot pull requests
waiting for me to review and merge. The detection layer had done its job. It
identified vulnerable dependencies and gave me useful findings, but the
automated remediation path stopped there.

That gap matters. Finding a vulnerable package is not always the same as
knowing which direct dependency, transitive path, override, or compatibility
constraint should change. An alert can identify the risk without producing a
safe patch for the repository that contains it.

I copied the finding titles and descriptions into Codex and used it to help
investigate the dependency trees. The useful part was not asking an agent to
make every warning disappear. It was using the agent to connect the alert to a
reasonable remediation path: explain why the package was present, identify
the files or overrides involved, and suggest commands I could run to verify a
change.

Some of my repositories intentionally restrict AI agents from directly
modifying dependency files. When those rules prevented Codex from applying a
change, I did not treat the restriction as an obstacle to work around. The
agent could remain an advisor. It could explain the likely fix, point me toward
the relevant dependency controls, or give me a command to run manually.

That division still provided much of the investigative value while keeping the
actual dependency decision and execution with me. Human control did not mean
working without AI assistance. It meant using the assistance inside an
explicit boundary.

## Closing The Remediation Gap

In
[lingua-core-platform PR 242](https://github.com/neibaur/lingua-core-platform/pull/242),
the resulting work resolved seven GitHub security concerns that did not have
existing Dependabot pull requests I could simply merge. The remediation
involved several dependency updates and overrides, including controls around
`js-yaml`, `fast-uri`, `nanoid`, and `undici`, along with an Astro-related
compatibility adjustment.

The individual package versions were less interesting than the workflow.
Automated detection found the problems. AI-assisted investigation helped trace
reasonable paths through the dependency graph. Repository governance kept the
agent's authority limited, and I retained responsibility for deciding and
applying the changes.

The same pattern appeared in this repository.
[PR 187](https://github.com/neibaur/100daydash.blog/pull/187) updated
transitive dependency controls involving `brace-expansion` and `fast-uri`.
[PR 188](https://github.com/neibaur/100daydash.blog/pull/188) continued the
remediation with controls involving `nanoid`, `postcss`, and `js-yaml`.
Together, those pull requests addressed two more security concerns without
ready-made Dependabot fixes.

This was not a replacement for dependency scanning or automated update tools.
It was a useful bridge when those tools supplied evidence but not a complete
remediation. The agent helped me reason about the gap without needing broader
permission than the repositories allowed.

## A Rule Should Protect Something Important

The professional side of the day pushed the lesson in the other direction. I
spent time reconsidering governance rules I had previously introduced.

It is easy to think of governance maturity as a one-way progression. Add a
check, make it required, prevent a bypass, and repeat. In practice, a control
can be technically enforceable and still provide too little value for the
friction it creates.

One example was a Husky check requiring conventional formatting for every
commit. A teammate did not particularly like the restriction. My first
responsibility was not to defend the rule because I had written it. It was to
revisit what the rule was protecting.

The workflow uses squash merging. The pull request title becomes the clean,
standardized commit message that reaches the important branch history.
Intermediate commits on a feature branch do not have the same long-term role.
Forcing every one of them to match the final convention added friction during
local development without materially improving the history that the team
keeps.

That made loosening the rule the better engineering decision. The desired
outcome still mattered, but enforcing it at every local commit did not.

This was a useful reminder that feedback from the people operating inside a
governed system is evidence. A complaint does not automatically make a control
wrong, but it should prompt a review of the risk, benefit, and placement of the
control. Rules should survive because they protect something important, not
because removing a rule feels like moving backward.

## Block, Warn, Or Remove

I made a similar adjustment to a security-related check. A particular
condition technically matched a rule, but after examining how the team
actually worked, it did not represent a meaningful security problem in that
context.

The choice was not limited to keeping a failing check or disabling security
validation entirely. The condition could become a warning.

That preserved visibility. If the context changes later, the warning still
provides evidence worth examining. At the same time, it stopped a low-risk
condition from blocking work as though it carried the same consequence as a
real security violation.

This distinction seems obvious when stated plainly, but automation makes it
easy to flatten every detected condition into the same response. A check finds
something, exits unsuccessfully, and the pull request stops. Mature governance
needs more judgment than that.

Some violations should block because allowing them through would create an
unacceptable risk. Some conditions should warn because they deserve attention
but not interruption. Some rules may no longer belong because their cost is
not justified by what they protect.

Stricter is not automatically safer. A pipeline filled with low-value blockers
can train people to view governance as noise, search for exceptions, or delay
useful work. Proportional responses make the important failures more credible.

## Put Enforcement At The Boundary That Matters

The commit-formatting example also clarified that the location of enforcement
matters as much as the rule itself.

If a convention only needs to be true when code enters a protected branch, the
pull-request boundary may be the right place to enforce it. PR automation can
inspect a title, metadata, required structure, or another repository standard
before the change becomes part of the lasting history.

That preserves the intended outcome without interrupting every local action
that precedes it. Developers can use intermediate commits in the way that best
supports their work, while the repository still receives a standardized final
commit through the squash merge.

Not every control belongs at the pull-request boundary. Local checks are useful
when fast feedback prevents wasted effort, and required CI checks are valuable
when a failure would make integration unsafe. The point is to choose the layer
deliberately.

Enforcing a standard earlier is only better when the earlier enforcement
meaningfully reduces risk or recovery cost. Otherwise, it may simply spread
the same rule across more of the developer experience.

## Proportional Governance Requires Maintenance

The day's security work and professional reflection were not arguments for
less governance in general. The dependency restrictions did something useful:
they kept an agent from making unapproved changes in a sensitive area. The
security alerts and pull-request checks also provided evidence I needed.

The lesson was that controls have to remain connected to their purpose.

When automated remediation was incomplete, I kept the dependency boundary and
changed how I used the agent. When a commit rule created friction without
improving the final history, I softened the rule and moved attention to the PR
boundary. When a security condition deserved visibility but not a hard stop, I
changed the response from failure to warning.

None of those decisions came from treating governance as unimportant. They
came from asking more specific questions: What risk is this rule controlling?
At what point does that risk become relevant? What evidence should remain
visible? What consequence is proportional when the condition occurs?

I am still learning how to answer those questions. Actually using these
controls with repositories and teammates is exposing tradeoffs that were less
obvious when the rules existed mainly as designs. That feedback is part of the
governance lifecycle. A rule should be reviewed and adjusted just like the
code it governs.

Governance is most useful when it creates the smallest amount of friction
necessary to protect something that actually matters.

## A Milestone Beyond The Repositories

The most important milestone around this day was not technical. My wife
returned to school through Western Governors University and has now completed
her bachelor's degree in accounting. I am proud of what she accomplished and
of the persistence it took to reach this point.

The timing feels fitting as I approach the end of this 100-day effort. Some of
the time and attention I have put into daily technology work can begin shifting
toward helping her explore accounting opportunities, prepare applications and
interviews, and hopefully find a good next opportunity before the end of the
year.

These 100 days were never only about accumulating commits. They helped me build
habits, improve how I work with AI, and become more deliberate about where
automation helps and where human judgment remains necessary. The best result
may be having more capability and attention to apply to the other things that
matter.

## Definition Of Done

Day 98 reached the August 7 proportional-governance checkpoint:

- followed Day 97 with the August 7, 2026 entry
- described the day as modest tech-debt work rather than a major build
- documented nine security concerns resolved across three pull requests
- explained the gap between automated vulnerability detection and ready-made
  remediation
- framed Codex as an investigative advisor operating within dependency rules
- preserved human control rather than bypassing repository governance
- kept professional examples broad and free of identifying details
- reconsidered conventional-commit enforcement in the context of squash merges
- distinguished blocking failures, visible warnings, and rules that may not
  belong
- connected PR-level enforcement to the boundary where a standard matters
- treated teammate feedback and operational experience as governance evidence
- celebrated my wife's WGU accounting degree and the family's next chapter
- connected the end of the 100-day effort to applying its habits beyond the
  repositories
