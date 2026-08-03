---
title: "Day 93 - August 2, 2026: Readiness Needs Evidence"
description: "A Day 93 reflection on rescheduling the DP-700 exam, confronting preparation gaps, and clearing security debt across two related portfolio repositories."
pubDate: "2026-08-02"
day: 93
dashboardSlug: "none"
dataSources:
  - name: "Kamolwan portfolio platform pull request 10"
    url: "https://github.com/neibaur/kamolwan-portfolio-platform/pull/10"
  - name: "Isaac Neibaur portfolio platform pull request 14"
    url: "https://github.com/neibaur/isaacneibaur-portfolio-platform/pull/14"
status: "published"
tags:
  - microsoft-fabric
  - certification
  - security-maintenance
  - dependency-management
  - dependabot
  - technical-debt
---

August 2 did not follow the plan I had expected.

The morning was supposed to end with me taking the Microsoft Fabric DP-700
certification exam. Instead, it exposed two different kinds of readiness: my
readiness for the assessment and my computer's readiness for an
online-proctored exam.

Neither was where it needed to be.

Later, security maintenance across two related portfolio repositories offered
a more concrete result. The implementation was complete because the changes
were validated and the outstanding findings were cleared, not simply because
I had edited two lockfiles.

Together, those experiences reinforced a lesson that applied equally well to
learning and maintenance: readiness should be demonstrated through evidence,
not assumed from familiarity.

## A Practice Score Made The Preparation Gap Measurable

I did not sleep particularly well because I knew I needed to get up early for
the exam. I had delayed preparing and did not feel nearly as ready as I should
have.

Before the appointment, I completed the full Microsoft-provided practice
assessment. I scored approximately 60%. Microsoft recommends reaching around
80% before treating the practice result as a strong readiness signal, so my
score confirmed that I still had meaningful gaps.

That was more useful than a vague feeling of unease. I was familiar with much
of the subject, but familiarity had allowed me to overestimate how reliably I
could retrieve details and choose between plausible answers. The score turned
that impression into measurable evidence.

Under normal circumstances, I would have postponed the exam. I had already
passed the deadline for changing the appointment at least 24 hours in advance,
however, so I believed I had no choice but to proceed.

The situation was partly of my own making. I should have prepared earlier and
used practice results sooner. At the same time, the assessment did what a good
readiness check should do: it showed me where I stood before the higher-stakes
event began.

## The Testing Environment Was Not Ready Either

When I logged in for the online-proctored exam, a sequence of technical
problems began.

My webcam initially did not work. I found the correct cable and reconnected
it, only to discover that my audio was then unavailable. My desk had been
configured for my work computer during the previous two weeks rather than my
personal computer, so I had to rearrange more connections before the webcam,
microphone, and other hardware checks passed.

The exam software then required me to force-quit several running applications.
After closing them, I encountered what appeared to be another firewall or
connectivity problem. I tried to troubleshoot it, but the exam system
eventually apologized for the technical problems and offered me the option to
reschedule.

The exam never properly began. I did not reach or attempt the actual exam
questions, and this was not a certification attempt that produced a pass or a
fail.

Although the technical failure was frustrating, the rescheduling option
ultimately worked in my favor. The practice result had already shown that I was
not adequately prepared. I moved the exam to September, giving myself time to
review the material deliberately instead of relying on familiarity and a
last-minute push.

I do not want to treat the technical trouble as an accomplishment or blame the
exam provider for the outcome. The useful part was the reality check. An
online exam depends on both subject preparation and a tested environment. In
this case, I had assumed too much about both.

For the next appointment, preparation needs to include structured study,
stronger practice results, and an earlier end-to-end check of the personal
computer, camera, microphone, required software, and network path. Readiness
is broader than knowing the syllabus.

## A Proven Security Fix Could Be Reused Carefully

The day's more concrete success came from two portfolio repositories with
closely related structures:

