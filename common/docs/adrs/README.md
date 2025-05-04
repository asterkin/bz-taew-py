# Architecture Decision Records (ADRs)

Architecture Decision Records (ADRs) are documents that capture important architectural decisions made throughout the development of the project. They provide a historical record of the decision-making process, the context, and the reasoning behind each decision. ADRs help maintain clarity, consistency, and transparency in the project's architecture.

ADRs are particularly valuable for:
- **Documenting Rationale**: Explaining why certain architectural choices were made, including the trade-offs considered.
- **Facilitating Communication**: Providing a shared understanding among team members, stakeholders, and future contributors.
- **Supporting Evolution**: Helping to adapt the architecture over time while preserving knowledge of past decisions.

To learn more about ADRs and their benefits, you can refer to the original ADR publication by Michael Nygard: [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## ADRs Table of Contents

| ADR Number                                                                  | Title                                                                                | Status   | Date       |
|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------|----------|------------|
| [ADR-001](./adr-001-apply-ports-and-adapters-pattern.md)                    | Apply "Ports and Adapters" Architecture Pattern                                      | Accepted | 2024-09-17 |
| [ADR-002](./adr-002-specify-port-interfaces-as-function-protocols.md)       | Specify Port Interfaces as Function Resolution Protocols and Group by External Actor | Accepted | 2024-09-05 |
| [ADR-003](./adr-003-define-sample-type-as-iterable-float.md)                | Define `Sample` Type as `Iterable[float]`                                            | Accepted | 2024-09-05 |
| [ADR-004](./adr-004-use-google-style-pydoc-format.md)                       | Use Google Style pydoc Format                                                        | Accepted | 2024-09-05 |
| [ADR-005](./adr-005-insulate-application-logic-from-calculation-engine.md)  | Insulate Application Logic from Calculation Engine through a Secondary Port          | Accepted | 2024-09-05 |
| [ADR-006](./adr-006-encapsulate-python-builttin-types-within-port-types.md) | Encapsulate Python Built-in Types Within Port Types                                  | Accepted | 2024-09-06 |
| [ADR-007](./adr-007-domain-model.md)                                        | Domain Model for CypherAI Verity Matcher                                             | Accepted | 2024-09-17 |
| [ADR-008](./adr-008-selected-toolset.md)                                    | Selected Toolset for CypherAI Verity Matcher Project                                 | Accepted | 2024-09-17 |

---

This table will be updated as new ADRs are added to the project.
