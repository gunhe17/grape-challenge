from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo, kst
from grapechallenge.domain.mission_template import MissionTemplate


class MissionTemplateModel(Base):
    __tablename__ = "mission_templates"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    type = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoMissionTemplate(Repo):
    __table__: str = "mission_templates"

    def __init__(
        self,
        id: str,
        mission_template: MissionTemplate,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.mission_template = mission_template
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        mission_template: MissionTemplate,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(mission_template.to_dict()),
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
        mission_template: MissionTemplate
    ) -> "RepoMissionTemplate":

        created = await cls.insert(
            session=session,
            model_class=MissionTemplateModel,
            data=cls._model(mission_template=mission_template)
        )

        return cls(
            id=created.id,
            mission_template=MissionTemplate.from_dict({
                "name": created.name,
                "content": created.content,
                "type": created.type,
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        mission_template: MissionTemplate,
        id: str
    ) -> "RepoMissionTemplate":

        updated = await cls.edit(
            session=session,
            model_class=MissionTemplateModel,
            data=mission_template.to_dict(),
            id=id
        )

        return cls(
            id=updated.id,
            mission_template=MissionTemplate.from_dict({
                "name": updated.name,
                "content": updated.content,
                "type": updated.type,
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
    ) -> Optional["RepoMissionTemplate"]:

        found = await cls.find(
            session=session,
            model_class=MissionTemplateModel,
            id=id
        )

        if not found:
            return None

        return cls(
            id=found.id,
            mission_template=MissionTemplate.from_dict({
                "name": found.name,
                "content": found.content,
                "type": found.type,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_by_name(
        cls,
        session: AsyncSession,
        name: str
    ) -> Optional["RepoMissionTemplate"]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=MissionTemplateModel,
            name=name
        )

        if not founds:
            return None

        found = founds[0]

        return cls(
            id=found.id,
            mission_template=MissionTemplate.from_dict({
                "name": found.name,
                "content": found.content,
                "type": found.type,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession
    ) -> Optional[List["RepoMissionTemplate"]]:
        
        async def find_all(
            session: AsyncSession,
            model_class
        ):
            query = select(model_class)
            result = await session.execute(query)
            return result.scalars().all()
        
        founds = await find_all(session, MissionTemplateModel)

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                mission_template=MissionTemplate.from_dict({
                    "name": item.name,
                    "content": item.content,
                    "type": item.type,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]