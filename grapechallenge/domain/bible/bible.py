from pydantic.dataclasses import dataclass
from pydantic import ValidationError

from grapechallenge.domain.common.error import InvalidTypeError
from grapechallenge.domain.bible.date import Date
from grapechallenge.domain.bible.content import Content
from grapechallenge.domain.bible.reference import Reference


@dataclass(frozen=True)
class Bible:
    date: Date
    content: Content
    reference: Reference

    # #
    # factory

    @classmethod
    def new(
        cls,
        *,
        date: Date,
        content: Content,
        reference: Reference,
    ) -> "Bible":
        try:
            return cls(
                date=date,
                content=content,
                reference=reference,
            )
        except ValidationError as e:
            raise InvalidTypeError.from_pydantic(e)

    @classmethod
    def from_dict(cls, data: dict) -> "Bible":
        return cls.new(
            date=Date.from_date(
                data.get("date", None)
            ),
            content=Content.from_str(
                data.get("content", None)
            ),
            reference=Reference.from_str(
                data.get("reference", None)
            ),
        )

    # #
    # query

    def to_dict(self) -> dict:
        return {
            "date": self.date.to_date(),
            "content": self.content.to_str(),
            "reference": self.reference.to_str(),
        }

    # #
    # update

    def update_date(self, date: Date) -> "Bible":
        return Bible.new(
            date=date,
            content=self.content,
            reference=self.reference,
        )

    def update_content(self, content: Content) -> "Bible":
        return Bible.new(
            date=self.date,
            content=content,
            reference=self.reference,
        )

    def update_reference(self, reference: Reference) -> "Bible":
        return Bible.new(
            date=self.date,
            content=self.content,
            reference=reference,
        )
