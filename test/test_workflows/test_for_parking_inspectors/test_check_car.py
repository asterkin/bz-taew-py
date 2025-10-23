import unittest
from decimal import Decimal
from datetime import datetime, timedelta

from domain.rate import Rate
from domain.ticket import Ticket
from ports.for_storing_rates import RatesRepository as RatesRepositoryProtocol
from ports.for_storing_tickets import TicketsRepository as TicketsRepositoryProtocol
from typing import Any
from ports.for_parking_inspectors import CheckCarResult, CheckCar as CheckCarProtocol
from taew.ports.for_logging import Logger as LoggerProtocol
from taew.ports.for_obtaining_current_datetime import Now as NowProtocol


def _get_rates() -> RatesRepositoryProtocol:
    """Factory method to create a RAM-based rates repository with sample data."""
    from adapters.ram.for_storing_rates.rates_repository import RatesRepository

    repository = RatesRepository()
    zone_a_rate = Rate(name="Zone A", euros_per_hour=Decimal("2.00"))
    zone_b_rate = Rate(name="Zone B", euros_per_hour=Decimal("1.50"))
    repository["zone_a"] = zone_a_rate
    repository["zone_b"] = zone_b_rate

    return repository


def _get_tickets_repository(
    tickets: list[Ticket] | None = None,
) -> TicketsRepositoryProtocol:
    """Factory method to create a RAM-based tickets repository with sample data."""
    from adapters.ram.for_storing_tickets.tickets_repository import TicketsRepository

    repository = TicketsRepository()

    if tickets:
        for ticket in tickets:
            repository[ticket.ticket_code] = ticket

    return repository


def _get_now_adapter(test_datetime: datetime) -> NowProtocol:
    """Factory method to create a RAM-based datetime adapter with specific timestamp."""
    from taew.adapters.python.ram.for_obtaining_current_datetime import Now

    return Now(_now=test_datetime)


def _get_logger() -> tuple[LoggerProtocol, list[tuple[Any, ...]]]:
    """Factory method to create a RAM-based logger for testing."""
    from taew.adapters.python.ram.for_logging import Logger

    calls_list: list[tuple[Any, ...]] = []
    logger = Logger(_calls=calls_list)
    return logger, calls_list


def _make_check_car(
    now_adapter: NowProtocol,
    rates_repository: RatesRepositoryProtocol,
    logger: LoggerProtocol,
    tickets_repository: TicketsRepositoryProtocol,
) -> CheckCarProtocol:
    """Factory method to create CheckCar workflow instance."""
    from workflows.for_parking_inspectors.check_car import CheckCar

    return CheckCar(
        _now=now_adapter,
        _rates=rates_repository,
        _logger=logger,
        _tickets=tickets_repository,
    )


