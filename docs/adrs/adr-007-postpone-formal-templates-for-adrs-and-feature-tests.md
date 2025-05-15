# ADR-007: Postpone Formal Templates for ADRs and Feature Tests

## Status
Accepted

## Context

As the BlueZone application evolves as a reference implementation of the "Ports and Adapters" architecture pattern, decisions are recorded using Architecture Decision Records (ADRs) and acceptance criteria are captured in structured feature tests.

In many projects, formal templates for ADRs and tests (e.g., standardized headers, sections, naming conventions) are adopted to ensure consistency and support automation. However, enforcing templates without automated validation tools or IDE/editor integration creates unnecessary friction and manual overhead.

Currently, ADRs are produced via structured dialogue with a chat-based assistant (e.g., ChatGPT), which ensures reasonably consistent style, structure, and depth of reasoning. Feature tests are also evolving iteratively alongside architecture decisions, and may eventually require their own standardization. For now, the primary priority is clarity of intent, not conformance to a rigid format.

Furthermore, looking ahead, ADRs are expected to evolve into a machine-readable knowledge base capable of answering architectural questions such as:
- "Why was this decision made?"
- "Is it permissible to do X in this context?"
- "What alternatives were considered?"

Premature standardization around templates may hinder this evolution and reduce flexibility at a stage where architectural exploration is still active.

## Decision

We explicitly postpone the adoption of formal templates for:
- Architecture Decision Records (ADRs).
- Feature test specifications.

At this stage:
- ADRs will continue to be drafted via dialogue with a structured assistant (e.g., ChatGPT), which helps maintain consistency and readability.
- Feature tests will be documented with a focus on clarity and completeness rather than adherence to a template.
- No rigid formatting rules or metadata requirements will be enforced.
- Automation and tooling support (e.g., IDE templates, linters, chat-based validation) may be introduced in the future to support standardization if and when it becomes beneficial.

## Consequences

- Developers are free to focus on substance over structure when documenting decisions and tests.
- Style and structure will remain organically consistent through conversational drafting and review, not enforced templates.
- Future efforts to standardize ADRs or test definitions will be guided by actual tooling needs, not premature process constraints.
- This decision may be revisited when the architecture matures or when automated support for template validation is introduced.
