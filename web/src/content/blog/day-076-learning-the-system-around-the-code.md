---
title: "Day 76 - July 16, 2026: Learning the System Around the Code"
description: "A Day 76 reflection on learning Notion during professional onboarding and treating the tools that hold a team's knowledge, decisions, and workflows as part of learning the job."
pubDate: "2026-07-16"
day: 76
dashboardSlug: "none"
dataSources:
  - "Notion documentation reviewed during professional onboarding"
  - "Thirty-minute live Notion training session"
status: "published"
tags:
  - professional-development
  - onboarding
  - notion
  - documentation
  - knowledge-management
  - ai-agents
  - ai-workflows
  - governance
---

Starting a new job has changed how I allocate time.

The hours that might previously have gone toward another implementation now
have to share space with learning a new role, a new organization, and the
systems surrounding its work. On July 16, that meant spending several hours
learning Notion, an important tool in my day-to-day environment.

I worked through at least ten pages of documentation covering different
features and workflows. I also attended an approximately thirty-minute live
training session led by a Notion representative. During that session, the
representative demonstrated how an AI-assisted workflow could be assembled to
help automate recurring tasks.

I did not build that workflow. I did not deploy an agent, complete a workplace
automation, or produce meaningful software implementation. There is no code
artifact from today to inflate into a delivery story.

Today's artifact was a more accurate mental model of the workspace where
future work will be discussed, stored, reviewed, and perhaps eventually
automated.

That is useful onboarding work because learning the tools surrounding the code
is part of learning the job.

## Documents That Behave More Like Systems

Notion begins with a familiar surface: a page where someone can write.

The underlying model is less static than that description suggests. A page is
assembled from blocks. A paragraph is a block, but so is a heading, list,
checkbox, callout, toggle, table, database view, image, video, audio file,
ordinary file, link, code sample, or embedded object.

Those parts can be inserted, moved, nested, transformed, linked, and reused.
A paragraph can become a heading. Supporting detail can sit inside a toggle.
A database view can appear beside explanatory prose. Media and source material
can live in the same working surface as the decision they support.

The result feels less like filling a sheet of paper and more like composing a
small interface. The page still communicates through writing, but its
structure can also guide how someone explores and updates the information.

Familiar Markdown-style input and keyboard shortcuts reduce the friction of
building that structure. I can keep my hands on the keyboard while creating
headings, lists, or code instead of interrupting each thought to search a
formatting toolbar.

One small discovery was especially relevant to engineering documentation.
`Ctrl/Cmd + E` applies inline code formatting. It is useful for a command name,
property, filename, or short value inside a sentence. It does not create a
multiline code block.

A full fenced code block can instead be started by typing three backticks at
the beginning of a line. That block does not have to remain generic. Notion
supports syntax highlighting for more than sixty programming languages, so
selecting the appropriate language can make a script, SQL query, JSON object,
configuration fragment, command sequence, or log excerpt substantially easier
to read.

That distinction matters in an engineering environment. Documentation often
needs to preserve the shape of technical material. Flattening a configuration
example into ordinary prose does not merely make it less attractive. It can
hide indentation, punctuation, and boundaries that carry meaning.

The code block is a small feature. The larger lesson is that useful technical
documentation needs enough structure to keep its evidence legible.

## The Dashboard Was Usually A Set Of Views

I initially described some Notion pages as dashboards. Visually, that was a
reasonable first impression. A page might collect project status, upcoming
work, ownership, and different summaries into one interactive surface.

The more precise mental model is often a page composed from databases and
database views.

Every item in a Notion database is also a page. The database gives those pages
shared properties such as status, owner, date, category, URL, relation,
formula, or progress. The page behind a record can then hold the richer notes,
files, decisions, and context that do not fit neatly into properties.

The same underlying records can appear through different views. One group may
need a table. Another workflow may make more sense as a board, list, calendar,
timeline, gallery, chart, or form. Those views can filter, sort, and group the
records without requiring a separate copy of the underlying information for
each audience.

That made the apparent dashboard easier to understand. It may not be a
conventional analytics dashboard backed by a separate reporting platform. It
may be a carefully arranged collection of linked database views, surrounded
by the prose needed to explain how the team should use them.

