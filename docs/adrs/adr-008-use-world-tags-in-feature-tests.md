# ADR-008: Use World Tags in Feature Tests to Support Strong Typing Without Enforcing It

## Status

Accepted

## Context

Each feature test in BlueZone validtates an interaction between an external actor and the system under test. The test environment (`World`) may vary depending on the use case and actor involved. For example, buying a ticket requires access to the payment port, while checking a parked car does not.

In dynamically typed environments, it is feasible to reuse a single, generic world and configure it at runtime. However, in statically typed environments, this approach leads to type inflation, weakened IDE support, and maintenance overhead.

To support both styles without enforcing either, BlueZone adopts a consistent tagging strategy in feature files.

## Decision

1. **All feature files must include a `@world.<actor>` tag**, where `<actor>` corresponds to the initiating driving port for the test scenario.

2. Tag values must follow the naming of primary driving ports defined in [ADR-005](./adr-005-bluezone-application-ports.md), namely:
   - `@world.ForCarDrivers`
   - `@world.ForParkingInspectors`
   - `@world.ForAdministrators`

3. **Typed implementations must use these tags to bind the feature to the appropriate `World` class**, enabling statically typed test contexts.

4. **Dynamic implementations may ignore the tags**, using a generic or runtime-configured world instead.

## Consequences

- Ensures a shared, consistent feature test suite across all language implementations.
- Enables clean separation of world classes in typed environments without imposing structure on dynamic ones.
- Reflects and reinforces actor-centric system modeling by associating worlds with initiating actors.
- Avoids a monolithic, overgeneralized `World` type that breaks modularity and type safety.

## Related

- [ADR-004: Use Gherkin for Acceptance Test Specifications](./adr-004-use-gherkin-for-acceptance-test-specifications.md)
- [ADR-005: BlueZone Application Ports](./adr-005-bluezone-application-ports.md)
- [ADR-006: Provide Full Support for Strong Typing Without Enforcing It](./adr-006-support-strong-type-checking-without-inforcing-it.md)

