---
title: "Day 12 - May 13, 2026: Declarative Agent Development and AccessBridge AI"
description: "Designing AccessBridge AI, an accessibility-focused declarative assistant in Microsoft Copilot Studio Lite, while documenting responsible AI guardrails, trusted-source grounding, and licensing constraints."
pubDate: "2026-05-13"
day: 12
dashboardSlug: "none"
status: "published"
tags:
  - ai-agents
  - accessibility
  - responsible-ai
  - governance
  - copilot-studio
  - founderz
  - no-code
  - enterprise-ai
dataSources:
  - name: "ADA.gov"
    url: "https://www.ada.gov/"
  - name: "Job Accommodation Network"
    url: "https://askjan.org/"
  - name: "RESNA"
    url: "https://www.resna.org/"
  - name: "Microsoft Accessibility"
    url: "https://www.microsoft.com/accessibility"
  - name: "W3C Web Accessibility Initiative"
    url: "https://www.w3.org/WAI/"
  - name: "Microsoft Copilot Studio"
    url: "https://www.microsoft.com/microsoft-copilot/microsoft-copilot-studio"
  - name: "Founderz Agent Explorer"
    url: "https://learn.founderz.com/"
---

Day 12 did not produce a dashboard.

The work focused on declarative AI agent development through the Microsoft
Founderz Agent Explorer challenge. The agent concept was AccessBridge AI, an
Adaptive Technology Resource Guide designed to help individuals with
disabilities, caregivers, educators, employers, and accessibility advocates
better understand assistive technology, workplace accommodations, accessibility
standards, ADA-related guidance, and trusted public accessibility resources.

This was not a day about building a polished production AI system. It was a day
about designing the operating shape of one: purpose, boundaries, trusted-source
grounding, fallback behavior, low-confidence handling, and the very real
enterprise constraints that determine whether an agent can move from
configuration to runtime.

## Goal / Intent

The goal was to design an accessibility-focused assistant using a declarative,
low-code workflow in Microsoft Copilot Studio Lite as part of the Founderz
Agent Explorer track.

AccessBridge AI was scoped as a resource guide, not a legal advisor, medical
provider, benefits administrator, or replacement for human accessibility
professionals. Its intended role was to help users navigate common questions in
plain language, point them toward trusted public resources, and make clear when
a question required professional, organizational, legal, medical, or
case-specific review.

The intended audiences were deliberately broad:

- individuals with disabilities exploring assistive technology
- caregivers helping someone understand available supports
- educators looking for accessibility and accommodation context
- employers thinking through workplace accommodation practices
- accessibility advocates looking for reputable public references

That audience mix shaped the tone. The assistant needed to be calm, plainspoken,
respectful, and careful. It needed to avoid sounding authoritative beyond its
evidence, especially around ADA-related guidance and accommodation decisions
that can depend on context, jurisdiction, employer process, medical details, and
individual need.

## Challenges / Discoveries

The main design challenge was scope control.

Accessibility questions often sit near sensitive domains: disability status,
employment rights, medical needs, school accommodations, procurement decisions,
and legal obligations. A general-purpose assistant can easily drift from
resource guidance into advice that sounds specific, official, or binding. That
is exactly the behavior AccessBridge AI needed to avoid.

The second challenge was hallucination risk.

An assistant that invents an accommodation requirement, misstates an
accessibility standard, or implies that a specific technology is always
appropriate can cause real confusion. Hallucination reduction was not treated as
a vague quality preference. It became part of the agent's core operating model:
ground responses in trusted public sources, distinguish general information from
case-specific decisions, and use fallback behavior when confidence is low.

The third challenge was platform dependency.

The agent configuration and design workflow functioned correctly, but the
current Microsoft 365 Copilot licensing level appeared to block full runtime
execution and live testing. That was not a failure of the design work. It was a
realistic engineering lesson about enterprise AI delivery: agent behavior
depends not only on prompts and knowledge sources, but also on entitlements,
tenant configuration, licensing, governance controls, and platform readiness.

That discovery matters because production AI systems are operational systems.
They inherit the constraints of the platform they run on. A design can be
coherent, responsible, and reviewable while still requiring licensing or
administrative readiness before users can test it end to end.

## Solutions / Work Performed

The first part of the work was defining the agent purpose.

AccessBridge AI was written as an Adaptive Technology Resource Guide. That
framing kept the assistant oriented toward education, navigation, and trusted
resource discovery rather than decision-making on behalf of the user. The agent
was instructed to provide general information, cite or reference trusted public
sources, and remind users when a topic requires qualified review.

The second part was refining governance instructions.

The agent behavior was shaped around several constraints:

- use plain language and avoid unnecessary jargon
- ask clarifying questions when the user's need is ambiguous
- avoid giving legal, medical, financial, or employment determinations
- explain uncertainty instead of hiding it
- redirect users to trusted sources for current rules or formal guidance
- avoid fabricating citations, standards, technologies, or policy requirements
- recommend human review for high-stakes or case-specific decisions

The third part was designing startup prompts for realistic accessibility
interactions.

The initial prompt set focused on questions a real user might ask:

