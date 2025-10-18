from pydantic.dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError


@dataclass(frozen=True)
class Mission:
    user_id: str
    template_id: str
    fruit_id: str

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        user_id: str,
        template_id: str,
        fruit_id: str,
    ) -> "Mission":
        try:
            return cls(
                user_id=user_id,
                template_id=template_id,
                fruit_id=fruit_id,
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "Mission":
        return cls.new(
            user_id=data.get("user_id", None),          #type: ignore
            template_id=data.get("template_id", None),  #type: ignore
            fruit_id=data.get("fruit_id", None),        #type: ignore
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "template_id": self.template_id,
            "fruit_id": self.fruit_id,
        }
