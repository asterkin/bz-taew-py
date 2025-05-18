# ADR-PY-001: Use Mono-Repository

## Status

Accepted

## Context

The BlueZone application follows the ["Ports and Adapters" architecture pattern](../../common/docs/adrs/adr-002-apply-ports-and-adapters-architecture-pattern), which emphasizes clear separation between core logic and external systems. This approach is reinforced by the language-neutral decision to [use separate repositories with Git subtree](../../common/docs/adrs/adr-003-use-separate-repositories-with-git-subtree), allowing shared specifications to be reused across multiple language implementations.

Within a single implementation, however—especially one like Python that favors flexibility and dynamic configuration—a mono-repository (monorepo) is more appropriate than scattering components across multiple repositories.

"Ports and Adapters" encourages defining multiple adapter implementations per port (e.g., real cloud service, local stub, in-memory mock), and organizing reusable combinations into runtime configurations. Managing each adapter in its own repository would quickly lead to an unmanageable proliferation of repositories and complicate project coordination.

Python, the implementation language for this project ([ADR-PY-000](./adr-py-000-use-python-as-implementation-language.md)), is well-suited for a mono-repository approach. It supports dynamic module loading and can manage multiple configurations without enforcing a rigid structure. If needed, isolated virtual environments can be used to support distinct adapter setups or test environments.

## Decision

The Python implementation of BlueZone will use a **mono-repository** structure. All components—core application logic, port definitions, adapter implementations (real and fake), scripts, and documentation—will be maintained in a single repository.

This will allow efficient development, testing, and maintenance of multiple runtime configurations and adapter variants.

The internal structure of the repository will be defined in [ADR-PY-002](./adr-py-002-define-folder-structure.md).

## References

- [ADR-002: Apply "Ports and Adapters" Architecture Pattern](../../common/docs/adrs/adr-002-apply-ports-and-adapters-architecture-pattern)
- [ADR-003: Use Separate Repositories with Git Subtree](../../common/docs/adrs/adr-003-use-separate-repositories-with-git-subtree)
- [ADR-PY-000: Use Python as Implementation Language](./adr-py-000-use-python-as-implementation-language.md)
- [What is a monorepo?](https://monorepo.tools/) – Canonical overview of monorepository principles and trade-offs
