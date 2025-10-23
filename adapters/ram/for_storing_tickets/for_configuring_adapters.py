"""Configurator for RAM-based tickets storage."""

from dataclasses import dataclass

from taew.adapters.python.ram.for_storing_data.for_configuring_adapters import (
    Configure as ConfigureBase,
)


@dataclass(eq=False, frozen=True)
class Configure(ConfigureBase):
    """Configurator for RAM-based tickets storage.

    Application-level configurator that sets proper package/file paths
    for bluezone-py application adapters.
    """

    def __post_init__(self) -> None:
        """Initialize package and file paths for this adapter."""
        object.__setattr__(self, "_package", __package__)
        object.__setattr__(self, "_file", __file__)
