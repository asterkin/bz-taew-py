# bluezone-app

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Docs](https://img.shields.io/badge/docs-📘%20available-blue)](./docs/README.md)
[![Last Commit](https://img.shields.io/badge/last--commit-private-lightgrey)](https://github.com/asterkin/bluezone-app/commits/main)
![Platform](https://img.shields.io/badge/platform-Linux-green)

This repository contains **programming language-neutral specifications and assets** for the BlueZone sample application, demonstrating the “Ports and Adapters” architecture pattern featured in the [*Hexagonal Architecture Explained*](https://store7710079.company.site/Hexagonal-Architecture-Explained-p655931616) book.

This pattern—also known as **Hexagonal Architecture**—promotes a clear separation of concerns by defining **ports** (interfaces) through which the core application logic interacts with the external world. These ports are then connected to external systems or technologies via **adapters**.

For a deeper understanding of this architecture, refer to the book [*Hexagonal Architecture Explained*](https://store7710079.company.site/Hexagonal-Architecture-Explained-p655931616) by Alistair Cockburn and Juan Manuel Garrido de Paz.

---

## Language-Specific Implementations

Technology-specific adapters and implementations of the BlueZone application are provided in separate repositories:

- [bluezone-app-py](https://github.com/asterkin/bluezone-app-py) – Python
- [bluezone-app-ts](https://github.com/asterkin/bluezone-app-ts) – TypeScript

> **TODO**: Expand this list as additional implementations become available.

This structure enables flexibility in choosing or switching between technology stacks.

---

The **BlueZone Sample Application** project aims to suggest—without enforcing—a canonical structure for non-trivial applications built using the “Ports and Adapters” architecture pattern.

For more detailed information, see the [documentation](./docs/README.md).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and open pull requests.

## Contact

For any questions or feedback, contact the author, Asher Sterkin, at [asher.sterkin@gmail.com](mailto:asher.sterkin@gmail.com).
