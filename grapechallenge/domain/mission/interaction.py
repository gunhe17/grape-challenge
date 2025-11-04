from typing import List
from pydantic.dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
    DisallowedValueError,
    InvalidLengthError,
)


@dataclass(frozen=True)
class Interaction:
    _value: List[str]
    _allowed_list = ["😆", "😮", "💪", "🙏", "👏"]

    # #
    # factory

    @classmethod
    def from_list(cls, value) -> "Interaction":
        if not isinstance(value, list):
            raise InvalidTypeError(target=cls.__name__, valid_type=list)

        for item in value:
            if not isinstance(item, str):
                raise InvalidTypeError(target=f"{cls.__name__} item", valid_type=str)

            if len(item) != 1:
                raise InvalidLengthError(target=f"{cls.__name__} item", min_len=1, max_len=1)

            if item not in cls._allowed_list:
                raise DisallowedValueError(target=f"{cls.__name__} item", allowed_list=cls._allowed_list)

        return cls(_value=value)

    # #
    # command

    def add(self, emoji: str) -> "Interaction":
        if not isinstance(emoji, str):
            raise InvalidTypeError(target=f"{self.__class__.__name__} item", valid_type=str)

        if len(emoji) != 1:
            raise InvalidLengthError(target=f"{self.__class__.__name__} item", min_len=1, max_len=1)

        if emoji not in self._allowed_list:
            raise DisallowedValueError(target=f"{self.__class__.__name__} item", allowed_list=self._allowed_list)

        return self.__class__(_value=self._value + [emoji])

    # #
    # query

    def to_list(self) -> List[str]:
        return self._value

    @classmethod
    def allowed(cls) -> List[str]:
        return cls._allowed_list
