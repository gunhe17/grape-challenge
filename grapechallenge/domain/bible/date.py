from datetime import date
from dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
)


@dataclass(frozen=True)
class Date:
    _value: date

    # #
    # factory

    @classmethod
    def from_date(cls, value) -> "Date":
        if not isinstance(value, date):
            raise InvalidTypeError(target=cls.__name__, valid_type=date)

        return cls(_value=value)

    # #
    # query

    def to_date(self) -> date:
        return self._value
