from decimal import Decimal
from typing import NamedTuple
from datetime import datetime


class Ticket(NamedTuple):
    """Data structure representing objects with the data of a parking ticket."""

    ticket_code: str
    """Unique identifier of the ticket.
    It is a 10-digit number with leading zeros if necessary."""

    car_plate: str
    """Plate of the car that has been parked."""

    rate_name: str
    """Rate name of the zone where the car is parked at."""

    starting_date_time: datetime
    """When the parking period begins."""

    ending_date_time: datetime
    """When the parking period expires."""

    price: Decimal
    """Amount of euros paid for the ticket."""

    payment_id: str
    """Unique identifier of the payment made to get the ticket."""
