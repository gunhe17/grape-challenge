from dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.mission_template.name import Name
from grapechallenge.domain.mission_template.content import Content
from grapechallenge.domain.mission_template.type import Type


@dataclass(frozen=True)
class MissionTemplate:
    name: Name
    content: Content
    type: Type

    # #
    # factory

    @classmethod
    def new(cls, *, name: Name, content: Content, type: Type) -> "MissionTemplate":
        try:
            return cls(
                name=name,
                content=content,
                type=type,
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "MissionTemplate":
        return cls.new(
            name=Name.from_str(
                data.get("name", None)
            ),
            content=Content.from_str(
                data.get("content", None)
            ),
            type=Type.from_str(
                data.get("type", None)
            ),
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "name": self.name.to_str(),
            "content": self.content.to_str(),
            "type": self.type.to_str(),
        }

    # #
    # update

    def update_name(self, name: Name) -> "MissionTemplate":
        return MissionTemplate.new(
            name=name,
            content=self.content,
            type=self.type,
        )

    def update_content(self, content: Content) -> "MissionTemplate":
        return MissionTemplate.new(
            name=self.name,
            content=content,
            type=self.type,
        )

    def update_type(self, type: Type) -> "MissionTemplate":
        return MissionTemplate.new(
            name=self.name,
            content=self.content,
            type=type,
        )
