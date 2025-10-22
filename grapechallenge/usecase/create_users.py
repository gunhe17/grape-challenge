from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.user import (
    RepoUser,
    User,
    Cell,
    Name,
)
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.create_user import CreateUserInput


class CreateUsersInput(BaseModel):
    users: List[CreateUserInput]

async def create_users(session: AsyncSession, request: Request, input: CreateUsersInput) -> UsecaseOutput:

    # create users
    created_list = await RepoUser.create_many(
        session=session,
        users=[
            User.new(
                cell=Cell.from_str(user_input.cell),
                name=Name.from_str(user_input.name),
            )
            for user_input in input.users
        ]
    )

    return UsecaseOutput(
        content={
            "users": [
                {
                    **created.summary()
                }
                for created in created_list
            ],
            "count": len(created_list)
        },
        code=201
    )


# #
# cli

""" example json file: 
    {
    "users": [
        {"cell": "김성민셀", "name": "김건희"},
    ]
    }
"""

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="JSON file path containing users array")

    args = parser.parse_args()

    return args

async def main():
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock
    import json

    args = get_arguments()

    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    async with transactional_session_helper() as session:
        result = await create_users(
            session=session,
            request=MagicMock(),
            input=CreateUsersInput(users=data['users'])
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())