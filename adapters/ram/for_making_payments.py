import uuid
from decimal import Decimal
from dataclasses import dataclass
from typing import Callable, Optional

from domain.payment_card import PaymentCard


@dataclass(frozen=True, eq=False)
class Pay:
    """RAM adapter for payment processing with configurable responses."""

    _response: Optional[str | Exception] = None
    _on_call: Optional[Callable[[Decimal, PaymentCard], None]] = None

    def __call__(self, *, euros: Decimal, payment_card: PaymentCard) -> str:
        """
        Execute payment workflow.

        Args:
            euros (Decimal): The amount to be paid.
            payment_card (PaymentCard): The payment card information.

        Returns:
            str: Payment request ID.

        Raises:
            Exception: If _response is configured as an exception.
        """
        # Log the call if callback is provided
        if self._on_call is not None:
            self._on_call(euros, payment_card)

        # Handle response based on type
        match self._response:
            case str() as response:
                return response
            case Exception() as exception:
                raise exception
            case None:
                return str(uuid.uuid4())
