from collections.abc import Iterable
from typing import Protocol, Callable, Optional, Any

from domain.ticket import Ticket


class TicketsRepository(Protocol):
    """Port for retrieving parking tickets."""

    def __getitem__(self, key: str, /) -> Ticket:
        """Retrieve a ticket by its identifier.

        Args:
            key: The ticket identifier or ticket code

        Returns:
            The Ticket object for the specified key

        Raises:
            KeyError: If the ticket with the given key is not found
        """
        ...

    def query(
        self,
        *,
        filter_fn: Callable[[Ticket], bool],
        sort_key: Optional[Callable[[Ticket], Any]] = None,
        reverse: bool = False,
    ) -> Iterable[Ticket]:
        """Query tickets based on a filter and sort_key functions.

        Args:
            filter_fn: A function that takes a Ticket object and returns True if it matches the query.
            sort_key: An optional function that takes a Ticket object and returns a value to sort by.
            reverse: Whether to reverse the sort order.

        Returns:
            A, potentially sorted, sequence of Ticket objects that match the query.
        """
        ...


class MutableTicketsRepository(Protocol):
    """Port for storing and retrieving parking tickets."""

    def __setitem__(self, key: str, value: Ticket, /) -> None:
        """Store a ticket with the given identifier.

        Args:
            key: The ticket identifier or ticket code
            value: The Ticket object to store
        """
        ...
