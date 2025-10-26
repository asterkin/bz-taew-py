from pathlib import Path
from datetime import date
from decimal import Decimal
from domain.rate import Rate

from taew.utils.ports import build
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigurePickle,
)
from taew.adapters.python.ram.for_obtaining_current_datetime.for_configuring_adapters import (
    Configure as ConfigureCurrentDateTime,
)
from adapters.dir.for_storing_tickets.for_configuring_adapters import (
    Configure as ConfigureTickets,
)
from adapters.ram.for_storing_rates.for_configuring_adapters import (
    Configure as ConfigureRates,
)
from adapters.ram.for_making_payments.for_configuring_adapters import (
    Configure as ConfigureMakingPayments,
)
from workflows.for_car_drivers.for_configuring_adapters import (
    Configure as ConfigureCarDrivers,
)
from workflows.for_parking_inspectors.for_configuring_adapters import (
    Configure as ConfigureParkingInspectors,
)
from taew.adapters.launch_time.for_binding_interfaces.for_configuring_adapters import (
    Configure as ConfigureBindingInterfaces,
)
from taew.adapters.cli.for_starting_programs.for_configuring_adapters import (
    Configure as ConfigureCLI,
)
from taew.adapters.python.pprint.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigurePPrint,
)
from taew.adapters.python.argparse.for_building_command_parsers.for_configuring_adapters import (
    Configure as ConfigureArgparse,
)
from taew.adapters.python.dataclass.for_finding_configurations.for_configuring_adapters import (
    Configure as ConfigureFindConfigurations,
)
from taew.adapters.python.typing.for_building_config_ports_mapping.for_configuring_adapters import (
    Configure as ConfigureBuildConfigPortsMapping,
)


# Configuration constants
TICKETS_FOLDER = Path("/tmp/tickets")

ports = build(
    ConfigureMakingPayments(),
    ConfigureCarDrivers(_min_euros=Decimal("0.50")),
    ConfigureParkingInspectors(),
    ConfigureCurrentDateTime(),
    ConfigureRates(
        Blue=Rate(name="Blue", euros_per_hour=Decimal("0.80")),
        Green=Rate(name="Green", euros_per_hour=Decimal("0.85")),
        Orange=Rate(name="Orange", euros_per_hour=Decimal("0.75")),
    ),
    ConfigureTickets(
        _folder=TICKETS_FOLDER,
        _extension="pkl",
        _serialization=ConfigurePickle(),
        _key_type=str,
    ),
)

ports_root = Root(Path("./"))
launch_ports = build(
    ConfigureBindingInterfaces(
        _root=ports_root,
    ),
    ConfigureCLI(
        _root=ports_root["adapters"]["cli"],  # type: ignore
        _ports_mapping=ports,
    ),
    ConfigurePPrint(),
    ConfigureArgparse(),
    ConfigureFindConfigurations(),
    ConfigureBuildConfigPortsMapping(
        _variants={
            date: {"_variant": "isoformat", "_format": "%m/%y"},
        }
    ),
)
