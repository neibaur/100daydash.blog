---
title: "Day 96 - August 5, 2026: Authenticated Testing Is a Trust Boundary"
description: "A Day 96 reflection on least privilege, secret delivery, test artifacts, and governance for AI-assisted Playwright testing."
pubDate: "2026-08-05"
day: 96
dashboardSlug: "none"
dataSources:
  - "Professional security research notes from August 5, 2026"
status: "published"
tags:
  - ai-agents
  - playwright
  - end-to-end-testing
  - secrets-management
  - least-privilege
  - security-governance
---

August 5 was primarily a research and design day.

I have been thinking about how an AI coding agent could help generate, run,
troubleshoot, and improve Playwright end-to-end tests. That workflow becomes
more complicated when a test must authenticate. The obvious question is where
to put the password, but that is only one small part of the problem.

The broader question is where the trust boundary should sit.

An authenticated browser session can expose much more than the credential used
to start it. Cookies, storage, bearer tokens, request headers, traces, logs,
screenshots, and network activity can all preserve or reveal access after the
application begins using the secret. A safe design therefore has to consider
the identity, session, environment, artifacts, and operating rules together.

I did not select or implement a final approach. The useful outcome was a more
complete set of questions to answer before granting an agent authenticated test
access.

## A Dedicated Identity Is A Starting Point

One option is a dedicated test account used only for agent-assisted testing.
That would separate the agent's activity from a person's account and make the
identity easier to recognize, audit, rotate, or disable.

Separation alone does not make the account safe, however. A dedicated identity
with broad permissions can still expose most of a test environment. The more
important question is whether the identity can be limited to the smallest set
of actions required by the approved scenarios.

That may mean different environment-specific accounts for different test
purposes rather than one powerful account that can exercise every workflow.
It may also mean accepting that some end-to-end scenarios should remain outside
the agent's scope. A test identity should be designed as a non-human identity,
with the same attention given to service accounts and CI automation.

Least privilege creates some operational cost. Narrow accounts require clearer
test boundaries and may need maintenance as scenarios change. Broad access is
more convenient, but convenience can hide how much authority has accumulated.
The design question is not how to let every test run with the least friction.
It is how to grant enough access for an explicit purpose without quietly
granting access to unrelated capabilities.

## The Secret's Location Is Not The Whole Threat Model

A normal local `.env` file is familiar and easy to use with development tools.
It is also easy to read, copy, include in diagnostic context, or accidentally
handle like ordinary configuration. A separate environment file for
agent-driven tests could make the boundary more visible and reduce accidental
reuse, but it would remain a file containing a long-lived secret unless other
controls changed too.

An isolated configuration mechanism could improve separation further. A
password or secrets vault is especially interesting when it can inject a
credential temporarily into a process without placing the value in a prompt or
persistent project file. Short-lived credentials could reduce the window of
use, and rotation could limit the value of material retained unexpectedly.

Those approaches can reduce accidental exposure. They do not make a secret
invisible after use.

Once the browser authenticates, the resulting session may be represented by a
cookie or token. The application may return sensitive values in responses.
Playwright may record traces, browser storage, console messages, screenshots,
or network details to support debugging. An agent allowed to inspect those
artifacts may receive the practical equivalent of access even if it never saw
the original password.

This changed the way I framed secret injection. It is an important control, but
it protects one stage of a longer lifecycle. The lifecycle also includes how
the browser uses the credential, what the test records, who can inspect the
recording, how output is redacted, and when artifacts are deleted.

## GitHub Secrets Solve A Different Part Of The Problem

GitHub secrets are useful for CI pipelines because the automation runs inside
a workflow with a defined secret-delivery mechanism. They can keep credentials
out of source control and support environment-specific approval and access
rules around automated jobs.

That does not automatically solve authenticated testing on a developer's local
machine. A local Playwright process still needs a local path to the credential,
and the agent still operates within the permissions and observable outputs of
that local session. Copying a CI secret into local configuration would move the
problem rather than resolve it.

CI and local execution may therefore need separate delivery models, identities,
and policies even when they exercise similar tests. Treating GitHub secrets as
a universal answer would blur an important boundary between centrally governed
automation and a developer workstation.

## Test Environments Still Contain Sensitive Access

It is tempting to treat lower-environment credentials as low risk by
definition. That assumption needs scrutiny.

A test environment may contain realistic data, connect to shared services, or
use authentication patterns that resemble those elsewhere. Its logs and test
artifacts may travel through systems with different retention policies. An
account intended for testing may also gain permissions over time as new
scenarios are added.

The right conclusion is not that every test credential should be treated as if
it unlocks production. It is that its risk should be assessed from what it can
actually reach and reveal. Restricted test data, environment-specific
identities, short validity periods, rotation, and careful artifact handling can
make the lower environment meaningfully lower risk. The label on the
environment cannot do that work by itself.

