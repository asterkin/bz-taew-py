"""Read-only rates repository adapter."""

from typing import TypeAlias
from domain.rate import Rate
from taew.adapters.python.ram.for_storing_data.data_repository import DataRepository


RatesRepository: TypeAlias = DataRepository[str, Rate]
