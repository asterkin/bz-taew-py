import unittest
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from domain.rate import Rate
from domain.payment_card import PaymentCard
from ports.for_making_payments import Pay as PayProtocol
from ports.for_car_drivers import BuyTicket as BuyTicketProtocol
from ports.for_storing_tickets import (
    MutableTicketsRepository as MutableTicketsRepositoryProtocol,
)
from ports.for_storing_rates import RatesRepository as RatesRepositoryProtocol
from adapters.ram.for_storing_tickets import (
    TicketsRepository as TicketsRepositoryProtocol,
)
from taew.ports.for_logging import Logger as LoggerProtocol
from taew.ports.for_obtaining_current_datetime import Now as NowProtocol


def _get_rates() -> RatesRepositoryProtocol:
    """Factory method to create a RAM-based rates repository with sample data."""
    from adapters.ram.for_storing_rates import RatesRepository

    repository = RatesRepository()
    zone_a_rate = Rate(name="Zone A", euros_per_hour=Decimal("2.00"))
    repository["zone_a"] = zone_a_rate

    return repository


def _get_mutable_tickets() -> MutableTicketsRepositoryProtocol:
    """Factory method to create a RAM-based mutable tickets repository."""
    from adapters.ram.for_storing_tickets import MutableTicketsRepository

    return MutableTicketsRepository()


def _get_tickets_repository_from_mutable(
    mutable_repo: MutableTicketsRepositoryProtocol,
) -> TicketsRepositoryProtocol:
    """Factory method to create a TicketsRepository by copying from MutableTicketsRepository.

    This validates that both RAM adapters work correctly and allows test verification.
    """
    from adapters.ram.for_storing_tickets import TicketsRepository

    # Create TicketsRepository and copy data from mutable repository
    return TicketsRepository(mutable_repo)  # type: ignore


def _get_pay_adapter() -> PayProtocol:
    """Factory method to create a RAM-based payment adapter."""
    from adapters.ram.for_making_payments import Pay

    # Use fixed response for deterministic testing
    return Pay(_response="test-payment-id-12345")


def _get_pay_adapter_with_exception(exception: Exception) -> PayProtocol:
    """Factory method to create a RAM-based payment adapter that raises an exception."""
    from adapters.ram.for_making_payments import Pay

    return Pay(_response=exception)


def _get_pay_adapter_with_logging(
    call_log: list[tuple[Decimal, PaymentCard]],
) -> PayProtocol:
    """Factory method to create a RAM-based payment adapter that logs calls."""
    from adapters.ram.for_making_payments import Pay

    def log_call(euros: Decimal, payment_card: PaymentCard) -> None:
        call_log.append((euros, payment_card))

    return Pay(_on_call=log_call)


def _get_now_adapter() -> NowProtocol:
    """Factory method to create a RAM-based datetime adapter with specific timestamp."""
    from taew.adapters.python.ram.for_obtaining_current_datetime import Now

    # Use a specific timestamp for deterministic testing
    test_datetime = datetime(2024, 1, 15, 10, 30, 0)
    return Now(_now=test_datetime)


def _get_logger() -> tuple[LoggerProtocol, list[tuple[Any, ...]]]:
    """Factory method to create a RAM-based logger for testing."""
    from taew.adapters.python.ram.for_logging import Logger

    calls_list: list[tuple[Any, ...]] = []
    logger = Logger(_calls=calls_list)
    return logger, calls_list


def _make_buy_ticket(
    now_adapter: NowProtocol,
    rates_repository: RatesRepositoryProtocol,
    pay_adapter: PayProtocol,
    logger: LoggerProtocol,
    tickets_repository: MutableTicketsRepositoryProtocol,
    min_euros: Decimal = Decimal("0.50"),
) -> BuyTicketProtocol:
    """Factory method to create BuyTicket workflow instance."""
    from workflows.for_car_drivers.buy_ticket import BuyTicket

    return BuyTicket(
        _now=now_adapter,
        _rates=rates_repository,
        _pay=pay_adapter,
        _logger=logger,
        _tickets=tickets_repository,
        _min_euros=min_euros,
    )


