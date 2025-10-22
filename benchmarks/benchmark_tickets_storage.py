"""Benchmark different marshalling configurations for tickets repository."""

import time
import shutil
from typing import Any, cast
from pathlib import Path
from datetime import datetime
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root

from benchmarks.fake_tickets import generate_fake_tickets
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigurePickle,
)
from taew.adapters.python.zlib.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigureZlib,
)
from taew.adapters.python.json.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigureJSON,
)
from taew.adapters.python.str.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigureStr,
)
from taew.adapters.python.io.bytesio.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigureBytesIO,
)
from adapters.dir.for_storing_tickets.for_configuring_adapters import (
    Configure as ConfigureTickets,
)
from taew.adapters.launch_time.for_binding_interfaces import Bind
from domain.ticket import Ticket
from ports.for_storing_tickets import MutableTicketsRepository, TicketsRepository


# Benchmark configuration
TICKET_COUNT = 10_000
BENCHMARK_DIR = Path("/tmp/benchmark-tickets")


def get_directory_size(path: Path) -> int:
    """Calculate total size of directory in bytes."""
    return sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())


def format_size(size_bytes: int) -> str:
    """Format size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes //= 1024
    return f"{size_bytes:.2f} TB"


def benchmark_configuration(
    name: str, serialization_config: Any, extension: str, complexity: int
) -> dict[str, Any]:
    """Benchmark a single configuration.

    Args:
        name: Configuration name
        serialization_config: Serialization configurator instance
        extension: File extension for this configuration
        complexity: Configuration complexity rating

    Returns:
        Dictionary with benchmark results
    """
    # Setup
    folder = BENCHMARK_DIR / name.lower().replace(" ", "-").replace("+", "-")
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Create tickets repository configuration
    configure = ConfigureTickets(
        _folder=folder,
        _extension=extension,
        _serialization=serialization_config,
        _key_type=str,
    )

    config = configure()
    # Bind the repository
    bind = Bind(Root(Path("./")))
    repo = bind(MutableTicketsRepository, config)

    # Generate test data
    tickets = generate_fake_tickets(TICKET_COUNT)

    # Benchmark write
    write_start = time.perf_counter()
    for ticket in tickets:
        repo[ticket.ticket_code] = ticket
    write_time = time.perf_counter() - write_start

    # Measure size
    total_size = get_directory_size(folder)
    avg_size = total_size / TICKET_COUNT

    # Benchmark read
    read_start = time.perf_counter()
    read_repo = cast(TicketsRepository, repo)
    for ticket in tickets:
        _ = read_repo[ticket.ticket_code]
    read_time = time.perf_counter() - read_start

    # Cleanup
    shutil.rmtree(folder)

    return {
        "name": name,
        "complexity": complexity,
        "write_time": write_time,
        "read_time": read_time,
        "total_size": total_size,
        "avg_size": avg_size,
        "write_per_ticket": write_time / TICKET_COUNT * 1000,  # ms
        "read_per_ticket": read_time / TICKET_COUNT * 1000,  # ms
    }


def main() -> None:
    """Run all benchmarks and display results."""
    print(f"Benchmarking {TICKET_COUNT} tickets with different configurations...\n")

    # Define configurations
    # Complexity rating: 1 = simple (single adapter), 2 = medium (2 adapters)
    configurations = [
        (
            "JSON",
            ConfigureJSON(_type=Ticket, _variants={datetime: "timestamp"}),
            "json",
            3,
        ),
        (
            "JSON + zlib",
            ConfigureZlib(
                _configure=ConfigureStr(
                    _configure=ConfigureJSON(
                        _type=Ticket, _variants={datetime: "timestamp"}
                    )
                )
            ),
            "jsonz",
            4,
        ),
        ("BytesIO", ConfigureBytesIO(_type=Ticket), "bin", 2),
        (
            "BytesIO + zlib",
            ConfigureZlib(_configure=ConfigureBytesIO(_type=Ticket)),
            "binz",
            3,
        ),
        ("pickle", ConfigurePickle(), "pkl", 1),
        ("pickle + zlib", ConfigureZlib(_configure=ConfigurePickle()), "pklz", 2),
    ]

    # Run benchmarks
    results: list[dict[str, Any]] = []
    for name, serialization_config, extension, complexity in configurations:
        print(f"Running: {name}...", end=" ", flush=True)
        result = benchmark_configuration(
            name, serialization_config, extension, complexity
        )
        results.append(result)
        print("✓")

    # Display results
    print("\n" + "=" * 105)
    print(
        f"{'Configuration':<20} {'Complexity':<12} {'Write (s)':<12} {'Read (s)':<12} {'Total Size':<15} {'Avg Size':<15}"
    )
    print("=" * 105)

    for r in results:
        print(
            f"{r['name']:<20} "
            f"{r['complexity']:<12} "
            f"{r['write_time']:<12.3f} "
            f"{r['read_time']:<12.3f} "
            f"{format_size(r['total_size']):<15} "
            f"{format_size(r['avg_size']):<15}"
        )

    print("=" * 105)

    # Show per-ticket timings
    print("\n" + "=" * 60)
    print(f"{'Configuration':<20} {'Write/ticket (ms)':<20} {'Read/ticket (ms)':<20}")
    print("=" * 60)

    for r in results:
        print(
            f"{r['name']:<20} "
            f"{r['write_per_ticket']:<20.4f} "
            f"{r['read_per_ticket']:<20.4f}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
