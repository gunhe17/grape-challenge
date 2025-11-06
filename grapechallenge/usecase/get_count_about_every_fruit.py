from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.fruit import RepoFruit
from grapechallenge.usecase.common.models import UsecaseOutput


class GetCountAboutEveryFruitInput(BaseModel):
    pass

async def get_count_about_every_fruit(session: AsyncSession, request: Request, input: GetCountAboutEveryFruitInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # get counts
    total = await RepoFruit.count_all(session=session)
    in_progress = await RepoFruit.count_in_progress(session=session)
    completed = await RepoFruit.count_completed(session=session)

    return UsecaseOutput(
        content={
            "total": total,
            "in_progress": in_progress,
            "completed": completed
        },
        code=200
    )
