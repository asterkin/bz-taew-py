from decimal import Decimal
from typing import Protocol

from domain.payment_card import PaymentCard


class Pay(Protocol):
    """Port for processing payments."""

    def __call__(self, *, euros: Decimal, payment_card: PaymentCard) -> str:
        """Process a payment transaction.

        Args:
            euros: Amount to be charged in euros
            payment_card: Payment card to be used for the transaction

        Returns:
            Payment identifier as string

        Raises:
            ValueError: If payment processing fails or card is invalid
        """
        ...
