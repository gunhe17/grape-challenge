from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from grapechallenge.domain.common.error import (
    NotInsertedError,
    NotEditedError,
    NotFoundError,
)


def kst(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None

    if isinstance(dt, str):
        return dt

    from grapechallenge.config import get_app_env
    app_env = get_app_env()

    if app_env == "dev":
        return dt.isoformat()
    
    if app_env == "prod":
        kst_tz = timezone(timedelta(hours=9))
        return dt.replace(tzinfo=timezone.utc).astimezone(kst_tz).isoformat()

class Repo:

    # #
    # CRUD

    @classmethod
    async def insert(cls, *, session: AsyncSession, model_class, data: dict):
        try:
            instance = model_class(**data)
            session.add(instance)
            await session.flush()
            return instance
        except Exception as e:
            raise NotInsertedError(target=str(data), exception=e)

    @classmethod
    async def insert_many(cls, *, session: AsyncSession, model_class, data_list: List[dict]):
        try:
            instances = [model_class(**data) for data in data_list]
            session.add_all(instances)
            await session.flush()
            return instances
        except Exception as e:
            raise NotInsertedError(target=f"{len(data_list)} records", exception=e)

    @classmethod
    async def edit(cls, session: AsyncSession, model_class, data: dict, id: str | int):
        try:
            result = await session.execute(
                select(model_class).where(model_class.id == id)
            )
            instance = result.scalar_one_or_none()

            if not instance:
                raise NotFoundError(target=f"{model_class.__tablename__}(id={id})", exception=None)

            # Update fields
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            instance.updated_at = datetime.now()
            await session.flush()

            return instance
        except Exception as e:
            raise NotEditedError(target=model_class.__tablename__, exception=e)

    @classmethod
    async def find(cls, session: AsyncSession, model_class, id: str | int):
        try:
            result = await session.execute(
                select(model_class).where(model_class.id == id)
            )
            instance = result.scalar_one_or_none()

            return instance
        except Exception as e:
            raise NotFoundError(target=f"{model_class.__tablename__}(id={id})", exception=e)

    @classmethod
    async def find_filtered_by_fields(cls, session: AsyncSession, model_class, **kwargs):
        try:
            query = select(model_class)
            for key, value in kwargs.items():
                if hasattr(model_class, key):
                    query = query.where(getattr(model_class, key) == value)

            result = await session.execute(query)
            instances = result.scalars().all()

            return instances
        except Exception as e:
            raise NotFoundError(target=f"{model_class.__tablename__}({kwargs})", exception=e)