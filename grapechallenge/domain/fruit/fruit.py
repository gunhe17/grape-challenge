from pydantic.dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.fruit import Status


@dataclass(frozen=True)
class Fruit:
    user_id: str
    template_id: str
    status: Status

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        user_id: str,
        template_id: str,
        status: Status,
    ) -> "Fruit":
        try:
            return cls(
                user_id=user_id,
                template_id=template_id,
                status=status
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "Fruit":
        return cls.new(
            user_id=data.get("user_id", None),          #type: ignore
            template_id=data.get("template_id", None),  #type: ignore
            status=Status.from_str(
                data.get("status", None)
            ),
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "template_id": self.template_id,
            "status": self.status.to_str(),
        }

    # #
    # update

    def next_status(self) -> "Fruit":
        current = self.status.to_str()

        match current:
            case "FIRST_STATUS":
                next_status = "SECOND_STATUS"
            case "SECOND_STATUS":
                next_status = "THIRD_STATUS"
            case "THIRD_STATUS":
                next_status = "FOURTH_STATUS"
            case "FOURTH_STATUS":
                next_status = "FIFTH_STATUS"
            case "FIFTH_STATUS":
                next_status = "SIXTH_STATUS"
            case "SIXTH_STATUS":
                next_status = "SEVENTH_STATUS"
            case "SEVENTH_STATUS":
                next_status = "SEVENTH_STATUS"
            case _:
                next_status = current

        return Fruit.new(
            user_id=self.user_id,
            template_id=self.template_id,
            status=Status.from_str(next_status),
        )