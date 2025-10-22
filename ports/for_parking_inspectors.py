from datetime import datetime
from typing import Protocol, NamedTuple


class CheckCarResult(NamedTuple):
    car_plate: str
    rate_name: str
    timestamp: datetime
    is_legally_parked: bool


class CheckCar(Protocol):
    def __call__(self, *, car_plate: str, rate_name: str) -> CheckCarResult: ...
