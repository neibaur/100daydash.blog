---
title: "Day 55 - June 25, 2026: Skills, Spreadsheets, and Not Overcalling Hallucinations"
description: "A Day 55 reflection on Microsoft 365 Copilot in Excel, agent skills for spreadsheet workflows, and evaluation discipline in HaoMiantiao PR review skill work."
pubDate: "2026-06-25"
day: 55
dashboardSlug: "none"
dataSources:
  - "Microsoft 365 Copilot in Excel event"
  - "HaoMiantiao PR review skill eval notes"
  - "HaoMiantiao advance.ts review discussion"
  - "reviewing-pull-requests skill v0.2.0 documentation"
  - "HaoMiantiao project handoff notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - copilot
  - excel
  - evals
  - haomiantiao
  - developer-experience
---

Day 55 had two very different surfaces and one shared lesson.

One surface was Excel.

The other was `haomiantiao`.

In the morning, I attended the Microsoft 365 Copilot in Excel session,
[Microsoft 365 Copilot in Excel - transform your spreadsheet workflows](https://msevents.microsoft.com/event?id=3545931614).

That was not a coding session in the usual sense. It was a practical
spreadsheet workflow session: clean up a dataset, shape it into tables, ask
questions in natural language, generate charts, and use the agent as a guided
assistant inside a tool that already owns a large amount of everyday business
data work.

Later, I continued the HaoMiantiao work with Claude around PR review skill
evaluation. That thread was much closer to code, but the underlying question
was the same: what does it mean to delegate work to an agent without letting
the agent become magic?

The answer keeps becoming more specific.

Give the agent bounded capabilities. Make the capability explicit. Make the
result reviewable. Keep durable project artifacts current. Then verify the
claim before turning it into process memory.

That was true in Excel.

It was also true in the review-skill eval work.

## Copilot As Spreadsheet Workflow Assistant

The Microsoft session framed Copilot in Excel as a shift away from manual
spreadsheet labor and toward guided, natural-language workflows.

That does not mean formulas disappear. It means the entry point changes.

Instead of starting every task by remembering the right function, manually
cleaning columns, building a table, and then deciding which chart to try, the
user can ask Copilot to help move through those steps. The demonstrated shape
was familiar but useful: clean up a dataset, create tables, generate charts or
graphs, and analyze data based on specific search criteria.

That is a practical kind of agent assistance.

It is not "replace the spreadsheet user." It is more like adding a guided
workflow layer over a tool people already use for messy, real-world data.

The interesting part for me was not only chart generation or cleanup. It was
the discussion of skills.

The session showed the idea of loading and using skills for data work. Some
skills can be available by default, so the agent decides when to use them.
Other skills can stay off by default and be called individually in a prompt.

That distinction is small, but it matters.

A default-enabled skill changes the agent's ambient behavior. The user does
not have to remember to ask for it, but the agent also has more discretion
about when to apply it. A prompt-invoked skill keeps the activation more
explicit. The user has to call for it, but that call becomes part of the
instruction trail.

Both modes are useful. They carry different governance tradeoffs.

The session also referenced searching for new skills through `skills.re`,
which made the skill idea feel less like a hidden feature and more like a
discoverable extension model. If spreadsheet work can be expanded by finding
and loading task-specific skills, then the agent is not just a chat layer. It
becomes a coordinator over named procedures.

That is the part I keep circling back to.

Good agent workflows need named capabilities. They need scoped activation.
They need enough visibility that a user can understand what kind of help is
being applied to the task.

## Web-Grounded Spreadsheet Analysis

Another pattern from the session was having the agent pull or reason over web
data as part of spreadsheet analysis.

That is a powerful idea.

It is also where governance starts to matter very quickly.

A spreadsheet can feel concrete because it has cells. Rows, columns, tables,
and charts all give the work a visible shape. But once an agent starts using
web data to enrich or interpret that sheet, the source boundary expands.

Where did the outside data come from? Was it current? Was it the right source?
Did the agent summarize it, transform it, or merely retrieve it? Did the final
chart blend spreadsheet data with external assumptions?

Those questions are not reasons to avoid the pattern.

They are reasons to make the pattern explicit.

This is the same governance instinct that has been showing up across the
agent-skill work: agent assistance is most useful when it is reviewable. If
Copilot can help clean data, create tables, generate charts, and reason across
web information, then the workflow should also leave the user with enough
evidence to understand what changed and why.

The magic version is "Copilot made a chart."

The useful version is "Copilot cleaned these fields, created this table,
queried or reasoned over these sources, and generated this chart from that
evidence."

That difference is the whole game.

## Skills As Controlled Delegation

The Excel session connected directly to my ongoing interest in agent skills,
governed workflows, and procedural memory.

A skill is a way to make an agent better at a class of work without rewriting
the user every time. It can encode preferred procedure, tool use, output
shape, review criteria, or domain-specific judgment.

But a skill is also delegation.

That means the question is not only "can the skill help?"

The better questions are:

- when should this skill activate?
- what evidence does it need?
- what output should it produce?
- what should it refuse to do?
- what does the human still need to verify?

The default-enabled versus prompt-invoked distinction from the Excel session
is one concrete version of that control problem.

A default-enabled skill is convenient. It can also become invisible if the
system does not show when it was used. A prompt-invoked skill is less
frictionless, but it makes the handoff clearer.

Neither pattern is universally right.

The useful design choice depends on risk, frequency, and the cost of being
wrong.

For routine spreadsheet cleanup, a default-enabled skill may be exactly right
if the changes are visible and reversible. For a high-stakes analysis that
uses external data, explicit invocation and source review might matter more.

That is the same shape I want in code review assistance.

Let the agent help, but do not let the help erase the control points.

## Returning To HaoMiantiao

The second thread of the day was HaoMiantiao and the PR review skill eval work.

This picked up from the Day 54 concern around the draft
`reviewing-pull-requests` skill. Version `0.2.0` had improved the skill by
adding PR body checks, citation discipline, synthesized-summary labeling, and
clearer model-reporting expectations.

But one open question still needed a more careful classification.

In the earlier PR #28 review discussion, there was a questionable suggestion
around `advance.ts`. The suspicion was that the review skill might have
fabricated a `shouldMaterialize` concept.

That would have been serious if true.

Fabricating a code concept and then reviewing against it is a different
failure than suggesting a refactor name. The first is hallucination. The
second may be a fair improvement suggestion, even if the wording is too
confident.

So we checked the code more carefully.

The relevant behavior was not an unconditional `.push` materialization. It
was gated by an inline composed condition around the target round, the match
count, and winner completion. A real `materializeRound` helper existed, and
the `.push` call used that helper.

That changed the classification.

The better read was not "confirmed fabrication." It was "fair refactor
suggestion, overconfidently phrased."

The review appeared to be suggesting that the inline composed condition could
be extracted into a named concept. It did not prove that the current code was
wrong. It also should not have been written as if the named concept already
existed.

That is a narrow distinction.

It is also exactly the kind of distinction that eval work has to preserve.

## The Evaluator Has To Be Governed Too

The most important lesson from that classification was not about
`advance.ts`.

It was about the evaluator.

If the eval process falsely accuses the reviewer of hallucination, then the
eval process has failed in the same family of way it is trying to detect.

That mattered.

The reviewer should not overstate what the code says. The evaluator should not
overstate what the reviewer did.

Holding both sides to the same standard is part of making the harness
trustworthy.

In this case, the remaining softnesses in the v0.2.0 behavior were real, but
they were not fabrications.

The phrasing around the refactor suggestion was too confident. The
commit-structure observation was more inference than verified fact because the
fixture did not include per-commit patches.

Those are meaningful issues.

They are also different from hallucinating a nonexistent requirement or
inventing code behavior out of nothing.

That classification matters because it changes the product decision. Version
`0.2.0` should not be described as a regression. It should be described as a
genuine improvement over `0.1.0`, while still not ready for promotion.

The README and results documentation were corrected accordingly.

That felt like the honest outcome.

## Draft-Only For The Right Reason

The review skill should remain draft-only for now.

But the reason matters.

It should not remain draft-only because version `0.2.0` regressed. The closer
read says it improved the behavior. It caught more of the right things, made
PR body handling more explicit, avoided the earlier bad citation pattern in
the replay, and kept useful review structure.

It should remain draft-only because the golden set is still too small.

That is a healthier reason.

A few cases can show promising movement. They cannot prove the skill is ready
to govern review.

The current evidence says the skill is moving in the right direction. It also
says the harness needs more cases, better fixture fidelity, and clearer
mechanical checks before promotion becomes reasonable.

That is progress without pretending certainty.

## The Line-Count Gate

One concrete follow-up came out of the PR #28 discussion: add a CI line-count
gate.

The review had surfaced a mismatch between the intended 400-line cap and the
actual PR size. Depending on a self-reported checklist count is too soft. If a
PR is supposed to stay under 400 lines, then CI should be able to count.

That is the kind of governance rule that wants to be mechanical.

Not because humans are careless. Because self-counting is the wrong place to
spend human attention.

If the repo wants a line-count cap, the cap should be checked by tooling. Then
reviewers can focus on whether an exception is justified instead of manually
reconstructing the count.

That pattern keeps appearing:

- move repeatable checks into tools
- keep judgment with humans
- record the result in durable project artifacts

That is how agent-assisted workflows become easier to trust.

## The Handoff Before M5

The other practical outcome was about handoff.

Before starting M5 in HaoMiantiao, the right move is to update the real
committed project state, not rely on chat memory.

That means updating `docs/PROJECT_STATE.md`, recording M4 as done, noting M5
as the next data-package milestone, capturing the skill eval status, and
listing the open tooling items such as the line-count gate.

Then M5 can start in a fresh chat against current repo state.

That may sound procedural, but it is the same controlled-delegation lesson in
another form.

Chat memory is useful while working. It is not the project record.

If the next agent session is going to draft the M5 spec, it should read the
committed project artifact. That artifact should describe what is done, what
is next, and what governance work remains open.

That keeps the agent grounded in the repo instead of the fog of a prior
conversation.

## The Shared Lesson

The Excel session and the HaoMiantiao eval work looked unrelated at first.

One was about spreadsheet workflows.

The other was about PR review skill evaluation.

But both were really about controlled delegation.

In Excel, Copilot skills show how agents can be given task-specific
capabilities for data cleanup, analysis, charting, and web-grounded workflows.
That can make spreadsheet work faster and more approachable, especially when
the agent can guide the user through tasks that used to require remembering
the right sequence of formulas, table operations, and charting decisions.

In HaoMiantiao, the PR review skill work showed the other side of the same
problem. Agents need evaluation harnesses, grounded evidence, careful
classification, and durable project artifacts so we do not over-trust or
over-condemn their output.

The useful pattern is not "let the agent do everything."

It is "give the agent bounded capabilities, then verify the result with
durable evidence."

That applies whether the agent is helping clean a spreadsheet, summarize a
pull request, suggest a refactor, or prepare the next milestone spec.

The agent can be useful.

The agent can also be wrong.

The process has to make both facts survivable.

## Why The Day Mattered

Day 55 mattered because it connected two versions of the same engineering
problem.

Copilot in Excel showed what agent skills look like in an everyday data
workflow: natural-language cleanup, table creation, charting, search-driven
analysis, and potentially web-grounded reasoning inside the spreadsheet
environment.

HaoMiantiao showed what it takes to make those kinds of skills governable:
eval cases, fixture fidelity, classification discipline, documentation
updates, and mechanical checks where process rules can be automated.

The lesson was not anti-agent.

It was the opposite.

Agents become more useful when their work is bounded, named, and reviewable.

Skills are powerful because they turn repeated patterns into reusable
procedure. Evals are powerful because they keep that procedure honest.
Project-state documents are powerful because they keep the next session
grounded in something more durable than memory.

That is the kind of agent workflow I want to keep building toward.

Not magic.

Governed assistance.

## Outcome

Day 55 connected Microsoft 365 Copilot in Excel with the ongoing HaoMiantiao
PR review skill evaluation work.

I attended the one-hour Microsoft event, "Microsoft 365 Copilot in Excel -
transform your spreadsheet workflows," and treated it as a practical example
of agent assistance inside spreadsheet work. The session showed Copilot
helping clean datasets, create tables, generate charts and graphs, and analyze
data based on search criteria. The most interesting part was the skills model:
skills can be available by default so the agent decides when to use them, or
left off by default and called individually in a prompt. The session also
referenced finding new skills through `skills.re` and showed patterns where
the agent can pull or reason over web data as part of spreadsheet analysis.

I then continued HaoMiantiao work with Claude around the PR review skill evals.
We revisited whether a PR review skill finding around `advance.ts` was a
genuine fabrication or a fair refactor suggestion. Manual checking showed that
the `.push` materialization was not unconditional. It was gated by an inline
composed condition involving the target round, match count, and completed
winners, and the real `.push` call used the existing `materializeRound`
helper. That made the better classification "fair refactor suggestion,
overconfidently phrased," not confirmed fabrication.

That classification mattered because the evaluator must be held to the same
standard as the reviewer. The README and results documentation were corrected
so version `0.2.0` of the PR review skill is described as a genuine
improvement over `0.1.0`, not as a regression. The remaining weaknesses were
still real, but they were not fabrications: the refactor suggestion was too
confident, and the commit-structure observation was more inference than
verified fact because the fixture did not include per-commit patches.

The skill should stay draft-only because the golden set is still too small,
not because the `0.2.0` behavior regressed. A concrete follow-up emerged: add
a CI line-count gate so a PR that exceeds the intended 400-line cap cannot
slip through based only on an honor-system self-count.

The handoff lesson before M5 was also clear. Update the committed
`docs/PROJECT_STATE.md`, record M4 as done, note M5 as the next data-package
milestone, capture skill eval status and open tooling items, and then start a
fresh M5 spec-drafting chat against current repo state.

## Definition Of Done

Day 55 reached a controlled-delegation checkpoint:

- attended the Microsoft 365 Copilot in Excel workflow session
- framed Copilot in Excel as practical spreadsheet and agent workflow work
- noted the shift from manual formulas and cleanup toward guided
  natural-language workflows
- captured examples of Copilot cleaning datasets, creating tables, generating
  charts and graphs, and analyzing data from search criteria
- identified Excel skills as the most important governance connection
- distinguished default-enabled skills from prompt-invoked skills
- noted `skills.re` as the referenced place to search for new skills
- connected web-grounded spreadsheet analysis to source and evidence review
- continued HaoMiantiao PR review skill evaluation work with Claude
- revisited the questionable `advance.ts` review finding
- verified that `.push` materialization was not unconditional
- verified that materialization was gated by an inline composed condition
- confirmed that a real `materializeRound` helper exists and is used
- reclassified the issue as a fair refactor suggestion with overconfident
  phrasing
- avoided falsely accusing the review skill of confirmed fabrication
- held the evaluator to the same evidence standard as the reviewer
- corrected the README and results interpretation for skill version `0.2.0`
- described `0.2.0` as a genuine improvement over `0.1.0`
- preserved the remaining concerns as softnesses rather than fabrications
- kept the skill draft-only because the golden set is too small
- identified a CI line-count gate as a concrete follow-up
- clarified the handoff path before M5
- planned to update the committed `docs/PROJECT_STATE.md`
- recorded M4 as done and M5 as the next data-package milestone
- captured skill eval status and open tooling items for the next session
- reinforced the larger pattern: bounded capabilities, grounded evidence, and
  durable artifacts before trust
