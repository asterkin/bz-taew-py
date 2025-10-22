from typing import Iterable
from dataclasses import dataclass

from domain.rate import Rate
from taew.ports.for_logging import Logger
from ports.for_storing_rates import RatesRepository


@dataclass(eq=False, frozen=True)
class GetRates:
    _rates: RatesRepository
    _logger: Logger

    def __call__(self) -> Iterable[Rate]:
        """
        Retrieve available parking rates.

        Args: None

        Returns: Iterable[Rate]
        """
        self._logger.info("Retrieving available parking rates")
        rates = list(self._rates.values())
        self._logger.info(
            "Retrieved %d parking rates",
            len(rates),
            extra={
                "rate_count": len(rates),
                "rate_names": [rate.name for rate in rates],
            },
        )
        return rates
