"""Tests for bz CLI command interface and functionality."""

import shutil
import unittest

from taew.domain.cli import Result
from taew.domain.cli_test import SubTest, Test
from taew.utils.unittest import TestCLI as BaseTestCLI

from configuration import TICKETS_FOLDER


class TestCLI(BaseTestCLI):
    """Test the bz CLI command interface and functionality."""

    def setUp(self) -> None:
        """Set up test environment by clearing tickets folder."""
        super().setUp()
        # Clear tickets folder from configuration
        if TICKETS_FOLDER.exists():
            shutil.rmtree(TICKETS_FOLDER)

    def test_help_and_version(self) -> None:
        """Test basic help and version commands."""
        self._run(
            Test(
                name="Help and Version",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="help",
                        args=("--help",),
                        expected=Result(
                            stdout="""
                                usage: bz [-h] [--version] {buy-ticket,check-car,get-rates} ...

                                Bluezone Application CLI Adapters Driver

                                positional arguments:
                                  {buy-ticket,check-car,get-rates}
                                    buy-ticket          Buys a parking ticket.
                                    check-car           Call self as a function.
                                    get-rates           Returns an iterable of available parking rates.

                                options:
                                  -h, --help            show this help message and exit
                                  --version             show program's version number and exit
                            """,
                            stderr="",
                            returncode=0,
                        ),
                    ),
                    SubTest(
                        name="version",
                        args=("--version",),
                        expected=Result(
                            stdout="bz - v0.1.0",
                            stderr="",
                            returncode=0,
                        ),
                    ),
                ),
            )
        )

    def test_get_rates(self) -> None:
        """Test get-rates command."""
        self._run(
            Test(
                name="Get Rates",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="get_rates_success",
                        args=("get-rates",),
                        expected=Result(
                            stdout="""
                                [Rate(name='Blue', euros_per_hour=Decimal('0.80')),
                                 Rate(name='Green', euros_per_hour=Decimal('0.85')),
                                 Rate(name='Orange', euros_per_hour=Decimal('0.75'))]
                            """,
                            stderr="""
                                INFO:Retrieving available parking rates
                                INFO:Retrieved 3 parking rates
                            """,
                            returncode=0,
                        ),
                    ),
                ),
            )
        )

    def test_check_car_success(self) -> None:
        """Test check-car command with valid inputs."""
        self._run(
            Test(
                name="Check Car Success",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="check_car_blue",
                        args=("check-car", "ABC123", "Blue"),
                        expected=Result(
                            stdout="""
                                CheckCarResult(car_plate='ABC123', rate_name='Blue', timestamp=<TIMESTAMP>, is_legally_parked=False)
                            """,
                            stderr="""
                                INFO:Starting parking inspection for car ABC123 in zone Blue
                                INFO:Parking inspection completed for car ABC123 - Status: ILLEGALLY PARKED
                            """,
                            returncode=0,
                        ),
                    ),
                ),
            )
        )

    def test_buy_ticket_success(self) -> None:
        """Test buy-ticket command with valid inputs."""
        self._run(
            Test(
                name="Buy Ticket Success",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="buy_ticket_blue_success",
                        args=(
                            "buy-ticket",
                            "ABC123",
                            "Blue",
                            "2.00",
                            '{"number":"1234567890123456","verification_code":"123","expiration":"12/25"}',
                        ),
                        expected=Result(
                            stdout="""
                                Ticket(ticket_code='<UUID>', car_plate='ABC123', rate_name='Blue', starting_date_time=<DATETIME>, ending_date_time=<DATETIME>, price=Decimal('2.00'), payment_id='<UUID>')
                            """,
                            stderr="""
                                INFO:Starting ticket purchase for car ABC123 in zone Blue for 2.00 euros
                                INFO:Processing payment of 2.00 euros
                                INFO:Payment successful with ID: <UUID>
                                INFO:Ticket purchase completed successfully for car ABC123 - Ticket: <UUID>
                            """,
                            returncode=0,
                        ),
                    ),
                ),
            )
        )

    def test_error_missing_arguments(self) -> None:
        """Test error cases with missing arguments."""
        self._run(
            Test(
                name="Missing Arguments",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="check_car_missing_args",
                        args=("check-car",),
                        expected=Result(
                            stdout="",
                            stderr="""
                                usage: bz check-car [-h] car_plate rate_name
                                bz check-car: error: the following arguments are required: car_plate, rate_name
                            """,
                            returncode=2,
                        ),
                    ),
                ),
            )
        )

    def test_error_invalid_rate_zone(self) -> None:
        """Test error case with invalid rate zone."""
        self._run(
            Test(
                name="Invalid Rate Zone",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="invalid_rate_zone",
                        args=("check-car", "ABC123", "InvalidZone"),
                        expected=Result(
                            stdout="",
                            stderr="""
                                INFO:Starting parking inspection for car ABC123 in zone InvalidZone
                                ERROR:Invalid rate name: InvalidZone
                                Error: Rate 'InvalidZone' does not exist
                            """,
                            returncode=1,
                        ),
                    ),
                ),
            )
        )

    def test_error_amount_below_minimum(self) -> None:
        """Test error case with amount below minimum."""
        self._run(
            Test(
                name="Amount Below Minimum",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="amount_below_minimum",
                        args=(
                            "buy-ticket",
                            "ABC123",
                            "Blue",
                            "0.25",
                            '{"number":"1234567890123456","verification_code":"123","expiration":"12/25"}',
                        ),
                        expected=Result(
                            stdout="",
                            stderr="""
                                INFO:Starting ticket purchase for car ABC123 in zone Blue for 0.25 euros
                                ERROR:Amount below minimum: 0.25 euros (minimum: 0.50)
                                Error: Amount 0.25 is less than minimum 0.50
                            """,
                            returncode=1,
                        ),
                    ),
                ),
            )
        )

    def test_error_invalid_card_number(self) -> None:
        """Test error case with invalid card number."""
        self._run(
            Test(
                name="Invalid Card Number",
                command="./bin/bz",
                subtests=(
                    SubTest(
                        name="invalid_card_number",
                        args=(
                            "buy-ticket",
                            "ABC123",
                            "Blue",
                            "2.00",
                            '{"number":"123456789","verification_code":"123","expiration":"12/25"}',
                        ),
                        expected=Result(
                            stdout="",
                            stderr="""
                                INFO:Starting ticket purchase for car ABC123 in zone Blue for 2.00 euros
                                ERROR:Payment card validation failed: Card number must be exactly 16 digits
                                Error: Card number must be exactly 16 digits
                            """,
                            returncode=1,
                        ),
                    ),
                ),
            )
        )


if __name__ == "__main__":
    unittest.main()
