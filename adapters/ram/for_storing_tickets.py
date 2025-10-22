from typing import TypeAlias
from domain.ticket import Ticket
from taew.adapters.python.ram.for_storing_data import (
    DataRepository,
    MutableDataRepository,
)


TicketsRepository: TypeAlias = DataRepository[str, Ticket]
MutableTicketsRepository: TypeAlias = MutableDataRepository[str, Ticket]
