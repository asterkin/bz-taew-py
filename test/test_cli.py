import re
import shutil
import unittest
import subprocess
from configuration import TICKETS_FOLDER


class TestCLI(unittest.TestCase):
    """Test the bz CLI command interface and functionality."""

    def setUp(self) -> None:
        """Set up test environment by clearing tickets folder."""
        # Clear tickets folder from configuration
        if TICKETS_FOLDER.exists():
            shutil.rmtree(TICKETS_FOLDER)

    def _run_bz_command(self, args: list[str]) -> tuple[str, str, int]:
        """
        Run bz command with given arguments and return stdout, stderr, return code.

        Args:
            args: Command line arguments for bz (without 'bz')

        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        cmd = ["./bin/bz"] + args
        result = subprocess.run(
            cmd, capture_output=True, text=True, env={"PYTHONPATH": "./"}
        )
        return result.stdout, result.stderr, result.returncode

    def _normalize_timing_data(self, text: str) -> str:
        """
        Normalize timing-dependent data in CLI output for comparison.

        Args:
            text: Raw CLI output text

        Returns:
            Text with timing data normalized
        """
        # Replace timestamps with placeholder
        text = re.sub(
            r"timestamp=datetime\.datetime\([^)]+\)", "timestamp=<TIMESTAMP>", text
        )
        # Replace datetime objects in general
        text = re.sub(r"datetime\.datetime\([^)]+\)", "<DATETIME>", text)
        # Replace UUIDs with placeholder
        text = re.sub(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "<UUID>",
            text,
        )

        return text

    def test_cli_commands(self) -> None:
        """Test various bz CLI commands with expected outputs."""
        test_cases: list[tuple[str, list[str], list[str], list[str], int]] = [
            # (test_name, args, expected_stdout_contains, expected_stderr_contains, expected_return_code)
            # Basic help and version
            (
                "help",
                ["--help"],
                [
                    "usage: bz",
                    "Bluezone Application CLI",
                    "get-rates",
                    "check-car",
                    "buy-ticket",
                ],
                [],
                0,
            ),
            ("version", ["--version"], ["bz - v0.1.0"], [], 0),
            # get-rates command
            (
                "get_rates_success",
                ["get-rates"],
                [
                    "Rate(name='Blue', euros_per_hour=Decimal('0.80'))",
                    "Rate(name='Green', euros_per_hour=Decimal('0.85'))",
                    "Rate(name='Orange', euros_per_hour=Decimal('0.75'))",
                ],
                [
                    "INFO:Retrieving available parking rates",
                    "INFO:Retrieved 3 parking rates",
                ],
                0,
            ),
            # check-car command - success cases
            (
                "check_car_help",
                ["check-car", "--help"],
                ["usage: bz check-car", "car_plate", "rate_name"],
                [],
                0,
            ),
            (
                "check_car_blue",
                ["check-car", "ABC123", "Blue"],
                [
                    "CheckCarResult(car_plate='ABC123', rate_name='Blue'",
                ],
                [
                    "INFO:Starting parking inspection for car ABC123 in zone Blue",
                    "INFO:Parking inspection completed for car ABC123",
                ],
                0,
            ),
            (
                "check_car_green",
                ["check-car", "XYZ456", "Green"],
                [
                    "CheckCarResult(car_plate='XYZ456', rate_name='Green'",
                ],
                [
                    "INFO:Starting parking inspection for car XYZ456 in zone Green",
                    "INFO:Parking inspection completed for car XYZ456",
                ],
                0,
            ),
            # buy-ticket command - success cases
            (
                "buy_ticket_help",
                ["buy-ticket", "--help"],
                [
                    "usage: bz buy-ticket",
                    "car_plate",
                    "rate_name",
                    "euros",
                    "payment_card",
                ],
                [],
                0,
            ),
            (
                "buy_ticket_blue_success",
                [
                    "buy-ticket",
                    "ABC123",
                    "Blue",
                    "2.00",
                    '{"number":"1234567890123456","verification_code":"123","expiration":"12/25"}',
                ],
                [
                    "Ticket(ticket_code=",
                    "car_plate='ABC123', rate_name='Blue'",
                    "price=Decimal('2.00')",
                ],
                [
                    "INFO:Starting ticket purchase for car ABC123 in zone Blue for 2.00 euros",
                    "INFO:Processing payment of 2.00 euros",
                    "INFO:Payment successful with ID:",
                    "INFO:Ticket purchase completed successfully",
                ],
                0,
            ),
            (
                "buy_ticket_green_success",
                [
                    "buy-ticket",
                    "XYZ456",
                    "Green",
                    "5.50",
                    '{"number":"9876543210987654","verification_code":"456","expiration":"08/26"}',
                ],
                [
                    "Ticket(ticket_code=",
                    "car_plate='XYZ456', rate_name='Green'",
                    "price=Decimal('5.50')",
                ],
                [
                    "INFO:Starting ticket purchase for car XYZ456 in zone Green for 5.50 euros",
                    "INFO:Processing payment of 5.50 euros",
                ],
                0,
            ),
            # Error cases - missing arguments
            (
                "check_car_missing_args",
                ["check-car"],
                [],
                ["error: the following arguments are required: car_plate, rate_name"],
                2,
            ),
            (
                "buy_ticket_missing_args",
                ["buy-ticket", "ABC123"],
                [],
                [
                    "error: the following arguments are required: rate_name, euros, payment_card"
                ],
                2,
            ),
            # Error cases - invalid commands
            (
                "invalid_command",
                ["invalid-command"],
                [],
                ["error: argument", "invalid choice: 'invalid-command'"],
                2,
            ),
            # Error cases - business logic validation
            (
                "invalid_rate_zone",
                ["check-car", "ABC123", "InvalidZone"],
                [],
                [
                    "INFO:Starting parking inspection for car ABC123 in zone InvalidZone",
                    "ERROR:Invalid rate name: InvalidZone",
                    "Error: Rate 'InvalidZone' does not exist",
                ],
                1,
            ),
            (
                "amount_below_minimum",
                [
                    "buy-ticket",
                    "ABC123",
                    "Blue",
                    "0.25",
                    '{"number":"1234567890123456","verification_code":"123","expiration":"12/25"}',
                ],
                [],
                [
                    "INFO:Starting ticket purchase for car ABC123 in zone Blue for 0.25 euros",
                    "ERROR:Amount below minimum: 0.25 euros (minimum: 0.50)",
                    "Error: Amount 0.25 is less than minimum 0.50",
                ],
                1,
            ),
            (
                "invalid_card_number",
                [
                    "buy-ticket",
                    "ABC123",
                    "Blue",
                    "2.00",
                    '{"number":"123456789","verification_code":"123","expiration":"12/25"}',
                ],
                [],
                [
                    "INFO:Starting ticket purchase for car ABC123 in zone Blue for 2.00 euros",
                    "ERROR:Payment card validation failed: Card number must be exactly 16 digits",
                    "Error: Card number must be exactly 16 digits",
                ],
                1,
            ),
            (
                "invalid_card_vc",
                [
                    "buy-ticket",
                    "ABC123",
                    "Blue",
                    "2.00",
                    '{"number":"1234567890123456","verification_code":"12","expiration":"12/25"}',
                ],
                [],
                [
                    "INFO:Starting ticket purchase for car ABC123 in zone Blue for 2.00 euros",
                    "ERROR:Payment card validation failed: Verification code must be exactly 3 digits",
                    "Error: Verification code must be exactly 3 digits",
                ],
                1,
            ),
        ]

        for (
            test_name,
            args,
            expected_stdout_parts,
            expected_stderr_parts,
            expected_return_code,
        ) in test_cases:
            with self.subTest(test=test_name):
                stdout, stderr, return_code = self._run_bz_command(args)

                # Normalize timing data for comparison
                normalized_stdout = self._normalize_timing_data(stdout)
                normalized_stderr = self._normalize_timing_data(stderr)

                # Check return code
                self.assertEqual(
                    return_code,
                    expected_return_code,
                    f"Expected return code {expected_return_code}, got {return_code}",
                )

                # Check stdout contains expected parts
                for expected_part in expected_stdout_parts:
                    self.assertIn(
                        expected_part,
                        normalized_stdout,
                        f"Expected '{expected_part}' in stdout:\n{normalized_stdout}",
                    )

                # Check stderr contains expected parts
                for expected_part in expected_stderr_parts:
                    self.assertIn(
                        expected_part,
                        normalized_stderr,
                        f"Expected '{expected_part}' in stderr:\n{normalized_stderr}",
                    )


if __name__ == "__main__":
    unittest.main()
