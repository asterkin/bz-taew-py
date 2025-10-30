# Contributing to bz-taew-py

Thank you for your interest in contributing to **bz-taew-py**! This project is part of the taew ecosystem, demonstrating the "Ports and Adapters" architecture pattern in Python.

## AI-Native Development Philosophy

**This is an AI-Native project.** All taew projects are designed to be developed with AI assistance and are optimized for AI-driven workflows.

### Working with AI Actors

We strongly recommend using an **AI Actor CLI or plugin** when contributing to this project.

**Tools used in this project:**
- **[Claude Code CLI](https://claude.ai/code)** - Primary development tool for implementing features, refactoring, and maintaining architecture
- **[Codex CLI](https://github.com/microsoft/vscode-codex)** - Consulted for complex architectural decisions (produces [AGENTS.md](./AGENTS.md))
- **GitHub Copilot** - Useful for code completion and boilerplate generation

Contributors are welcome to use these or other AI assistants. We encourage contributions that evolve AI assistant configurations or update the [AGENTS.md](./AGENTS.md) file with your experiences.

These tools understand the project architecture through [CLAUDE.md](./CLAUDE.md) and can help you:
- Navigate the hexagonal architecture
- Implement new adapters following established patterns
- Maintain consistency with architectural principles
- Run tests and static analysis
- Follow the project's coding conventions

### Why AI-Native?

The taew framework and its sample applications use:
- **Protocol-based ports** for clear interface boundaries
- **Declarative configuration** in `configuration.py`
- **Convention over configuration** to minimize boilerplate
- **Comprehensive documentation** in [CLAUDE.md](./CLAUDE.md) for AI comprehension

This design makes the codebase exceptionally well-suited for AI-assisted development. See [CLAUDE.md](./CLAUDE.md) for detailed architectural principles and patterns.

## How to Contribute

### 1. Types of Contributions Welcome

We welcome:
- **Bug reports** - Clear descriptions with reproduction steps
- **Bug fixes** - Pull requests that fix identified issues
- **Documentation improvements** - Clarifications, examples, corrections
- **Feature proposals** - Open an issue first to discuss
- **New adapters** - Additional implementations of existing ports
- **Test improvements** - Enhanced coverage, better test data

We appreciate your patience as we review contributions carefully.

### 2. Contribution Process

#### Step 1: Fork and Clone
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/bz-taew-py.git
cd bz-taew-py
```

#### Step 2: Set Up Development Environment
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
make sync

# Run tests to verify setup
make test-unit

# Run static analysis
make static
```

#### Step 3: Create a Feature Branch

**For Claude Code CLI or VSCode Plugin users:**

You can use the `/issue-new` slash command for coordinated creation of a GitHub issue and corresponding branch:

```bash
/issue-new <label> "<title>" ["<description>"]
```

Example:
```bash
/issue-new enhancement "Add PostgreSQL storage adapter" "Implement ticket storage using PostgreSQL database"
```

This automatically creates the issue, creates a branch, and switches to it.

**For other users:**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

#### Step 4: Make Your Changes

- Follow the architectural patterns documented in [CLAUDE.md](./CLAUDE.md)
- Add tests for new functionality
- Update documentation as needed
- Run `make all` before committing to ensure quality

#### Step 5: Commit Your Changes
```bash
git add .
git commit -m "Brief description of your changes"
```

**Commit message guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues when applicable ("Fix #123: Description")

#### Step 6: Push and Create Pull Request

**For certified contributors using Claude Code CLI or VSCode Plugin:**

Certified contributors can use the `/issue-close` slash command to automatically commit, push, create a pull request, merge the branch, and close the issue:

```bash
/issue-close
```

This streamlined workflow is available only to contributors with merge permissions.

**For other contributors:**

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Test results (if applicable)

### 3. Pull Request Review Process

**Important: Merge Restrictions**

This repository has **branch protection rules** enabled:
- ✅ Pull requests are required for all changes to `main`
- ✅ At least 1 approval is required before merging
- ✅ Direct pushes to `main` are blocked
- ✅ Force pushes are blocked
- ✅ Only repository maintainers can merge PRs

**What this means for contributors:**
- You can fork, branch, and create pull requests
- **You cannot merge your own PRs**
- The repository owner will review and merge approved changes
- This ensures code quality and architectural consistency

### 4. Code Quality Standards

All contributions must pass:

#### Static Analysis
```bash
make static           # Runs ruff, mypy, and pyright
make ruff-check       # Linting
make ruff-format      # Code formatting
make mypy             # Type checking (mypy)
make pyright          # Type checking (pyright)
```

#### Tests
```bash
make test-unit        # Unit tests
make coverage         # Test coverage report
```

#### Complete Pipeline
```bash
make all              # Runs sync, static, coverage, and benchmarks
```

**Requirements:**
- All tests must pass
- Type checking must pass (strict mode)
- Code must be formatted with ruff
- New features require tests
- Public APIs require documentation

### 5. Architectural Guidelines

This project follows **Ports & Adapters (Hexagonal Architecture)**:

#### Adding New Adapters
1. Define the port interface in `ports/` (if new capability)
2. Implement adapter in `adapters/` (RAM, directory, or new provider)
3. Create `for_configuring_adapters.py` with `Configure` class
4. Register in `configuration.py`
5. Add tests in `test/`

#### Adding New Workflows
1. Create workflow in `workflows/for_<actor>/`
2. Define dependencies as port protocols
3. Implement business logic orchestrating ports
4. Create CLI adapter in `adapters/cli/` if needed
5. Add configuration class
6. Add tests

See [CLAUDE.md](./CLAUDE.md) for detailed architectural documentation.

### 6. Documentation Standards

- Keep [CLAUDE.md](./CLAUDE.md) up-to-date with architectural changes
- Update [README.md](./README.md) for user-facing changes
- Add ADRs (Architecture Decision Records) for significant decisions in `docs/adrs/`
- Include docstrings for public APIs
- Update type hints when modifying signatures

### 7. Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Email**: For security concerns, email [asher.sterkin@gmail.com](mailto:asher.sterkin@gmail.com)

### 8. Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [asher.sterkin@gmail.com](mailto:asher.sterkin@gmail.com).

## Development Tips

### Using AI Assistants Effectively

When using AI assistants (Claude Code, Copilot, etc.):

1. **Share context**: Point the AI to [CLAUDE.md](./CLAUDE.md) for architectural understanding
2. **Use make targets**: Ask AI to run `make static` and `make test-unit`
3. **Verify patterns**: Have AI check that new code follows existing adapter patterns
4. **Generate tests**: AI can help create comprehensive test cases
5. **Refactor safely**: AI can help maintain type safety during refactoring

### Project Structure Quick Reference

```
bz-taew-py/
├── domain/              # Pure data structures (value objects, entities)
├── ports/               # Protocol interfaces (contracts)
├── workflows/           # Business logic (orchestrates ports)
├── adapters/            # Implementations (CLI, storage, etc.)
├── test/                # Unit and integration tests
├── configuration.py     # Dependency injection wiring
└── bin/bz               # CLI entry point
```

### Common Tasks

```bash
# Run specific test file
python -m pytest test/test_specific.py

# Check types only
make mypy

# Format code
make ruff-format

# Run benchmarks
make benchmark

# Generate coverage report
make coverage
```

## Questions?

If you have questions about contributing:
1. Check [CLAUDE.md](./CLAUDE.md) for architectural guidance
2. Review existing code for patterns
3. Open a GitHub discussion
4. Consult your AI coding assistant
5. Email the maintainer

Thank you for contributing to bz-taew-py!
