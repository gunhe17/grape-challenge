from pydantic.dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
    EmptyValueError,
)


@dataclass(frozen=True)
class Cell:
    _value: str

    # #
    # factory

    @classmethod
    def from_str(cls, value) -> "Cell":
        if not isinstance(value, str):
            raise InvalidTypeError(target=cls.__name__, valid_type=str)

        if value == "":
            raise EmptyValueError(target=cls.__name__)

        return cls(_value=value)

    # #
    # query

    def to_str(self) -> str:
        return self._value
