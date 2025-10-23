from datetime import datetime
from typing import Optional, List, Union
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from grapechallenge.database.database import Base
from grapechallenge.domain.common.repo import Repo, kst
from grapechallenge.domain.user import User


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    cell = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)


class RepoUser(Repo):
    __table__: str = "users"

    def __init__(
        self,
        id: str,
        user: User,
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.user = user
        self.created_at = created_at
        self.updated_at = updated_at

    # #
    # helper

    @classmethod
    def _model(
        cls,
        *,
        user: User,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> dict:
        return {
            "id": id or str(uuid4()),
            **(user.to_dict()),
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
        user: User
    ) -> "RepoUser":

        created = await cls.insert(
            session=session,
            model_class=UserModel,
            data=cls._model(user=user)
        )

        return cls(
            id=created.id,
            user=User.from_dict({
                "cell": created.cell,
                "name": created.name
            }),
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    @classmethod
    async def create_many(
        cls,
        session: AsyncSession,
        users: List[User]
    ) -> List["RepoUser"]:

        data_list = [cls._model(user=user) for user in users]

        created_list = await cls.insert_many(
            session=session,
            model_class=UserModel,
            data_list=data_list
        )

        return [
            cls(
                id=created.id,
                user=User.from_dict({
                    "cell": created.cell,
                    "name": created.name
                }),
                created_at=created.created_at,
                updated_at=created.updated_at,
            )
            for created in created_list
        ]

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        user: User,
        id: str
    ) -> "RepoUser":
        
        updated = await cls.edit(
            session=session, 
            model_class=UserModel, 
            data=user.to_dict(), 
            id=id
        )

        return cls(
            id=updated.id,
            user=User.from_dict({
                "cell": updated.cell,
                "name": updated.name
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
    ) -> Optional["RepoUser"]:
        
        found = await cls.find(
            session=session, 
            model_class=UserModel, 
            id=id
        )

        if found is None:
            return None

        return cls(
            id=found.id,
            user=User.from_dict({
                "cell": found.cell,
                "name": found.name
            }),
            created_at=found.created_at,
            updated_at=found.updated_at,
        )

    @classmethod
    async def get_by_cell(
        cls,
        session: AsyncSession,
        cell: str
    ) -> Optional[List["RepoUser"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=UserModel,
            cell=cell
        )

        if not founds:
            return None

        return [
            cls(
                id=found.id,
                user=User.from_dict({
                    "cell": found.cell,
                    "name": found.name
                }),
                created_at=found.created_at,
                updated_at=found.updated_at,
            )
            for found in founds
        ]

    @classmethod
    async def get_all_cells(
        cls,
        session: AsyncSession
    ) -> Optional[List[str]]:
        from sqlalchemy import distinct
        from sqlalchemy.future import select

        async def find_all_distinct_cells(
            session: AsyncSession,
            model_class
        ):
            query = select(distinct(model_class.cell)).order_by(model_class.cell)
            result = await session.execute(query)
            return result.scalars().all()

        cells = await find_all_distinct_cells(session, UserModel)

        if not cells:
            return None

        return list(cells)

    # TODO: LOG-IN field
    @classmethod
    async def get_by_cell_and_name(
        cls,
        session: AsyncSession,
        cell: str,
        name: str
    ) -> Optional[List["RepoUser"]]:

        founds = await cls.find_filtered_by_fields(
            session=session,
            model_class=UserModel,
            cell=cell,
            name=name
        )

        if not founds:
            return None

        return [
            cls(
                id=found.id,
                user=User.from_dict({
                    "cell": found.cell,
                    "name": found.name
                }),
                created_at=found.created_at,
                updated_at=found.updated_at,
            )
            for found in founds
        ]