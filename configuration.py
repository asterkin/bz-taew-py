from pathlib import Path
from datetime import date
from decimal import Decimal
from domain.rate import Rate

import site
from taew.domain.logging import INFO
from domain.payment_card import PaymentCard
from taew.domain.configuration import PortConfigurationDict, PortsMapping
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigurePickle,
)
from taew.adapters.python.json.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigureJSON,
)
from adapters.dir.for_storing_tickets.for_configuring_adapters import (
    Configure as ConfigureTickets,
)

from ports import (
    for_storing_rates,
    for_making_payments,
    for_car_drivers,
    for_parking_inspectors,
)
from taew.ports import (
    for_logging,
    for_starting_programs,
    for_stringizing_objects,
    for_binding_interfaces,
    for_building_command_parsers,
    for_obtaining_current_datetime,
)

# Configuration constants
TICKETS_FOLDER = Path("/tmp/tickets")
TAEW_ROOT = site.getsitepackages()[0]


def _config_logger(name: str) -> PortsMapping:
    return {
        for_logging: PortConfigurationDict(
            adapter="taew.adapters.python.logging",
            root=TAEW_ROOT,
            kwargs=dict(
                name=name,
                config=dict(
                    level=INFO,
                    format="{levelname}:{message}",
                    style="{",
                ),
            ),
        )
    }


ports: PortsMapping = {  # type: ignore[assignment]
    for_storing_rates: PortConfigurationDict(
        adapter="adapters.ram",
        kwargs=dict(
            kwargs=dict(
                Blue=Rate(name="Blue", euros_per_hour=Decimal("0.80")),
                Green=Rate(name="Green", euros_per_hour=Decimal("0.85")),
                Orange=Rate(name="Orange", euros_per_hour=Decimal("0.75")),
            )
        ),
    ),
    for_making_payments: "adapters.ram",
    for_obtaining_current_datetime: PortConfigurationDict(
        adapter="taew.adapters.python.datetime",
        root=TAEW_ROOT,
    ),
    for_car_drivers: PortConfigurationDict(
        adapter="workflows",
        kwargs=dict(_min_euros=Decimal("0.50")),
        ports=_config_logger("Port: for_car_drivers"),
    ),
    for_parking_inspectors: PortConfigurationDict(
        adapter="workflows",
        ports=_config_logger("Port: for_parking_inspectors"),
    ),
} | ConfigureTickets(
    _folder=TICKETS_FOLDER,
    _extension="pkl",
    _serialization=ConfigurePickle(),
    _key_type=str,
)()

ports_root = Root(Path("./"))

launch_ports: PortsMapping = {
    for_starting_programs: PortConfigurationDict(
        adapter="taew.adapters.cli",
        root=TAEW_ROOT,
        kwargs=dict(
            _root=ports_root["adapters"]["cli"],  # type: ignore
            _ports=ports,
        ),
        ports={
            for_binding_interfaces: PortConfigurationDict(
                adapter="taew.adapters.launch_time",
                root=TAEW_ROOT,
                kwargs=dict(_root=ports_root),
            ),
        },
    ),
    for_binding_interfaces: PortConfigurationDict(
        adapter="taew.adapters.launch_time",
        root=TAEW_ROOT,
        kwargs=dict(_root=ports_root),
    ),
    for_stringizing_objects: PortConfigurationDict(
        adapter="taew.adapters.python.pprint",
        root=TAEW_ROOT,
    ),
    for_building_command_parsers: PortConfigurationDict(
        adapter="taew.adapters.python.argparse",
        root=TAEW_ROOT,
        ports={
            for_stringizing_objects: PortConfigurationDict(
                adapter={
                    Decimal: PortConfigurationDict(
                        adapter="taew.adapters.python.decimal",
                        root=TAEW_ROOT,
                    ),
                    PaymentCard: ConfigureJSON(
                        _type=PaymentCard,
                        _variants={date: {"_variant": "isoformat", "_format": "%m/%y"}},
                    )()[for_stringizing_objects],
                }
            )
        },
    ),
}