This does not make Notion a replacement for a full database server,
business-intelligence platform, or custom application. It does give workspace
information enough structure and interactivity to support workflows that
would be awkward in a collection of isolated documents.

The interesting combination is document flexibility with some of the
structure of a lightweight relational work-management system. A record can be
both a row with predictable properties and a page with human context. A view
can answer a particular operational question without fragmenting the source
records into another spreadsheet.

The power is not in a single database view. It is in the connection between
the view, its records, and the documents around them.

## AI Needs Organized Context

The live training made that connection more important.

The Notion representative demonstrated how an AI-assisted workflow could help
automate recurring tasks. I observed how such a workflow could be assembled;
I did not create a production agent or automate a real process today.

Notion's AI capabilities can work with information already present in pages
and databases. Depending on the plan, permissions, connections, and
configuration available, an agent can help research workspace information,
summarize material, create or edit pages, update database records, prepare
recurring reports, or extract and route tasks. Connected sources can provide
additional context, while configured triggers or schedules can begin
authorized recurring work.

There is an important difference between an interactive request and a durable
automation. A user-invoked Notion Agent can assist with one-time work during a
conversation. Custom Agents can be configured for recurring workflows and can
run in response to schedules or workspace events.

Neither kind of agent eliminates the need to understand the process. An agent
still operates through the context it can access, the permissions it has, and
the instructions it receives. A flexible workspace that has grown without
clear conventions can give both people and AI contradictory names, stale
pages, ambiguous ownership, or several competing sources of truth.

That changes the value of documentation. A page or database record is no
longer useful only when a person remembers to open it. Organized knowledge can
also become context that an authorized AI system uses to answer a question or
perform work.

The reverse is equally important. AI does not make disorganized knowledge
reliable. Its usefulness depends heavily on the quality, structure,
permissions, and freshness of the material available to it.

Before automating a process, I need to understand how the team already works.
Otherwise, automation can make a mistaken assumption recur more efficiently.

## Meeting Notes That Stay Connected

AI Meeting Notes offered a concrete example of knowledge becoming part of a
larger system.

The potential workflow includes transcription, summarization, and extracting
action items. Summary instructions can be customized, and the resulting notes
can be stored in a designated database. From there, meeting knowledge can be
linked to other pages and revisited through search.

The value is larger than receiving a concise recap after a call. A summary in
an isolated document can disappear almost as easily as the conversation it
describes. Notes stored as part of the workspace can remain connected to the
relevant projects, tasks, owners, and decisions. A later search can recover
not only what was discussed but also how that discussion relates to ongoing
work.

I did not personally record or transcribe a meeting today. Any real use of
recording or transcription also requires appropriate participant disclosure,
consent, permissions, and compliance with organizational policy. Technical
availability is not permission.

That boundary belongs inside the workflow rather than in a footnote after it.
A useful knowledge system needs trustworthy inputs and responsible collection
practices before it needs a clever summary.

## A Wiki Needs Maintenance, Not Just Creation

The most interesting part of the documentation was not how quickly a new page
could be created. It was how a page could remain accountable after creation.

A Notion page can be turned into a wiki, allowing important organizational
knowledge to be centralized. Wiki pages can have owners. They can also be
marked as verified, providing a visible indication that someone has confirmed
the information is current.

Verification can last indefinitely or for a defined period. When a
time-limited verification expires, the owner can be prompted to review and
verify the page again. Relevant surfaces, including search results, can show a
verification indicator.

That resembles software governance more than casual note-taking.

Writing documentation once is comparable to shipping code once and assuming
it will remain correct forever. Systems change. Responsibilities move.
Interfaces and policies evolve. Without ownership, review intervals, and a
visible signal of freshness, a polished page can become confidently wrong.

Ownership turns maintenance from an informal hope into an explicit
responsibility. Expiring verification creates a review cycle. The visible
indicator helps readers distinguish knowledge that someone has recently
examined from material whose status is uncertain.

That should also improve the quality of context available to search and AI
systems. Current, well-owned, internally consistent documentation is a better
foundation than abandoned or contradictory pages. I am not claiming that a
verification badge guarantees a particular AI ranking or response. The lesson
is more fundamental: governance improves the trustworthiness of the knowledge
that people and agents are allowed to use.

