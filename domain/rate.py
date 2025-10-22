from decimal import Decimal
from typing import NamedTuple


class Rate(NamedTuple):
    """Data structure representing a parking rate."""

    name: str
    """Name of the rate/zone."""

    euros_per_hour: Decimal
    """Amount of euros charged per hour."""
