from pydantic.dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
    EmptyValueError,
    DisallowedValueError,
)


@dataclass(frozen=True)
class Type:
    _value: str
    _allowed_list = ["NORMAL", "EVENT"]

    # #
    # factory

    @classmethod
    def from_str(cls, value) -> "Type":
        if not isinstance(value, str):
            raise InvalidTypeError(target=cls.__name__, valid_type=str)

        if value == "":
            raise EmptyValueError(target=cls.__name__)

        if value not in cls._allowed_list:
            raise DisallowedValueError(target=cls.__name__, allowed_list=cls._allowed_list)

        return cls(_value=value)

    # #
    # query

    def to_str(self) -> str:
        return self._value
