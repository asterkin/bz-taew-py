# bluezone-app

This repository contains programming language-neutral specifications and assets for the BlueZone sample application, demonstrating the "Ports and Adapters" architecture pattern featured in the ["Hexagonal Architecture Explained"](https://store7710079.company.site/Hexagonal-Architecture-Explained-p655931616) book.

This pattern, also known as **Hexagonal Architecture**, focuses on the clear separation of concerns by defining "ports" (interfaces) that the core application logic uses to interact with the external world. These ports are then connected to various external systems or technologies using "adapters".

For a deeper understanding of **Hexagonal Architecture**, please refer to the book ["Hexagonal Architecture Explained"](https://store7710079.company.site/Hexagonal-Architecture-Explained-p655931616) by Alistair Cockburn and Juan Manuel Garrido de Paz.

Specific technology adapters implemented in various programming languages are implemented in separate repositories with the following naming convention: `bluezone-app-<language>` (e.g., `bluezone-app-py`, `bluezone-app-ts`), enabling flexibility in selecting or switching to different technology stacks.

**TODO: provide a detailed list of language-specific repositories**

The **BlueZone Sample Application** project aims to suggest, without enforcing, a canonical structure for non-trivial applications built with the "Ports and Adapters" architecture pattern.

For more detailed information, please refer to the [documentation](./docs/README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and open pull requests.

## Contact

For any questions or feedback, feel free to contact the author, Asher Sterkin, at asher.sterkin@gmail.com.

---
