"""Configurator for RAM-based rates storage."""

from dataclasses import dataclass
from typing import cast

from taew.adapters.python.ram.for_storing_data.for_configuring_adapters import (
    Configure as ConfigureBase,
)

from domain.rate import Rate


@dataclass(eq=False, frozen=True)
class _Configure(ConfigureBase):
    """Configurator for RAM-based rates storage.

    Application-level configurator that sets proper package/file paths
    for bluezone-py application adapters.
    """

    def __post_init__(self) -> None:
        """Initialize package and file paths for this adapter."""
        object.__setattr__(self, "_package", __package__)
        object.__setattr__(self, "_file", __file__)


def Configure(**kwargs: Rate) -> _Configure:
    """Create configurator for RAM-based rates storage.

    Application-level configurator that sets proper package/file paths
    for bluezone-py application adapters.

    Returns:
        Configurator for RAM-based rates storage.
    """
    return _Configure(_values=cast(dict[str, object], kwargs))
