"""Mutable tickets repository adapter."""

from typing import TypeAlias
from domain.ticket import Ticket
from taew.adapters.python.dir.for_storing_data.mutable_data_repository import (
    MutableDataRepository,
)


MutableTicketsRepository: TypeAlias = MutableDataRepository[str, Ticket]
