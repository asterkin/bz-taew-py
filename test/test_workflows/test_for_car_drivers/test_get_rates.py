import unittest
from decimal import Decimal
from typing import Any

from domain.rate import Rate
from taew.ports.for_logging import Logger as LoggerProtocol
from ports.for_car_drivers import GetRates as GetRatesProtocol
from ports.for_storing_rates import RatesRepository as RatesRepositoryProtocol


def _get_rates() -> RatesRepositoryProtocol:
    """Factory method to create a RAM-based rates repository with sample data."""
    from adapters.ram.for_storing_rates import RatesRepository
    from decimal import Decimal

    repository = RatesRepository()

    # Populate with sample data
    zone_a_rate = Rate(name="Zone A", euros_per_hour=Decimal("1.50"))
    zone_b_rate = Rate(name="Zone B", euros_per_hour=Decimal("2.00"))
    zone_c_rate = Rate(name="Zone C", euros_per_hour=Decimal("3.50"))

    repository["zone_a"] = zone_a_rate
    repository["zone_b"] = zone_b_rate
    repository["zone_c"] = zone_c_rate

    return repository


def _get_logger() -> tuple[LoggerProtocol, list[tuple[Any, ...]]]:
    """Factory method to create a RAM-based logger for testing."""
    from taew.adapters.python.ram.for_logging import Logger

    calls_list: list[tuple[Any, ...]] = []
    logger = Logger(_calls=calls_list)
    return logger, calls_list


def _make_get_rates(
    rates_repository: RatesRepositoryProtocol, logger: LoggerProtocol
) -> GetRatesProtocol:
    """Factory method to create GetRates workflow instance."""
    from workflows.for_car_drivers.get_rates import GetRates

    return GetRates(_rates=rates_repository, _logger=logger)


class TestGetRates(unittest.TestCase):
    """Test cases for GetRates workflow."""

    def test_returns_all_rates_from_repository(self) -> None:
        """Test that GetRates returns all rates from the repository."""
        # Given
        rates_repository = _get_rates()
        logger, log_calls = _get_logger()
        get_rates = _make_get_rates(rates_repository, logger)

        # When
        result = list(get_rates())

        # Then
        self.assertEqual(len(result), 3)
        # Check that all expected rates are present
        rate_names = [rate.name for rate in result]
        self.assertIn("Zone A", rate_names)
        self.assertIn("Zone B", rate_names)
        self.assertIn("Zone C", rate_names)

        # Verify logging - check that rates retrieval was logged
        info_logs = [call for call in log_calls if call[0] == "info"]
        self.assertGreaterEqual(
            len(info_logs), 2, "Expected info logs for retrieval start and completion"
        )

        # Verify that rate count was logged
        rate_count_logged = any(
            "Retrieved %d parking rates" in str(call[1]) and call[2] == (3,)
            for call in info_logs
        )
        self.assertTrue(rate_count_logged, "Expected rate count to be logged")

    def test_returns_empty_iterable_when_repository_is_empty(self) -> None:
        """Test that GetRates returns empty iterable when repository has no rates."""
        # Given
        from adapters.ram.for_storing_rates import RatesRepository

        empty_repository: RatesRepositoryProtocol = RatesRepository()
        logger, _ = _get_logger()
        get_rates = _make_get_rates(empty_repository, logger)

        # When
        result = list(get_rates())

        # Then
        self.assertEqual(len(result), 0)

    def test_workflow_preserves_rate_order(self) -> None:
        """Test that GetRates preserves the order from repository values()."""
        # Given
        from adapters.ram.for_storing_rates import RatesRepository

        rate1 = Rate(name="First", euros_per_hour=Decimal("1.00"))
        rate2 = Rate(name="Second", euros_per_hour=Decimal("2.00"))

        rates_repository = RatesRepository()
        rates_repository["first"] = rate1
        rates_repository["second"] = rate2

        logger, _ = _get_logger()
        get_rates = _make_get_rates(rates_repository, logger)

        # When
        result = list(get_rates())

        # Then
        self.assertEqual(result, [rate1, rate2])


if __name__ == "__main__":
    unittest.main()