- [kamolwan-portfolio-platform pull request 10](https://github.com/neibaur/kamolwan-portfolio-platform/pull/10)
- [isaacneibaur-portfolio-platform pull request 14](https://github.com/neibaur/isaacneibaur-portfolio-platform/pull/14)

Each repository had two Dependabot findings involving transitive development
dependencies of `markdownlint-cli2`. One affected `js-yaml`, where YAML
merge-key chains could cause quadratic CPU consumption. The other affected
`linkify-it`, where its `mailto:` validation path could also lead to
quadratic-complexity denial of service.

The two sites shared the same underlying dependency pattern, so the first fix
provided a proven remediation for the second. In both repositories, I updated
the pnpm override for `js-yaml` from version 4.2.0 to 4.3.0, added an override
for `linkify-it` 5.0.2, and regenerated `pnpm-lock.yaml` so the resolved
dependency graph matched the declared policy.

That reuse was efficient, but it still required applying and validating the
change separately in each codebase. Similar structure made the solution
transferable; it did not make verification optional.

## Security Work Ends With Verification

Changing a package version is an action. Clearing the security condition
without breaking the project is the outcome.

Both pull requests recorded the same verification evidence:

- `pnpm audit` reported zero vulnerabilities
- the repository's full `pnpm validate` command passed
- `git diff --check` passed
- the Hugo production build completed successfully
- Dependabot alerts 4 and 5 were resolved

The builds continued to report existing upstream deprecation warnings, but
those warnings were unrelated to these changes. Keeping that distinction
visible matters. A focused security patch should resolve the findings in scope
without claiming to eliminate every maintenance concern in the repository.

Both pull requests were merged after the checks passed. Each repository's two
outstanding security findings were fully cleared.

This was modest maintenance work, but it was worth doing. Security alerts are
easy to leave in place when they affect development tooling rather than the
main application path. Allowing them to accumulate still creates debt. It
weakens the signal from future alerts and leaves known dependency problems for
someone to rediscover later.

Overrides and lockfiles also need ongoing attention. An override expresses an
intentional dependency decision, while the lockfile records the graph that the
package manager will actually install. Keeping both current makes the
remediation reproducible and reviewable.

## Evidence Changed The Meaning Of The Day

The morning and afternoon produced very different feelings, but the same
standard applied to both.

My familiarity with Microsoft Fabric did not prove that I was ready for the
DP-700 assessment. The approximately 60% practice score showed that my current
recall and decision-making were below the level I wanted. Rescheduling for
September created an opportunity to respond to that evidence with a more
intentional study plan.

Likewise, editing package configuration in two repositories did not prove that
the security work was complete. The clean audit, passing validation, successful
production builds, merged pull requests, and cleared alerts supplied that
evidence.

Not every productive day follows its expected plan. August 2 did not end with
a certification attempt, and I should not pretend the technical interruption
was a substitute for better preparation. It did, however, replace an
assumption with a useful measurement.

The portfolio maintenance supplied the clearer success: two related
repositories, one carefully reused remediation pattern, and four resolved
security findings. In both parts of the day, the most reliable conclusion came
from what I could verify rather than what felt familiar.

## Outcome

Day 93 became a lesson in evidence-based readiness.

The DP-700 exam never properly began because of technical problems during the
online-proctoring setup. Before that point, an approximately 60% score on the
official practice assessment had already shown that I needed more preparation.
I rescheduled the exam for September and now have time to approach both the
material and the testing environment more deliberately.

I also completed matching dependency-security fixes in two closely related
portfolio repositories. Each change upgraded the `js-yaml` override, added a
`linkify-it` override, regenerated the pnpm lockfile, passed the repositories'
validation and production builds, returned a clean audit, and resolved two
Dependabot findings.

The day did not produce the result I expected in the morning. It did produce a
better standard for the next attempt and a verified maintenance result in the
afternoon.

## Definition Of Done

Day 93 reached the August 2 readiness and security-maintenance checkpoint:

- followed Day 92 with the August 2, 2026 entry
- acknowledged delayed preparation without turning the reflection into
  excessive self-criticism
- reported the approximately 60% official practice-assessment score as a
  readiness signal
- did not claim that the actual DP-700 exam began, was failed, or was passed
- described the online-proctoring problems without treating them as an
  accomplishment or assigning blame
- recorded that the exam was rescheduled for September without inventing an
  exact date
- distinguished subject readiness from testing-environment readiness
- linked both portfolio security pull requests
- described only dependency changes supported by the pull-request diffs
- identified `js-yaml` 4.3.0 and `linkify-it` 5.0.2 as the remediated versions
- explained the role of pnpm overrides and the regenerated lockfiles
- recorded the clean audits, passing validation, clean diff checks, and
  successful Hugo production builds
- distinguished unrelated upstream deprecation warnings from the security
  findings in scope
- confirmed that two Dependabot findings were resolved in each repository
- connected both themes through evidence-based readiness
