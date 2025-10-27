from pathlib import Path
from datetime import date
from decimal import Decimal
from domain.rate import Rate

from taew.utils.cli import configure
from taew.adapters.python.inspect.for_browsing_code_tree.root import Root
from taew.adapters.python.pickle.for_serializing_objects.for_configuring_adapters import (
    Configure as Pickle,
)
from taew.adapters.python.ram.for_obtaining_current_datetime.for_configuring_adapters import (
    Configure as CurrentDateTime,
)
from adapters.dir.for_storing_tickets.for_configuring_adapters import (
    Configure as Tickets,
)
from adapters.ram.for_storing_rates.for_configuring_adapters import (
    Configure as Rates,
)
from adapters.ram.for_making_payments.for_configuring_adapters import (
    Configure as MakingPayments,
)
from workflows.for_car_drivers.for_configuring_adapters import (
    Configure as CarDrivers,
)
from workflows.for_parking_inspectors.for_configuring_adapters import (
    Configure as ParkingInspectors,
)


# Configuration constants
TICKETS_FOLDER = Path("/tmp/tickets")
ports_root = Root(Path("./"))

launch_ports = configure(
    ports_root,
    MakingPayments(),
    CarDrivers(_min_euros=Decimal("0.50")),
    ParkingInspectors(),
    CurrentDateTime(),
    Rates(
        Blue=Rate(name="Blue", euros_per_hour=Decimal("0.80")),
        Green=Rate(name="Green", euros_per_hour=Decimal("0.85")),
        Orange=Rate(name="Orange", euros_per_hour=Decimal("0.75")),
    ),
    Tickets(
        _folder=TICKETS_FOLDER,
        _extension="pkl",
        _serialization=Pickle(),
        _key_type=str,
    ),
    variants={
        date: {"_variant": "isoformat", "_format": "%m/%y"},
    },
)
