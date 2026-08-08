---
title: "Day 97 - August 6, 2026: When CI Failure Is Outside the Repository"
description: "A Day 97 reflection on external CI outages, stale workflow state, risk-based governance, and troubleshooting beyond the pull request UI."
pubDate: "2026-08-06"
day: 97
dashboardSlug: "none"
dataSources:
  - name: "GitHub Status: Incident with Actions"
    url: "https://www.githubstatus.com/api/v2/incidents/qcvjkzcs7j74.json"
status: "published"
tags:
  - ci-cd
  - github-actions
  - repository-governance
  - incident-response
  - troubleshooting
  - security
  - ai-assisted-development
---

August 6 was an unexpected lesson in diagnosing a system one layer beyond the
repository.

I had already spent considerable time establishing protected-branch rules and
CI checks. Across roughly 70 pull requests, I had repeatedly watched the same
governance path work: open a pull request, run the required automation, receive
review, and merge only after the evidence was complete.

That history mattered because two teammates began using the workflow in earnest
on August 6, and both encountered strange failures at almost the same time.
Actions checks remained queued or appeared stuck. Copilot review took much
longer than usual. Restarting automation produced inconsistent results. One
check might recover while another continued waiting.

Because this happened just as other people began depending on a workflow I had
built, my first instinct was to question the repository configuration. Several
hours of troubleshooting eventually showed that the controls were not the
source of the failure. GitHub Actions itself was experiencing a major incident.

The day became less about fixing CI and more about learning how to reason when
reliable automation depends on unreliable external state.

## Check The Service Before Rebuilding The System

When the first pull request stalled, investigating the repository was
reasonable. When a second person encountered similar behavior at the same
time, the probability should have shifted more quickly toward a shared external
dependency.

GitHub's public [status incident](https://www.githubstatus.com/api/v2/incidents/qcvjkzcs7j74.json)
confirmed that Actions workflows were failing or delayed in starting, queued
jobs could time out, and API requests could fail. As recovery continued,
GitHub reported that webhook triggers were being throttled, so push and pull
request events were not consistently starting workflows. It also described
runners retrying jobs that were no longer valid, with both GitHub-hosted and
self-hosted runners affected. Copilot code review and the Copilot coding agent
could also experience delays or failures.

Those public symptoms aligned remarkably well with what we were seeing.

GitHub began reporting the incident at 15:22 UTC on August 6. System-wide
queues and webhook throughput did not return to normal until shortly after
midnight UTC, and the incident was marked resolved at 02:04 UTC on August 7.
At resolution time, GitHub said a detailed root-cause analysis would follow.
I therefore know the publicly reported symptoms and recovery behavior, but I
do not know enough to claim a definitive technical cause.

That distinction is useful during an incident. The status page did not repair
our pull requests, but it changed the investigation. Instead of repeatedly
altering known-good repository settings, I could compare our symptoms with the
platform's updates and avoid inventing a local explanation for external
behavior.

