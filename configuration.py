from pathlib import Path
from datetime import date
from decimal import Decimal
from domain.rate import Rate

import site
from domain.payment_card import PaymentCard
from taew.domain.configuration import PortConfigurationDict, PortsMapping
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigurePickle,
)
from taew.adapters.python.json.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigureJSON,
)
from taew.adapters.python.logging.for_logging.for_configuring_adapters import (
    Configure as ConfigureLogging,
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

from ports import (
    for_making_payments,
    for_car_drivers,
    for_parking_inspectors,
)
from taew.ports import (
    for_starting_programs,
    for_stringizing_objects,
    for_binding_interfaces,
    for_building_command_parsers,
)

# Configuration constants
TICKETS_FOLDER = Path("/tmp/tickets")
TAEW_ROOT = site.getsitepackages()[0]


ports: PortsMapping = (
    {  # type: ignore[assignment]
        for_making_payments: "adapters.ram",
        for_car_drivers: PortConfigurationDict(
            adapter="workflows",
            kwargs=dict(_min_euros=Decimal("0.50")),
            ports=ConfigureLogging(_name="Port: for_car_drivers")(),
        ),
        for_parking_inspectors: PortConfigurationDict(
            adapter="workflows",
            ports=ConfigureLogging(_name="Port: for_parking_inspectors")(),
        ),
    }
    | ConfigureCurrentDateTime()()
    | ConfigureRates(
        Blue=Rate(name="Blue", euros_per_hour=Decimal("0.80")),
        Green=Rate(name="Green", euros_per_hour=Decimal("0.85")),
        Orange=Rate(name="Orange", euros_per_hour=Decimal("0.75")),
    )()
    | ConfigureTickets(
        _folder=TICKETS_FOLDER,
        _extension="pkl",
        _serialization=ConfigurePickle(),
        _key_type=str,
    )()
)

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
