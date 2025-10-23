from pydantic.dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
    EmptyValueError,
    InvalidLengthError,
)


@dataclass(frozen=True)
class Content:
    _value: str

    # #
    # factory

    @classmethod
    def from_str(cls, value) -> "Content":
        if not isinstance(value, str):
            raise InvalidTypeError(target=cls.__name__, valid_type=str)

        if value == "":
            raise EmptyValueError(target=cls.__name__)

        if len(value) > 40:
            raise InvalidLengthError(target=cls.__name__, min_len=1, max_len=40)

        return cls(_value=value)

    # #
    # query

    def to_str(self) -> str:
        return self._value
