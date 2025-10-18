from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo
from grapechallenge.domain.fruit import Fruit


class FruitModel(Base):
    __tablename__ = "fruits"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(String(36), ForeignKey("fruit_templates.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoFruit(Repo):
    __table__: str = "fruits"

    def __init__(
        self,
        id: str,
        fruit: Fruit,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.fruit = fruit
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        fruit: Fruit,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(fruit.to_dict()),
            "created_at": created_at or datetime.now(),
            "updated_at": updated_at,
        }

    def summary(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    # #
    # command

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        fruit: Fruit
    ) -> "RepoFruit":

        created = await cls.insert(
            session=session,
            model_class=FruitModel,
            data=cls._model(fruit=fruit)
        )

        return cls(
            id=created.id,
            fruit=Fruit.from_dict({
                "user_id": created.user_id,
                "template_id": created.template_id,
                "status": created.status,
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        fruit: Fruit,
        id: str
    ) -> "RepoFruit":

        updated = await cls.edit(
            session=session,
            model_class=FruitModel,
            data=fruit.to_dict(),
            id=id
        )

        return cls(
            id=updated.id,
            fruit=Fruit.from_dict({
                "user_id": updated.user_id,
                "template_id": updated.template_id,
                "status": updated.status,
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
    ) -> Optional["RepoFruit"]:

        found = await cls.find(
            session=session,
            model_class=FruitModel,
            id=id
        )

        if not found:
            return None

        return cls(
            id=found.id,
            fruit=Fruit.from_dict({
                "user_id": found.user_id,
                "template_id": found.template_id,
                "status": found.status,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )


    # #
    # unique
    
    # #
    # joined

    # *joined query는 dict를 반환한다.

    @classmethod
    async def get_is_in_progressed_by_user_id(
        cls,
        session: AsyncSession,
        user_id: str
    ) -> Optional[dict]:
        from grapechallenge.domain.fruit_template import FruitTemplateModel
        async def find_in_progressed_fruit_by_user_id_with_template(
            session: AsyncSession,
            model_class,
            user_id: str
        ):
            query = select(model_class, FruitTemplateModel).where(
                model_class.user_id == user_id,
                model_class.status != "COMPLETED"
            ).join(
                FruitTemplateModel,
                model_class.template_id == FruitTemplateModel.id
            )
            result = await session.execute(query)
            return result.first()

        found = await find_in_progressed_fruit_by_user_id_with_template(session, FruitModel, user_id)

        if not found:
            return None

        return {
            "fruit_id": found[0].id,
            "status": found[0].status,
            "name": found[1].name,
            "type": found[1].type,
            "first_status": found[1].first_status,
            "second_status": found[1].second_status,
            "third_status": found[1].third_status,
            "fourth_status": found[1].fourth_status,
            "fifth_status": found[1].fifth_status,
            "sixth_status": found[1].sixth_status,
            "seventh_status": found[1].seventh_status,
            "created_at": found[0].created_at,
            "updated_at": found[0].updated_at,
        }

    @classmethod
    async def get_by_user_id_with_template(
        cls,
        session: AsyncSession,
        user_id: str
    ) -> Optional[List[dict]]:
        from grapechallenge.domain.fruit_template import FruitTemplateModel
        async def find_by_user_id_with_template(
            session: AsyncSession,
            model_class,
            user_id: str
        ):
            query = select(
                model_class, 
                FruitTemplateModel
            ).join(
                FruitTemplateModel,
                model_class.template_id == FruitTemplateModel.id
            ).where(
                model_class.user_id == user_id
            )
            result = await session.execute(query)
            return result.all()
        
        founds = await find_by_user_id_with_template(session, FruitModel, user_id)

        if not founds:
            return None

        return [
            {
                "fruit_id": found[0].id,
                "status": found[0].status,
                "name": found[1].name,
                "type": found[1].type,
                "first_status": found[1].first_status,
                "second_status": found[1].second_status,
                "third_status": found[1].third_status,
                "fourth_status": found[1].fourth_status,
                "fifth_status": found[1].fifth_status,
                "sixth_status": found[1].sixth_status,
                "seventh_status": found[1].seventh_status,
                "created_at": found[0].created_at,
                "updated_at": found[0].updated_at,
            }
            for found in founds
        ]