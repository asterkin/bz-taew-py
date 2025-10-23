"""Common workflow configuration base class."""

from dataclasses import dataclass

from taew.domain.configuration import PortsMapping
from taew.adapters.python.dataclass.for_configuring_adapters import (
    Configure as ConfigureBase,
)
from taew.adapters.python.logging.for_logging.for_configuring_adapters import (
    Configure as ConfigureLogging,
)


@dataclass(eq=False, frozen=True)
class ConfigureWorkflow(ConfigureBase):
    """Base configurator for workflow adapters.

    Provides common configuration for workflows including:
    - Automatic adapter path resolution to "workflows"
    - Root marker override to enable proper adapter discovery
    - Nested logging port configuration

    Subclasses should override:
    - _name: The workflow name (used for logging)
    - Additional kwargs as needed (e.g., _min_euros for car_drivers)
    """

    _name: str = ""
    _root_marker: str = "workflows"
    _ports: str = "ports"

    # Note: Subclasses must override __post_init__ to set _package and _file

    def _nested_ports(self) -> PortsMapping:
        """Configure logging port for this workflow."""
        return ConfigureLogging(_name=f"Port: {self._name}")()