class TestBuyTicket(unittest.TestCase):
    """Test cases for BuyTicket workflow."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.now_adapter = _get_now_adapter()
        self.rates_repository = _get_rates()
        self.tickets_repository = _get_mutable_tickets()
        self.pay_adapter = _get_pay_adapter()
        self.logger, self.log_calls = _get_logger()

        self.valid_card = PaymentCard(
            number="1234567890123456",
            verification_code="123",
            expiration=date(2025, 12, 31),
        )

    def test_successful_ticket_purchase(self) -> None:
        """Test successful ticket purchase with valid inputs."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        # When
        ticket = buy_ticket(
            car_plate="ABC123",
            rate_name="zone_a",
            euros=Decimal("4.00"),
            payment_card=self.valid_card,
        )

        # Then
        self.assertEqual(ticket.car_plate, "ABC123")
        self.assertEqual(ticket.rate_name, "zone_a")
        self.assertEqual(ticket.price, Decimal("4.00"))
        # Payment ID should match the fixed response from test adapter
        self.assertEqual(ticket.payment_id, "test-payment-id-12345")
        self.assertEqual(len(ticket.ticket_code), 36)  # UUID format: 8-4-4-4-12
        self.assertRegex(
            ticket.ticket_code,
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        )
        self.assertGreater(ticket.ending_date_time, ticket.starting_date_time)

        # Verify ticket was stored by copying to read-capable repository
        tickets_for_verification = _get_tickets_repository_from_mutable(
            self.tickets_repository
        )
        self.assertIn(ticket.ticket_code, tickets_for_verification)
        self.assertEqual(tickets_for_verification[ticket.ticket_code], ticket)

        # Verify logging - check that key workflow events were logged
        log_calls = self.log_calls
        self.assertGreater(
            len(log_calls), 0, "Expected logging calls during workflow execution"
        )

        # Check for start and completion info logs
        info_logs = [call for call in log_calls if call[0] == "info"]
        self.assertGreaterEqual(
            len(info_logs), 2, "Expected at least start and completion info logs"
        )

        # Verify workflow start was logged
        start_log_found = any(
            "Starting ticket purchase" in str(call[1]) for call in info_logs
        )
        self.assertTrue(start_log_found, "Expected workflow start to be logged")

        # Verify successful completion was logged
        completion_log_found = any(
            "completed successfully" in str(call[1]) for call in info_logs
        )
        self.assertTrue(
            completion_log_found, "Expected successful completion to be logged"
        )

    def test_rejects_amount_below_minimum(self) -> None:
        """Test that amounts below minimum are rejected."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
            min_euros=Decimal("1.00"),
        )

        # When/Then
        with self.assertRaises(ValueError) as cm:
            buy_ticket(
                car_plate="ABC123",
                rate_name="zone_a",
                euros=Decimal("0.50"),
                payment_card=self.valid_card,
            )

        self.assertIn("less than minimum", str(cm.exception))

    def test_rejects_amount_with_wrong_precision(self) -> None:
        """Test that amounts without exactly 2 decimal places are rejected."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        # When/Then - Test with 1 decimal place
        with self.assertRaises(ValueError) as cm:
            buy_ticket(
                car_plate="ABC123",
                rate_name="zone_a",
                euros=Decimal("4.0"),
                payment_card=self.valid_card,
            )

        self.assertIn("exactly 2 decimal places", str(cm.exception))

        # When/Then - Test with 3 decimal places
        with self.assertRaises(ValueError) as cm:
            buy_ticket(
                car_plate="ABC123",
                rate_name="zone_a",
                euros=Decimal("4.000"),
                payment_card=self.valid_card,
            )

        self.assertIn("exactly 2 decimal places", str(cm.exception))

    def test_rejects_nonexistent_rate(self) -> None:
        """Test that nonexistent rate names are rejected."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        # When/Then
        with self.assertRaises(ValueError) as cm:
            buy_ticket(
                car_plate="ABC123",
                rate_name="nonexistent_zone",
                euros=Decimal("4.00"),
                payment_card=self.valid_card,
            )

        self.assertIn("not found", str(cm.exception))

    def test_payment_failure_propagates_error(self) -> None:
        """Test that payment failures are propagated as expected."""

        # Given - create a test-specific failing pay adapter
        failing_pay_adapter = _get_pay_adapter_with_exception(
            ValueError("Card declined")
        )
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            failing_pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        # When/Then
        with self.assertRaises(ValueError) as cm:
            buy_ticket(
                car_plate="ABC123",
                rate_name="zone_a",
                euros=Decimal("4.00"),
                payment_card=self.valid_card,
            )

        self.assertIn("Card declined", str(cm.exception))

        # Verify no ticket was stored when payment fails
        tickets_for_verification = _get_tickets_repository_from_mutable(
            self.tickets_repository
        )
        self.assertEqual(len(tickets_for_verification), 0)

        # Verify error was logged
        log_calls = self.log_calls
        error_logs = [call for call in log_calls if call[0] == "error"]
        self.assertGreater(
            len(error_logs), 0, "Expected error to be logged for payment failure"
        )

    def test_calculates_correct_parking_duration(self) -> None:
        """Test that parking duration is calculated correctly based on rate."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        # When - Pay for exactly 2 hours at 2.00/hour rate
        ticket = buy_ticket(
            car_plate="ABC123",
            rate_name="zone_a",
            euros=Decimal("4.00"),
            payment_card=self.valid_card,
        )

        # Then - Duration should be 2 hours
        duration = ticket.ending_date_time - ticket.starting_date_time
        self.assertEqual(duration.total_seconds(), 2 * 3600)  # 2 hours in seconds

        # Verify deterministic timestamps from our RAM adapter
        expected_start = datetime(2024, 1, 15, 10, 30, 0)
        expected_end = datetime(2024, 1, 15, 12, 30, 0)  # 2 hours later
        self.assertEqual(ticket.starting_date_time, expected_start)
        self.assertEqual(ticket.ending_date_time, expected_end)

    def test_rejects_invalid_card_number(self) -> None:
        """Test that invalid card numbers are rejected."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        invalid_cards = [
            PaymentCard("12345678901234567", "123", date(2025, 12, 31)),  # 17 digits
            PaymentCard("123456789012345", "123", date(2025, 12, 31)),  # 15 digits
            PaymentCard(
                "123456789012345a", "123", date(2025, 12, 31)
            ),  # contains letter
            PaymentCard("", "123", date(2025, 12, 31)),  # empty
        ]

        for invalid_card in invalid_cards:
            with self.subTest(card_number=invalid_card.number):
                # When/Then
                with self.assertRaises(ValueError) as cm:
                    buy_ticket(
                        car_plate="ABC123",
                        rate_name="zone_a",
                        euros=Decimal("4.00"),
                        payment_card=invalid_card,
                    )

                self.assertIn(
                    "Card number must be exactly 16 digits", str(cm.exception)
                )

    def test_rejects_invalid_verification_code(self) -> None:
        """Test that invalid verification codes are rejected."""
        # Given
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            self.pay_adapter,
            self.logger,
            self.tickets_repository,
        )

        invalid_cards = [
            PaymentCard("1234567890123456", "1234", date(2025, 12, 31)),  # 4 digits
            PaymentCard("1234567890123456", "12", date(2025, 12, 31)),  # 2 digits
            PaymentCard(
                "1234567890123456", "12a", date(2025, 12, 31)
            ),  # contains letter
            PaymentCard("1234567890123456", "", date(2025, 12, 31)),  # empty
        ]

        for invalid_card in invalid_cards:
            with self.subTest(verification_code=invalid_card.verification_code):
                # When/Then
                with self.assertRaises(ValueError) as cm:
                    buy_ticket(
                        car_plate="ABC123",
                        rate_name="zone_a",
                        euros=Decimal("4.00"),
                        payment_card=invalid_card,
                    )

                self.assertIn(
                    "Verification code must be exactly 3 digits", str(cm.exception)
                )

    def test_payment_adapter_logging(self) -> None:
        """Test that payment adapter can log payment calls."""
        # Given
        call_log: list[tuple[Decimal, PaymentCard]] = []
        pay_adapter_with_logging = _get_pay_adapter_with_logging(call_log)
        buy_ticket = _make_buy_ticket(
            self.now_adapter,
            self.rates_repository,
            pay_adapter_with_logging,
            self.logger,
            self.tickets_repository,
        )

        # When
        payment_card = PaymentCard(
            number="1234567890123456",
            verification_code="123",
            expiration=date(2025, 12, 31),
        )
        buy_ticket(
            car_plate="ABC123",
            rate_name="zone_a",
            euros=Decimal("2.00"),
            payment_card=payment_card,
        )

        # Then - verify the payment call was logged
        self.assertEqual(len(call_log), 1)
        logged_euros, logged_card = call_log[0]
        self.assertEqual(logged_euros, Decimal("2.00"))
        self.assertEqual(logged_card.number, "1234567890123456")
        self.assertEqual(logged_card.verification_code, "123")
        self.assertEqual(logged_card.expiration, date(2025, 12, 31))


if __name__ == "__main__":
    unittest.main()
