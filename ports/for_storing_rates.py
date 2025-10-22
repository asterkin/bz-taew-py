from typing import Iterable, Protocol

from domain.rate import Rate


class RatesRepository(Protocol):
    """Port for storing and retrieving parking rates."""

    def __contains__(self, key: str, /) -> bool:
        """Check if a rate exists in the repository.

        Args:
            key: The rate identifier or zone name

        Returns:
            True if the rate exists, False otherwise
        """
        ...

    def __getitem__(self, key: str, /) -> Rate:
        """Retrieve a rate by its identifier/zone name.

        Args:
            key: The rate identifier or zone name

        Returns:
            The Rate object for the specified key

        Raises:
            KeyError: If the rate with the given key is not found
        """
        ...

    def values(self) -> Iterable[Rate]:
        """Retrieve all available rates.

        Returns:
            An iterable of all Rate objects in the repository
        """
        ...
