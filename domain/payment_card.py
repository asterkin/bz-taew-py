from datetime import date
from typing import NamedTuple


class PaymentCard(NamedTuple):
    """Data structure representing a payment card used for parking payments."""

    number: str
    """Card number (16 digits)."""

    verification_code: str
    """Verification code (3 digits)."""

    expiration: date
    """Expiration date (month and year)."""
