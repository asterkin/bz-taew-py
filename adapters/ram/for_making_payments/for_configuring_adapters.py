"""Configurator for RAM-based payment processing adapter."""

from dataclasses import dataclass

from taew.adapters.python.dataclass.for_configuring_adapters import (
    Configure as ConfigureBase,
)


@dataclass(eq=False, frozen=True)
class Configure(ConfigureBase):
    """Configurator for RAM-based payment processing adapter.

    Provides simple configuration for in-memory payment processing
    (always successful, returns UUID).

    Example:
        from adapters.ram.for_making_payments.for_configuring_adapters import Configure

        ports = Configure()()
    """

    _ports: str = "ports"
    _root_marker: str = "/adapters"

    def __post_init__(self) -> None:
        object.__setattr__(self, "_package", __package__)
        object.__setattr__(self, "_file", __file__)
