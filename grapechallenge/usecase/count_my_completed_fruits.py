from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class CountMyCompletedFruitsInput(BaseModel):
    pass

async def count_my_completed_fruits(session: AsyncSession, request: Request, input: CountMyCompletedFruitsInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get count
    found = await RepoFruit.count_my_completed(
        session=session,
        user_id=user_id
    )

    return UsecaseOutput(
        content={
            "count": found
        },
        code=200
    )
