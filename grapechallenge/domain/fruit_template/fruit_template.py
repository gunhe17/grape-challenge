from dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.fruit_template import (
    Name,
    Type,
    FirstStatus,
    SecondStatus,
    ThirdStatus,
    FourthStatus,
    FifthStatus,
    SixthStatus,
    SeventhStatus,
)


@dataclass(frozen=True)
class FruitTemplate:
    name: Name
    type: Type
    first_status: FirstStatus
    second_status: SecondStatus
    third_status: ThirdStatus
    fourth_status: FourthStatus
    fifth_status: FifthStatus
    sixth_status: SixthStatus
    seventh_status: SeventhStatus

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        name: Name,
        type: Type,
        first_status: FirstStatus,
        second_status: SecondStatus,
        third_status: ThirdStatus,
        fourth_status: FourthStatus,
        fifth_status: FifthStatus,
        sixth_status: SixthStatus,
        seventh_status: SeventhStatus,
    ) -> "FruitTemplate":
        try:
            return cls(
                name=name,
                type=type,
                first_status=first_status,
                second_status=second_status,
                third_status=third_status,
                fourth_status=fourth_status,
                fifth_status=fifth_status,
                sixth_status=sixth_status,
                seventh_status=seventh_status,
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "FruitTemplate":
        return cls.new(
            name=Name.from_str(
                data.get("name", None)
            ),
            type=Type.from_str(
                data.get("type", None)
            ),
            first_status=FirstStatus.from_str(
                data.get("first_status", None)
            ),
            second_status=SecondStatus.from_str(
                data.get("second_status", None)
            ),
            third_status=ThirdStatus.from_str(
                data.get("third_status", None)
            ),
            fourth_status=FourthStatus.from_str(
                data.get("fourth_status", None)
            ),
            fifth_status=FifthStatus.from_str(
                data.get("fifth_status", None)
            ),
            sixth_status=SixthStatus.from_str(
                data.get("sixth_status", None)
            ),
            seventh_status=SeventhStatus.from_str(
                data.get("seventh_status", None)
            ),
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "name": self.name.to_str(),
            "type": self.type.to_str(),
            "first_status": self.first_status.to_str(),
            "second_status": self.second_status.to_str(),
            "third_status": self.third_status.to_str(),
            "fourth_status": self.fourth_status.to_str(),
            "fifth_status": self.fifth_status.to_str(),
            "sixth_status": self.sixth_status.to_str(),
            "seventh_status": self.seventh_status.to_str(),
        }

    # #
    # update

    def update_name(self, name: Name) -> "FruitTemplate":
        return FruitTemplate.new(
            name=name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_type(self, type: Type) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_first_status(self, first_status: FirstStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_second_status(self, second_status: SecondStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_third_status(self, third_status: ThirdStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_fourth_status(self, fourth_status: FourthStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_fifth_status(self, fifth_status: FifthStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_sixth_status(self, sixth_status: SixthStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=sixth_status,
            seventh_status=self.seventh_status,
        )

    def update_seventh_status(self, seventh_status: SeventhStatus) -> "FruitTemplate":
        return FruitTemplate.new(
            name=self.name,
            type=self.type,
            first_status=self.first_status,
            second_status=self.second_status,
            third_status=self.third_status,
            fourth_status=self.fourth_status,
            fifth_status=self.fifth_status,
            sixth_status=self.sixth_status,
            seventh_status=seventh_status,
        )