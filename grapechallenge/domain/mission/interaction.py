from typing import List, Dict
from pydantic.dataclasses import dataclass

from grapechallenge.domain.common.error import (
    InvalidTypeError,
    DisallowedValueError,
)


@dataclass(frozen=True)
class Interaction:
    _value: List[Dict[str, str]]
    _allowed_list = ["😆", "😮", "💪", "🙏", "👏"]

    # #
    # factory

    @classmethod
    def from_list(cls, value: List[Dict[str, str]]) -> "Interaction":
        if not isinstance(value, list):
            raise InvalidTypeError(target=cls.__name__, valid_type=list)

        for item in value:
            if not isinstance(item, dict):
                raise InvalidTypeError(target=f"{cls.__name__} item", valid_type=dict)

            if not "icon" in item:
                raise ValueError(f"{cls.__name__} item must have 'icon'")
            
            if not "user_id" in item:
                raise ValueError(f"{cls.__name__} item must have 'user_id'")

            if not item["icon"] in cls._allowed_list:
                raise DisallowedValueError(target=f"{cls.__name__} icon", allowed_list=cls._allowed_list)

        return cls(_value=value)
    
    # #
    # command

    def add(self, emoji: str, user_id: str) -> "Interaction":
        if emoji not in self._allowed_list:
            raise DisallowedValueError(target="emoji", allowed_list=self._allowed_list)

        filtered = [item for item in self._value if item["user_id"] != user_id]

        added = filtered
        added.append({"icon": emoji, "user_id": user_id})

        return self.__class__(_value=added)

    # #
    # query

    def to_list(self) -> List[Dict[str, str]]:
        return self._value
    
    def to_mine(self, user_id: str) -> Dict[str, str]:
        return (
            [item for item in self._value if item["user_id"] == user_id]
        )[0]

    @classmethod
    def allowed(cls) -> List[str]:
        return cls._allowed_list