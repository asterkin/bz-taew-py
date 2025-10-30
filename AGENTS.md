# AGENTS.md

This file orients Codex-powered agents to the BlueZone Python implementation so you can think about architectural evolution without rediscovering the current design each time. It focuses on the moving parts you are most likely to reason about when proposing structural changes.

## System Snapshot
- **Purpose**: Parking ticket application showcasing a Ports & Adapters (hexagonal) style implementation shared across multiple languages.
- **Language & Runtime**: Python 3.14+ with strict type checking (ruff, mypy, pyright) and UV for dependency management (`uv.lock`).
- **Foundation Library**: [taew-py](https://github.com/asterkin/taew-py) underpins dependency injection, CLI routing, logging, serialization, and adapter configuration primitives. Domain and workflow code stay taew-agnostic; only adapters, configuration, and the CLI shim depend on it.
- **Runtime Shell**: CLI entrypoint at `bin/bz` binds `taew.ports.for_starting_programs.Main` against the configured adapters (see `configuration.py`) and forwards `sys.argv`.
- **Shared Assets**: `common/` subtree mirrors the canonical BlueZone specification (domain docs, reusable acceptance artifacts). Treat it as read-only reference material.

## Execution Flow
1. User runs `./bin/bz ...`.
2. Entry shim resolves the `Main` port via `taew.adapters.launch_time.for_binding_interfaces.bind()` using the `adapters` mapping exported from `configuration.py`.
3. taew locates CLI adapters under `adapters/cli`, exposes commands, and marshals CLI arguments to matching port calls.
4. CLI adapters simply re-export the desired port. taew injects the corresponding workflow instance (resolved via Ports Mapping).
5. Workflow executes domain logic by collaborating with other ports (repositories, payment processor, clock, logger).
6. Responses bubble back through taew, which handles formatting, logging, and CLI output.

## Architectural Layers
- **Domain (`domain/`)**: Immutable value objects (`PaymentCard`, `Rate`, `Ticket`). No logic beyond data validation embodied in Python types.
- **Ports (`ports/`)**: Protocol definitions that encode the application’s capabilities. Key groups:
  - `for_car_drivers`: `GetRates`, `BuyTicket`.
  - `for_parking_inspectors`: `CheckCar` + `CheckCarResult`.
  - Storage ports: `RatesRepository`, `TicketsRepository`, `MutableTicketsRepository`.
  - Payments: `Pay`.
- **Workflows (`workflows/`)**: Business logic orchestrators that depend solely on ports. Subdirectories mirror port namespaces (`for_car_drivers`, `for_parking_inspectors`). Each workflow is a dataclass with injected collaborators.
  - Common configurator logic in `workflows/_common.py` wires logging and adapter metadata.
- **Adapters (`adapters/`)**: Concrete implementations of ports.
  - `cli/`: Thin re-exports so taew can map CLI commands to workflows (e.g., `adapters/cli/buy_ticket.py` exposes `BuyTicket`).
  - `ram/`: In-memory adapters (e.g., `for_making_payments.Pay` returns UUIDs; `for_storing_rates` and `for_storing_tickets` backed by taew RAM repositories).
  - `dir/`: Filesystem-backed ticket repositories using taew’s directory storage helpers.
- **Configuration (`configuration.py`)**: Declarative wiring via `taew.utils.cli.configure(...)`. Selects which adapters fulfill which ports, seeds data, and exports the `adapters` mapping consumed by the CLI.

## Key Workflows & Collaborations
### Car Driver Port (`workflows/for_car_drivers`)
- **`GetRates`**: Logs retrieval, returns `RatesRepository.values()`.
- **`BuyTicket`**:
  - Validates payment card format (16-digit number, 3-digit CVV) and amount precision/minimum (uses `_min_euros` injected via configuration).
  - Retrieves zone rate, computes duration from `euros / rate.euros_per_hour`.
  - Calls `Pay` port to process payment; defaults to RAM adapter generating UUIDs but can be swapped for real processors.
  - Builds `Ticket` value object with timestamps based on injected `Now` port and stores through `MutableTicketsRepository`.
  - Emits structured log events throughout (success & error cases) using injected `Logger`.

### Parking Inspector Port (`workflows/for_parking_inspectors`)
- **`CheckCar`**:
  - Verifies rate exists via `RatesRepository`.
  - Retrieves current time (`Now`) and queries `TicketsRepository` for most recent ticket matching car/rate.
  - Determines legality by comparing stored ticket end time to current time.
  - Returns `CheckCarResult`, again logging key steps and failure paths.

## Persistence & State
- **Rates**: Default configuration seeds three `Rate` objects (Blue, Green, Orange) through `adapters.ram.for_storing_rates`. These live in-memory during process lifetime.
- **Tickets**: Default wiring uses directory adapter with pickle serialization targeting `/tmp/tickets` (configurable via `TICKETS_FOLDER`). RAM adapters are also available for tests or ephemeral runs.
- **Payments**: RAM adapter in `adapters/ram/for_making_payments` supports deterministic responses (preconfigured UUID, exception, or callback hook) for testing scenarios.
- **Serialization Variants**: `configuration.py` customizes date serialization (ISO format) via the `variants` argument passed to `configure`.
- **Benchmarks**: `benchmarks/` hosts exploratory comparisons of ticket storage adapters focusing on different serialization strategies (bytes vs. str encodings). Current results favor the Pickle-based directory adapter for its minimal configuration and solid performance, although it produces larger artifacts than alternatives. That trade-off is acceptable for the present exploratory setup.

## Cross-Cutting Concerns
- **Dependency Injection**: taew resolves dependencies purely from the declarative `configure(...)` call. Each adapter exposes a `Configure` class that records metadata (module path, file) so taew can autoload implementations.
- **Logging**: Workflows receive `taew.ports.for_logging.Logger`. Default configuration leverages taew’s logging adapter configured within workflow configurators (`ConfigureWorkflow._nested_ports`).
- **CLI Contract**: Commands and argument schemas are inferred by taew from port signatures. To add a new CLI command, expose a port in `adapters/cli`, provide a workflow implementing it, and wire the workflow via configuration.
- **Testing**: `test/test_cli.py` executes real CLI commands end-to-end, normalizing dynamic data (timestamps, UUIDs). Tests clear the tickets folder before each run, exercising the directory adapter. Additional tests can live in `test/test_workflows/` (currently placeholder).

## Configuration Walkthrough (`configuration.py`)
- Imports all relevant `Configure` classes (`CarDrivers`, `ParkingInspectors`, `Rates`, `Tickets`, etc.).
- Sets `TICKETS_FOLDER = Path("/tmp/tickets")`—update here if you change persistence location.
- Calls `configure(...)` with:
  - Workflow configurators (`CarDrivers`, `ParkingInspectors`) optionally parameterized (`_min_euros`).
  - Core adapters (`CurrentDateTime`, `Rates`, `Tickets`, `MakingPayments`).
  - Serialization variants dict (currently special handling for `datetime.date`).
- Returns a `PortsMapping` object assigned to `adapters`; imported by the CLI entrypoint and test harnesses.

## Extension Hooks for Brainstorming
1. **Swapping Persistence**: Replace `Tickets` configurator with database-backed adapter (implement new adapter package and update `configure(...)`). Ensure repository protocols stay pure.
2. **Integrating Real Payments**: Provide new implementation of `ports.for_making_payments.Pay` (e.g., Stripe) and expose configuration knobs for credentials.
3. **New User Journeys**: Add new ports/workflows for scenarios like extending tickets, managing accounts, or analytics. Follow existing pattern: define protocol → implement workflow → expose CLI adapter → configure.
4. **Observability Enhancements**: taew logging is centralized; consider configuring structured log sinks or wrapping `Logger` port with additional context (correlation IDs).
5. **API Surface**: While current façade is CLI-only, the hexagonal layout makes adding HTTP adapters straightforward—define new adapter package (e.g., `adapters/http`) that binds to existing workflows.
6. **Shared Specifications**: Align any cross-language architectural changes by updating `common/` (in upstream repo). Keep this implementation-specific repo focused on Python adapters/workflows.

Keep this file updated whenever the architecture model shifts (new ports, cross-cutting services, persistence strategy changes) so future Codex sessions can jump straight into higher-level design thinking.
