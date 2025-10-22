from typing import TypeAlias
from domain.rate import Rate


RatesRepository: TypeAlias = dict[str, Rate]
