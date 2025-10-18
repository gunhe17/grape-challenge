from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, ForeignKey, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo
from grapechallenge.domain.mission import Mission


class MissionModel(Base):
    __tablename__ = "missions"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(String(36), ForeignKey("mission_templates.id", ondelete="CASCADE"), nullable=False)
    fruit_id = Column(String(36), ForeignKey("fruits.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoMission(Repo):
    __table__: str = "missions"

    def __init__(
        self,
        id: str,
        mission: Mission,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.mission = mission
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        mission: Mission,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(mission.to_dict()),
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
        mission: Mission
    ) -> "RepoMission":

        created = await cls.insert(
            session=session,
            model_class=MissionModel,
            data=cls._model(mission=mission)
        )

        return cls(
            id=created.id,
            mission=Mission.from_dict({
                "user_id": created.user_id,
                "template_id": created.template_id,
                "fruit_id": created.fruit_id,
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        mission: Mission,
        id: str
    ) -> "RepoMission":

        updated = await cls.edit(
            session=session,
            model_class=MissionModel,
            data=mission.to_dict(),
            id=id
        )

        return cls(
            id=updated.id,
            mission=Mission.from_dict({
                "user_id": updated.user_id,
                "template_id": updated.template_id,
                "fruit_id": updated.fruit_id,
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
    ) -> Optional["RepoMission"]:

        found = await cls.find(
            session=session,
            model_class=MissionModel,
            id=id
        )

        if not found:
            return None

        return cls(
            id=found.id,
            mission=Mission.from_dict({
                "user_id": found.user_id,
                "template_id": found.template_id,
                "fruit_id": found.fruit_id,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_by_user_id(
        cls,
        session: AsyncSession,
        user_id: str
    ) -> Optional[List["RepoMission"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=MissionModel,
            user_id=user_id
        )

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                mission=Mission.from_dict({
                    "user_id": item.user_id,
                    "template_id": item.template_id,
                    "fruit_id": item.fruit_id,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]

    @classmethod
    async def get_by_fruit_id(
        cls,
        session: AsyncSession,
        fruit_id: str
    ) -> Optional[List["RepoMission"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=MissionModel,
            fruit_id=fruit_id
        )

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                mission=Mission.from_dict({
                    "user_id": item.user_id,
                    "template_id": item.template_id,
                    "fruit_id": item.fruit_id,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]

    @classmethod
    async def has_today_mission_with_template(
        cls,
        session: AsyncSession,
        user_id: str,
        template_id: str
    ) -> bool:
        """
        Check if user has created a mission with the given template_id today
        """
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        query = select(func.count(MissionModel.id)).where(
            and_(
                MissionModel.user_id == user_id,
                MissionModel.template_id == template_id,
                MissionModel.created_at >= today_start,
                MissionModel.created_at <= today_end
            )
        )

        result = await session.execute(query)
        count = result.scalar()

        return count > 0