My improved troubleshooting order is simple: if multiple previously reliable
workflows begin failing unusually and simultaneously, check the
[GitHub Status page](https://www.githubstatus.com/) early. Local evidence still
matters, but platform health becomes part of that evidence.

## Governance Is A Risk-Control System

The outage also created a governance decision.

The affected pull requests contained very low-risk changes, and the repository
was still early in its lifecycle. The required checks were not reporting failed
code. They were unavailable because verified third-party infrastructure could
not process them reliably.

After waiting without a useful recovery timeline, I temporarily removed the
requirement for the affected checks. This was not a decision to abandon the
checks or weaken the long-term protected-branch model. It was a conscious
response to a specific risk:

1. The changes were low risk.
2. The repository was at an early stage.
3. The disruption was external rather than evidence of a defective change.
4. Any legitimate finding that appeared later could be handled immediately in
   a follow-up pull request.
5. The purpose of the control was to manage engineering risk, not to stop all
   work regardless of context.

The team could continue with other tasks, so bypassing the checks did not
ultimately become necessary to complete the work. Before I finished for the
day, I restored the requirements and left the protected-branch governance
intact.

That sequence matters. Silently leaving a protection disabled after an outage
would turn a temporary exception into policy drift. Recording the reason,
limiting the scope, and restoring the normal rule kept the exception connected
to the risk that justified it.

Strong controls and engineering judgment are not opposites. A control is most
valuable when engineers understand which risk it manages and can evaluate an
exception without treating convenience as evidence.

## Platform Recovery Did Not Recover Every Pull Request

When GitHub Actions recovered, I expected the affected pull requests to recover
with it. Two checks still displayed the equivalent of waiting for a response.

Trying to cancel them in the GitHub interface did not work. The interface said
I was not allowed to perform that action. Because these were not my changes, I
also had no meaningful code update to push merely to generate another event.

This was the point where the incident changed from a service-availability
problem into a state-reconciliation problem.

GitHub's final status updates noted that some workflow-triggering events during
the incident had not been processed and could not be replayed automatically.
Customers might need to repeat a triggering action, update a pull request, or
rerun a workflow where possible. Global platform health therefore did not
guarantee that every individual workflow had reached a coherent state.

That is an important property of distributed systems: recovery of the service
does not necessarily repair every object that passed through it during the
failure window.

## Inspect The State Beneath The Interface

I used Codex with the Luna model as a troubleshooting partner and asked for
terminal commands that could help me inspect what GitHub believed was happening.

The goal was not to make the AI fix the outage. It was to move beyond the one
representation available in the web interface. Using command-line and API
tooling, I identified the relevant workflow and check identifiers, inspected
their reported states, and compared those results with what the pull request
page appeared to show.

The representations did not agree cleanly. A check could present as if it were
still running or waiting in one context while its associated state was already
closed or completed in another. That inconsistency was the clue. I was no
longer looking at a genuinely executing job that needed more time. I was
looking at stale state left behind by the incident.

The practical lesson was broader than GitHub Actions. A user interface is one
projection of distributed system state. It may combine cached data, status
rollups, asynchronous events, and permissions into a convenient view. When the
view stops making sense, the underlying API or CLI representation can expose
the identifiers and state transitions needed to form a better hypothesis.

Codex helped me find appropriate diagnostic paths more quickly. The useful
work was still evidence gathering: inspect the state, compare representations,
and choose the smallest recovery action that fit what the system reported.

## Resetting The Event Worked Better Than Resetting The Job

The eventual recovery mechanism was surprisingly simple: close the pull
request and reopen it.

That lifecycle change caused GitHub to treat the pull request as a fresh event
and trigger the appropriate checks again. Restarting an individual job had not
been enough because the stale condition appeared to sit above that job. A new
pull request event gave the automation a clean path through the recovered
platform.

I would not treat closing and reopening a pull request as a universal remedy
for GitHub Actions problems. It was the pragmatic mechanism that worked in this
specific incident after the broader service had recovered and the underlying
state appeared inconsistent.

The more reusable lesson is to identify the level at which state is stuck.
Repairing a child job may not help when the parent event was never processed
correctly. Sometimes retriggering the higher-level lifecycle is simpler and
safer than trying to repair the orphaned execution state directly.

## Security Evidence Changed While The Work Waited

Once the automation triggered correctly, one more complication appeared.

A dependency and security risk check that had passed earlier now found a new
issue. Enough time had passed during the outage and recovery that the evidence
used by the check had changed.

I created a separate pull request to remediate the newly surfaced dependency
risk. After that fix merged, I updated the affected branch. The previously
stuck pull request ran again against the corrected state, all required checks
passed, and it could be merged normally into the protected branch.

The new finding was inconvenient, but it also demonstrated why continuously
evaluated security checks have value. A green result describes the state and
knowledge available at a point in time. It is not a permanent property of a
branch. New vulnerability information, updated analysis, or a changed base can
produce a different answer later.

The ending was satisfying because I did not ultimately need to bypass the
governance model. Once the external service recovered and the new dependency
risk was addressed, the protections worked exactly as intended.

## Outcome

Day 97 turned several stuck pull requests into a practical lesson about the
boundaries of repository automation.

I spent more time questioning my configuration than I would have liked, but
the repeated failures across multiple users were evidence that the problem
might exist above the repository. The status page confirmed that Actions,
webhook processing, runner assignment, and related Copilot services were
experiencing the same categories of disruption that we observed.

The incident also clarified how I want to handle similar situations. Check
external-service health early. Separate unavailable evidence from negative
evidence. Make governance exceptions according to explicit risk, keep them
temporary, and restore the normal controls. After platform recovery, verify
the state of individual workflows instead of assuming every object recovered
with the service. When the interface is ambiguous, inspect the underlying
state. If a job cannot be repaired, consider whether its higher-level event
needs to be retriggered.

Most importantly, successful CI/CD does not eliminate operational judgment.
Protected branches, automated review, and security checks make changes safer,
but they depend on external infrastructure and time-sensitive information.
Their value comes from understanding what their evidence means, including the
moments when that evidence is temporarily unavailable or newly changed.

## Definition Of Done

Day 97 reached the August 6 external-CI-reliability checkpoint:

- followed Day 96 with the August 6, 2026 entry
- kept the professional setting, employer, repositories, people, architecture,
  identifiers, commands, dependencies, and findings private
- verified the outage symptoms and timeline against GitHub's public status
  incident
- distinguished reported symptoms and recovery behavior from an unpublished
  definitive root cause
- treated simultaneous unusual failures as a reason to check external-service
  health early
- framed protected-branch checks as risk controls rather than immovable goals
- documented the temporary governance exception and restoration of required
  checks
- explained why platform recovery did not guarantee workflow-state recovery
- used CLI and API inspection to reason about stale state beneath the UI
- framed Codex as a diagnostic partner rather than the solution to the outage
- described closing and reopening the pull request as the recovery that worked
  here, not a universal recommendation
- connected the later dependency finding to time-sensitive security evidence
- recorded that remediation restored a clean run through all required checks
  and allowed the protected-branch workflow to complete normally
