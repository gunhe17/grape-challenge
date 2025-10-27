from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, Date, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo, kst
from grapechallenge.domain.bible import Bible


class BibleModel(Base):
    __tablename__ = "bibles"

    id = Column(String(36), primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    content = Column(String(1000), nullable=False)
    reference = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoBible(Repo):
    __table__: str = "bibles"

    def __init__(
        self,
        id: str,
        bible: Bible,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.bible = bible
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        bible: Bible,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(bible.to_dict()),
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
        bible: Bible
    ) -> "RepoBible":

        created = await cls.insert(
            session=session,
            model_class=BibleModel,
            data=cls._model(bible=bible)
        )

        return cls(
            id=created.id,
            bible=Bible.from_dict({
                "date": created.date,
                "content": created.content,
                "reference": created.reference,
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        bible: Bible,
        id: str
    ) -> "RepoBible":

        updated = await cls.edit(
            session=session,
            model_class=BibleModel,
            data=bible.to_dict(),
            id=id
        )

        return cls(
            id=updated.id,
            bible=Bible.from_dict({
                "date": updated.date,
                "content": updated.content,
                "reference": updated.reference,
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
    ) -> Optional["RepoBible"]:

        found = await cls.find(
            session=session,
            model_class=BibleModel,
            id=id
        )

        if not found:
            return None

        return cls(
            id=found.id,
            bible=Bible.from_dict({
                "date": found.date,
                "content": found.content,
                "reference": found.reference,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_today_bible_verse(
        cls,
        session: AsyncSession
    ) -> Optional["RepoBible"]:
        from datetime import datetime, timezone, timedelta
        from grapechallenge.config import get_app_env

        app_env = get_app_env()

        if app_env == "dev":
            today = datetime.now(timezone.utc).date()
        elif app_env == "prod":
            kst = timezone(timedelta(hours=9))
            today = datetime.now(kst).date()
        else:
            return None

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=BibleModel,
            date=today
        )

        if not founds:
            return None

        found = founds[0]

        return cls(
            id=found.id,
            bible=Bible.from_dict({
                "date": found.date,
                "content": found.content,
                "reference": found.reference,
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession
    ) -> Optional[List["RepoBible"]]:

        async def find_all(
            session: AsyncSession,
            model_class
        ):
            query = select(model_class)
            result = await session.execute(query)
            return result.scalars().all()

        founds = await find_all(session, BibleModel)

        if not founds:
            return None

        return [
            cls(
                id=item.id,
                bible=Bible.from_dict({
                    "date": item.date,
                    "content": item.content,
                    "reference": item.reference,
                }),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in founds
        ]