- "What assistive technologies might help someone with low vision at work?"
- "Where can an employer learn about reasonable accommodations?"
- "How do WCAG resources explain accessible web content?"
- "What should I know before asking for an accommodation?"
- "Can you help me compare captioning, screen reader, and speech-to-text tools?"

Those prompts were not written as demo theater. They were designed to expose
whether the agent could stay in scope, communicate plainly, and route users
toward reputable resources without pretending to make final decisions.

The fourth part was trusted-source grounding.

The public sources selected for the first grounding set were:

- ADA.gov for federal ADA information and plain-language civil rights guidance
- AskJAN.org for workplace accommodation examples and employer/employee context
- RESNA.org for assistive technology and rehabilitation engineering resources
- Microsoft Accessibility for platform accessibility features and inclusive
  technology guidance
- W3C Web Accessibility Initiative for web accessibility standards, WCAG
  education, and implementation guidance

These sources gave the agent a healthier operating base than open-ended web
generation. They also made the assistant easier to govern because the response
surface could be evaluated against known public references.

## Technical Observations

Declarative agent development changes where engineering judgment shows up.

In a traditional code-heavy build, a large part of the work lives in functions,
tests, API contracts, and deployment scripts. In Copilot Studio Lite, more of
the engineering surface moves into agent instructions, topic design, knowledge
source selection, fallback behavior, and runtime policy. That does not make the
work less technical. It makes the technical decisions more operational and more
governance-heavy.

Low-confidence handling is a product feature.

For AccessBridge AI, low confidence should not produce a vague answer padded
with confident language. The safer behavior is to acknowledge uncertainty,
explain what kind of information is missing, suggest a narrower question, and
point to a trusted source. In accessibility contexts, "I do not have enough
information to answer that reliably" can be a better answer than a polished
guess.

Out-of-scope behavior also needs to be designed, not improvised.

The assistant should not draft legal conclusions, diagnose disabilities,
determine whether a specific accommodation must be approved, evaluate an
individual's medical eligibility, or speak on behalf of an employer, school, or
government agency. It can explain general concepts, suggest relevant resources,
and help users prepare better questions for qualified professionals.

Grounding reduces risk, but it does not remove responsibility.

Trusted public sources help limit hallucination and improve answer quality, but
they do not guarantee correctness. Sources change. Legal and institutional
processes vary. Accessibility needs are personal and contextual. A responsible
assistant has to communicate those limits clearly.

The licensing discovery was equally technical.

The current Microsoft 365 Copilot entitlement appeared to allow the design and
configuration path while blocking full runtime execution and live testing. That
kind of partial capability is common in enterprise platforms. It creates a
separation between design readiness and operational readiness. For future work,
agent delivery planning needs to include licensing checks, tenant policy review,
admin controls, test-user access, and deployment-path validation before treating
the system as production-testable.

## Definition of Done

Day 12 was complete when:

- AccessBridge AI had a clear purpose as an Adaptive Technology Resource Guide
- the intended audience included individuals with disabilities, caregivers,
  educators, employers, and accessibility advocates
- the assistant was scoped for general resource guidance rather than legal,
  medical, employment, or benefits determinations
- governance instructions emphasized plain language, transparency, uncertainty,
  and responsible escalation
- fallback behavior was designed for ambiguous, high-stakes, or out-of-scope
  questions
- low-confidence handling was treated as expected product behavior
- startup prompts covered realistic accessibility and accommodation scenarios
- trusted public grounding sources were identified
- ADA.gov, AskJAN.org, RESNA.org, Microsoft Accessibility, and W3C WAI were used
  as the core public reference set
- Copilot Studio Lite operational constraints were documented
- the Microsoft 365 Copilot licensing limitation was recognized as an
  entitlement and readiness issue rather than a design failure
- the Microsoft Founderz Agent Explorer track was completed
- the Agent Explorer Certificate of Completion was earned

## Reflection / Lessons Learned

Human-centered AI design starts with restraint.

AccessBridge AI became more useful when it was not asked to be everything. Its
value is in helping users understand options, vocabulary, standards, and
resources. It should make people better prepared for conversations with
professionals, employers, educators, advocates, or agencies. It should not
pretend to replace those relationships.

Accessibility-focused conversational design also requires humility.

People may come to the assistant with frustration, urgency, confusion, or a need
that does not fit neatly into a predefined category. Plain language matters.
Tone matters. Transparency matters. A good answer should reduce burden, not add
new procedural fog.

Trusted-source grounding is a governance control.

For this kind of agent, grounding is not just a quality feature. It is part of
the safety model. Public accessibility resources make the assistant more
auditable, easier to review, and less likely to invent unsupported claims. The
agent still needs guardrails, but the source strategy gives those guardrails
something concrete to hold.

The licensing constraint was one of the most useful discoveries of the day.

It showed that responsible AI work does not stop at prompt design. Enterprise AI
systems depend on identity, entitlements, tenant policy, administrative control,
licensing, user access, and deployment paths. A blocked runtime test is not just
a blocker. It is information about production readiness.

The day closed with completion of the Microsoft Founderz Agent Explorer track
and the Agent Explorer Certificate of Completion. The certificate marked the end
of the learning track, but the more durable takeaway was operational: building
AI agents responsibly means designing behavior, constraints, sources, and
deployment realities together.
