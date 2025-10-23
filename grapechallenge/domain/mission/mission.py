from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.mission.content import Content


@dataclass(frozen=True)
class Mission:
    user_id: str
    template_id: str
    fruit_id: str
    content: Optional[Content]

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        user_id: str,
        template_id: str,
        fruit_id: str,
        content: Optional[Content],
    ) -> "Mission":
        try:
            return cls(
                user_id=user_id,
                template_id=template_id,
                fruit_id=fruit_id,
                content=content,
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "Mission":
        return cls.new(
            user_id=data.get("user_id", None),          #type: ignore
            template_id=data.get("template_id", None),  #type: ignore
            fruit_id=data.get("fruit_id", None),        #type: ignore
            content=(
                Content.from_str(data["content"]) if data["content"] else None
            )
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "template_id": self.template_id,
            "fruit_id": self.fruit_id,
            "content": (
                self.content.to_str() if self.content else None
            )
        }