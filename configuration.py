from pathlib import Path
from datetime import date
from decimal import Decimal
from domain.rate import Rate

import site
from domain.payment_card import PaymentCard
from taew.domain.configuration import PortConfigurationDict, PortsMapping
from taew.utils.ports import build
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as ConfigurePickle,
)
from taew.adapters.python.json.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigureJSON,
)
from taew.adapters.python.decimal.for_stringizing_objects.for_configuring_adapters import (
    Configure as ConfigureDecimal,
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

from taew.ports import (
    for_starting_programs,
    for_stringizing_objects,
    for_binding_interfaces,
    for_building_command_parsers,
)

# Configuration constants
TICKETS_FOLDER = Path("/tmp/tickets")
TAEW_ROOT = site.getsitepackages()[0]


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
                    Decimal: ConfigureDecimal()()[for_stringizing_objects],
                    PaymentCard: ConfigureJSON(
                        _type=PaymentCard,
                        _variants={date: {"_variant": "isoformat", "_format": "%m/%y"}},
                    )()[for_stringizing_objects],
                }
            )
        },
    ),
}
