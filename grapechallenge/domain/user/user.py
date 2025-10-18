from pydantic.dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.user import (
    Cell,
    Name,
)


@dataclass(frozen=True)
class User:
    cell: Cell
    name: Name

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        cell: Cell,
        name: Name,
    ) -> "User":
        try:
            return cls(
                cell=cell,
                name=name
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls.new(
            cell=Cell.from_str(
                data.get("cell", None)
            ),
            name=Name.from_str(
                data.get("name", None)
            ),
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "cell": self.cell.to_str(),
            "name": self.name.to_str(),
        }

    # #
    # update

    def update_cell(self, cell: Cell) -> "User":
        return User.new(
            cell=cell,
            name=self.name
        )

    def update_name(self, name: Name) -> "User":
        return User.new(
            cell=self.cell,
            name=name
        )
