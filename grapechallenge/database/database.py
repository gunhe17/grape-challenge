# pip
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
# local
from grapechallenge.config import (
    get_app_env, 
    get_database_config
)

Base = declarative_base()


class DatabaseClient:
    _tables_created = False

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine: AsyncEngine = create_async_engine(
            url=self.database_url, 
            echo=self._activate_echo()
        )
        self.async_session = async_sessionmaker(
            bind=self.engine, 
            expire_on_commit=False, 
            class_=AsyncSession
        )

    def _activate_echo(self):
        APP_ENV = get_app_env()
        return APP_ENV == "dev"

    async def create_tables_once_in_process(self):
        if not DatabaseClient._tables_created:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            DatabaseClient._tables_created = True

    async def __aenter__(self):
        await self.create_tables_once_in_process()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.engine.dispose()


@asynccontextmanager
async def transactional_session(async_session_factory):
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


@asynccontextmanager
async def transactional_session_helper():
    async with DatabaseClient(get_database_config().database_url()) as db_client:
        async with transactional_session(db_client.async_session) as session:
            yield session
