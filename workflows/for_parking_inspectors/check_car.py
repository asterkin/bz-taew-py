from dataclasses import dataclass

from taew.ports.for_logging import Logger
from ports.for_parking_inspectors import CheckCarResult
from ports.for_storing_rates import RatesRepository
from ports.for_storing_tickets import TicketsRepository
from taew.ports.for_obtaining_current_datetime import Now


@dataclass(eq=False, frozen=True)
class CheckCar:
    _now: Now
    _rates: RatesRepository
    _logger: Logger
    _tickets: TicketsRepository

    def __call__(self, *, car_plate: str, rate_name: str) -> CheckCarResult:
        self._logger.info(
            "Starting parking inspection for car %s in zone %s",
            car_plate,
            rate_name,
            extra={"car_plate": car_plate, "rate_name": rate_name},
        )

        if rate_name not in self._rates:
            error_msg = f"Rate '{rate_name}' does not exist"
            self._logger.error(
                "Invalid rate name: %s",
                rate_name,
                extra={"car_plate": car_plate, "rate_name": rate_name},
            )
            raise ValueError(error_msg)

        now = self._now()
        self._logger.debug(
            "Inspection timestamp: %s",
            now,
            extra={"car_plate": car_plate, "timestamp": now.isoformat()},
        )

        # Query for tickets matching car_plate and rate_name, sorted by ending_date_time descending
        self._logger.debug(
            "Querying tickets for car %s in zone %s",
            car_plate,
            rate_name,
            extra={"car_plate": car_plate, "rate_name": rate_name},
        )
        matching_tickets = self._tickets.query(
            filter_fn=lambda t: t.car_plate == car_plate and t.rate_name == rate_name,
            sort_key=lambda t: t.ending_date_time,
            reverse=True,
        )

        # Get the latest ticket (most recent ending_date_time)
        latest_ticket = next(iter(matching_tickets), None)

        if latest_ticket:
            self._logger.debug(
                "Found latest ticket %s for car %s, expires at %s",
                latest_ticket.ticket_code,
                car_plate,
                latest_ticket.ending_date_time,
                extra={
                    "car_plate": car_plate,
                    "ticket_code": latest_ticket.ticket_code,
                    "expiry_time": latest_ticket.ending_date_time.isoformat(),
                },
            )
        else:
            self._logger.debug(
                "No tickets found for car %s in zone %s",
                car_plate,
                rate_name,
                extra={"car_plate": car_plate, "rate_name": rate_name},
            )

        # Determine if legally parked
        is_legally_parked = (
            latest_ticket is not None and latest_ticket.ending_date_time > now
        )

        self._logger.info(
            "Parking inspection completed for car %s - Status: %s",
            car_plate,
            "LEGALLY PARKED" if is_legally_parked else "ILLEGALLY PARKED",
            extra={
                "car_plate": car_plate,
                "rate_name": rate_name,
                "is_legally_parked": is_legally_parked,
                "timestamp": now.isoformat(),
                "has_valid_ticket": latest_ticket is not None,
                "ticket_code": latest_ticket.ticket_code if latest_ticket else None,
            },
        )

        return CheckCarResult(
            car_plate=car_plate,
            rate_name=rate_name,
            timestamp=now,
            is_legally_parked=is_legally_parked,
        )
