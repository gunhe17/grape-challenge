from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.user import (
    RepoUser,
    User,
    Cell,
    Name,
)
from grapechallenge.usecase.common.models import UsecaseOutput


class CreateUserInput(BaseModel):
    cell: str
    name: str

async def create_user(session: AsyncSession, request: Request, input: CreateUserInput) -> UsecaseOutput:
    
    # create user
    created = await RepoUser.create(
        session=session,
        user=User.new(
            cell=Cell.from_str(input.cell),
            name=Name.from_str(input.name),
        )
    )

    return UsecaseOutput(
        content={
            **created.summary()
        },
        code=201
    )


# #
# cli

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", type=str, required=True)
    parser.add_argument("--name", type=str, required=True)

    args = parser.parse_args()

    return args


async def main():
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock
    args = get_arguments()

    async with transactional_session_helper() as session:
        result = await create_user(
            session=session,
            request=MagicMock(),
            input=CreateUserInput(
                cell=args.cell,
                name=args.name,
            )
        )
        print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
