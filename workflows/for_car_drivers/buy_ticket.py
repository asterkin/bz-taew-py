import re
import uuid
from decimal import Decimal
from dataclasses import dataclass
from datetime import timedelta

from domain.ticket import Ticket
from ports.for_making_payments import Pay
from taew.ports.for_logging import Logger
from domain.payment_card import PaymentCard
from ports.for_storing_rates import RatesRepository
from taew.ports.for_obtaining_current_datetime import Now
from ports.for_storing_tickets import MutableTicketsRepository


_CARD_NUMBER_PATTERN = re.compile(r"^\d{16}$")
_VERIFICATION_CODE_PATTERN = re.compile(r"^\d{3}$")


@dataclass(eq=False, frozen=True)
class BuyTicket:
    """Workflow for buying a parking ticket for a car driver."""

    _now: Now
    _rates: RatesRepository
    _pay: Pay
    _logger: Logger
    _tickets: MutableTicketsRepository
    _min_euros: Decimal

    def _validate_payment_card(self, payment_card: PaymentCard) -> None:
        """Validate payment card data.

        Args:
            payment_card: The payment card to validate

        Raises:
            ValueError: If card data is invalid
        """
        # Validate card number (16 digits)
        if not _CARD_NUMBER_PATTERN.match(payment_card.number):
            raise ValueError("Card number must be exactly 16 digits")

        # Validate verification code (3 digits)
        if not _VERIFICATION_CODE_PATTERN.match(payment_card.verification_code):
            raise ValueError("Verification code must be exactly 3 digits")

        # Validation for expiration date format is already handled by the date type
        # The PaymentCard.expiration field ensures month/year only format

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
            ValueError: If euros does not have exactly 2 decimal places.
            ValueError: If payment_card data is invalid.
        """
        self._logger.info(
            "Starting ticket purchase for car %s in zone %s for %s euros",
            car_plate,
            rate_name,
            euros,
            extra={
                "car_plate": car_plate,
                "rate_name": rate_name,
                "amount": str(euros),
            },
        )

        # Validate payment card (early validation to block problems without duplication)
        self._logger.debug("Validating payment card")
        try:
            self._validate_payment_card(payment_card)
            self._logger.debug("Payment card validation successful")
        except ValueError as e:
            self._logger.error(
                "Payment card validation failed: %s",
                str(e),
                extra={"car_plate": car_plate, "validation_error": str(e)},
            )
            raise

        # Verify euros has exactly 2 decimal places
        if euros.as_tuple().exponent != -2:
            error_msg = f"Amount {euros} must have exactly 2 decimal places"
            self._logger.error(
                "Invalid amount precision: %s",
                error_msg,
                extra={
                    "car_plate": car_plate,
                    "amount": str(euros),
                    "exponent": euros.as_tuple().exponent,
                },
            )
            raise ValueError(error_msg)

        # Verify minimum euros
        if euros < self._min_euros:
            error_msg = f"Amount {euros} is less than minimum {self._min_euros}"
            self._logger.error(
                "Amount below minimum: %s euros (minimum: %s)",
                euros,
                self._min_euros,
                extra={
                    "car_plate": car_plate,
                    "amount": str(euros),
                    "minimum": str(self._min_euros),
                },
            )
            raise ValueError(error_msg)

        # Verify rate exists
        try:
            rate = self._rates[rate_name]
            self._logger.debug(
                "Found rate %s: %s euros per hour",
                rate_name,
                rate.euros_per_hour,
                extra={
                    "rate_name": rate_name,
                    "euros_per_hour": str(rate.euros_per_hour),
                },
            )
        except KeyError:
            error_msg = f"Rate name '{rate_name}' not found"
            self._logger.error(
                "Rate not found: %s",
                rate_name,
                extra={"car_plate": car_plate, "rate_name": rate_name},
            )
            raise ValueError(error_msg)

        # Process payment (may raise ValueError for invalid card or other exceptions for service issues)
        self._logger.info(
            "Processing payment of %s euros",
            euros,
            extra={"car_plate": car_plate, "amount": str(euros)},
        )
        try:
            payment_id = self._pay(euros=euros, payment_card=payment_card)
            self._logger.info(
                "Payment successful with ID: %s",
                payment_id,
                extra={
                    "car_plate": car_plate,
                    "payment_id": payment_id,
                    "amount": str(euros),
                },
            )
        except Exception as e:
            self._logger.error(
                "Payment failed: %s",
                str(e),
                exc_info=True,
                extra={"car_plate": car_plate, "amount": str(euros), "error": str(e)},
            )
            raise

        # Calculate parking duration based on payment amount and hourly rate
        hours = euros / rate.euros_per_hour
        self._logger.debug(
            "Calculated parking duration: %s hours",
            hours,
            extra={
                "car_plate": car_plate,
                "hours": float(hours),
                "rate": str(rate.euros_per_hour),
            },
        )

        # Create ticket with timestamps
        now = self._now()
        starting_date_time = now
        ending_date_time = now + timedelta(hours=float(hours))

        self._logger.debug(
            "Ticket times - Start: %s, End: %s",
            starting_date_time,
            ending_date_time,
            extra={
                "car_plate": car_plate,
                "start_time": starting_date_time.isoformat(),
                "end_time": ending_date_time.isoformat(),
            },
        )

        # Generate ticket code (UUID for stable random ID)
        ticket_code = str(uuid.uuid4())
        self._logger.debug(
            "Generated ticket code: %s",
            ticket_code,
            extra={"car_plate": car_plate, "ticket_code": ticket_code},
        )

        # Create ticket
        ticket = Ticket(
            ticket_code=ticket_code,
            car_plate=car_plate,
            rate_name=rate_name,
            starting_date_time=starting_date_time,
            ending_date_time=ending_date_time,
            price=euros,
            payment_id=payment_id,
        )

        # Store ticket
        self._logger.debug(
            "Storing ticket in repository",
            extra={"car_plate": car_plate, "ticket_code": ticket_code},
        )
        self._tickets[ticket_code] = ticket

        self._logger.info(
            "Ticket purchase completed successfully for car %s - Ticket: %s",
            car_plate,
            ticket_code,
            extra={
                "car_plate": car_plate,
                "ticket_code": ticket_code,
                "amount": str(euros),
                "rate_name": rate_name,
                "payment_id": payment_id,
                "duration_hours": float(hours),
            },
        )

        return ticket
