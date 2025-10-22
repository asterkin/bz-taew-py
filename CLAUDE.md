# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **bluezone-app-py** project - a Python implementation of the BlueZone parking ticket application, showcasing the "Ports and Adapters" architecture pattern. This project builds upon the [bluezone-app](https://github.com/asterkin/bluezone-app) repository (included as a subtree under `common/`) and uses the [taew-py](https://github.com/asterkin/taew-py) library for the Ports & Adapters framework.

## Development Commands

This project uses UV for dependency management and a root-level Makefile for task automation.

### Testing and Coverage
- `make test-unit` - Run unit tests using unittest discovery from `./test` directory
- `make coverage` - Run full test suite with coverage analysis
- `make erase-coverage` - Clean coverage data
- `make combine-coverage` - Combine coverage data from parallel test runs
- `make report-coverage` - Display coverage report

### Static Analysis
- `make static` - Run all static analysis tools (ruff, mypy, pyright)
- `make ruff-check` - Run ruff linting (excludes `./typings`)
- `make ruff-format` - Run ruff formatting
- `make mypy` - Run MyPy type checking on source and `./bin/bz`
- `make pyright` - Run Pyright type checking on source and `./bin/bz`

### Benchmarks
- `make benchmark` - Run performance benchmarks (currently: ticket storage)

### Development Workflow
- `make sync` - Sync dependencies using `uv sync`
- `make all` - Execute complete pipeline: sync, static analysis, coverage, and benchmarks

## Architecture

This application implements the **Ports & Adapters (Hexagonal Architecture)** pattern using the [taew-py](https://github.com/asterkin/taew-py) framework. The architecture separates the BlueZone parking domain logic from external dependencies through well-defined interfaces (ports).

### Project Structure

```
bluezone-app-py/
├── domain/              # BlueZone domain models
│   ├── payment_card.py  # Payment card value object
│   ├── rate.py          # Parking rate value object
│   └── ticket.py        # Parking ticket entity
├── ports/               # Port interfaces for external dependencies
│   ├── for_car_drivers.py         # Interface for car driver operations
│   ├── for_making_payments.py     # Payment processing interface
│   ├── for_parking_inspectors.py  # Parking inspector operations
│   ├── for_storing_rates.py       # Rate storage interface
│   └── for_storing_tickets.py     # Ticket storage interface
├── adapters/            # Adapter implementations
│   ├── cli/             # CLI-specific adapters
│   ├── dir/             # Directory-based storage adapters
│   └── ram/             # In-memory storage adapters
├── workflows/           # Application workflows (use cases)
├── test/                # Unit and integration tests
├── bin/                 # Executable scripts
│   └── bz               # Main CLI entry point
├── configuration.py     # Port-to-adapter wiring configuration
└── common/              # Shared specifications from bluezone-app (subtree)
```

### Domain Layer

**Domain Models** (`domain/`):
- `payment_card.py` - Represents payment card details (card number, CVV, expiry)
- `rate.py` - Parking rate information (zone, hourly rate)
- `ticket.py` - Parking ticket (registration, zone, payment details, timestamps)

These models contain the core business logic and are independent of any infrastructure concerns.

### Ports Layer

**Port Interfaces** (`ports/`):
Defines the contracts that adapters must implement to provide infrastructure capabilities:

- `for_car_drivers.py` - Operations for car drivers (check parking, buy tickets)
- `for_making_payments.py` - Payment processing capabilities
- `for_parking_inspectors.py` - Ticket verification for inspectors
- `for_storing_rates.py` - Rate persistence interface
- `for_storing_tickets.py` - Ticket persistence interface

All ports use Python protocols for type safety and follow dependency inversion principles.

### Adapter Layer

**Adapter Implementations** (`adapters/`):

- **CLI Adapters** (`adapters/cli/`) - Command-line interface implementations
- **Directory Storage** (`adapters/dir/`) - File system-based persistence
- **RAM Storage** (`adapters/ram/`) - In-memory storage for testing/development

Adapters are configured in `configuration.py` using the taew-py framework's port binding system.

### CLI Application

**Entry Point** (`bin/bz`):
The main CLI executable that:
1. Loads port configuration from `configuration.py`
2. Uses taew-py's `Bind` mechanism to wire ports to adapters
3. Delegates to taew-py's CLI framework for command routing and execution

The CLI automatically discovers commands from the workflow layer and provides a dynamic command-line interface.

### Configuration

**Port Wiring** (`configuration.py`):
Defines `ports_root` and `launch_ports` to map port interfaces to their adapter implementations. This configuration drives the dependency injection at application startup.

### Key Design Patterns

1. **Hexagonal Architecture**: Domain logic isolated from infrastructure via ports
2. **Dependency Inversion**: Domain depends on port abstractions, not concrete adapters
3. **Protocol-Based Interfaces**: All ports use Python protocols for type safety
4. **Dependency Injection**: taew-py's `Bind` mechanism wires adapters at runtime
5. **Type Safety**: Strict MyPy and Pyright configurations ensure correctness

This architecture enables:
- Easy substitution of adapters (e.g., swap RAM storage for database storage)
- Testing domain logic independently of infrastructure
- Adding new capabilities by implementing port interfaces
- Multiple adapter implementations for the same port (e.g., RAM vs. directory storage)