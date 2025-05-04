# BlueZone Application Documentation

This documentation provides a comprehensive overview of the **BlueZone** project, including its use cases, architectural decisions, and key terms and concepts.

## Documentation Contents

- **[Glossary](./glossary.md)**: Definitions of key terms and concepts used throughout the project documentation.
- **[Use Cases](./use-cases/README.md)**: Detailed specifications of the various use cases supported by the system.
- **[Architecture Decision Records (ADRs)](./adrs/README.md)**: Documentation of key architectural decisions made throughout the development process.

## How to Use This Documentation

- Start with the **Glossary** to familiarize yourself with the terminology.
- Review the **Use Cases** to understand the specific scenarios the system addresses.
- Explore the **ADRs** to learn about the architectural choices and rationale behind the project's design.

For a high-level overview of the project goals and details, please see the [top-level README](../README.md).

## Use Case Model

The formal use case model of the Blue Zone application is provided in the [use-cases README](./docs/use-cases/README.md). This document details the application's core use cases, including their actors, flows, and alternative scenarios.

**TODO: move to the first ADR**
You can also view the UML class diagram illustrating this architecture in the context of the Blue Zone application [here](./docs/diagrams/bluezone-ports-and-adapters.png).
**TODO: provide an updated UML diagram**

## Acceptance Tests

Acceptance test suite for the BlueZone application, derived from its [use-cases](./docs/use-cases/README.md), is specifed in a programming language and technology neutral form thus allowing to ensure application behaviour while varying underlying technology choices.

## Installation

This is reposiotry is supposed to be included in a programming language specific repository as a [github subtree](https://docs.github.com/en/get-started/using-git/about-git-subtree-merges) using the following command:

```shell
# Add as subtree named 'common'
git subtree add --prefix=common https://github.com/asterkin/bluezone-app.git main
```

To install system modules, common for all programming languages (e.g. UML diagrams generation), invoke:

```shell
./scripts/install.sh
```

## UML Diagrams Generation

The Makefile included in this repository provides a generic solution for generating UML diagrams from the [PlantUML](https://pdf.plantuml.net/1.2021.1/PlantUML_Language_Reference_Guide_en.pdf) specification source file.
***TODO: guidelines how to use it the language-specific projects***
