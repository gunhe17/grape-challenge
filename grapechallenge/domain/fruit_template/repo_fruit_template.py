from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo, kst
from grapechallenge.domain.fruit_template import FruitTemplate


class FruitTemplateModel(Base):
    __tablename__ = "fruit_templates"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    first_status = Column(String(500), nullable=False)
    second_status = Column(String(500), nullable=False)
    third_status = Column(String(500), nullable=False)
    fourth_status = Column(String(500), nullable=False)
    fifth_status = Column(String(500), nullable=False)
    sixth_status = Column(String(500), nullable=False)
    seventh_status = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoFruitTemplate(Repo):
    __table__: str = "fruit_templates"

    def __init__(
        self,
        id: str,
        fruit_template: FruitTemplate,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.fruit_template = fruit_template
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        fruit_template: FruitTemplate,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(fruit_template.to_dict()),
            "created_at": created_at or datetime.now(),
            "updated_at": updated_at,
        }

    def summary(self) -> dict:
        return {
            "id": self.id,
            "created_at": kst(self.created_at),
            "updated_at": kst(self.updated_at),
        }

    # #
    # command

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        fruit_template: FruitTemplate
    ) -> "RepoFruitTemplate":

        created = await cls.insert(
            session=session,
            model_class=FruitTemplateModel,
            data=cls._model(fruit_template=fruit_template)
        )

        return cls(
            id=created.id,
            fruit_template=FruitTemplate.from_dict({
                "name": created.name,
                "type": created.type,
                "first_status": created.first_status,
                "second_status": created.second_status,
                "third_status": created.third_status,
                "fourth_status": created.fourth_status,
                "fifth_status": created.fifth_status,
                "sixth_status": created.sixth_status,
                "seventh_status": created.seventh_status,
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        fruit_template: FruitTemplate,
        id: str
    ) -> "RepoFruitTemplate":

        updated = await cls.edit(
            session=session,
            model_class=FruitTemplateModel,
            data=fruit_template.to_dict(),
            id=id
        )

        return cls(
            id=updated.id,
            fruit_template=FruitTemplate.from_dict({
                "name": updated.name,
                "type": updated.type,
                "first_status": updated.first_status,
                "second_status": updated.second_status,
                "third_status": updated.third_status,
                "fourth_status": updated.fourth_status,
                "fifth_status": updated.fifth_status,
                "sixth_status": updated.sixth_status,
                "seventh_status": updated.seventh_status,
            }),
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

    # #
    # query

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        id: str
    ) -> Optional["RepoFruitTemplate"]:

        found = await cls.find(
            session=session,
            model_class=FruitTemplateModel,
            id=id
        )

        if not found:
            return None

        return cls(
            id=found.id,
            fruit_template=FruitTemplate.from_dict({
                "name": found.name,
                "type": found.type,
                "first_status": found.first_status,
                "second_status": found.second_status,
                "third_status": found.third_status,
                "fourth_status": found.fourth_status,
                "fifth_status": found.fifth_status,
                "sixth_status": found.sixth_status,
                "seventh_status": found.seventh_status,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_by_name(
        cls,
        session: AsyncSession,
        name: str
    ) -> Optional[List["RepoFruitTemplate"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=FruitTemplateModel,
            name=name
        )

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                fruit_template=FruitTemplate.from_dict({
                    "name": item.name,
                    "type": item.type,
                    "first_status": item.first_status,
                    "second_status": item.second_status,
                    "third_status": item.third_status,
                    "fourth_status": item.fourth_status,
                    "fifth_status": item.fifth_status,
                    "sixth_status": item.sixth_status,
                    "seventh_status": item.seventh_status,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]

    @classmethod
    async def get_by_type(
        cls,
        session: AsyncSession,
        type: str
    ) -> Optional[List["RepoFruitTemplate"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=FruitTemplateModel,
            type=type
        )

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                fruit_template=FruitTemplate.from_dict({
                    "name": item.name,
                    "type": item.type,
                    "first_status": item.first_status,
                    "second_status": item.second_status,
                    "third_status": item.third_status,
                    "fourth_status": item.fourth_status,
                    "fifth_status": item.fifth_status,
                    "sixth_status": item.sixth_status,
                    "seventh_status": item.seventh_status,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession
    ) -> Optional[List["RepoFruitTemplate"]]:
        
        async def find_all(
            session: AsyncSession,
            model_class
        ):
            query = select(model_class)
            result = await session.execute(query)
            return result.scalars().all()
        
        founds = await find_all(session, FruitTemplateModel)

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                fruit_template=FruitTemplate.from_dict({
                    "name": item.name,
                    "type": item.type,
                    "first_status": item.first_status,
                    "second_status": item.second_status,
                    "third_status": item.third_status,
                    "fourth_status": item.fourth_status,
                    "fifth_status": item.fifth_status,
                    "sixth_status": item.sixth_status,
                    "seventh_status": item.seventh_status,
                }),
                created_at=item.created_at,
                updated_at=(
                    item.updated_at if item.updated_at else None
                ),
            )
            for item in founds
        ]