## Debugging Artifacts Are Part Of The Access Surface

Playwright's debugging output is one reason end-to-end testing is effective.
Traces can show what happened across a browser session. Screenshots make visual
failures concrete. Console and network logs help distinguish an application
problem from an automation problem.

Those same capabilities complicate claims that an agent is restricted.

If an agent can read browser storage, cookies, request headers, bearer tokens,
responses, traces, screenshots, or console output, its effective access is
defined by that complete view rather than only by whether it can open the
original environment file. A narrowly injected credential can still create a
broadly observable session.

This makes artifact policy part of identity policy. Useful controls may include
redaction, limiting which diagnostics are collected, retaining artifacts only
as long as needed, restricting who or what can inspect them, and ensuring that
test data is appropriate for capture. The exact balance remains unresolved
because removing too much diagnostic evidence can make failed tests difficult
to understand.

The goal is not to eliminate observability. It is to decide deliberately which
evidence is necessary and how its sensitivity will be managed.

## A Development Exception Can Become A Production Pattern

Another concern is how a narrowly approved development practice might evolve.

A test-only identity and a local workflow can appear successful, making it
tempting to reuse the model for production smoke testing. The technical shape
may look similar, but the risk changes substantially when the environment,
data, availability expectations, and consequences of a mistake change.

That transition should not happen through convenience or precedent. Rules need
to distinguish test automation from production validation explicitly. Any
increase in environment sensitivity or account authority should require a new
security review and human approval rather than inheriting approval from a
lower-risk experiment.

This is partly a governance problem. A technically narrow design can expand
gradually as more tests, permissions, and environments are added. Without a
documented boundary, each small extension may look harmless even though their
combined effect creates broad access.

The approval should describe the permitted identities, environments,
scenarios, data, artifacts, and credential lifetimes. Anything outside that
scope should be a new decision.

## Technical Controls And Governance Need Each Other

No single mechanism answered every question I explored.

A stronger model would likely combine least-privilege, environment-specific
test identities with short-lived credential delivery. It would restrict the
data visible to those identities, rotate secrets, redact sensitive output, and
set retention rules for traces and other artifacts. It would also state clearly
that permission for test automation does not authorize production validation.

Governance supplies the boundary that individual controls cannot. It can
require human approval before an agent receives broader access, define who may
change the account's permissions, and trigger a separate review when a workflow
moves to a more sensitive environment.

Technical controls make those decisions enforceable. Governance makes their
intent reviewable and helps prevent a temporary testing exception from becoming
an undocumented permanent capability.

The agent itself is not uniquely dangerous in this model. CI runners, service
accounts, test frameworks, and other non-human identities create comparable
questions about authority, secret delivery, observable output, and auditability.
Agent-assisted testing deserves the same disciplined treatment, adapted to the
fact that the agent may actively inspect diagnostics while troubleshooting.

## Outcome

Day 96 produced a clearer threat model, not a deployed solution.

I moved from asking where an AI coding agent's test password should live to
asking what the entire authenticated workflow could expose. That includes the
account's permissions, the environments and data it can reach, the lifetime of
the credential and session, the browser state created after login, the
debugging artifacts retained by Playwright, and the possibility that a
development practice could later be reused in production.

Secret injection can reduce accidental disclosure, especially when credentials
are temporary and never written to a project file or prompt. It cannot guarantee
that authenticated access remains invisible once the browser starts using it.
The session and its evidence become part of the trust boundary.

My next step is to document that boundary more formally, compare local and CI
secret-delivery approaches, define artifact and redaction requirements, and
identify the minimum test scenarios and permissions that would be useful. Only
after that work should an approved model grant an agent authenticated test
access.

## Definition Of Done

Day 96 reached the August 5 security-research checkpoint:

- followed Day 95 with the August 5, 2026 entry
- treated the work as investigation and architectural questioning rather than
  a completed implementation
- considered a dedicated test identity without assuming dedicated means safe
- compared broad access with scenario-specific least privilege
- distinguished normal `.env` files, isolated local configuration, vault-based
  injection, and CI secret delivery
- explained why GitHub secrets do not automatically solve local authenticated
  Playwright execution
- treated cookies, tokens, traces, logs, screenshots, storage, headers, and
  network activity as part of the access surface
- recognized that lower-environment credentials and realistic test data can
  remain sensitive
- connected secret rotation, short lifetimes, redaction, and artifact retention
  to the complete credential lifecycle
- separated test automation approval from any future production validation
- required a new review and human approval before increasing agent access
- kept the professional context deliberately general and confidential
- ended with threat-boundary documentation and approach comparison as the next
  steps before authenticated access is granted
