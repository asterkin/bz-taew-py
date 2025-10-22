"""Read-only tickets repository adapter."""

from typing import TypeAlias
from domain.ticket import Ticket
from taew.adapters.python.dir.for_storing_data.data_repository import DataRepository


TicketsRepository: TypeAlias = DataRepository[str, Ticket]
