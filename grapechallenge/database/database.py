# pip
from contextlib import asynccontextmanager
from sqlalchemy import (
    inspect, 
    text
)
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
    _tables_patched = False

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

    def _patch_schema(self, conn):
        inspector = inspect(conn)

        for table_name, table in Base.metadata.tables.items():
            if not inspector.has_table(table_name):
                continue

            existing_cols = {col['name'] for col in inspector.get_columns(table_name)}
            model_cols = {col.name: col for col in table.columns}
            missing_cols = set(model_cols.keys()) - existing_cols

            for col_name in missing_cols:
                col = model_cols[col_name]
                col_type = str(col.type.compile(conn.dialect))
                nullable = "NULL" if col.nullable else "NOT NULL"
                sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {nullable}"

                if get_app_env() == "dev":
                    print(f"[AUTO-MIGRATION] {sql}")

                conn.execute(text(sql))

    async def create_tables_once_in_process(self):
        if not DatabaseClient._tables_created:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("Database: create table worked")
            DatabaseClient._tables_created = True

    async def patch_tables_once_in_process(self):
        if not DatabaseClient._tables_patched:
            async with self.engine.begin() as conn:
                await conn.run_sync(self._patch_schema)
                print("Database: patch table worked")
            DatabaseClient._tables_patched = True

    async def __aenter__(self):
        await self.create_tables_once_in_process()
        await self.patch_tables_once_in_process()
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
