# Installation

This repository is intended to be included in a language-specific project as a [GitHub subtree](https://docs.github.com/en/get-started/using-git/about-git-subtree-merges), using the following command:

```shell
git subtree add --prefix=common https://github.com/asterkin/bluezone-app.git main
```

## Installing Common Tools

To install system-wide dependencies common to all language-specific projects (e.g., UML diagram generation), run:

```shell
./common/scripts/install.sh
```

## Updating the Subtree

To pull the latest version of this repository into your language-specific project:

```shell
./common/scripts/pull.sh
```

## UML Diagram Generation

The [Makefile](../Makefile) included in this repository provides a reusable setup for generating UML diagrams from [PlantUML](https://pdf.plantuml.net/1.2021.1/PlantUML_Language_Reference_Guide_en.pdf) source files.

> **TODO**: Add guidelines for how to use the Makefile in language-specific projects.
