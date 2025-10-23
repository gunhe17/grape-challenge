from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, ForeignKey, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo, kst
from grapechallenge.domain.mission import Mission


class MissionModel(Base):
    __tablename__ = "missions"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    template_id = Column(String(36), ForeignKey("mission_templates.id", ondelete="CASCADE"), nullable=False)
    fruit_id = Column(String(36), ForeignKey("fruits.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(1000), nullable=True)
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
            "created_at": kst(self.created_at),
            "updated_at": kst(self.updated_at),
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
                "content": created.content,
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
                "content": updated.content,
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
                "content": found.content,
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
                    "content": item.content,
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
                    "content": item.content,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]
    
    # #
    # unique

    @classmethod
    async def is_template_completed_today(
        cls,
        session: AsyncSession,
        user_id: str,
        template_id: str
    ) -> bool:
        from datetime import datetime, timezone, timedelta
        from sqlalchemy import Date, cast
        from grapechallenge.config import get_app_env

        app_env = get_app_env()

        if app_env == "dev":
            # Development: Use UTC
            today = datetime.now(timezone.utc).date()
            query = select(func.count(MissionModel.id)).where(
                and_(
                    MissionModel.user_id == user_id,
                    MissionModel.template_id == template_id,
                    cast(MissionModel.created_at, Date) == today
                )
            )
        else:
            # Production: Use KST (UTC+9)
            kst = timezone(timedelta(hours=9))
            today_kst = datetime.now(kst).date()
            query = select(func.count(MissionModel.id)).where(
                and_(
                    MissionModel.user_id == user_id,
                    MissionModel.template_id == template_id,
                    cast(
                        func.timezone(
                            'Asia/Seoul',
                            func.timezone('UTC', MissionModel.created_at)
                        ),
                        Date
                    ) == today_kst
                )
            )

        result = await session.execute(query)
        count = result.scalar()

        return (count or 0) > 0
    
    # #
    # joined

    # *joined query는 dict를 반환한다.

    @classmethod
    async def get_by_template_name(
        cls,
        session: AsyncSession,
        name: str,
        date: Optional[str] = None
    ) -> Optional[List[dict]]:
        from grapechallenge.domain.mission_template.repo_mission_template import MissionTemplateModel
        from grapechallenge.domain.user.repo_user import UserModel

        async def find_by_template_name(
            session: AsyncSession,
            model_class,
            name: str,
            date: Optional[str] = None
        ):
            from datetime import datetime, timezone, timedelta
            from sqlalchemy import Date, cast
            from grapechallenge.config import get_app_env

            conditions = [MissionTemplateModel.name == name]

            if date == "today":
                app_env = get_app_env()

                if app_env == "dev":
                    # Development: Use UTC
                    today = datetime.now(timezone.utc).date()
                    conditions.append(
                        cast(model_class.created_at, Date) == today
                    )
                else:
                    # Production: Use KST (UTC+9)
                    kst = timezone(timedelta(hours=9))
                    today_kst = datetime.now(kst).date()
                    conditions.append(
                        cast(
                            func.timezone(
                                'Asia/Seoul',
                                func.timezone('UTC', model_class.created_at)
                            ),
                            Date
                        ) == today_kst
                    )

            query = select(
                model_class,
                MissionTemplateModel,
                UserModel
            ).join(
                MissionTemplateModel,
                model_class.template_id == MissionTemplateModel.id
            ).join(
                UserModel,
                model_class.user_id == UserModel.id
            ).where(
                and_(*conditions)
            )
            result = await session.execute(query)
            return result.all()

        founds = await find_by_template_name(session, MissionModel, name, date)

        if not founds:
            return None

        return [
            {
                "mission_id": found[0].id,
                "mission_user_id": found[0].user_id,
                "mission_template_id": found[0].template_id,
                "mission_fruit_id": found[0].fruit_id,
                "mission_content": found[0].content,
                "mission_created_at": found[0].created_at,
                "mission_updated_at": found[0].updated_at,
                "template_id": found[1].id,
                "template_name": found[1].name,
                "template_content": found[1].content,
                "template_type": found[1].type,
                "template_created_at": found[1].created_at,
                "template_updated_at": found[1].updated_at,
                "user_id": found[2].id,
                "user_cell": found[2].cell,
                "user_name": found[2].name,
                "user_created_at": found[2].created_at,
                "user_updated_at": found[2].updated_at,
            }
            for found in founds
        ]