Flexible tools need this discipline precisely because they make creation so
easy. Without conventions, a workspace can accumulate duplicate databases,
unowned pages, inconsistent properties, and several plausible answers to the
same question.

The wiki model acknowledges that knowledge has a lifecycle.

## Learning The Environment Before Automating It

Onboarding is not limited to checking out a repository, installing a toolchain,
and reading code.

Every organization has an operational layer around the codebase. Decisions
are recorded somewhere. Work is categorized, assigned, and reviewed
somewhere. Meeting context either reaches the next task or disappears.
Documentation either has an owner or slowly becomes historical evidence.

In my new role, Notion participates in that layer. It can function as a
document editor, wiki, task system, structured workspace database, meeting
archive, and interface to AI-assisted work. Learning those connections is more
important than memorizing each menu or shortcut in isolation.

After several hours and at least ten documentation pages, I do not claim
mastery. I now have better questions.

Which databases are authoritative? Which views exist for different teams?
What naming and property conventions keep them coherent? Which wiki pages have
owners and review cycles? Where do meeting decisions become tasks? What can AI
access, and what is it authorized to change? Which recurring work is stable
enough to automate?

The next step is to observe how my actual team has organized its workspace
without exposing or inventing details about that internal environment. Good
automation should follow an understanding of real processes, not a generic
demonstration imposed on them.

Today produced no commit from the learning itself. It still reduced the chance
that I will treat an important database as a static document, mistake a view
for a separate source of truth, or automate a workflow before understanding
its ownership and permissions.

Learning the environment is not separate from doing the work well.

It is how future implementation begins with a better model of the system
around it.

## Outcome

Day 76 was a professional onboarding and structured-learning day rather than a
software implementation day.

I spent several hours learning Notion, reviewed at least ten pages of its
documentation, and attended an approximately thirty-minute live session led
by a Notion representative. The session included a demonstration of assembling
an AI-assisted workflow that could help automate recurring tasks. I observed
the demonstration but did not build or deploy an agent or workplace
automation.

The study connected Notion's block-based document model with its databases and
views, clarified the distinction between inline code and language-aware code
blocks, and refined my use of the word "dashboard." It also explored how AI
Meeting Notes can keep meeting knowledge connected to workspace records, with
the necessary disclosure, consent, permission, and policy boundaries.

The strongest lesson came from wiki ownership and verification. Documentation
becomes more dependable when someone is responsible for it, its freshness is
visible, and review occurs on a defined cycle. That governance matters to the
people reading the workspace and to the quality of context available to
authorized AI systems.

No meaningful software implementation or production code was completed. The
day's useful result was a better model of the operational system surrounding
the code and a clearer reason to understand that system before automating it.

## Definition Of Done

Day 76 reached the workplace-system learning checkpoint:

- followed Day 75 with the July 16, 2026 entry
- treated several hours of Notion study as deliberate professional onboarding
- recorded at least ten documentation pages without inventing their titles
- recorded the approximately thirty-minute Notion-led training session
- described the AI workflow as a demonstration rather than an implementation
- claimed no production agent, workplace automation, ticket, or deliverable
- stated plainly that no meaningful software implementation was completed
- described pages as compositions of movable and transformable blocks
- connected Markdown-style input and keyboard shortcuts to lower writing
  friction
- distinguished `Ctrl/Cmd + E` inline code from a fenced multiline code block
- recorded syntax highlighting for more than sixty programming languages
- explained database items as pages with structured properties
- described multiple views over the same underlying records
- refined the dashboard model into a composition of linked database views
- avoided presenting Notion as a replacement for every specialized system
- distinguished user-invoked Notion Agent work from recurring Custom Agents
- tied AI usefulness to context, permissions, configuration, and instructions
- described AI Meeting Notes without claiming that I recorded a meeting
- included disclosure, consent, permissions, and organizational-policy limits
- treated meeting notes as knowledge connected to projects and decisions
- described wiki ownership, verification, expiration, and review
- avoided claiming that verification guarantees AI search behavior
- connected documentation governance to software governance
- set observation of the team's real workspace as the next learning step
- made understanding the workflow a prerequisite to automating it