class TestCheckCar(unittest.TestCase):
    """Test cases for CheckCar workflow."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.rates_repository = _get_rates()

        # Base time for consistent testing
        self.now = datetime(2024, 1, 15, 14, 0, 0)

    def test_wrong_rate_name_raises_value_error(self) -> None:
        """Test that using a non-existent rate name raises ValueError."""
        # Given
        now_adapter = _get_now_adapter(self.now)
        tickets_repository = _get_tickets_repository([])
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When/Then
        with self.assertRaises(ValueError) as cm:
            check_car(car_plate="ABC123", rate_name="nonexistent_zone")

        self.assertEqual(str(cm.exception), "Rate 'nonexistent_zone' does not exist")

    def test_valid_parking_returns_legally_parked_true(self) -> None:
        """Test that a car with a valid (non-expired) ticket is legally parked."""
        # Given
        now_adapter = _get_now_adapter(self.now)

        valid_ticket = Ticket(
            ticket_code="1234567890",
            car_plate="ABC123",
            rate_name="zone_a",
            starting_date_time=self.now - timedelta(hours=1),
            ending_date_time=self.now + timedelta(hours=1),
            price=Decimal("4.00"),
            payment_id="payment_1",
        )

        tickets_repository = _get_tickets_repository([valid_ticket])
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When
        result = check_car(car_plate="ABC123", rate_name="zone_a")

        # Then
        self.assertIsInstance(result, CheckCarResult)
        self.assertEqual(result.car_plate, "ABC123")
        self.assertEqual(result.rate_name, "zone_a")
        self.assertEqual(result.timestamp, self.now)
        self.assertTrue(result.is_legally_parked)

    def test_no_ticket_found_returns_legally_parked_false(self) -> None:
        """Test that a car with no tickets is not legally parked."""
        # Given
        now_adapter = _get_now_adapter(self.now)

        tickets_repository = _get_tickets_repository([])
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When
        result = check_car(car_plate="ABC123", rate_name="zone_a")

        # Then
        self.assertEqual(result.car_plate, "ABC123")
        self.assertEqual(result.rate_name, "zone_a")
        self.assertEqual(result.timestamp, self.now)
        self.assertFalse(result.is_legally_parked)

    def test_expired_ticket_returns_legally_parked_false(self) -> None:
        """Test that a car with an expired ticket is not legally parked."""
        # Given
        now_adapter = _get_now_adapter(self.now)

        expired_ticket = Ticket(
            ticket_code="1234567890",
            car_plate="ABC123",
            rate_name="zone_a",
            starting_date_time=self.now - timedelta(hours=3),
            ending_date_time=self.now - timedelta(hours=1),
            price=Decimal("4.00"),
            payment_id="payment_1",
        )

        tickets_repository = _get_tickets_repository([expired_ticket])
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When
        result = check_car(car_plate="ABC123", rate_name="zone_a")

        # Then
        self.assertEqual(result.car_plate, "ABC123")
        self.assertEqual(result.rate_name, "zone_a")
        self.assertEqual(result.timestamp, self.now)
        self.assertFalse(result.is_legally_parked)

    def test_uses_latest_ticket_when_multiple_exist(self) -> None:
        """Test that the workflow uses the latest ticket when multiple exist."""
        # Given
        now_adapter = _get_now_adapter(self.now)

        older_expired_ticket = Ticket(
            ticket_code="1111111111",
            car_plate="ABC123",
            rate_name="zone_a",
            starting_date_time=self.now - timedelta(hours=5),
            ending_date_time=self.now - timedelta(hours=3),
            price=Decimal("2.00"),
            payment_id="payment_1",
        )

        newer_valid_ticket = Ticket(
            ticket_code="2222222222",
            car_plate="ABC123",
            rate_name="zone_a",
            starting_date_time=self.now - timedelta(hours=1),
            ending_date_time=self.now + timedelta(hours=1),
            price=Decimal("4.00"),
            payment_id="payment_2",
        )

        tickets_repository = _get_tickets_repository(
            [older_expired_ticket, newer_valid_ticket]
        )
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When
        result = check_car(car_plate="ABC123", rate_name="zone_a")

        # Then - should use newer valid ticket
        self.assertTrue(result.is_legally_parked)

    def test_filters_by_both_car_plate_and_rate_name(self) -> None:
        """Test that tickets are filtered by both car_plate and rate_name."""
        # Given
        now_adapter = _get_now_adapter(self.now)

        different_car_ticket = Ticket(
            ticket_code="1111111111",
            car_plate="XYZ789",
            rate_name="zone_a",
            starting_date_time=self.now - timedelta(hours=1),
            ending_date_time=self.now + timedelta(hours=1),
            price=Decimal("4.00"),
            payment_id="payment_1",
        )

        different_zone_ticket = Ticket(
            ticket_code="2222222222",
            car_plate="ABC123",
            rate_name="zone_b",
            starting_date_time=self.now - timedelta(hours=1),
            ending_date_time=self.now + timedelta(hours=1),
            price=Decimal("3.00"),
            payment_id="payment_2",
        )

        tickets_repository = _get_tickets_repository(
            [different_car_ticket, different_zone_ticket]
        )
        logger, _ = _get_logger()
        check_car = _make_check_car(
            now_adapter, self.rates_repository, logger, tickets_repository
        )

        # When - check for ABC123 in zone_a (should find no matching tickets)
        result = check_car(car_plate="ABC123", rate_name="zone_a")

        # Then - no matching ticket found
        self.assertFalse(result.is_legally_parked)


if __name__ == "__main__":
    unittest.main()
