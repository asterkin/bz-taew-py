from decimal import Decimal
from typing import Protocol, Iterable

from domain.rate import Rate
from domain.ticket import Ticket
from domain.payment_card import PaymentCard


class GetRates(Protocol):
    """Protocol for retrieving available parking rates for car drivers."""

    def __call__(self) -> Iterable[Rate]:
        """Returns an iterable of available parking rates."""
        ...


class BuyTicket(Protocol):
    """Protocol for buying a parking ticket for a car driver."""

    def __call__(
        self,
        *,
        car_plate: str,
        rate_name: str,
        euros: Decimal,
        payment_card: PaymentCard,
    ) -> Ticket:
        """Buys a parking ticket.

        Args:
            car_plate: Plate of the car that has been parked.
            rate_name: Rate name of the zone where the car is parked at.
            euros: Amount of euros to be paid.
            payment_card: Payment card used for the transaction.

        Returns:
            Ticket: The purchased parking ticket.

        Raises:
            ValueError: If rate_name is not found.
            ValueError: If euros is less than configured minimum.
            ValueError: If payment_card data is invalid.
        """
        ...
