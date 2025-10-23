"""Configurator for parking inspectors workflow adapter."""

from dataclasses import dataclass

from workflows._common import ConfigureWorkflow


@dataclass(eq=False, frozen=True)
class Configure(ConfigureWorkflow):
    """Configurator for parking inspectors workflow.

    Configures the workflow with:
    - Logging to "Port: for_parking_inspectors"

    Example:
        from workflows.for_parking_inspectors.for_configuring_adapters import Configure

        ports = Configure()()
    """

    _name: str = "for_parking_inspectors"

    def __post_init__(self) -> None:
        object.__setattr__(self, "_package", __package__)
        object.__setattr__(self, "_file", __file__)
