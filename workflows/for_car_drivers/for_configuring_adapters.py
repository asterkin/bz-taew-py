"""Configurator for car drivers workflow adapter."""

from dataclasses import dataclass
from decimal import Decimal

from workflows._common import ConfigureWorkflow


@dataclass(eq=False, frozen=True)
class Configure(ConfigureWorkflow):
    """Configurator for car drivers workflow.

    Configures the workflow with:
    - Logging to "Port: for_car_drivers"
    - Minimum euro amount validation

    Example:
        from workflows.for_car_drivers.for_configuring_adapters import Configure

        ports = Configure(_min_euros=Decimal("0.50"))()
    """

    _name: str = "for_car_drivers"
    _min_euros: Decimal = Decimal("0.50")

    def __post_init__(self) -> None:
        object.__setattr__(self, "_package", __package__)
        object.__setattr__(self, "_file", __file__)
